from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.models.enums import (
    DocStatusEnum,
    DocTypeEnum,
)


class Docs(Base):
    __tablename__ = "docs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    doc_type: Mapped[DocTypeEnum] = mapped_column(
        Enum(DocTypeEnum),
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    status: Mapped[DocStatusEnum] = mapped_column(
        Enum(DocStatusEnum),
        nullable=False,
        default=DocStatusEnum.PENDING,
    )

    carrier_id: Mapped[int] = mapped_column(
        ForeignKey(
            "carriers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    carrier: Mapped["Carrier"] = relationship(
        "Carrier",
        back_populates="docs",
    )