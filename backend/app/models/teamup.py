"""
SQLAlchemy model for Marvel Rivals team-up meta statistics.
"""

from sqlalchemy import Column, Float, Integer, String

from backend.app.db.database import Base


class TeamUp(Base):
    """
    Database table representing a team-up combination's meta statistics.

    The `heroes` field stores the participating hero names as a comma-separated
    string because team-up variants are ingested from external meta sources in a
    compact source-driven format.
    """

    __tablename__ = "teamups"

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
    source = Column(String, nullable=False, default="rivalsmeta")
    source_url = Column(String, nullable=True)

    def __repr__(self) -> str:
        """
        Return a compact debug representation of the team-up record.
        """

        return (
            f"<TeamUp(teamup_name='{self.teamup_name}', "
            f"heroes='{self.heroes}', variant_size={self.variant_size}, "
            f"win_rate={self.win_rate}, pick_rate={self.pick_rate}, "
            f"season='{self.season}')>"
        )