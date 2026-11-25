
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


if TYPE_CHECKING:
    from models.periods import Period


class Reward(Base):
    __tablename__ = "rewards"

    __table_args__ = (
        UniqueConstraint(
            "period_id",
            "slot_no",
            name="uq_reward_slot",
        ),
    )

    # 与 Period 建立多对一关系
    period: Mapped["Period"] = relationship(
        "Period",
        back_populates="rewards",
    )

    # 奖励记录编号
    id: Mapped[int] = mapped_column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="奖励记录编号",
    )

    # 所属期数标识
    period_id: Mapped[str] = mapped_column(
        mysql.VARCHAR(128),
        ForeignKey("periods.id", ondelete="CASCADE"),
        nullable=False,
        comment="所属期数标识",
    )

    # 当期奖励顺序
    slot_no: Mapped[int] = mapped_column(
        mysql.INTEGER(unsigned=True),
        nullable=False,
        comment="当期奖励顺序，从一开始",
    )

    # 奖励名称
    name: Mapped[str] = mapped_column(
        mysql.VARCHAR(128),
        nullable=False,
        comment="奖励名称",
    )

    # 可选图标
    icon: Mapped[str | None] = mapped_column(
        mysql.VARCHAR(255),
        nullable=True,
        comment="可选图标标识",
    )

    # 获得数量
    amount: Mapped[int] = mapped_column(
        mysql.BIGINT(unsigned=True),
        nullable=False,
        comment="获得数量",
    )

    # 获得条件
    condition_text: Mapped[str] = mapped_column(
        mysql.TEXT(),
        nullable=False,
        comment="获得条件",
    )
