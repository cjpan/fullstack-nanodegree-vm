from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Catalog, Item
app = Flask(__name__)

engine = create_engine('sqlite:///items_in_kyoto.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalogs/<int:catalog_id>/')
def catalogItem(catalog_id=1):
	catalog = session.query(Catalog).filter_by(id=catalog_id).one()
	items = session.query(Item).filter_by(catalog_id=catalog_id)

	return render_template('catalogItems.html', catalog=catalog, items=items)

@app.route('/catalogs/<int:catalog_id>/new/', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
	if request.method == 'POST':
		newItem = Item(
			name=request.form['name'], 
			description = request.form['description'],
			picture_url = request.form['picture_url'],
			homepage_url = request.form['homepage_url'],
			catalog_id = catalog_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('catalogItem', catalog_id = catalog_id))
	else:
		catalog = session.query(Catalog).filter_by(id = catalog_id).one()
		return render_template('newCatalogItem.html', catalog_id = catalog_id, 
			catalog = catalog)

@app.route('/catalogs/<int:catalog_id>/<int:item_id>/edit/', methods=['POST', 'GET'])
def editCatalogItem(catalog_id, item_id):
	if request.method == 'POST':
		editedItem = session.query(Item).filter_by(item_id=item_id).one()
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
		return redirect(url_for('catalogItem'), catalog_id = catalog_id)
	else:
		return render_template('editCatalogItem.html', 
			catalog_id = catalog_id, item_id = item_id, i = editedItem)

@app.route('/catalogs/<int:catalog_id>/<int:item_id>/delete/')
def deleteCatalogItem(catalog_id, item_id):
	output = "delete the item"
	return output

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)

