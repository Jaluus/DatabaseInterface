from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from dbConnection import dbConnectionQuery

app = Flask(__name__)

# # You need cors!!
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

db = dbConnectionQuery()


@app.route("/")
@cross_origin()
def index():
    return "Hello Dude"


@app.route("/flakes", methods=["GET"])
@cross_origin()
def data_GET():
    # here we want to get the value of user (i.e. ?user=some-value)
    query_dict = request.args
    print(query_dict)
    flake_dict = db.get_flakes(query_dict)
    return jsonify(flake_dict)


@app.route("/flakes", methods=["POST"])
@cross_origin()
def data_POST():
    # here we want to get the value of user (i.e. ?user=some-value)

    f = request.files["20x"]
    v = request.values.to_dict(flat=False)
    print(v)
    f.save(secure_filename(f.filename))
    return "file uploaded successfully"


@app.route("/flakes", methods=["DELETE"])
@cross_origin()
def data_DELETE():
    flake_id = request.args.get("id")
    try:
        flake_id = int(flake_id)
        return "Deleted Flake"
    except:
        return "Invalid Key"


if __name__ == "__main__":

    # use host = "0.0.0.0" to make it available on the local net, aka all the IP adresses of the machine
    app.run(debug=True, host="0.0.0.0")
