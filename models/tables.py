# -*- coding: utf-8 -*-
from datetime import datetime


def get_first_name():
    name = 'Nobody'
    if auth.user:
        name = auth.user.first_name
    return name

CATEGORY = ['Car', 'Bike', 'Books', 'Music', 'Outdoors', 'For the house', 'Misc']

# db.define_table('image',
#    Field('filename', 'upload'),
#    format = '%(title)s')

db.define_table('bboard',
                Field('name'),
                Field('user_id', db.auth_user),
                Field('title'),
                Field('phone'),
                Field('email'),
                Field('category'),
                Field('date_posted', 'datetime'),
                Field('is_sold', 'boolean'),
                Field('filename', 'upload'),
                Field('bbmessage', 'text'),
                )



db.bboard.id.readable = False
db.bboard.bbmessage.label = 'Message'
db.bboard.name.default = get_first_name()
db.bboard.date_posted.default = datetime.utcnow()
db.bboard.name.writable = False
db.bboard.date_posted.writable = False
db.bboard.user_id.default = auth.user_id
db.bboard.user_id.writable = db.bboard.user_id.readable = False
db.bboard.email.requires = IS_EMAIL()
db.bboard.category.requires = IS_IN_SET(CATEGORY)
db.bboard.category.default = 'Misc'
db.bboard.category.required = True
db.bboard.filename.readable = False
#db.bboard.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')


