from flask import Flask, request, jsonify
from zipfile import ZipFile
from flask_cors import CORS, cross_origin
from Database_tables import *
from functions import *
import cv2

# Some Constants
IMAGE_DIRECTORY = r"C:\Users\duden\Desktop\BA_tests\Upload_Images\Images"
USERNAME = "root"
PASSWORD = "root"
HOST = "localhost"
PORT = "3306"
DB_NAME = "Full_Flakes"

# # You need cors!!
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
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


@app.route("/upload", methods=["POST"])
def UPLOAD_FILES():
    file = request.files["zip"]
    if file.filename[-4:] != ".zip":
        return "wrong Filetype"

    file_path = os.path.join(IMAGE_DIRECTORY, file.filename)
    file.save(file_path)

    with ZipFile(file_path, "r") as zipObj:
        zipObj.extractall(file_path[:-4])

    Upload_scan_directory_to_db(db, file_path[:-4])

    return "File uploaded successfully"


@app.route("/triggerDBintegration", methods=["GET"])
def DB_UPLOAD():
    pass


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
