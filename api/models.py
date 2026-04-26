from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

# Hero class definition
class Hero(Base):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, nullable=False, index=True)
    role = Column(String, nullable=False)
    tier = Column(String, nullable=True)
    win_rate = Column(Float, nullable=False)
    pick_rate = Column(Float, nullable=False)
    ban_rate = Column(Float, nullable=False)
    matches_played = Column(Integer, nullable=False)
    season = Column(String, nullable=False)
    source = Column(String, nullable=False, default='rivalstracker')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Hero(name='{self.name}', role='{self.role}', tier='{self.tier}', win_rate={self.win_rate}, pick_rate={self.pick_rate}, ban_rate={self.ban_rate}, matches_played={self.matches_played}, season='{self.season}', source='{self.source}')>"

