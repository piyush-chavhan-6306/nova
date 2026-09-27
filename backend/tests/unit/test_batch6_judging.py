import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.hackathon import Hackathon
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.submission import Submission
from app.models.user import User
from app.models.judge import Judge
from app.models.rubric import Rubric
from app.models.rubric_criterion import RubricCriterion
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, TeamRole, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_b6_fixtures():
    db = SessionLocal()

    # Hackathon
    hack = db.query(Hackathon).filter(Hackathon.id == "hack_b6_test").first()
    if not hack:
        hack = Hackathon(id="hack_b6_test", name="Batch 6 Judging Hackathon", status=HackathonStatus.ACTIVE)
        db.add(hack)

    # Team 1 (Competitors)
    t1 = db.query(Team).filter(Team.id == "team_b6_1").first()
    if not t1:
        t1 = Team(id="team_b6_1", hackathon_id="hack_b6_test", name="B6 Alpha Team")
        db.add(t1)

    # User 1 (Team 1 Member & Competitor Judge)
    u_competitor = db.query(User).filter(User.id == "usr_b6_comp").first()
    if not u_competitor:
        u_competitor = User(
            id="usr_b6_comp",
            email="b6_comp@example.com",
            name="Competitor User",
            role="PARTICIPANT",
            hashed_password=get_password_hash("password123")
        )
        db.add(u_competitor)

    tm1 = db.query(TeamMember).filter(TeamMember.id == "tm_b6_1").first()
    if not tm1:
        tm1 = TeamMember(id="tm_b6_1", team_id="team_b6_1", user_id="usr_b6_comp", role=TeamRole.LEAD)
        db.add(tm1)

    # Submission 1 (by Team 1)
    sub1 = db.query(Submission).filter(Submission.id == "sub_b6_1").first()
    if not sub1:
        sub1 = Submission(
            id="sub_b6_1",
            hackathon_id="hack_b6_test",
            team_id="team_b6_1",
            title="B6 Alpha Project",
            status=SubmissionStatus.SUBMITTED
        )
        db.add(sub1)

    # User 2 (Pure External Judge)
    u_external_judge = db.query(User).filter(User.id == "usr_b6_ext_judge").first()
    if not u_external_judge:
        u_external_judge = User(
            id="usr_b6_ext_judge",
            email="b6_ext_judge@example.com",
            name="External Judge",
            role="JUDGE",
            hashed_password=get_password_hash("password123")
        )
        db.add(u_external_judge)

    j_ext = db.query(Judge).filter(Judge.id == "jdg_b6_ext").first()
    if not j_ext:
        j_ext = Judge(id="jdg_b6_ext", user_id="usr_b6_ext_judge", hackathon_id="hack_b6_test", title="Senior Architect")
        db.add(j_ext)

    # User 3 (Judge who is also a competitor in team 1)
    j_comp = db.query(Judge).filter(Judge.id == "jdg_b6_comp").first()
    if not j_comp:
        j_comp = Judge(id="jdg_b6_comp", user_id="usr_b6_comp", hackathon_id="hack_b6_test", title="Peer Judge")
        db.add(j_comp)

    # Rubric & Rubric Criterion
    rubric = db.query(Rubric).filter(Rubric.id == "rubric_b6_1").first()
    if not rubric:
        rubric = Rubric(id="rubric_b6_1", hackathon_id="hack_b6_test", name="B6 Evaluation Rubric")
        db.add(rubric)

    crit = db.query(RubricCriterion).filter(RubricCriterion.id == "crit_b6_1").first()
    if not crit:
        crit = RubricCriterion(
            id="crit_b6_1",
            rubric_id="rubric_b6_1",
            name="Innovation",
            max_score=10.0,
            weight=1.0
        )
        db.add(crit)

    db.commit()
    db.close()

    return {
        "hackathon_id": "hack_b6_test",
        "submission_id": "sub_b6_1",
        "ext_judge_id": "jdg_b6_ext",
        "comp_judge_id": "jdg_b6_comp",
        "ext_user_id": "usr_b6_ext_judge",
        "comp_user_id": "usr_b6_comp",
        "criterion_id": "crit_b6_1"
    }


def test_peer_isolation_prevents_conflicted_assignment(setup_b6_fixtures):
    """T2 Check: Assignment of judge competing in the event or on team must be blocked."""
    f = setup_b6_fixtures
    payload = {
        "submission_id": f["submission_id"],
        "judge_id": f["comp_judge_id"]
    }

    res = client.post("/api/v1/judging/assignments", json=payload, headers={"Authorization": f["ext_user_id"]})
    assert res.status_code == 403
    assert "peer isolation" in res.json()["detail"].lower()


def test_assign_external_judge_success(setup_b6_fixtures):
    f = setup_b6_fixtures
    payload = {
        "submission_id": f["submission_id"],
        "judge_id": f["ext_judge_id"]
    }

    res = client.post("/api/v1/judging/assignments", json=payload, headers={"Authorization": f["ext_user_id"]})
    assert res.status_code == 201
    asgn = res.json()
    assert asgn["judge_id"] == f["ext_judge_id"]
    assert asgn["submission_id"] == f["submission_id"]


def test_submit_review_success(setup_b6_fixtures):
    f = setup_b6_fixtures
    payload = {
        "submission_id": f["submission_id"],
        "comment": "Outstanding technical architecture and execution!",
        "scores": [
            {
                "criterion_id": f["criterion_id"],
                "score": 9.5,
                "comment": "Great innovation"
            }
        ]
    }

    res = client.post("/api/v1/judging/reviews", json=payload, headers={"Authorization": f["ext_user_id"]})
    assert res.status_code == 201
    rev = res.json()
    assert rev["status"] == "SUBMITTED"
    assert rev["judge_id"] == f["ext_judge_id"]


def test_peer_isolation_prevents_conflicted_review(setup_b6_fixtures):
    """T2 Check: Submitting review from a judge who is a competitor must be blocked."""
    f = setup_b6_fixtures
    payload = {
        "submission_id": f["submission_id"],
        "comment": "Self-evaluation attempt",
        "scores": []
    }

    res = client.post("/api/v1/judging/reviews", json=payload, headers={"Authorization": f["comp_user_id"]})
    assert res.status_code == 403
    assert "peer isolation" in res.json()["detail"].lower()
