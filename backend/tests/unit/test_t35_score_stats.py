import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, Submission, Judge, Review, Score
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole, SubmissionStatus, ReviewStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t35_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t35_{uid}"
    hack = Hackathon(id=hack_id, name="T35 Score Stats Hackathon", status=HackathonStatus.ACTIVE)
    db.add(hack)

    # Submissions
    sub1 = Submission(id=f"sub_t35_1_{uid}", hackathon_id=hack_id, team_id=f"tm1_{uid}", title="Project 1", status=SubmissionStatus.SUBMITTED)
    sub2 = Submission(id=f"sub_t35_2_{uid}", hackathon_id=hack_id, team_id=f"tm2_{uid}", title="Project 2", status=SubmissionStatus.SUBMITTED)
    db.add(sub1)
    db.add(sub2)

    # Judge
    j_user_id = f"usr_t35_{uid}"
    j_user = User(id=j_user_id, email=f"j_{uid}@example.com", name="Judge T35", role=UserRole.JUDGE, hashed_password=get_password_hash("password"))
    db.add(j_user)

    j_profile = Judge(id=f"jdg_t35_{uid}", user_id=j_user_id, hackathon_id=hack_id)
    db.add(j_profile)

    # Reviews
    rev1 = Review(id=f"rev_t35_1_{uid}", submission_id=sub1.id, judge_id=j_profile.id, status=ReviewStatus.SUBMITTED)
    rev2 = Review(id=f"rev_t35_2_{uid}", submission_id=sub2.id, judge_id=j_profile.id, status=ReviewStatus.SUBMITTED)
    rev3 = Review(id=f"rev_t35_3_{uid}", submission_id=sub1.id, judge_id=j_profile.id, status=ReviewStatus.SUBMITTED)
    db.add(rev1)
    db.add(rev2)
    db.add(rev3)

    # Scores
    sc1 = Score(id=f"sc_1_{uid}", review_id=rev1.id, criterion_id="c1", score=10.0)
    sc2 = Score(id=f"sc_2_{uid}", review_id=rev2.id, criterion_id="c1", score=50.0)
    sc3 = Score(id=f"sc_3_{uid}", review_id=rev3.id, criterion_id="c1", score=12.0)
    db.add(sc1)
    db.add(sc2)
    db.add(sc3)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "judge_id": f"jdg_t35_{uid}"
    }


def test_t35_score_stats_and_outliers(setup_t35_fixtures):
    f = setup_t35_fixtures

    # 1. Get Hackathon Score Statistics
    res_stats = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/score-statistics")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["score_count"] == 3
    assert stats["minimum"] == 10.0
    assert stats["maximum"] == 50.0

    # 2. Get Judge Score Statistics
    res_jstats = client.get(f"/api/v1/judges/{f['judge_id']}/score-statistics")
    assert res_jstats.status_code == 200
    jstats = res_jstats.json()
    assert jstats["completed_reviews"] == 3

    # 3. Get Score Outliers
    res_outliers = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/score-outliers")
    assert res_outliers.status_code == 200
    outliers = res_outliers.json()
    assert "outliers_count" in outliers
