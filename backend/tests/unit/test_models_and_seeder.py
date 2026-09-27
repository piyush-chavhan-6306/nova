from app.core.database import SessionLocal
from app.models import Hackathon, Track, Judge, Team, Submission, Review, Score, User


def test_fixture_seeder_counts():
    db = SessionLocal()
    try:
        hackathon = db.query(Hackathon).first()
        assert hackathon is not None
        assert hackathon.name == "Sample Hack 2026"

        tracks_count = db.query(Track).count()
        assert tracks_count == 8

        judges_count = db.query(Judge).count()
        assert judges_count == 30

        teams_count = db.query(Team).count()
        assert teams_count == 40

        submissions_count = db.query(Submission).count()
        assert submissions_count >= 40

        reviews_count = db.query(Review).count()
        assert reviews_count > 0

        scores_count = db.query(Score).count()
        assert scores_count > 0
    finally:
        db.close()


def test_user_roles():
    db = SessionLocal()
    try:
        organizer = db.query(User).filter(User.id == "usr_organizer").first()
        assert organizer is not None
        assert organizer.role.value == "ORGANIZER"
    finally:
        db.close()
