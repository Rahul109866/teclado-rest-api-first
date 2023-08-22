import uuid
from flask import Flask, request, make_response
from db import stores, items

app = Flask(__name__)




@app.get('/home')
def get_data():
    return {'stores': list(stores.values())}, 200

@app.post('/store')
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post('/item')
def create_item():
    item_data = request.get_json()
    
    
    
    if item_data["store_id"] not in stores:
        return {"message": "store not found"}, 404
        
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": "item_id"}
    items[item_id] = item
    
    return item, 201

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Not found"}, 404
    
    
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return  items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404
    



if __name__ == '__main__':
    app.run(debug=True)