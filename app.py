import uuid  # unique user id generation module
# Flask.request module that has methods to parse incoming json data from the client etc
from flask import Flask, request, make_response
# import the empty dicts from db.py to simulate a database
from db import stores, items
from flask_smorest import abort

app = Flask(__name__)  # initialise a flask instance


@app.get('/home')  # return all the stores in our app currently
def get_data():
    return {'stores': list(stores.values())}, 200


@app.post('/store')  # create a store
def create_store():
    # use request.get_json() to parse json client payload to python objects
    store_data = request.get_json()
    # create a hexadecimal unique user id from uuid module using uuid4 methodology
    store_id = uuid.uuid4().hex

    # unpack the parsed json payload to a store dictionary
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post('/item')  # create an item
def create_item():
    item_data = request.get_json()  # parse incoming json item payload to python objects

    # check if the store actually exists to an item to
    if item_data["store_id"] not in stores:
        # use smorest to handle error display
        abort(404, message="store not found.")

    item_id = uuid.uuid4().hex  # create uuid for item using uuid library
    # same unpacking the payload and attach it with item id
    item = {**item_data, "id": "item_id"}
    # attach it to item database(dict from db.py) which has item details and store_id
    items[item_id] = item

    return item, 201  # return item to signify item has been created


@app.get("/store/<string:store_id>")  # return store detail with store_id
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not Found.")


@app.get("/item")  # get all items regardless of shops
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")  # return the item details based on item_id
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")


if __name__ == '__main__':
    app.run(debug=True)
