# -*- coding: utf-8 -*-
from datetime import datetime


def get_name():
    name = 'Nobody'
    if auth.user:
        name = auth.user.first_name + ' ' + auth.user.last_name
    return name

def get_phone():
    phone = ''
    if auth.user:
        phone = auth.user.phone
    return phone

CATEGORY = ['Car', 'Bike', 'Books', 'Music', 'Outdoors', 'For the house', 'Misc']


db.define_table('bboard',
                Field('name'),
                Field('user_id', db.auth_user),
                Field('title'),
                Field('phone'),
                Field('email'),
                Field('category'),
                Field('date_posted', 'datetime'),
                Field('price'),
                Field('is_sold', 'boolean'),
                Field('filename', 'upload'),
                Field('bbmessage', 'text'),
                )


db.bboard.id.readable = False

db.bboard.user_id.default = auth.user_id
db.bboard.user_id.writable = db.bboard.user_id.readable = False

db.bboard.name.default = get_name()
db.bboard.name.writable = False

db.bboard.phone.default = get_phone()
db.bboard.phone.requires = IS_MATCH('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$', error_message='Not a valid phone number. Please enter (xxx)-xxx-xxxx')
db.bboard.email.requires = IS_EMAIL()

db.bboard.category.requires = IS_IN_SET(CATEGORY, zero=None)
db.bboard.category.default = 'Misc'
db.bboard.category.required = True

db.bboard.date_posted.default = datetime.utcnow()
db.bboard.date_posted.represent = lambda value, row: value.strftime("%m/%d/%y - %I:%M %p")
db.bboard.date_posted.writable = False

db.bboard.price.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The price should be in the range 0..100000')
db.bboard.price.represent = lambda value, row: '$'+value

db.bboard.filename.readable = False

db.bboard.bbmessage.label = 'Message'


