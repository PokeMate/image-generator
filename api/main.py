from flask import Flask, escape, request, jsonify, abort, request, send_from_directory
from flask_restplus import Api, Resource, reqparse, fields
from generator import ImageGenerator
import json
import uuid
import os
from cleanup import clean_images

IMAGE_DIR = "{}/api/static/cleaned-images".format(os.getcwd())

# flask app configuration
app = Flask(__name__, static_folder='static')
api = Api(app, doc="/swagger/")

# image gnerator
generator = ImageGenerator()

UPLOAD_DIRECTORY = "./api/static/images"

fields = api.model('NewPokemonImageRequestBody', {
    'id1': fields.Integer(description='pokedex id', required=True, min=1),
    'id2': fields.Integer(description='pokedex id', required=True, min=1),
})


@api.route("/home")
class Home(Resource):
    @api.doc("home")
    def get(self):
        return jsonify("Welcome to PokeMate image generator!")


@api.route("/image-generator")
class Generator(Resource):
    @api.doc(model='NewPokemonImageRequestBody')
    def post(self):
        id1 = id2 = new_id = url1 = url2 = ""

        # parse the request
        try:
            json_data = json.loads(request.data)
            id1 = json_data["id1"]
            id2 = json_data["id2"]
            new_id = json_data["newId"]
        except:
            print("Error parsing the body of the request")
            return jsonify("Error parsing the body of the request")

        # generate new image
        # try:
        generator.generate_image(id1, id2, new_id)

        # except:
        #     print("Error generating new image")
        # return jsonify("Error generating new image")

        file_path = "{}/api/static/cleaned-images/".format(os.getcwd())
        file_name = "{}.png".format(new_id)

        print(file_path)
        return send_from_directory(file_path, file_name, as_attachment=True)


@api.route('/image/<id>')
class Download(Resource):
    def get(self, id):
        file_path = IMAGE_DIR
        file_name = "{}.png".format(id)

        return send_from_directory(file_path, file_name, as_attachment=True)


if __name__ == "__main__":
    image_path = "{}/api/static/images/".format(os.getcwd())
    clean_images_path = "{}/api/static/cleaned-images/".format(os.getcwd())
    clean_images(image_path, clean_images_path)

    app.run(debug=True, host="0.0.0.0", port=5001)
