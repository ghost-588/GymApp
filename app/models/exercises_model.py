from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Foreign Keys
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("all_exercises.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    exercise = relationship(
        "AllExercises",
        back_populates="exercises",
        foreign_keys=[exercise_id],
        passive_deletes=True,
    )
    user = relationship(
        "User", back_populates="exercises", foreign_keys=[user_id], passive_deletes=True
    )

    sets = relationship(
        "Set",
        back_populates="exercise",
        foreign_keys="[Set.exercise_id]",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
