""" Profile Model """
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.tomboonedotcom.extensions import db

if TYPE_CHECKING:
    from src.tomboonedotcom.Models.Project import Project
    from src.tomboonedotcom.Models.Employer import Employer
    from src.tomboonedotcom.Models.Consulting import Consulting
    from src.tomboonedotcom.Models.Education import Education


class Profile(db.Model):
    """ Profile Model """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=True)
    tagline: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(120), nullable=True)
    github: Mapped[str] = mapped_column(String(120), nullable=True)
    linkedin: Mapped[str] = mapped_column(String(120), nullable=True)
    about: Mapped[str] = mapped_column(TEXT, nullable=True)
    projects: Mapped[List['Project']] = relationship(back_populates='profile')
    employers: Mapped[List['Employer']] = relationship(back_populates='profile')
    consulting: Mapped[List['Consulting']] = relationship(back_populates='profile')
    education: Mapped[List['Education']] = relationship(back_populates='profile')

    def __repr__(self):
        return f'<Profile {self.id}>'
