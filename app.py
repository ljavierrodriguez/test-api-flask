from flask import Flask, jsonify, render_template, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Test, Profile, Contact

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand) # init, migrate, upgrade

CORS(app)

@app.route("/", methods=['GET'])
def main():
    return render_template('index.html')


@app.route("/tests", methods=['GET', 'POST'])
@app.route("/tests/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def test(id = None):
    if request.method == 'GET':
        if id is not None:
            test = Test.query.get(id) # None por defecto si no consigue el registro
            if test:
                return jsonify(test.serialize()), 200
            return jsonify({"msg": "Test not found"}), 404
        else:
            tests = Test.query.all()
            tests = list(map(lambda test: test.serialize(), tests))
            return jsonify(tests), 200

    if request.method == 'POST':
        name = request.json.get("name", None)
        email = request.json.get("email", None)

        if not name:
            return jsonify({"msg": "Name is required"}), 400
        if not email:
            return jsonify({"msg": "Email is required"}), 400

        test = Test()
        test.name = name
        test.email = email


        profile = Profile()
        profile.bio = request.json.get("bio", "")
        profile.facebook = request.json.get("facebook", "")
        profile.twitter = request.json.get("twitter", "")

        test.profile = profile

        test.save()

        #db.session.add(test)
        #db.session.commit()
        return jsonify(test.serialize()), 201
    if request.method == 'PUT':
        return jsonify({"msg": "Ingresando por el metodo PUT"}), 200
    if request.method == 'DELETE':
        return jsonify({"msg": "Ingresando por el metodo DELETE"}), 200


@app.route("/profile", methods=['GET'])
def profile():
    profile = Profile.query.get(1)
    profile.twitter = "luisjrodriguezo"
    profile.update()
    test = profile.test.serialize()
    return jsonify(test), 200


@app.route("/contacts", methods=['GET', 'POST'])
@app.route("/contacts/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def contacts(id = None):
    if request.method == 'GET':
        if id is not None:
            contact = Contact.query.get(id) # None por defecto si no consigue el registro
            if contact:
                return jsonify(contact.serialize()), 200
            return jsonify({"msg": "Contact not found"}), 404
        else:
            contacts = Contact.query.all()
            contacts = list(map(lambda test: contact.serialize(), contacts))
            return jsonify(contacts), 200

    if request.method == 'POST':
        name = request.json.get("name", None)
        phone = request.json.get("phone", None)
        test_id = request.json.get("test_id", None)

        if not name:
            return jsonify({"msg": "Name is required"}), 400
        if not phone:
            return jsonify({"msg": "Phone is required"}), 400
        if not test_id:
            return jsonify({"msg": "Test Id is required"}), 400

        test = Test.query.get(test_id)
        if not test:
            return jsonify({"msg": "Test Not Found"}), 400

        contact = Contact()
        contact.name = name
        contact.phone = phone
        contact.test_id = test_id
        contact.save()

        #db.session.add(test)
        #db.session.commit()
        return jsonify(contact.serialize()), 201
    if request.method == 'PUT':
        return jsonify({"msg": "Ingresando por el metodo PUT"}), 200
    if request.method == 'DELETE':
        return jsonify({"msg": "Ingresando por el metodo DELETE"}), 200

if __name__ == "__main__":
    manager.run()