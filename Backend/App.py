import sys
import zipfile
from io import BytesIO
from zipfile import ZipFile

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin

from config import config
from Database_tables import *
from functions import *

# Some Constants
IMAGE_DIRECTORY = r"C:\Users\duden\Desktop\Mikroskop Bilder"

KEYCHAIN = config()

USERNAME = KEYCHAIN["username"]
PASSWORD = KEYCHAIN["password"]
HOST = KEYCHAIN["host"]
PORT = KEYCHAIN["port"]
DATABASE = KEYCHAIN["database"]

# # You need cors!!
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
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
    try:
        file = request.files["zip"]
        if file.filename[-4:] != ".zip":
            return "wrong Filetype"

        file_path = os.path.join(IMAGE_DIRECTORY, file.filename)
        file.save(file_path)

        with ZipFile(file_path, "r") as zipObj:
            zipObj.extractall(file_path[:-4])

        Upload_scan_directory_to_db(db, file_path[:-4])

        return "File uploaded successfully"
    except:
        return "Something went wrong!"


@app.route("/flakes", methods=["GET"])
@cross_origin()
def FLAKE_GET():
    # here we want to get the value of user (i.e. ?user=some-value)
    query_dict = request.args
    flake_dict = get_flakes(db, query_dict)
    return jsonify(flake_dict)


@app.route("/downloadFlake", methods=["GET"])
@cross_origin()
def FLAKE_DOWNLOAD():
    # here we want to get the value of user (i.e. ?user=some-value)
    try:
        flake_id = int(request.args.get("flake_id"))

        flake_query = {"flake_id": flake_id}
        flake_dict = get_flakes(db, flake_query)[0]
        flake_dir = os.path.join(IMAGE_DIRECTORY, flake_dict["flake_path"])

        # Keep the Zipfile only in Memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            for file_name in os.listdir(flake_dir):
                file_path = os.path.join(flake_dir, file_name)
                zf.write(file_path, file_name)
        memory_file.seek(0)

        return send_file(
            memory_file,
            download_name=f"Flake_{flake_id:.0f}.zip",
            as_attachment=True,
        )
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "Wrong Query, Please use $flake_id=[The needed Flake ID]"


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
        flake_id = int(request.args.get("flake_id"))
        delete_flake(db, IMAGE_DIRECTORY, flake_id)
        return "Deleted Flake"
    except:
        return "Invalid Key"


@app.route("/scans", methods=["DELETE"])
@cross_origin()
def SCAN_DELETE():
    try:
        scan_id = int(request.args.get("scan_id"))
        delete_scan(db, IMAGE_DIRECTORY, scan_id)
        return "Deleted SCAN"
    except:
        return "Invalid Key"


if __name__ == "__main__":
    # use host = "0.0.0.0" to make it available on the local net, aka all the IP adresses of the machine
    # Upload_scan_directory_to_db(
    #     db,
    #     r"C:\Users\Uslu.INSTITUT2B\Desktop\Mikroskop_Bilder\Eikes_Flocken_Full_Final",
    # )
    # Upload_scan_directory_to_db(
    #     db, r"C:\Users\Uslu.INSTITUT2B\Desktop\Mikroskop_Bilder\Luca_Scan_060721"
    # )
    app.run(debug=True, host="0.0.0.0")
