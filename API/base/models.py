from datetime import datetime, timedelta
from database import Base
from sqlalchemy.orm import Mapped, mapped_column

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    @property
    def created_at_with_utc(self):
        return self.created_at + timedelta(hours=5)
    
    @property
    def updated_at_with_utc(self):
        return self.updated_at + timedelta(hours=5)