from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# =========================
# GET ROUTES
# =========================


@app.route("/bakeries")
def bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries]), 200


@app.route("/baked_goods")
def baked_goods():
    baked_goods = BakedGood.query.all()
    return jsonify([bg.to_dict() for bg in baked_goods]), 200


# =========================
# POST ROUTE
# =========================


@app.route("/baked_goods", methods=["POST"])
def create_baked_good():
    baked_good = BakedGood(
        name=request.form.get("name"),
        price=request.form.get("price"),
        bakery_id=request.form.get("bakery_id"),
    )

    db.session.add(baked_good)
    db.session.commit()

    return jsonify(baked_good.to_dict()), 201


# =========================
# PATCH ROUTE
# =========================


@app.route("/bakeries/<int:id>", methods=["PATCH"])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404

    if request.form.get("name"):
        bakery.name = request.form.get("name")

    db.session.commit()

    return jsonify(bakery.to_dict()), 200


# =========================
# DELETE ROUTE
# =========================


@app.route("/baked_goods/<int:id>", methods=["DELETE"])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        return jsonify({"error": "Baked good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good successfully deleted"}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
