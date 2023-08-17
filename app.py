from flask import Flask, request, make_response

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]


@app.get('/home')
def get_data():
    return {'store': stores}, 200

@app.post('/store')
def create_store():
    request_data = request.get_json()
    for store in request_data:
        new_store = {"name": store['name'], "items": []}
        stores.append(new_store)
    response = make_response("Store saved succesfully", 201)
    return response


@app.post('/store/<string:name>/item')
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {"name": request_data["name"], "price": request_data['price']}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store Not Found."}, 404

@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return store
    return {"message": "store not found"}, 404



if __name__ == '__main__':
    app.run(debug=True)