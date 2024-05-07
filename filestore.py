from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./data"


@app.route("/upload", methods=["POST"])
@cross_origin()
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({"message": "File uploaded successfully"}), 200


@app.route("/listfiles", methods=["GET"])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"files": files}), 200


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/delete/<filename>", methods=["GET"])
def delete_file(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"message": "File deleted successfully"}), 200
    except FileNotFoundError:
        return jsonify({"message": "File not found"}), 404


if __name__ == "__main__":
    app.run(debug=False)
