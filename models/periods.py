from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Index, UniqueConstraint, text
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.monsters import Monster
from models.rewards import Reward


class Period(Base):
    __tablename__ = "periods"
    __table_args__ = (
        UniqueConstraint(
            "mode", "major_version", "minor_version", "half",
            name="uq_period_version",
        ),
        Index("ix_period_mode_start", "mode", "start_time"),
        Index("ix_period_start", "start_time"),
        CheckConstraint("major_version >= 1"),
        CheckConstraint("minor_version BETWEEN 1 AND 7"),
        CheckConstraint("end_time > start_time"),
    )

    id: Mapped[str] = mapped_column(
        mysql.VARCHAR(128), primary_key=True, comment="前端期数标识"
    )
    mode: Mapped[str] = mapped_column(
        mysql.ENUM("fiction", "forgotten", "apocalypse", "arbitration"),
        comment="玩法代码",
    )
    major_version: Mapped[int] = mapped_column(
        mysql.INTEGER(), comment="大版本号"
    )
    minor_version: Mapped[int] = mapped_column(
        mysql.INTEGER(), comment="小版本序号，范围一至七"
    )
    half: Mapped[str] = mapped_column(
        mysql.ENUM("上半", "下半"), comment="半期"
    )

    # MySQL DATETIME 不保存时区，按表约定写入 UTC 时间。
    start_time: Mapped[datetime] = mapped_column(
        mysql.DATETIME(fsp=6), comment="开放时间，世界协调时"
    )
    end_time: Mapped[datetime] = mapped_column(
        mysql.DATETIME(fsp=6), comment="结束时间，世界协调时"
    )
    total_hp: Mapped[int] = mapped_column(
        mysql.BIGINT(unsigned=True), comment="当期全部阵容血量之和"
    )
    created_at: Mapped[datetime] = mapped_column(
        mysql.TIMESTAMP(fsp=6),
        server_default=text("CURRENT_TIMESTAMP(6)"),
        comment="记录创建时间",
    )

    # slot_no 决定怪物阵容与奖励的展示顺序。
    monsters: Mapped[list[Monster]] = relationship(
        back_populates="period",
        order_by="Monster.slot_no",
        cascade="save-update, merge, delete",
        passive_deletes=True,
    )
    rewards: Mapped[list[Reward]] = relationship(
        back_populates="period",
        order_by="Reward.slot_no",
        cascade="save-update, merge, delete",
        passive_deletes=True,
    )
    @property
    def version(self) -> str:
        return f"{self.major_version}.{self.minor_version}"