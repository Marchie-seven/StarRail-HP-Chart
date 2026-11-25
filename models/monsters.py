
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Monster(Base):
    __tablename__ = "monsters"

    __table_args__ = (
        UniqueConstraint(
            "period_id",
            "slot_no",
            name="uq_monster_slot"
        ),
    )

    period = relationship(
        "Period",
        back_populates="monsters"
    )

    weaknesses = relationship(
        "MonsterWeakness",
        back_populates="monster"
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    period_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("periods.id"),
        index=True,
        nullable=False
    )

    slot_no: Mapped[int] = mapped_column(
        index=True,
        nullable=False
    )

    source_id: Mapped[str] = mapped_column(
        String(200),
        index=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        index=True,
        nullable=False
    )

    hp: Mapped[int] = mapped_column(
        index=True,
        nullable=False
    )

    floor: Mapped[str] = mapped_column(
        String(200),
        index=True,
        nullable=False
    )

    room: Mapped[str] = mapped_column(
        String(200),
        index=True,
        nullable=False
    )

    note: Mapped[str] = mapped_column(
        String(200),
        index=True,
        nullable=False
    )
