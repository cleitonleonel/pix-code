from sqlalchemy import DECIMAL, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import mapper_registry


@mapper_registry.mapped_as_dataclass
class PixModel:
    __tablename__ = "pix"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, init=False, default=None, autoincrement=True
    )

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

    clicks: Mapped[int] = mapped_column(Integer, init=False, default=0, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    pix_key: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    identification: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=True)
    br_code: Mapped[str] = mapped_column(Text, nullable=False)
    base64_qr: Mapped[str] = mapped_column(Text, nullable=False)
    hash_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    __mapper_args__ = {"eager_defaults": True}

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "clicks": self.clicks,
            "full_name": self.full_name,
            "pix_key": self.pix_key,
            "city": self.city,
            "zip_code": self.zip_code,
            "amount": str(self.amount),
            "description": self.description,
            "identification": self.identification,
            "location": self.location,
            "br_code": self.br_code,
            "base64_qr": self.base64_qr,
            "hash_id": self.hash_id,
        }
