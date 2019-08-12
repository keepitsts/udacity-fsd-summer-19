#Import Dependencies
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catagory, StoreItem

app = Flask(__name__)

engine = create_engine('sqlite:///storeitemsinventory.db')
Base.metadata.bind = engine

#Create a Session
DBSession = sessionmaker(bind=engine)
session = DBSession()



#JSON API Endpoints

#@app.route('/')
@app.route('/catagory/JSON')
def catagoriesJSON():
    catagories = session.query(Catagory).all()
    return jsonify(catagories=[c.serialize for c in catagories])


@app.route('/catagory/storeItems/JSON')
def showStoreItemJSON():
    storeItem = session.query(StoreItem).all()
    return jsonify(storeItem=[s.serialize for s in storeItem])


@app.route('/catagory/items/JSON')
def showCatagoryItemsJSON():
    catagory = session.query(StoreItem).filter_by(id=catagory_id).one()
    items = session.query(StoreItem).filter_by(catagory_id=catagory_id).all()
    
    return jsonify(StoreItems=[i.serialize for i in items])

@app.route('/catagory/<int:catagory_id>/items/<int:item_id>/JSON')
def storeItemsJSON(catagory_id, item_id):
    store_item = session.query(StoreItem).all()
    return jsonify(store_item=store_item.serialize)



"""
The following routes and functions pull data from the Store Items Inventory database
and inserts the data into html templates.
"""

#Catagories

#Show all catagories.
@app.route('/')
@app.route('/catagory/')
def showCatagories():
    catagories = session.query(Catagory).all()
    #return "These are the catagories."
    return render_template('catagories.html', catagories=catagories)




#Create a new catagory.
@app.route('/catagory/new/', methods=['GET', 'POST'])
def newCatagory():
    if request.method == 'POST':
        newCatagory = Catagory(name=request.form['name'])
        session.add(newCatagory)
        session.commit()
        flash("New catagory created!")
        return redirect(url_for('showCatagories'))
    else:
        return render_template('newCatagory.html')


#Edit a catagory.
@app.route('/catagory/<int:catagory_id>/edit/', methods=['GET','POST'])
def editCatagory(catagory_id):
    editedCatagory = session.query(
        Catagory).filter_by(id=catagory_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCatagory.name = request.form['name']
            session.add(editedCatagory)
            session.commit()
            flash("Catagory has been edited")
            return redirect(url_for('showCatagories'))
    else:
        return render_template('editCatagory.html', catagory=editedCatagory)        


#Delete a catagory.
@app.route('/catagory/<int:catagory_id>/delete/', methods=['GET', 'POST'])
def deleteCatagory(catagory_id):
    catagoryToDelete = session.query(Catagory).filter_by(id=catagory_id).one()
    if request.method == 'POST':
        session.delete(catagoryToDelete)
        session.commit()
        flash("Catagory has been deleted!")
        return redirect(url_for('showCatagories', catagory_id=catagory_id))
    else:
        return render_template('deleteCatagory.html', catagory=catagoryToDelete)



#Items

#This function shows all the items in a catagory.
@app.route('/catagory/<int:catagory_id>/')
@app.route('/catagory/<int:catagory_id>/items/')
def showItems(catagory_id):
    catagory = session.query(Catagory).filter_by(id=catagory_id).one()
    items = session.query(StoreItem).filter_by(catagory_id=catagory_id).all()
    return render_template('item.html', items=items, catagory=catagory)

#Create a new store item.
@app.route('/catagory/<int:catagory_id>/<int:item_id>new/', methods=['GET','POST'])
def newStoreItem(catagory_id, item_id):
    catagory = session.query(Catagory).filter_by(id=catagory_id).one()
    if request.method == 'POST':
        newItem = StoreItem(name=request.form['name'], author=request.form['author'],genre=request.form['genre'], price=request.form['price'], description=request.form['description'])

        session.add(newItem)
        session.commit()
        flash("New item has been created!")

        return redirect(url_for('showItems', catagory_id=catagory_id, item_id=item_id))

    else:
        return render_template('newItem.html', catagory_id=newItem)

#Edit a store item.
@app.route('/catagory/<int:catagory_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editStoreItem(catagory_id,item_id):
    editedStoreItem = session.query(StoreItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedStoreItem.name = request.form['name']
        if request.form['author']:
            editedStoreItem.author = request.form['author']
        if request.form['genre']:
            editedStoreItem.genre = request.form['genre']
        if request.form['price']:
            editedStoreItem.price = request.form['price']
        if request.form['description']:
            editedStoreItem.description = request.form['description']

        session.add(editedStoreItem)
        session.commit()
        flash("Item has been edited!")
        return "Here you can edit an item."

    else:
        return 


#Delete a store item.
@app.route('/catagory/<int:catagory_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteStoreItem(catagory_id, item_id):
    itemToDelete = session.query(StoreItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted!")
        return "Item Deleted"
    else:
        return "Test"

#Starting the Flask Server

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='localhost', port=5000)
