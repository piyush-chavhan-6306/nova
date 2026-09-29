from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base

class Prize(Base):
    __tablename__ = "prizes"

    id = Column(String(50), primary_key=True, index=True)
    hackathon_id = Column(String(50), ForeignKey("hackathons.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=True)
    value = Column(String(100), nullable=True)
