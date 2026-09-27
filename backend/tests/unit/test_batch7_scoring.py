import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.hackathon import Hackathon
from app.models.team import Team
from app.models.submission import Submission
from app.models.user import User
from app.models.judge import Judge
from app.models.judge_assignment import JudgeAssignment
from app.models.review import Review
from app.models.rubric import Rubric
from app.models.rubric_criterion import RubricCriterion
from app.models.score import Score
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, SubmissionStatus, ReviewStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_b7_fixtures():
    db = SessionLocal()

    # Hackathon
    hack = db.query(Hackathon).filter(Hackathon.id == "hack_b7_test").first()
    if not hack:
        hack = Hackathon(id="hack_b7_test", name="Batch 7 Scoring Hackathon", status=HackathonStatus.ACTIVE)
        db.add(hack)

    # Teams
    t1 = db.query(Team).filter(Team.id == "team_b7_1").first()
    if not t1:
        t1 = Team(id="team_b7_1", hackathon_id="hack_b7_test", name="Gold Team")
        db.add(t1)

    t2 = db.query(Team).filter(Team.id == "team_b7_2").first()
    if not t2:
        t2 = Team(id="team_b7_2", hackathon_id="hack_b7_test", name="Silver Team")
        db.add(t2)

    # Submissions
    sub1 = db.query(Submission).filter(Submission.id == "sub_b7_1").first()
    if not sub1:
        sub1 = Submission(id="sub_b7_1", hackathon_id="hack_b7_test", team_id="team_b7_1", title="Top Winner Project", status=SubmissionStatus.SUBMITTED)
        db.add(sub1)

    sub2 = db.query(Submission).filter(Submission.id == "sub_b7_2").first()
    if not sub2:
        sub2 = Submission(id="sub_b7_2", hackathon_id="hack_b7_test", team_id="team_b7_2", title="Runner Up Project", status=SubmissionStatus.SUBMITTED)
        db.add(sub2)

    # Judge User
    u_judge = db.query(User).filter(User.id == "usr_b7_judge").first()
    if not u_judge:
        u_judge = User(id="usr_b7_judge", email="b7_judge@example.com", name="B7 Judge", role="JUDGE", hashed_password=get_password_hash("password123"))
        db.add(u_judge)

    j_profile = db.query(Judge).filter(Judge.id == "jdg_b7_1").first()
    if not j_profile:
        j_profile = Judge(id="jdg_b7_1", user_id="usr_b7_judge", hackathon_id="hack_b7_test")
        db.add(j_profile)

    # Rubric
    rub = db.query(Rubric).filter(Rubric.id == "rubric_b7_1").first()
    if not rub:
        rub = Rubric(id="rubric_b7_1", hackathon_id="hack_b7_test", name="B7 Rubric")
        db.add(rub)

    crit = db.query(RubricCriterion).filter(RubricCriterion.id == "crit_b7_1").first()
    if not crit:
        crit = RubricCriterion(id="crit_b7_1", rubric_id="rubric_b7_1", name="Execution", max_score=10.0, weight=1.0)
        db.add(crit)

    # Assignments & Reviews for Sub 1 (Score 9.5)
    asgn1 = db.query(JudgeAssignment).filter(JudgeAssignment.id == "asgn_b7_1").first()
    if not asgn1:
        asgn1 = JudgeAssignment(id="asgn_b7_1", judge_id="jdg_b7_1", submission_id="sub_b7_1")
        db.add(asgn1)

    rev1 = db.query(Review).filter(Review.id == "rev_b7_1").first()
    if not rev1:
        rev1 = Review(id="rev_b7_1", assignment_id="asgn_b7_1", judge_id="jdg_b7_1", submission_id="sub_b7_1", status=ReviewStatus.SUBMITTED, comment="Awesome")
        db.add(rev1)

    scr1 = db.query(Score).filter(Score.id == "scr_b7_1").first()
    if not scr1:
        scr1 = Score(id="scr_b7_1", review_id="rev_b7_1", criterion_id="crit_b7_1", score=9.5)
        db.add(scr1)

    # Assignments & Reviews for Sub 2 (Score 7.0)
    asgn2 = db.query(JudgeAssignment).filter(JudgeAssignment.id == "asgn_b7_2").first()
    if not asgn2:
        asgn2 = JudgeAssignment(id="asgn_b7_2", judge_id="jdg_b7_1", submission_id="sub_b7_2")
        db.add(asgn2)

    rev2 = db.query(Review).filter(Review.id == "rev_b7_2").first()
    if not rev2:
        rev2 = Review(id="rev_b7_2", assignment_id="asgn_b7_2", judge_id="jdg_b7_1", submission_id="sub_b7_2", status=ReviewStatus.SUBMITTED, comment="Good")
        db.add(rev2)

    scr2 = db.query(Score).filter(Score.id == "scr_b7_2").first()
    if not scr2:
        scr2 = Score(id="scr_b7_2", review_id="rev_b7_2", criterion_id="crit_b7_1", score=7.0)
        db.add(scr2)

    db.commit()
    db.close()

    return {
        "hackathon_id": "hack_b7_test",
        "judge_user_id": "usr_b7_judge"
    }


def test_calculate_leaderboard(setup_b7_fixtures):
    f = setup_b7_fixtures
    res = client.post(f"/api/v1/hackathons/{f['hackathon_id']}/results/calculate", headers={"Authorization": f["judge_user_id"]})
    assert res.status_code == 200
    lb = res.json()
    assert lb["total_submissions"] == 2
    results = lb["results"]
    assert results[0]["submission_id"] == "sub_b7_1"
    assert results[0]["rank"] == 1
    assert results[0]["final_score"] == 9.5

    assert results[1]["submission_id"] == "sub_b7_2"
    assert results[1]["rank"] == 2
    assert results[1]["final_score"] == 7.0


def test_get_leaderboard(setup_b7_fixtures):
    f = setup_b7_fixtures
    res = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/results")
    assert res.status_code == 200
    lb = res.json()
    assert len(lb["results"]) == 2


def test_export_csv(setup_b7_fixtures):
    """T2 Check: Export leaderboard results as CSV download."""
    f = setup_b7_fixtures
    res = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/results/export")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert 'attachment; filename=' in res.headers["content-disposition"]
    
    csv_text = res.text
    lines = csv_text.strip().split("\n")
    assert len(lines) >= 3
    assert "Rank,Submission ID,Title,Team Name,Track Name,Final Score" in lines[0]
    assert "1,sub_b7_1,Top Winner Project,Gold Team,,9.5" in lines[1]
