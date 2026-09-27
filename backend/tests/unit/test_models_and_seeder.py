import pytest
from app.core.database import SessionLocal
from app.models import User, Hackathon, Track, Team, Submission


def test_fixture_seeder_counts():
    db = SessionLocal()
    try:
        hackathon = db.query(Hackathon).first()
        assert hackathon is not None
        assert hackathon.name == "Sample Hack 2026"

        tracks_count = db.query(Track).count()
        assert tracks_count >= 8

        teams_count = db.query(Team).count()
        assert teams_count >= 40

        submissions_count = db.query(Submission).count()
        assert submissions_count >= 40
    finally:
        db.close()


def test_user_roles_seeded():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        assert len(users) >= 4
        roles = {u.role.value for u in users}
        assert "ORGANIZER" in roles
        assert "JUDGE" in roles
        assert "PARTICIPANT" in roles
    finally:
        db.close()
