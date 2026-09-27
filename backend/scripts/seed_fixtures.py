import json
import os
import sys
from datetime import datetime

# Adjust path to import backend app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import (
    User, Hackathon, Track, Team, TeamMember, Submission,
    Judge, JudgeTrack, JudgeAssignment, Rubric, RubricCriterion,
    Review, Score
)
from app.utils.enums import UserRole, HackathonStatus, TeamRole, SubmissionStatus, ReviewStatus


def parse_iso_datetime(dt_str: str) -> datetime:
    if not dt_str:
        return datetime.utcnow()
    try:
        if dt_str.endswith("Z"):
            dt_str = dt_str[:-1]
        return datetime.fromisoformat(dt_str)
    except Exception:
        return datetime.utcnow()


def find_fixture_file(explicit_path=None) -> str:
    if explicit_path and os.path.exists(explicit_path):
        return explicit_path
    
    candidates = [
        "fixtures.json",
        "fixtures (1).json",
        "../dogfood-portal/dogfood/fixtures (1).json",
        "../dogfood-portal/dogfood/fixtures.json",
        "d:/hackathons/dogfood/dogfood-portal/dogfood/fixtures (1).json",
        "d:/hackathons/dogfood/dogfood-portal/dogfood/fixtures.json",
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Could not locate fixtures.json or fixtures (1).json in standard paths.")


def seed_fixtures(db: Session, fixture_path: str):
    print(f"Loading fixtures from: {fixture_path}")
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Event / Hackathon
    evt_data = data.get("event", {})
    evt_id = evt_data.get("id", "evt_01")
    event = db.query(Hackathon).filter(Hackathon.id == evt_id).first()
    if not event:
        event = Hackathon(
            id=evt_id,
            name=evt_data.get("name", "Sample Hack 2026"),
            description="Official Dogfood Hackathon 2026",
            submissions_close=parse_iso_datetime(evt_data.get("submissions_close", "2026-03-01T18:00:00Z")),
            status=HackathonStatus.CLOSED  # Submissions closed for fixture testing
        )
        db.add(event)
    else:
        event.name = evt_data.get("name", event.name)
        event.submissions_close = parse_iso_datetime(evt_data.get("submissions_close", "2026-03-01T18:00:00Z"))
    db.flush()

    # 2. Tracks
    tracks_data = data.get("tracks", [])
    for t_info in tracks_data:
        t_id = t_info.get("id")
        t_obj = db.query(Track).filter(Track.id == t_id).first()
        if not t_obj:
            t_obj = Track(
                id=t_id,
                hackathon_id=event.id,
                name=t_info.get("name", f"Track {t_id}")
            )
            db.add(t_obj)
    db.flush()

    # 3. Default Rubric & Rubric Criteria
    rubric = db.query(Rubric).filter(Rubric.hackathon_id == event.id).first()
    if not rubric:
        rubric = Rubric(id=f"rub_{event.id}", hackathon_id=event.id, name="Default Scoring Rubric")
        db.add(rubric)
        db.flush()

    # Criteria map
    criteria_names = ["functionality", "quality", "innovation", "design", "impact"]
    criteria_map = {}
    for c_name in criteria_names:
        c_obj = db.query(RubricCriterion).filter(RubricCriterion.rubric_id == rubric.id, RubricCriterion.name == c_name).first()
        if not c_obj:
            c_obj = RubricCriterion(
                id=f"crit_{c_name}",
                rubric_id=rubric.id,
                name=c_name,
                weight=1.0,
                max_score=5.0
            )
            db.add(c_obj)
            db.flush()
        criteria_map[c_name] = c_obj

    # Create special test Organizer user
    org_user = db.query(User).filter(User.id == "usr_organizer").first()
    if not org_user:
        org_user = User(
            id="usr_organizer",
            email="organizer@example.org",
            name="Organizer Admin",
            role=UserRole.ORGANIZER
        )
        db.add(org_user)
        db.flush()

    # 4. Judges
    judges_data = data.get("judges", [])
    for j_info in judges_data:
        j_id = j_info.get("id")
        j_email = j_info.get("email")
        j_name = j_info.get("name", "Judge User")

        # User profile
        u_obj = db.query(User).filter(User.email == j_email).first()
        if not u_obj:
            u_obj = User(
                id=f"usr_{j_id}",
                email=j_email,
                name=j_name,
                role=UserRole.JUDGE
            )
            db.add(u_obj)
            db.flush()

        # Judge profile
        j_obj = db.query(Judge).filter(Judge.id == j_id).first()
        if not j_obj:
            j_obj = Judge(
                id=j_id,
                user_id=u_obj.id,
                hackathon_id=event.id,
                title="Judge"
            )
            db.add(j_obj)
            db.flush()

        # Judge tracks
        for trk_id in j_info.get("tracks", []):
            jt_id = f"jt_{j_id}_{trk_id}"
            jt_obj = db.query(JudgeTrack).filter(JudgeTrack.id == jt_id).first()
            if not jt_obj:
                jt_obj = JudgeTrack(id=jt_id, judge_id=j_obj.id, track_id=trk_id)
                db.add(jt_obj)

    db.flush()

    # 5. Teams & Team Members
    teams_data = data.get("teams", [])
    for tm_info in teams_data:
        tm_id = tm_info.get("id")
        tm_name = tm_info.get("name", f"Team {tm_id}")
        members = tm_info.get("members", [])

        t_obj = db.query(Team).filter(Team.id == tm_id).first()
        if not t_obj:
            t_obj = Team(id=tm_id, hackathon_id=event.id, name=tm_name, join_code=f"code_{tm_id}")
            db.add(t_obj)
            db.flush()

        for idx, m_email in enumerate(members):
            m_user = db.query(User).filter(User.email == m_email).first()
            if not m_user:
                m_user = User(
                    id=f"usr_mem_{m_email.split('@')[0]}",
                    email=m_email,
                    name=m_email.split('@')[0],
                    role=UserRole.PARTICIPANT
                )
                db.add(m_user)
                db.flush()

            tm_mem_id = f"tm_mem_{tm_id}_{m_user.id}"
            mem_obj = db.query(TeamMember).filter(TeamMember.id == tm_mem_id).first()
            if not mem_obj:
                role = TeamRole.LEAD if idx == 0 else TeamRole.MEMBER
                mem_obj = TeamMember(id=tm_mem_id, team_id=t_obj.id, user_id=m_user.id, role=role)
                db.add(mem_obj)

    db.flush()

    # Create specific Dogfood test Participant user
    prt_user = db.query(User).filter(User.id == "prt_01").first()
    if not prt_user:
        prt_user = User(
            id="prt_01",
            email="participant@example.org",
            name="Priya Participant",
            role=UserRole.PARTICIPANT
        )
        db.add(prt_user)
        db.flush()

    # 6. Projects / Submissions
    projects_data = data.get("projects", [])
    for p_info in projects_data:
        p_id = p_info.get("id")
        sub_obj = db.query(Submission).filter(Submission.id == p_id).first()
        if not sub_obj:
            sub_obj = Submission(
                id=p_id,
                hackathon_id=event.id,
                team_id=p_info.get("team"),
                track_id=p_info.get("track"),
                title=p_info.get("title"),
                summary=p_info.get("summary", ""),
                repo_url=p_info.get("repo_url", ""),
                status=SubmissionStatus.SUBMITTED,
                submitted_at=parse_iso_datetime(p_info.get("submitted_at"))
            )
            db.add(sub_obj)
    db.flush()

    # 7. Scores & Reviews
    scores_data = data.get("scores", [])
    for idx, s_info in enumerate(scores_data):
        j_id = s_info.get("judge")
        p_id = s_info.get("project")
        crit_dict = s_info.get("criteria", {})
        comment = s_info.get("comment", "")

        # Create or fetch assignment
        asgn_id = f"asgn_{j_id}_{p_id}"
        asgn = db.query(JudgeAssignment).filter(JudgeAssignment.id == asgn_id).first()
        if not asgn:
            asgn = JudgeAssignment(id=asgn_id, judge_id=j_id, submission_id=p_id)
            db.add(asgn)
            db.flush()

        # Create or fetch review
        rev_id = f"rev_{j_id}_{p_id}"
        rev = db.query(Review).filter(Review.id == rev_id).first()
        if not rev:
            rev = Review(
                id=rev_id,
                assignment_id=asgn.id,
                judge_id=j_id,
                submission_id=p_id,
                status=ReviewStatus.SUBMITTED,
                comment=comment,
                submitted_at=datetime.utcnow()
            )
            db.add(rev)
            db.flush()

        # Add scores
        for c_key, val in crit_dict.items():
            if c_key in criteria_map:
                c_obj = criteria_map[c_key]
                sc_id = f"sc_{rev.id}_{c_obj.id}"
                sc_item = db.query(Score).filter(Score.id == sc_id).first()
                if not sc_item:
                    sc_item = Score(
                        id=sc_id,
                        review_id=rev.id,
                        criterion_id=c_obj.id,
                        score=float(val)
                    )
                    db.add(sc_item)

    db.commit()
    print("Database seeding completed successfully!")
    print("\nTest Logins for .dogfood.toml:")
    print("  organizer   = \"Cookie: session=org_7f2a\"")
    print("  judge_a     = \"Cookie: session=jdg_a_91bc\" (Ada Okonkwo / jdg_01)")
    print("  judge_b     = \"Cookie: session=jdg_b_44de\" (Wei Lindqvist / jdg_02)")
    print("  participant = \"Cookie: session=prt_2e88\"")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    try:
        f_path = find_fixture_file()
        seed_fixtures(db_session, f_path)
    finally:
        db_session.close()
