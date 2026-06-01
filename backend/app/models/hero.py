"""
SQLAlchemy model for Marvel Rivals hero meta statistics.
"""

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from backend.app.db.database import Base


class Hero(Base):
    """
    Database table representing a hero's meta statistics.

    Each row stores source-derived performance data for a Marvel Rivals hero,
    including role, tier, win rate, pick rate, ban rate, match volume, season,
    and source metadata.
    """

    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    normalized_name = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    tier = Column(String, nullable=True)

    win_rate = Column(Float, nullable=False)
    pick_rate = Column(Float, nullable=False)
    ban_rate = Column(Float, nullable=False)
    matches_played = Column(Integer, nullable=False)

    season = Column(String, nullable=False)
    source = Column(String, nullable=False, default="rivalsmeta")
    source_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """
        Return a compact debug representation of the hero record.
        """

        return (
            f"<Hero(name='{self.name}', role='{self.role}', tier='{self.tier}', "
            f"win_rate={self.win_rate}, pick_rate={self.pick_rate}, "
            f"ban_rate={self.ban_rate}, season='{self.season}')>"
        )