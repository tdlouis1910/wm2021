import bcrypt
from sqlalchemy import *
from sqlalchemy.orm import synonym, relationship

from app.common.extensions import Model
from app.common.utils import *
import urllib.parse

from flask import abort

def datetime_format(dt, f):
    return dt.strftime(f) if dt else None


class WaterMeter(Model):
    __tablename__ = 'water_meter'

    idx = Column('idx', INT, primary_key=True, autoincrement=True)
    customer_id = Column('customer_id', INT, nullable=False)
    owner_id = Column('owner_id', INT, nullable=False)
    previous_record_idx = Column('previous_record_idx', INT, ForeignKey('record_idx_logs.idx'), nullable=False)
    record_idx = Column('record_idx',INT, ForeignKey('record_idx_logs.idx'), nullable=False)
    record_count = Column('record_count', INT, nullable=False)
    _created_at = Column('created_at', DATETIME, nullable=False, server_default=func.current_timestamp())
    _updated_at = Column('updated_at', DATETIME, nullable=True)
    _deleted_at = Column('deleted_at', DATETIME, nullable=True)


    # previous_record_idx = relationship('RecordIndex', lazy='dynamic', foreign_keys=[previous_record_idx])


    # previous_record_idx = relationship('RecordIndex', lazy='dynamic', primaryjoin="WaterMeter.previous_record_idx == RecordIndex.idx")
    # record_idx = relationship('RecordIndex', lazy='dynamic', primaryjoin="WaterMeter.record_idx == RecordIndex.idx")


    def __init__(self, customer_id='', owner_id=None, previous_record_idx=None, record_idx=None, record_count=None,
                 **kwargs):

        self.customer_id = customer_id,
        self.owner_id = owner_id,
        self.previous_record_idx = previous_record_idx,
        self.record_idx = record_idx,
        self.record_count = record_count
    

    @property
    def created_at(self):
        return datetime_format(self._created_at, '%Y.%m.%d %H:%M:%S')

    created_at = synonym('_created_at', descriptor=created_at)

    @property
    def updated_at(self):
        return datetime_format(self._updated_at, '%Y.%m.%d %H:%M:%S')

    updated_at = synonym('_updated_at', descriptor=updated_at)


    @property
    def deleted_at(self):
        return datetime_format(self._deleted_at, '%Y.%m.%d %H:%M:%S')

    @deleted_at.setter
    def deleted_at(self, deleted_at):
        self._deleted_at = deleted_at

    deleted_at = synonym('_deleted_at', descriptor=deleted_at)


    def dict(self, filter=None):
        dic = dict(
            idx = self.idx,
            customer_id = self.customer_id,
            owner_id = self.owner_id,
            prev_idx = self.previous_record_idx,
            record_idx = self.record_idx,
            record_count = self.record_count
        )

        if filter is not None:
            dic = {key: dic.get(key, None) for key in dic if key in filter}

        return dic
