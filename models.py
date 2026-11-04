from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    String,
    false,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(9), unique=True)
    name: Mapped[str] = mapped_column(String(100))

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint(
            "student_id ~ '^[0-9]{4}-[0-9]{4}$'",
            name="ck_users_student_id_format",
        ),
        CheckConstraint("length(trim(name)) > 0", name="ck_users_name_not_blank"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    rack: Mapped[str] = mapped_column(String(30))
    avg_minutes: Mapped[int] = mapped_column()

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("avg_minutes > 0", name="ck_services_avg_minutes"),
    )


class CollateralType(db.Model):
    __tablename__ = "collateral_types"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="collateral_type")


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="RESTRICT"))
    collateral_type_id: Mapped[int] = mapped_column(
        ForeignKey("collateral_types.id", ondelete="RESTRICT")
    )
    pe_class: Mapped[bool] = mapped_column(default=False, server_default=false())
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")
    collateral_type: Mapped["CollateralType"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
        CheckConstraint(
            "called_at IS NULL OR called_at >= created_at",
            name="ck_tickets_called_after_created",
        ),
        # One active ticket per student (FR-10, NFR-02), enforced by the database.
        Index(
            "uq_tickets_one_active_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("status IN ('waiting', 'called')"),
        ),
    )