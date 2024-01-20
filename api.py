from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# Load products from JSON file

products = []
with open("products.json", "r") as f:
    products = json.load(f)
    print('Products : ', products)

# GET /api/products
@app.route('/api/products', methods=["GET"])
def get_products():
    num = 2
    return jsonify({'products': products})

# GET /api/products/<id>
@app.route("/api/products/<int:id>", methods=["GET"])
def get_product(id):
    print('ID : ', id)
    print('Type : ', type(id))
    product = []
    for p in products:
        print(p['id'])
    return jsonify(products)

# POST /api/products
@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data or not all(key in data for key in ["name", "price"]):
        abort(400)

    product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"],
    }
    products.append(product)
    with open("products.json", "w") as f:
        json.dump(products, f)
    return jsonify(product), 201

# PUT /api/products/<id>
@app.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = next((product for product in products if product["id"] == id), None)
    if not product:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400)

    for key, value in data.items():
        if key in product:
            product[key] = value

    with open("products.json", "w") as f:
        json.dump(products, f)
    return jsonify(product)

# DELETE /api/products/<id>
@app.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = next((product for product in products if product["id"] == id), None)
    if not product:
        abort(404)

    products.remove(product)
    with open("products.json", "w") as f:
        json.dump(products, f)
    return jsonify({}), 204

@app.route('/', methods = ['GET'])
def home():
    return "<h1>Hello </h1>"

app.run()