import bcrypt
from sqlalchemy import *
from sqlalchemy.orm import synonym, relationship

from app.common.extensions import Model
from app.common.utils import *
import urllib.parse

from flask import abort

def datetime_format(dt, f):
    return dt.strftime(f) if dt else None


class User(Model):
    __tablename__ = 'users'

    idx = Column('idx', INT, primary_key=True, autoincrement=True)
    email = Column('email', VARCHAR(50), nullable=False)
    _pw = Column('password', VARCHAR(100), nullable=False)
    profile_img = Column('profile_img', INT, ForeignKey('files.idx'), nullable=True)
    name = Column('name', VARCHAR(100), nullable=True)
    _birth = Column('birth', DATE, nullable=True)
    phone_number = Column('phone_number', VARCHAR(50), nullable=True)
    introduce = Column('introduce', VARCHAR(50), nullable=True)
    token = Column('token', VARCHAR(200), nullable=True)
    _created_at = Column('created_at', DATETIME, nullable=False, server_default=func.current_timestamp())
    _updated_at = Column('updated_at', DATETIME, nullable=False, server_default=func.current_timestamp(), server_onupdate=func.current_timestamp())
    _deleted_at = Column('deleted_at', DATETIME, nullable=True)
    _last_record_index_at = Column('last_record_index_at', DATETIME, nullable=True)
    _login_at = Column('login_at', DATETIME, nullable=True)

    profile_img_file = relationship('File', lazy='joined', uselist=False, foreign_keys=[profile_img])


    def __init__(self, email='', pw='', name=None, profile_img=None, phone_number=None, birth=None, token=None, introduce=None,
                 **kwargs):
        self.email = email
        self.pw = pw
        self.name = name
        self.profile_img = profile_img
        self.phone_number = phone_number
        self.birth = birth
        self.token = token
        self.introduce = introduce
    

    @property
    def pw(self):
        return self._pw

    @pw.setter
    def pw(self, pw):
        self._pw = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())

    pw = synonym('_pw', descriptor=pw)

    @property
    def profile_img_url(self):
        return urllib.parse.unquote(self.profile_img_file.url) if self.profile_img_file is not None else None

    @property
    def birth(self):
        return datetime_format(self._birth, '%Y.%m.%d')

    @birth.setter
    def birth(self, birth):
        self._birth = birth

    birth = synonym('_birth', descriptor=birth)

    @property
    def created_at(self):
        return datetime_format(self._created_at, '%Y.%m.%d %H:%M:%S')

    created_at = synonym('_created_at', descriptor=created_at)

    # @property
    # def updated_at(self):
    #     return datetime_format(self._updated_at, '%Y.%m.%d %H:%M:%S')

    # updated_at = synonym('_updated_at', descriptor=updated_at)

    # @property
    # def blocked_at(self):
    #     return datetime_format(self._blocked_at, '%Y.%m.%d %H:%M:%S')

    # @blocked_at.setter
    # def blocked_at(self, blocked_at):
    #     self._blocked_at = blocked_at

    # blocked_at = synonym('_blocked_at', descriptor=blocked_at)

    @property
    def deleted_at(self):
        return datetime_format(self._deleted_at, '%Y.%m.%d %H:%M:%S')

    # @deleted_at.setter
    # def deleted_at(self, deleted_at):
    #     self._deleted_at = deleted_at

    # deleted_at = synonym('_deleted_at', descriptor=deleted_at)

    @property
    def login_at(self):
        return datetime_format(self._login_at, '%Y.%m.%d %H:%M:%S')

    # @login_at.setter
    # def login_at(self, login_at):
    #     self._login_at = login_at

    # login_at = synonym('_login_at', descriptor=login_at)

    # @property
    # def consent_to_conditions(self):
    #     return datetime_format(self._consent_to_conditions, '%Y.%m.%d %H:%M:%S')

    # @consent_to_conditions.setter
    # def consent_to_conditions(self, consent_to_conditions):
    #     self._consent_to_conditions = consent_to_conditions

    # consent_to_conditions = synonym('_consent_to_conditions', descriptor=consent_to_conditions)

    @classmethod
    def authenticate(cls, email=None, password=None):
        if not email or not password:
            return None
        try:
            user = cls.query.filter(User.email == email).first()
            password = password.strip()
        
            if user and bcrypt.checkpw(password.encode('utf8'), user._pw.encode('utf8')):
                return user
        except:
             abort(500)

    def dict(self, filter=None):
        dic = dict(
            idx=self.idx,
            email=self.email,
            name=self.name,
            profile_img=self.profile_img,
            profile_img_url=self.profile_img_url,
            phone_number=self.phone_number,
            birth=self.birth,
            token=self.token,
            created_at=self.created_at,
            # updated_at=self.updated_at,
            # blocked_at=self.blocked_at,
            # deleted_at=self.deleted_at,
            # login_at=self.login_at,
            # consent_to_conditions=self.consent_to_conditions,
        )

        if filter is not None:
            dic = {key: dic.get(key, None) for key in dic if key in filter}

        return dic

    def dict_login(self, filter=None):
        dic = dict(
            idx=self.idx,
            token=self.token
        )

        if filter is not None:
            dic = {key: dic.get(key, None) for key in dic if key in filter}

        return dic
    
    def dict_profile(self, filter=None):
        dic = dict(
            idx=self.idx,
            email=self.email,
            name=self.name,
            profile_img_url=self.profile_img_url,
            phone_number=self.phone_number,
            created_at=self.created_at,
            introduce = self.introduce
        )

        if filter is not None:
            dic = {key: dic.get(key, None) for key in dic if key in filter}

        return dic