# -*- coding: utf-8 -*-
# Nguyen Do - 1357775 - shanedo@ucsc.edu
# CMPS 183 - HW1

#########################################################################
## This is a controller for online fleamarket
##
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

"""def index():
    
    This index appears when you go to bboard/default/index . 

    # We want to generate an index of the posts. 
    posts = db().select(db.bboard.ALL)
    return dict(posts=posts)
"""
@auth.requires_login()
def add():
    """Add a post."""
    db.bboard.is_sold.readable = False
    form = SQLFORM(db.bboard)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("A New Post is Created Successfully")
        redirect(URL('default', 'index'))
    return dict(form=form)

def view():
    """View a post."""
    # p = db(db.bboard.id == request.args(0)).select().first()
    p = db.bboard(request.args(0)) or redirect(URL('default', 'index'))
    title=p.title
    db.bboard.title.readable = False
    db.bboard.is_sold.readable = False

    if not p.is_sold:
        # If the record is ours, we can edit/delete it. If not, view only
        b = IMG(_src=URL('static/images','sale.png'))
    else:
        b = IMG(_src=URL('static/images','sold.png'))


    form = SQLFORM(db.bboard, record=p, readonly=True)
    has_image = False
    if p.filename != None:
        has_image = True
    # p.name would contain the name of the poster.
    return dict(form=form,image=p.filename,has_image=has_image,title=title,is_sold_icon=b)

@auth.requires_login()
def edit():
    """View a post."""
    # p = db(db.bboard.id == request.args(0)).select().first()
    p = db.bboard(request.args(0)) or redirect(URL('default', 'index'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('default', 'index'))
    form = SQLFORM(db.bboard, record=p)
    if form.process().accepted:
        session.flash = T('Updated')
        redirect(URL('default', 'view', args=[p.id]))
    # p.name would contain the name of the poster.
    return dict(form=form)

@auth.requires_login()
@auth.requires_signature()
def delete():
    """Deletes a post."""
    p = db.bboard(request.args(0)) or redirect(URL('default', 'index'))

    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('default', 'index'))

    form = FORM.confirm('Yes', {'No':URL('default', 'index')})
    title = p.title
    if form.accepted:
        db(db.bboard.id == p.id).delete()
        redirect(URL('default', 'index'))
    return dict(form=form,title=title)
    session.flash = T('Deleted')
    
def index():
    """Better index."""
    # Let's get all data. 
    show_all = request.args(0) == 'all'
    print show_all
    #q = db.bboard
    q = (db.bboard) if show_all else (db.bboard.is_sold == False)
    db.bboard.is_sold.readable = False

    if show_all:
        button = A('See unsold', _class='btn', _href=URL('default', 'index'))
    else:
        button = A('See all', _class='btn', _href=URL('default', 'index', args=['all']))
    
    def generate_buttons(row):
        # If the record is ours, we can edit/delete it. If not, view only
        b = ''
        #b = A('View', _class='btn', _href=URL('default', 'view', args=[row.id]))
        if (auth.user_id == row.user_id and row.user_id != None):
            b = A('Edit', _class='btn btn-warning', _href=URL('default', 'edit', user_signature=True, args=[row.id]))
            b += ' '
            b += A('Delete', _class='btn btn-danger', _href=URL('default', 'delete', user_signature=True, args=[row.id]))
        return b

    def is_sold(row):
        # If the record is ours, we can edit/delete it. If not, view only
        b = IMG(_src=URL('static/images','sale.png'), user_signature=True)
        if row.is_sold:
            b = IMG(_src=URL('static/images','sold.png'), user_signature=True)

        return b
    
    def shorten_post(row):
        return A(row.bbmessage[:10]+'...', _class='', _href=URL('default', 'view', args=[row.id])) 
    
    # Creates extra buttons.
    
    links = [
        dict(header='', body = generate_buttons),
        ]

    if len(request.args) == 0 or 1:
        # We are in the main index.
        links.insert(0, (dict(header='Message', body = shorten_post)))
        links.insert(1, (dict(header=(button), body = is_sold)))
        db.bboard.bbmessage.readable = False

    #if request.args(0) == 'add':
    #    db.bboard.is_sold.readable = False
    
    start_idx = 1 if show_all else 0

    form = SQLFORM.grid(q, 
        fields=[db.bboard.title, db.bboard.user_id, db.bboard.date_posted, 
                db.bboard.category, db.bboard.price, 
                db.bboard.bbmessage, db.bboard.is_sold],
        editable=False, deletable=False, details=False, create=False, 
        links=links,
        paginate=10,
        exportclasses=dict(xml=False, html=False, csv_with_hidden_cols=False, csv=False, 
                           tsv_with_hidden_cols=False, tsv=False, json=False),
        args=request.args[:start_idx],
        )
    return dict(form=form,toggle_show_all=button)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
