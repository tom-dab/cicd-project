from flask import Flask, jsonify, request

app = Flask(__name__)
products = []

@app.route('/product', methods=['GET'])
def get_product():
    # Produit codé en dur
    return jsonify({"name": "Stylo", "price": 2.5})

@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    if price is None or price < 0:
        return jsonify({"error": "Le prix doit être positif"}), 400
    products.append({"name": name, "price": price})
    return jsonify({"message": "Produit ajouté"}), 201

if __name__ == '__main__':
    app.run(debug=True)
