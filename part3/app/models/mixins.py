"""SQLAlchemy mixin for our haunted models! 👻"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.declarative import declared_attr

from app import db


class SQLAlchemyMixin:
    """Our magical SQL translator! ✨"""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # Colonnes communes à tous les modèles
    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
    is_active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
