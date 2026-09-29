import csv
import io
import statistics
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.hackathon import Hackathon
from app.models.submission import Submission
from app.models.review import Review
from app.models.judge import Judge
from app.models.track import Track
from app.models.registration import Registration
from app.models.team import Team
from app.models.judge_conflict import JudgeConflict
from app.models.judge_assignment import JudgeAssignment
from app.models.audit_log import AuditLog
from app.models.result import Result
from app.schemas.organizer_analytics import (
    SubmissionAnalyticsResponse, JudgingAnalyticsResponse,
    TrackAnalyticsItem, IntegrityCheckResponse, IntegrityAlertItem,
    OrganizerDashboardResponse
)
from app.utils.enums import SubmissionStatus, ReviewStatus, UserRole
from app.core.exceptions import ForbiddenException, NotFoundException
from app.core.dependencies import UserIdentity, verify_hackathon_owner


class OrganizerService:
    def __init__(self, db: Session):
        self.db = db

    def _verify_organizer(self, current_user: UserIdentity, hackathon_id: Optional[str] = None):
        if current_user.role not in [UserRole.ORGANIZER, UserRole.ADMIN]:
            raise ForbiddenException("Only organizers or admins can access these endpoints")
        if hackathon_id:
            verify_hackathon_owner(hackathon_id, current_user, self.db)

    def get_submission_analytics(self, hackathon_id: str, current_user: UserIdentity) -> SubmissionAnalyticsResponse:
        self._verify_organizer(current_user, hackathon_id)

        subs = self.db.query(Submission).filter(Submission.hackathon_id == hackathon_id).all()
        total = len(subs)
        submitted = sum(1 for s in subs if s.status == SubmissionStatus.SUBMITTED)
        draft = sum(1 for s in subs if s.status == SubmissionStatus.DRAFT)
        locked = sum(1 for s in subs if s.status == SubmissionStatus.LOCKED)

        by_track: Dict[str, int] = {}
        by_tech: Dict[str, int] = {}

        for s in subs:
            t_name = s.track.name if s.track else "Unassigned"
            by_track[t_name] = by_track.get(t_name, 0) + 1

            techs = getattr(s, 'technologies', None)
            if techs:
                tech_list = [t.strip() for t in techs.split(",") if t.strip()]
                for tech in tech_list:
                    by_tech[tech] = by_tech.get(tech, 0) + 1

        return SubmissionAnalyticsResponse(
            hackathon_id=hackathon_id,
            total_submissions=total,
            submitted=submitted,
            draft=draft,
            locked=locked,
            by_track=by_track,
            by_technology=by_tech
        )

    def get_judging_analytics(self, hackathon_id: str, current_user: UserIdentity) -> JudgingAnalyticsResponse:
        self._verify_organizer(current_user, hackathon_id)

        reviews = (
            self.db.query(Review)
            .join(Submission, Review.submission_id == Submission.id)
            .filter(Submission.hackathon_id == hackathon_id)
            .all()
        )
        total_rev = len(reviews)
        completed = sum(1 for r in reviews if r.status == ReviewStatus.SUBMITTED)
        pending = max(0, total_rev - completed)
        pct = round((completed / total_rev * 100.0), 2) if total_rev > 0 else 0.0

        scores = [sum(s.score for s in r.scores) for r in reviews if r.status == ReviewStatus.SUBMITTED and r.scores]
        avg_score = round(statistics.mean(scores), 2) if scores else 0.0

        # Score distribution ranges: 0-25, 25-50, 50-75, 75-100
        dist = {"0-25": 0, "25-50": 0, "50-75": 0, "75-100": 0}
        for sc in scores:
            if sc < 25:
                dist["0-25"] += 1
            elif sc < 50:
                dist["25-50"] += 1
            elif sc < 75:
                dist["50-75"] += 1
            else:
                dist["75-100"] += 1

        judges = self.db.query(Judge).filter(Judge.hackathon_id == hackathon_id).all()
        workload = []
        for j in judges:
            j_revs = [r for r in reviews if r.judge_id == j.id]
            j_tot = len(j_revs)
            j_comp = sum(1 for r in j_revs if r.status == ReviewStatus.SUBMITTED)
            workload.append({
                "judge_id": j.id,
                "judge_name": j.user.name if j.user else j.id,
                "total_assigned": j_tot,
                "completed": j_comp
            })

        return JudgingAnalyticsResponse(
            hackathon_id=hackathon_id,
            total_reviews=total_rev,
            completed=completed,
            pending=pending,
            completion_percentage=pct,
            average_score=avg_score,
            score_distribution=dist,
            judge_workload=workload
        )

    def get_track_analytics(self, hackathon_id: str, current_user: UserIdentity) -> List[TrackAnalyticsItem]:
        self._verify_organizer(current_user, hackathon_id)

        tracks = self.db.query(Track).filter(Track.hackathon_id == hackathon_id).all()
        result = []
        for tr in tracks:
            subs = self.db.query(Submission).filter(Submission.track_id == tr.id).all()
            proj_count = len(subs)

            sub_ids = [s.id for s in subs]
            reviews = self.db.query(Review).filter(Review.submission_id.in_(sub_ids)).all() if sub_ids else []
            rev_count = len(reviews)
            comp_count = sum(1 for r in reviews if r.status == ReviewStatus.SUBMITTED)
            pct = round((comp_count / rev_count * 100.0), 2) if rev_count > 0 else 0.0

            scores = [sum(s.score for s in r.scores) for r in reviews if r.status == ReviewStatus.SUBMITTED and r.scores]
            avg_sc = round(statistics.mean(scores), 2) if scores else 0.0

            result.append(TrackAnalyticsItem(
                track_id=tr.id,
                track_name=tr.name,
                projects_count=proj_count,
                judges_count=len(tr.judges),
                reviews_count=rev_count,
                average_score=avg_sc,
                completion_percentage=pct
            ))
        return result

    def run_integrity_checks(self, hackathon_id: str, current_user: UserIdentity) -> IntegrityCheckResponse:
        self._verify_organizer(current_user, hackathon_id)

        alerts: List[IntegrityAlertItem] = []

        # 1. Check for judges assigned to own project / team
        assignments = (
            self.db.query(JudgeAssignment)
            .join(Submission, JudgeAssignment.submission_id == Submission.id)
            .filter(Submission.hackathon_id == hackathon_id)
            .all()
        )
        for a in assignments:
            if a.judge and a.submission and a.submission.team:
                team_user_ids = [tm.user_id for tm in a.submission.team.members]
                if a.judge.user_id in team_user_ids:
                    alerts.append(IntegrityAlertItem(
                        alert_type="ASSIGNMENT_SELF_JUDGING",
                        severity="HIGH",
                        message=f"Judge {a.judge.user.name if a.judge.user else a.judge_id} assigned to own team project {a.submission.title}",
                        entity_id=a.id
                    ))

        # 2. Check for active conflicts
        conflicts = (
            self.db.query(JudgeConflict)
            .join(Judge, JudgeConflict.judge_id == Judge.id)
            .filter(Judge.hackathon_id == hackathon_id, JudgeConflict.status.in_(["DECLARED", "APPROVED"]))
            .all()
        )
        for c in conflicts:
            alerts.append(IntegrityAlertItem(
                alert_type="ACTIVE_CONFLICT",
                severity="MEDIUM",
                message=f"Active conflict declared by judge {c.judge_id} for submission {c.submission_id}",
                entity_id=c.id
            ))

        # 3. Duplicate repo check
        subs = self.db.query(Submission).filter(Submission.hackathon_id == hackathon_id).all()
        repos: Dict[str, List[str]] = {}
        for s in subs:
            if s.repo_url:
                repos.setdefault(s.repo_url.strip(), []).append(s.id)

        for repo, sub_ids in repos.items():
            if len(sub_ids) > 1:
                alerts.append(IntegrityAlertItem(
                    alert_type="DUPLICATE_REPOSITORY",
                    severity="HIGH",
                    message=f"Repository URL {repo} shared by submissions: {', '.join(sub_ids)}",
                    entity_id=sub_ids[0]
                ))

        return IntegrityCheckResponse(
            hackathon_id=hackathon_id,
            total_checks=3,
            alerts_count=len(alerts),
            alerts=alerts
        )

    def get_organizer_dashboard(self, hackathon_id: str, current_user: UserIdentity) -> OrganizerDashboardResponse:
        self._verify_organizer(current_user, hackathon_id)

        hack = self.db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
        if not hack:
            raise NotFoundException("Hackathon", hackathon_id)

        reg_count = self.db.query(Registration).filter(Registration.hackathon_id == hackathon_id).count()
        team_count = self.db.query(Team).filter(Team.hackathon_id == hackathon_id).count()
        sub_count = self.db.query(Submission).filter(Submission.hackathon_id == hackathon_id).count()
        
        judging_analytics = self.get_judging_analytics(hackathon_id, current_user)
        integrity_checks = self.run_integrity_checks(hackathon_id, current_user)
        conflicts_count = (
            self.db.query(JudgeConflict)
            .join(Judge, JudgeConflict.judge_id == Judge.id)
            .filter(Judge.hackathon_id == hackathon_id)
            .count()
        )

        return OrganizerDashboardResponse(
            hackathon_id=hackathon_id,
            registrations={"total": reg_count},
            teams={"total": team_count},
            submissions={"total": sub_count},
            judging={
                "total_reviews": judging_analytics.total_reviews,
                "completed": judging_analytics.completed,
                "completion_percentage": judging_analytics.completion_percentage
            },
            conflicts={"total": conflicts_count},
            integrity={"alerts_count": integrity_checks.alerts_count},
            results={"status": hack.results_status}
        )

    # Advanced Exports
    def export_judging_csv(self, hackathon_id: str, current_user: UserIdentity) -> str:
        self._verify_organizer(current_user, hackathon_id)

        reviews = (
            self.db.query(Review)
            .join(Submission, Review.submission_id == Submission.id)
            .filter(Submission.hackathon_id == hackathon_id)
            .all()
        )
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Review ID", "Submission ID", "Judge ID", "Status", "Total Score", "Comment"])

        for r in reviews:
            tot = sum(s.score for s in r.scores) if r.scores else 0.0
            writer.writerow([r.id, r.submission_id, r.judge_id, r.status, tot, r.comment or ""])

        return output.getvalue()

    def export_judges_csv(self, hackathon_id: str, current_user: UserIdentity) -> str:
        self._verify_organizer(current_user, hackathon_id)

        judges = self.db.query(Judge).filter(Judge.hackathon_id == hackathon_id).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Judge ID", "User ID", "Name", "Email", "Assigned Assignments"])

        for j in judges:
            asgn_count = len(j.assignments)
            writer.writerow([
                j.id,
                j.user_id,
                j.user.name if j.user else "",
                j.user.email if j.user else "",
                asgn_count
            ])

        return output.getvalue()

    def export_audit_csv(self, hackathon_id: str, current_user: UserIdentity) -> str:
        self._verify_organizer(current_user, hackathon_id)

        logs = self.db.query(AuditLog).filter(AuditLog.hackathon_id == hackathon_id).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Audit ID", "User ID", "Action", "Target Type", "Target ID", "Details", "Timestamp"])

        for l in logs:
            writer.writerow([l.id, l.user_id or "", l.action, l.target_type or "", l.target_id or "", l.details or "", l.timestamp])

        return output.getvalue()

    def export_integrity_csv(self, hackathon_id: str, current_user: UserIdentity) -> str:
        self._verify_organizer(current_user, hackathon_id)

        checks = self.run_integrity_checks(hackathon_id, current_user)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Alert Type", "Severity", "Message", "Entity ID"])

        for a in checks.alerts:
            writer.writerow([a.alert_type, a.severity, a.message, a.entity_id or ""])

        return output.getvalue()
