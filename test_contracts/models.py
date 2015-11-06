# -*- coding: utf-8 -*-
from datetime import datetime as dt
import hashlib
import os
import random
import string
from flask_security import UserMixin, RoleMixin
from flask_security.utils import verify_password, encrypt_password
from flask import request
from test_contracts.words import nouns, adjectives
from test_contracts.database import (
    db,
    Model,
    SurrogatePK,
)


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

user_interests = db.Table('user_interests',
                          db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                          db.Column('interest_id', db.Integer(), db.ForeignKey('interests.id')))

user_crewroles = db.Table('user_crewroles',
                          db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                          db.Column('crewroles_id', db.Integer(), db.ForeignKey('crewroles.id')))

contract_notes = db.Table('contract_notes',
                          db.Column('note_id', db.Integer(), db.ForeignKey('note.id')),
                          db.Column('contract_id', db.Integer(), db.ForeignKey('contract.id')))

contract_events = db.Table('contract_events',
                           db.Column('event_id', db.Integer(), db.ForeignKey('event.id')),
                           db.Column('contract_id', db.Integer(), db.ForeignKey('contract.id')))


class Interests(SurrogatePK, Model):
    __tablename__ = 'interests'
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean(), default=0)

    def __repr__(self):
        return '{name}'.format(name=self.name)


class CrewRoles(SurrogatePK, Model):
    __tablename__ = 'crewroles'
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean(), default=0)

    def __repr__(self):
        return '{name}'.format(name=self.name)


class Role(SurrogatePK, Model, RoleMixin):
    __tablename__ = 'role'
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '{name}'.format(name=self.name)


class User(SurrogatePK, Model, UserMixin):
    __tablename__ = 'user'
    # Site specific
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, nullable=False, default=dt.utcnow())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    avatar_hash = db.Column(db.String(32))
    # Security
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer())
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    # Contact Info
    email = db.Column(db.String(80), unique=True, nullable=False)
    anonymous = db.Column(db.Boolean)
    website = db.Column(db.String(255), nullable=True)
    organization = db.Column(db.String(10), nullable=True)
    spectrum = db.Column(db.String(10), nullable=True)
    handle = db.Column(db.String(100), nullable=True)
    # jobs
    contracts = db.relationship('Contract', foreign_keys='Contract.user_id', backref='user',
                                lazy='dynamic')
    assigned_to = db.relationship('Contract', foreign_keys='Contract.assigned_to', backref='assigned',
                                  lazy='dynamic')
    interests = db.relationship('Interests', secondary=user_interests,
                                backref=db.backref('users', lazy='dynamic'))
    crewroles = db.relationship('CrewRoles', secondary=user_crewroles,
                                backref=db.backref('users', lazy='dynamic'))
    notes = db.relationship('Note', backref='user')
    events = db.relationship('Event', backref='user')
    recipient = db.relationship('Messages', foreign_keys='Messages.recipient_id', backref='recipient', lazy='dynamic')
    sender = db.relationship('Messages', foreign_keys='Messages.sender_id', backref='sender', lazy='dynamic')
    user_for = db.relationship('Messages', foreign_keys='Messages.user_for_id', backref='user_for', lazy='dynamic')

    def __init__(self, email, password=None, **kwargs):
        db.Model.__init__(self, email=email, **kwargs)
        if self.email is not None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = encrypt_password(password)

    def check_password(self, value):
        return verify_password(value, self.password)

    def gravatar(self, size=100, default='identicon', rating='r'):
        if self.email is None:
            return
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        if self.avatar_hash is None:
            self.avatar_hash = hash
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '{username}'.format(username=self.username)


class Services(SurrogatePK, Model):
    __tablename__ = 'services'
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    category = db.Column(db.Integer, db.ForeignKey('servicecategory.id'))
    Contract = db.relationship('Contract', backref='services',
                               lazy='dynamic')
    active = db.Column(db.Boolean(), default='False')

    def __repr__(self):
        return '{name}'.format(name=self.name)


class ServiceCategory(SurrogatePK, Model):
    __tablename__ = 'servicecategory'
    name = db.Column(db.String(50), unique=True)
    services = db.relationship('Services', backref='servicecategory')

    def __repr__(self):
        return '{name}'.format(name=self.name)


class Divisions(SurrogatePK, Model):
    __tablename__ = 'divisions'
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean(), default='False')

    def __repr__(self):
        return '{name}'.format(name=self.name)


class Ships(SurrogatePK, Model):
    __tablename__ = 'ships'
    name = db.Column(db.String(100))
    manufacturer = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    maxcrew = db.Column(db.String(100))
    scu = db.Column(db.String(100))
    lifesupport = db.Column(db.String(100))
    gunners = db.Column(db.String(100))
    contract = db.relationship('Contract', backref='ship', lazy='dynamic')

    def __repr__(self):
        return '{name}'.format(name=self.name)


class Manufacturer(SurrogatePK, Model):
    __tablename__ = 'manufacturer'
    name = db.Column(db.String(100))
    abbr = db.Column(db.String(7))
    ship = db.relationship('Ships', backref='Manufacturer', lazy='dynamic')

    def __repr__(self):
        return '{name}'.format(name=self.name)


class Contract(SurrogatePK, Model):
    __tablename__ = 'contract'
    # basic contract info
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_location = db.Column(db.String(200))
    end_location = db.Column(db.String(200))
    description = db.Column(db.Text)
    time = db.Column(db.DateTime())
    code = db.Column(db.String(100))
    invoice = db.Column(db.String(50))
    # support info
    scu = db.Column(db.Integer)
    fuel = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    # crew info
    pilot = db.Column(db.Integer)
    radar = db.Column(db.Integer)
    weapons = db.Column(db.Integer)
    gunner = db.Column(db.Integer)
    engineer = db.Column(db.Integer)
    navigation = db.Column(db.Integer)
    communications = db.Column(db.Integer)
    security = db.Column(db.Integer)
    science = db.Column(db.Integer)
    medical = db.Column(db.Integer)
    # technical info and contractor
    created_on = db.Column(db.DateTime(), default=dt.utcnow())
    last_updated = db.Column(db.DateTime(), default=dt.utcnow())
    # status codes
    # 6 = new, 5 = pending, 4 = assigned, 3 = in progress, 2 = completed, 1 = cancelled, 0 = denied
    status = db.Column(db.String(10), default=6)
    notes = db.relationship('Note', secondary=contract_notes,
                            backref=db.backref('contract', lazy='dynamic'))
    events = db.relationship('Event', secondary=contract_events,
                             backref=db.backref('contract', lazy='dynamic'))

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
        if self.invoice is None:
            self.invoice = Contract.create_invoice_id()
        if self.code is None:
            self.code = Contract.create_code_word()


    @staticmethod
    def create_invoice_id():
        chars = string.ascii_lowercase + string.digits
        random.seed = os.urandom(1024)
        invoice_id = ''.join(random.choice(chars) for i in range(8))
        invoice_check = Contract.query.filter_by(invoice=invoice_id).first()

        if invoice_check is not None:
            Contract.invoice_id()
        else:
            return invoice_id.upper()

    @staticmethod
    def create_code_word():
        random.seed = os.urandom(1024)
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        code = '{0} {1}'.format(adjective.capitalize(), noun.capitalize())
        code_check = Contract.query.filter_by(code=code).first()

        if code_check is not None:
            Contract.code_word()
        else:
            return code

    def __repr__(self):
        return '{invoice}'.format(invoice=self.invoice)


class StaticPage(SurrogatePK, Model):
    __tablename__ = 'static'
    name = db.Column(db.String(50), unique=True)
    content = db.Column(db.UnicodeText)

    def __repr__(self):
        return '{name}'.format(name=self.name)


class Faq(SurrogatePK, Model):
    __tablename__ = 'faq'
    category = db.Column(db.String(80))
    active = db.Column(db.Boolean)
    question = db.Column(db.Text)
    answer = db.Column(db.UnicodeText)

    def __repr__(self):
        return '{id}'.format(id=self.id)


class Note(SurrogatePK, Model):
    __tablename__ = "note"
    time = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note = db.Column(db.Text)
    staff_flag = db.Column(db.Boolean)
    contractor_flag = db.Column(db.Boolean)
    client_flag = db.Column(db.Boolean)

    def __repr__(self):
        return '{id}'.format(id=self.id)


class Event(SurrogatePK, Model):
    __tablename__ = "event"
    time = db.Column(db.DateTime(), default=dt.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event = db.Column(db.String(255))
    staff_flag = db.Column(db.Boolean, default=1)
    contractor_flag = db.Column(db.Boolean, default=1)
    client_flag = db.Column(db.Boolean, default=1)

    def __repr__(self):
        return '{id}'.format(id=self.id)


class Messages(SurrogatePK, Model):
    __tablename__ = 'messages'
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_for_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    unread = db.Column(db.Boolean, nullable=False, default=True)
    trash = db.Column(db.Boolean, nullable=False, default=False)
    draft = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '{id}'.format(id=self.id)