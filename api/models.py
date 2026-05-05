from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from api.database import Base

class Hero(Base):
    """
    SQLAlchemy model for the Hero table in the database.
    """
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, nullable=False, index=True)
    normalized_name = Column(String, unique=False, nullable=False, index=True)
    role = Column(String, nullable=False)
    tier = Column(String, nullable=True)
    win_rate = Column(Float, nullable=False)
    pick_rate = Column(Float, nullable=False)
    ban_rate = Column(Float, nullable=False)
    matches_played = Column(Integer, nullable=False)
    season = Column(String, nullable=False)
    source = Column(String, nullable=False, default='rivalsmeta')
    source_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        """
        Return a string representation of the Hero instance for debugging purposes.
        """
        return f"<Hero(name='{self.name}', role='{self.role}', tier='{self.tier}', win_rate={self.win_rate}, pick_rate={self.pick_rate}, ban_rate={self.ban_rate}, matches_played={self.matches_played}, season='{self.season}', source='{self.source}', source_url='{self.source_url}')>"

class TeamUp(Base):
    """
    SQLAlchemy model for the TeamUp table in the database.
    """
    __tablename__ = 'teamups'

    id = Column(Integer, primary_key=True, index=True)
    teamup_name = Column(String, nullable=False)
    normalized_teamup_name = Column(String, nullable=False, index=True)
    heroes = Column(String, nullable=False)
    variant_size = Column(Integer, nullable=False)
    tier = Column(String, nullable=True)
    win_rate = Column(Float, nullable=False)
    pick_rate = Column(Float, nullable=True)
    matches_played = Column(Integer, nullable=False)
    season = Column(String, nullable=False)
    source = Column(String, nullable=False, default='rivalsmeta')
    source_url = Column(String, nullable=True)

    def __repr__(self):
        """
        Return a string representation of the TeamUp instance for debugging purposes.
        """
        return f"<TeamUp(teamup_name='{self.teamup_name}', normalized_teamup_name='{self.normalized_teamup_name}', heroes='{self.heroes}', variant_size={self.variant_size}, win_rate={self.win_rate}, pick_rate={self.pick_rate}, matches_played={self.matches_played}, season='{self.season}', source='{self.source}', source_url='{self.source_url}')>"