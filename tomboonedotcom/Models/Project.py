""" Project Model """
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tomboonedotcom.extensions import db

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from tomboonedotcom.Models import Profile


class Project(db.Model):
    """ Project Model """
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    sort: Mapped[int] = mapped_column()
    profile_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    profile: Mapped['Profile'] = relationship(back_populates='projects')
