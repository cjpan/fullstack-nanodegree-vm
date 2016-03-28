from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flask import session as login_session, make_response
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Catalog, Item
app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']




engine = create_engine('sqlite:///items_in_kyoto.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	#return "The current session state is %s" % login_session['state']
	print "The current session state is %s" % login_session['state']
	print login_session
	return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		print request.args.get('state')
		print login_session
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

	output = ''
	output += '<h1>Welcome, %s!</h1>' % login_session['username']
	output += '<img src="%s" style="width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">' % login_session['picture']
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
	url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		# Reset user's session.
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/')
@app.route('/catalogs/<int:catalog_id>/')
def catalogItem(catalog_id=1):
	catalog = session.query(Catalog).filter_by(id=catalog_id).one()
	items = session.query(Item).filter_by(catalog_id=catalog_id)
	return render_template('catalogItems.html', catalog=catalog, items=items)

@app.route('/catalogs/<int:catalog_id>/item/JSON')
def catalogItemJSON(catalog_id=1):
	catalog = session.query(Catalog).filter_by(id=catalog_id).one()
	items = session.query(Item).filter_by(catalog_id=catalog_id)
	return jsonify(Items=[i.serialize for i in items])

@app.route('/catalogs/<int:catalog_id>/item/<int:item_id>/JSON')
def itemJSON(catalog_id=1, item_id=1):
	item = session.query(Item).filter_by(item_id=item_id).one()
	return jsonify(Item = item.serialize)

@app.route('/catalogs/<int:catalog_id>/new/', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newItem = Item(
			name=request.form['name'], 
			description = request.form['description'],
			picture_url = request.form['picture_url'],
			homepage_url = request.form['homepage_url'],
			catalog_id = catalog_id)
		session.add(newItem)
		session.commit()
		flash("new item created!")
		return redirect(url_for('catalogItem', catalog_id = catalog_id))
	else:
		catalog = session.query(Catalog).filter_by(id = catalog_id).one()
		return render_template('newCatalogItem.html', catalog_id = catalog_id, 
			catalog = catalog)

@app.route('/catalogs/<int:catalog_id>/<int:item_id>/edit/', methods=['POST', 'GET'])
def editCatalogItem(catalog_id, item_id):
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

@app.route('/catalogs/<int:catalog_id>/<int:item_id>/delete/', methods = ['POST', 'GET'])
def deleteCatalogItem(catalog_id, item_id):
	itemToDelete = session.query(Item).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Item deleted!")
		return redirect(url_for('catalogItem', catalog_id = catalog_id))
	else:
		return render_template('deleteCatalogItem.html', item = itemToDelete)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)

