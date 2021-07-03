from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Database_tables import *
from functions import *
import cv2

# Some Constants
IMAGE_DIRECTORY = r"C:\Users\jlusl\Desktop\Mikroskop_Bilder"

app = Flask(__name__)

# # You need cors!!
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Add a Keychain Later
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:root@localhost:3306/Full_Flakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# init the APP With the Database
db.app = app
db.init_app(app)

# Create the Database if its not existante
db.create_all()


@app.route("/")
@cross_origin()
def index():
    return "Hello Dude"


@app.route("/flakes", methods=["GET"])
@cross_origin()
def FLAKE_GET():
    # here we want to get the value of user (i.e. ?user=some-value)
    query_dict = request.args
    flake_dict = get_flakes(db, query_dict)
    return jsonify(flake_dict)


@app.route("/scans", methods=["GET"])
@cross_origin()
def SCAN_GET():
    # here we want to get the value of user (i.e. ?user=some-value)
    query_dict = request.args
    scan_dict = get_scans(db, query_dict)
    print(scan_dict)
    return jsonify(scan_dict)


# @app.route("/flakes", methods=["POST"])
# @cross_origin()
# def data_POST():
#     f = request.files["20x"]
#     print(f)
#     v = request.values.to_dict(flat=False)
#     print(v)
#     f.save(v["filename"][0])
#     return "file uploaded successfully"


@app.route("/flakes", methods=["DELETE"])
@cross_origin()
def FLAKES_DELETE():
    try:
        flake_id = int(request.args.get("id"))
        delete_flake(db, IMAGE_DIRECTORY, flake_id)
        return "Deleted Flake"
    except:
        return "Invalid Key"


@app.route("/scans", methods=["DELETE"])
@cross_origin()
def SCAN_DELETE():
    try:
        scan_id = int(request.args.get("id"))
        # delete_scan(db, IMAGE_DIRECTORY, scan_id)
        return "Deleted SCAN"
    except:
        return "Invalid Key"


if __name__ == "__main__":

    # use host = "0.0.0.0" to make it available on the local net, aka all the IP adresses of the machine
    app.run(debug=True, host="0.0.0.0")
