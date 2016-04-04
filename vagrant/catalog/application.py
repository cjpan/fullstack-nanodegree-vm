from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flask import session as login_session, make_response
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Catalog, Item, User
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///items_in_kyoto.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    
    # Verify that the access token is usded for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is usded for the intended user.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's clilent ID doesn't match apps."), 401)
        print "Token's clilent ID doesn't match apps."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params = params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, %s!</h1>' % login_session['username']
    output += '<img src="%s" style="width: 100px; height: 100px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">' % login_session['picture']
    flash("you are now logged in as %s" % login_session['username'])
    return output

# DISCONNCET
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Execute HTTP GET request to revoke current token.
    access_token = credentials.access_token
    print access_token
    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print result

    if result['status'] == '200':
        # Reset user's session.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        flash('Successfully logged out.')
    else:
        flash('Logout failed.')
        
    return redirect(url_for('showCatalogs'))

@app.route('/logout')
def logout():
    if 'gplus_id' in login_session:
        return gdisconnect()

# User helper functions
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture= login_session['picture']
    )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Show all catalogs
@app.route('/')
@app.route('/catalogs/')
def showCatalogs():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    if 'username' not in login_session:
        return render_template('publiccatalogs.html', catalogs=catalogs)
    else:
        return render_template('catalogs.html', catalogs=catalogs)

# Create a new catalog
@app.route('/catalogs/new/', methods=['GET','POST'])
def newCatalog():
    if 'username' not in login_session:
        return redirect(url_for('/login'))
    if request.method == 'POST':
        newCatalog = Catalog(name = request.form['name'], 
            user_id=login_session['user_id'])
        session.add(newCatalog)
        flash('New Catalog %s Successfully Created' % newCatalog.name)
        session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('newCatalog.html')

# Edit a catalog
@app.route('/catalogs/<int:catalog_id>/edit/', methods = ['GET', 'POST'])
def editCatalog(catalog_id):
    editedCatalog = session.query(Catalog).filter_by(id = catalog_id).one()
    if 'username' not in login_session:
        return redirect(url_for('/login'))
    if editedCatalog.user_id != login_session['user_id']:
        return "<script>" \
               "function alertFunction() {" \
               "alert('You are not authorized to edit this catalog');" \
               "}" \
               "</script>" \
               "<body onload='alertFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedCatalog.name = request.form['name']
            flash('Catalog Successfully Edited %s' % editedCatalog.name)
            return redirect(url_for('showCatalogs'))
    else:
        return render_template('editCatalog.html', catalog = editedCatalog)

# Delete a catalog
@app.route('/catalogs/<int:catalog_id>/delete/', methods = ['GET','POST'])
def deleteCatalog(catalog_id):
    catalogToDelete = session.query(Catalog).filter_by(id = catalog_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if catalogToDelete.user_id != login_session['user_id']:
        return "<script>" \
               "function alertFunction() {" \
               "alert('You are not authorized to edit this catalog');" \
               "}" \
               "</script>" \
               "<body onload='alertFunction()'>"
    if request.method == 'POST':
        session.delete(catalogToDelete)
        flash('%s Successfully Deleted' % catalogToDelete.name)
        session.commit()
        return redirect(url_for('showCatalogs', catalog_id = catalog_id))
    else:
        return render_template('deleteCatalog.html',catalog = catalogToDelete)

# Show all items
@app.route('/catalogs/<int:catalog_id>/')
def catalogItem(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Item).filter_by(catalog_id=catalog_id)
    creator = getUserInfo(catalog.user_id)
    return render_template('catalogItems.html', catalog=catalog, items=items, creator=creator)

# Create a new item
@app.route('/catalogs/<int:catalog_id>/new/', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    if catalog.user_id != login_session['user_id']:
        return "<script>" \
               "function alertFunction() {" \
               "alert('You are not authorized to edit this catalog');" \
               "}" \
               "</script>" \
               "<body onload='alertFunction()'>"
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'], 
            description = request.form['description'],
            picture_url = request.form['picture_url'],
            homepage_url = request.form['homepage_url'],
            catalog_id = catalog_id,
            user_id=login_session['user_id']
            )
        session.add(newItem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('catalogItem', catalog_id = catalog_id))
    else:
        return render_template('newCatalogItem.html', catalog_id = catalog_id, 
            catalog = catalog)

# Edit a new item
@app.route('/catalogs/<int:catalog_id>/<int:item_id>/edit/', methods=['POST', 'GET'])
def editCatalogItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    if catalog.user_id != login_session['user_id']:
        return "<script>" \
               "function alertFunction() {" \
               "alert('You are not authorized to edit this catalog');" \
               "}" \
               "</script>" \
               "<body onload='alertFunction()'>"
        
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['picture_url']:
            editedItem.picture_url = request.form['picture_url']
        if request.form['homepage_url']: 
            editedItem.homepage_url = request.form['homepage_url']
        session.add(editedItem)
        session.commit()
        flash("Item edited!")
        return redirect(url_for('catalogItem', catalog_id = catalog_id))
    else:
        return render_template('editCatalogItem.html', item = editedItem)

# Delete an item
@app.route('/catalogs/<int:catalog_id>/<int:item_id>/delete/', methods = ['POST', 'GET'])
def deleteCatalogItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    if catalog.user_id != login_session['user_id']:
        return "<script>" \
               "function alertFunction() {" \
               "alert('You are not authorized to edit this catalog');" \
               "}" \
               "</script>" \
               "<body onload='alertFunction()'>"
    itemToDelete = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('catalogItem', catalog_id = catalog_id))
    else:
        return render_template('deleteCatalogItem.html', item = itemToDelete)


# API endpoints
@app.route('/catalogs/JSON/')
def catalogsJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[i.serialize for c in catalogs])

@app.route('/catalogs/<int:catalog_id>/item/JSON')
def catalogItemJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Item).filter_by(catalog_id=catalog_id).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalogs/<int:catalog_id>/item/<int:item_id>/JSON')
def itemJSON(catalog_id, item_id):
    item = session.query(Item).filter_by(item_id=item_id).one()
    return jsonify(item = item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

