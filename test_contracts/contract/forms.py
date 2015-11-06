# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import QuerySelectField
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, DateTimeField, BooleanField
from wtforms.validators import DataRequired

from test_contracts.models import Services, Ships



def support():
    return Services.query.filter_by(category='1').all()


def combat():
    return Services.query.filter_by(category='3').all()


def shiptype():
    return Ships.query.all()


class BasicOrder(Form):
    start_location = StringField("Start Location")
    end_location = StringField("End Location")
    ship = QuerySelectField(query_factory=shiptype, label="Ship Being Used")
    description = TextAreaField("Description of Job", [DataRequired("Please provide a brief description.")])
    time = DateTimeField(label="Estimated Time")
    submit = SubmitField(label='Submit')


class Support(BasicOrder, Form):
    service = QuerySelectField(query_factory=support)
    scu = IntegerField("SCU Amount")
    fuel = IntegerField("Fuel Amount")
    passengers = IntegerField("Passenger Count")


class Crew(BasicOrder, Form):
    pilot = IntegerField("Pilots")
    radar = IntegerField("Radar Operators")
    weapons = IntegerField("Weapon Operators")
    gunner = IntegerField("Gunners")
    engineer = IntegerField("Engineers")
    navigation = IntegerField("Navigations")
    communications = IntegerField("Communications")
    security = IntegerField("Ship Security")
    science = IntegerField("Science")
    medical = IntegerField("Medical")


class Combat(BasicOrder, Form):
    service = QuerySelectField(query_factory=combat)
    scu = IntegerField("SCU Amount")
    fuel = IntegerField("Fuel Amount")
    passengers = IntegerField("Passenger Count")


class ChangeTime(Form):
    time = DateTimeField(label="Estimated Time")
    submit = SubmitField(label='Change')


class AddNote(Form):
    private = BooleanField(label="Private")
    note = TextAreaField()
    submit = SubmitField(label='Add')