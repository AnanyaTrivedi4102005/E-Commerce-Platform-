from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 50000, "quantity": 5},
    {"id": 2, "name": "Mouse", "price": 500, "quantity": 10}
]

html = """
<!DOCTYPE html>
<html>
<head>
    <title>E-Commerce Product Management</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f4; }
        h1 { color: #333; }
        input { padding: 10px; margin: 5px; }
        button { padding: 10px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: center; }
        th { background: #333; color: white; }
        a { color: red; }
    </style>
</head>
<body>
    <h1>E-Commerce Product Management</h1>

    <h2>Add Product</h2>
    <form action="/add" method="POST">
        <input name="name" placeholder="Product Name" required>
        <input name="price" type="number" min="0" step="0.01"
               placeholder="Price" required>
        <input name="quantity" type="number" min="0"
               placeholder="Quantity" required>
        <button type="submit">Add Product</button>
    </form>

    <h2>Product List</h2>
    <table>
        <tr>
            <th>ID</th><th>Name</th><th>Price</th>
            <th>Quantity</th><th>Action</th>
        </tr>
        {% for p in products %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.name }}</td>
            <td>{{ p.price }}</td>
            <td>{{ p.quantity }}</td>
            <td>
                <form action="/update/{{ p.id }}" method="POST">
                    <input name="price" type="number" min="0"
                           step="0.01" placeholder="New Price" required>
                    <button type="submit">Update</button>
                </form>
                <form action="/delete/{{ p.id }}" method="POST">
                    <button type="submit">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(html, products=products)


@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    price = float(request.form["price"])
    quantity = int(request.form["quantity"])

    if not name or price < 0 or quantity < 0:
        return "Invalid product details", 400

    new_id = max((p["id"] for p in products), default=0) + 1
    products.append({
        "id": new_id,
        "name": name,
        "price": price,
        "quantity": quantity
    })
    return redirect("/")


@app.route("/update/<int:id>", methods=["POST"])
def update_product(id):
    price = float(request.form["price"])

    if price < 0:
        return "Invalid price", 400

    for product in products:
        if product["id"] == id:
            product["price"] = price
            return redirect("/")

    return "Product not found", 404


@app.route("/delete/<int:id>", methods=["POST"])
def delete_product(id):
    for product in products:
        if product["id"] == id:
            products.remove(product)
            return redirect("/")

    return "Product not found", 404


if __name__ == "__main__":
    app.run(debug=True)

