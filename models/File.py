from sqlalchemy import *
from sqlalchemy.orm import synonym

from app.common.extensions import Model
from app.common.utils import *


class File(Model):
    __tablename__ = 'files'

    idx = Column('idx', INT, primary_key=True, autoincrement=True)
    url = Column('url', VARCHAR(255), nullable=True)
    mime = Column('mime', VARCHAR(100), nullable=True)
    _created_at = Column('created_at', DATETIME, nullable=False, server_default=func.current_timestamp())

    def __init__(self, url=None, mime=None,
                 **kwargs):
        self.url = url
        self.mime = mime

    @property
    def filename(self):
        return self.url[self.url.rfind("/")+1:]

    @property
    def created_at(self):
        return datetime_format(self._created_at, '%Y.%m.%d %H:%M:%S')

    created_at = synonym('_created_at', descriptor=created_at)

    def dict(self):
        return dict(
            idx=self.idx,
            url=self.url,
            filename=self.filename,
            mime=self.mime,
            created_at=self.created_at
        )
