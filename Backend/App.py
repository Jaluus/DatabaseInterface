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
IMAGE_DIRECTORY = r"C:\Users\Uslu.INSTITUT2B\Desktop\Mikroskop_Bilder"

# Get the Connection information from our file
KEYCHAIN = config()
USERNAME = KEYCHAIN["username"]
PASSWORD = KEYCHAIN["password"]
HOST = KEYCHAIN["host"]
PORT = KEYCHAIN["port"]
DATABASE = KEYCHAIN["database"]

# Define the Image names of the images to which the scalebar will be added
SCALEBAR_IMAGE_NAMES = [
    "2.5x.png",
    "5x.png",
    "20x.png",
    "50x.png",
    "100x.png",
]

# Activate CORS to prevent errors
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Set the connection URI
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 16 Gb max upload
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000 * 1000

# initialzie the app with the Database
db.app = app
db.init_app(app)

# Create the Database, if it is not existant
db.create_all()

# Define the default route
@app.route("/")
@cross_origin()
def index():
    return "Default Route, not set"


# Define the the upload route, POST
@app.route("/upload", methods=["POST"])
def UPLOAD_FILES():
    print("trying to upload...")
    try:
        file = request.files["zip"]
        if file.filename[-4:] != ".zip":
            return "wrong Filetype"

        print(f"receiving {file.filename}...")

        file_path = os.path.join(IMAGE_DIRECTORY, file.filename)

        print(f"saving to {file_path}")

        file.save(file_path)

        print(f"File saved")

        with ZipFile(file_path, "r") as zipObj:
            zipObj.extractall(file_path[:-4])

        Upload_scan_directory_to_db(db, file_path[:-4])

        return "File uploaded successfully"
    except:
        return "Something went wrong!"


# Return the flake metadata based on the filter arguments
@app.route("/flakes", methods=["GET"])
@cross_origin()
def FLAKE_GET():
    # here we want to get the value of user (i.e. ?user=some-value)
    query_dict = request.args
    flake_dict = get_flakes(db, query_dict)
    return jsonify(flake_dict)


@app.route("/thicknesses", methods=["GET"])
@cross_origin()
def FLAKE_THICKNESSES_GET():
    unique_thicknesses = get_unique_thicknesses(db)
    print(unique_thicknesses)
    return jsonify(unique_thicknesses)


@app.route("/materials", methods=["GET"])
@cross_origin()
def FLAKE_MATERIALS_GET():
    unique_materials = get_unique_materials(db)
    return jsonify(unique_materials)


@app.route("/users", methods=["GET"])
@cross_origin()
def USERS_GET():
    unique_users = get_unique_users(db)
    return jsonify(unique_users)


# Return the requested Flake based on the ID as a Zip file
# Zip is being created in memory
# TODO: Add a scalebar if requested by using OPENCV
@app.route("/downloadFlake", methods=["GET"])
@cross_origin()
def FLAKE_DOWNLOAD():
    try:
        flake_id = int(request.args.get("flake_id"))
        scalebar_download = request.args.get("scalebar")

        flake_query = {"flake_id": flake_id}
        flake_dict = get_flakes(db, flake_query)[0]
        flake_dir = os.path.join(IMAGE_DIRECTORY, flake_dict["flake_path"])

        # Create a ZIP-file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            for file_name in os.listdir(flake_dir):
                file_path = os.path.join(flake_dir, file_name)

                if file_name in SCALEBAR_IMAGE_NAMES and scalebar_download is not None:
                    try:
                        # create the scalebar image and add it to the zip, remove it afterwards
                        scale_bar_path = add_scalebar(file_path)
                        zf.write(scale_bar_path, file_name)
                        os.remove(scale_bar_path)
                    except:
                        zf.write(file_path, file_name)
                else:
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


# Return the scan metadata
@app.route("/scans", methods=["GET"])
@cross_origin()
def SCAN_GET():
    # here we want to get the value of user (i.e. ?user=some-value)
    query_dict = request.args
    scan_dict = get_scans(db, query_dict)
    return jsonify(scan_dict)


# Delete a flake based on the flake id
# TODO: Delete the scan / Chip if no more Chips / Flakes are on the scan
@app.route("/flakes", methods=["DELETE"])
@cross_origin()
def FLAKES_DELETE():
    try:
        flake_id = int(request.args.get("flake_id"))
        delete_flake(db, IMAGE_DIRECTORY, flake_id)
        return "Deleted Flake"
    except:
        return "Invalid Key"


# Delete every flake and chip within a certain scan
# Also delete the Scan itself
@app.route("/scans", methods=["DELETE"])
@cross_origin()
def SCAN_DELETE():
    try:
        scan_id = int(request.args.get("scan_id"))
        print(f"Deleting Scan {scan_id}")
        delete_scan(db, IMAGE_DIRECTORY, scan_id)
        return "Deleted SCAN"
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "Unexpected error, Maybe scan id not present?"


if __name__ == "__main__":
    # use host = "0.0.0.0" to make it available on the local net, aka all the IP adresses of the machine
    # Upload_scan_directory_to_db(
    #     db,
    #     r"C:\Users\Uslu.INSTITUT2B\Desktop\Mikroskop_Bilder\Eikes_Flocken_Full_Final",
    # )
    # Upload_scan_directory_to_db(
    #     db, r"C:\Users\Uslu.INSTITUT2B\Desktop\Mikroskop_Bilder\graphene_taoufiq"
    # )
    app.run(debug=True, host="0.0.0.0")
