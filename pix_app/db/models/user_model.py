import bcrypt
from sqlalchemy import Boolean, DateTime, Integer, LargeBinary, String, func
from sqlalchemy.orm import Mapped, mapped_column
from pix_app.db.base import mapper_registry


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, init=False, autoincrement=True
    )

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default=None,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
        default=None,
        onupdate=func.now(),
        nullable=False,
    )

    __mapper_args__ = {"eager_defaults": True}

    def set_password(self, password: str) -> None:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
        }
