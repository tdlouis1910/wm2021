import bcrypt
from sqlalchemy import *
from sqlalchemy.orm import synonym, relationship

from app.common.extensions import Model
from app.common.utils import *
import urllib.parse

from flask import abort

def datetime_format(dt, f):
    return dt.strftime(f) if dt else None


class Customer(Model):
    __tablename__ = 'customers'

    idx = Column('idx', INT, primary_key=True, autoincrement=True)
    email = Column('email', VARCHAR(100), nullable=False)
    name = Column('name', VARCHAR(50), nullable=True)
    phone_number = Column('phone_number', VARCHAR(12), nullable=False)
    area = Column('area', VARCHAR(50), nullable=True)
    district = Column('district', VARCHAR(50), nullable=True)
    province = Column('province', VARCHAR(50), nullable=True)
    enabled = Column('enabled', VARCHAR(5), nullable=True)
    _created_at = Column('created_at', DATETIME, nullable=False, server_default=func.current_timestamp())
    _deleted_at = Column('deleted_at', DATETIME, nullable=True)


    def __init__(self, email='', name=None, phone_number=None, area=None, district=None, province=None, enabled=None,
                 **kwargs):

        self.email = email
        self.name = name
        self.phone_number = phone_number
        self.area = area
        self.district = district
        self.province = province
        self.enabled = "True"
    

    @property
    def created_at(self):
        return datetime_format(self._created_at, '%Y.%m.%d %H:%M:%S')

    created_at = synonym('_created_at', descriptor=created_at)

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
            email = self.email,
            name = self.name,
            phone_number = self.phone_number,
            area = self.area,
            district = self.district,
            province = self.province,
            enabled = True
        )

        if filter is not None:
            dic = {key: dic.get(key, None) for key in dic if key in filter}

        return dic
