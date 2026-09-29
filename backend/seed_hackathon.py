import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal, engine, Base
import app.models
Base.metadata.create_all(bind=engine)

from app.models.hackathon import Hackathon
from app.models.track import Track
from app.utils.enums import HackathonStatus
from datetime import datetime

db = SessionLocal()

# Create demo hackathon
existing = db.query(Hackathon).filter(Hackathon.id == "evt_01").first()
if not existing:
    h = Hackathon(
        id="evt_01",
        name="NOVA AI Innovation Challenge 2026",
        description="Build the future of AI-powered developer tools. This is your chance to create groundbreaking solutions that push the boundaries of what's possible with LLMs, autonomous agents, and browser automation.",
        status=HackathonStatus.ACTIVE,
        organizer_id="usr_org_001",
        max_team_size=4,
        min_team_size=1,
        blind_review_enabled=True,
        registration_start=datetime(2026, 1, 1),
        registration_end=datetime(2026, 10, 31),
        submissions_start=datetime(2026, 1, 15),
        submissions_close=datetime(2026, 11, 30),
        payment_required=False,
        registration_fee=0.0,
        currency="USD",
        results_status="DRAFT"
    )
    db.add(h)
    db.flush()
    print("Created hackathon evt_01:", h.name)

    # Add tracks
    tracks = [
        ("trk_01", "Developer Tools & Automation", "Build tools that help developers build faster."),
        ("trk_02", "AI Agents & LLMs", "Autonomous AI agents solving real-world problems."),
        ("trk_03", "Web3 & Decentralization", "Decentralized apps and blockchain innovation."),
        ("trk_04", "Climate Tech", "Technology for a sustainable future."),
    ]
    for tid, tname, tdesc in tracks:
        t = Track(id=tid, hackathon_id="evt_01", name=tname, description=tdesc)
        db.add(t)
        print(f"  Added track: {tname}")
else:
    print(f"Hackathon evt_01 already exists: {existing.name}")
    # Ensure organizer is correct
    existing.organizer_id = "usr_org_001"
    print("Updated organizer_id")

db.commit()
db.close()
print("Hackathon seed complete!")
