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
    if "name" not in store_data:
        abort(400, message="Ensure Name is included in JSON payload.")

    for store in stores.values():  # check for duplicate store names
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists")

    # create a hexadecimal unique user id from uuid module using uuid4 methodology
    store_id = uuid.uuid4().hex

    # unpack the parsed json payload to a store dictionary
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201




@app.get("/store/<string:store_id>")  # return store detail with store_id
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not Found.")


@app.delete("/store/<string:store_id>")  # return store detail with store_id
def get_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not Found.")


@app.get("/store/<string:store_id>/items")
def get_store_items(store_id):
    try:
        store_items = [item for item in items.values(
        ) if item["store_id"] == store_id]

        return {"Store": stores[store_id]["name"], "Items": store_items}
    except KeyError:
        return abort(400, message="Store is not found.")


@app.get("/item")  # get all items regardless of shops
def get_all_items():
    return {"items": list(items.values())}

@app.post('/item')  # create an item
def create_item():
    item_data = request.get_json()  # parse incoming json item payload to python objects
    if (
        "price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data

    ):
        abort(
            400,
            message="Ensure price, name or the store Id are included in the JSON payload"
        )

    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(
                400,
                message=f"Item already exists."
            )

    # check if the store actually exists to an item to
    if item_data["store_id"] not in stores:
        # use smorest to handle error display
        abort(404, message="store not found.")

    item_id = uuid.uuid4().hex  # create uuid for item using uuid library
    # same unpacking the payload and attach it with item id
    item = {**item_data, "id": item_id}
    # attach it to item database(dict from db.py) which has item details and store_id
    items[item_id] = item

    return item, 201  # return item to signify item has been created

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if (
        "name" not in item_data or
        "price" not in item_data
    ):
        abort(400,message="Ensure price and name are included in the JSON payload.")
    try:
        item = items[item_id]
        item |= item_data #update the item data in items dict
        
        return item
    
    except KeyError:
        abort(404,message="Item not found.")
        

@app.get("/item/<string:item_id>")  # return the item details based on item_id
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")


# return the item details based on item_id
@app.delete("/item/<string:item_id>")
def get_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")


if __name__ == '__main__':
    app.run(debug=True)

    print("Stores dictionary contents: ")
    for store_id, store in stores.items():
        print(f"Store ID: {store_id},\nStore Name: {store}")

    print("Items dictionary contents: ")
    for item_id, item in items.items():
        print(f"Item ID: {item_id}")
        for key, value in item.items():
            print(f"  {key}: {value}")
