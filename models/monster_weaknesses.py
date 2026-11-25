from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base



class MonsterWeakness(Base):
        __tablename__ = "monster_weaknesses"
        __table_args__ = (
            UniqueConstraint("monster_id", "element", name="uq_monster_element"),
        )
        monster = relationship(
            "Monster",
            back_populates="weaknesses"
        )

        id: Mapped[int] = mapped_column(
            mysql.BIGINT(unsigned=True),
            primary_key=True,
            autoincrement=True,
            comment="弱点记录编号",
        )
        monster_id: Mapped[int] = mapped_column(
            mysql.BIGINT(unsigned=True),
            ForeignKey("monsters.id", ondelete="CASCADE"),
            comment="怪物出场记录编号",
        )
        element: Mapped[str] = mapped_column(
            mysql.VARCHAR(32), comment="弱点属性名称"
        )












