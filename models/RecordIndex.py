import bcrypt
from sqlalchemy import *
from sqlalchemy.orm import synonym, relationship

from app.common.extensions import Model
from app.common.utils import *
import urllib.parse

from flask import abort

def datetime_format(dt, f):
    return dt.strftime(f) if dt else None


class RecordIndex(Model):
    __tablename__ = 'record_idx_logs'

    idx = Column('idx', INT, primary_key=True, autoincrement=True)
    user_idx = Column('user_idx', INT, nullable=False)
    record_value = Column('record_value', VARCHAR(10), nullable=False)
    _created_at = Column('created_at', DATETIME, nullable=False, server_default=func.current_timestamp())


    # previous_record_idx = relationship('', lazy='dynamic',)


    def __init__(self, user_idx='', record_value=None,
                 **kwargs):

        self.user_idx = user_idx,
        self.record_value = record_value
    

    @property
    def created_at(self):
        return datetime_format(self._created_at, '%Y.%m.%d %H:%M:%S')

    created_at = synonym('_created_at', descriptor=created_at)


    def dict(self, filter=None):
        dic = dict(
            idx = self.idx,
            user_idx = self.user_idx,
            record_value = self.record_value,
            created_at = self.created_at
        )

        if filter is not None:
            dic = {key: dic.get(key, None) for key in dic if key in filter}

        return dic
