from flask import Flask, escape, request, jsonify, abort, request, send_from_directory
from flask_restplus import Api, Resource, reqparse, fields
from generator import ImageGenerator
import json
import requests as req
import uuid

import os

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


# routes
@api.route("/home")
class Home(Resource):
    @api.doc("home")
    def get(self):
        return jsonify("Welcome to PokeMate image generator!")


# routes
@api.route("/image-generator")
class Generator(Resource):
    @api.doc(model='NewPokemonImageRequestBody')
    def post(self):
        id1 = id2 = new_id = url1 = url2 = ""

        img_id = uuid.uuid1()

        # parse the request
        try:
            json_data = json.loads(request.data)
            id1 = json_data["id1"]
            id2 = json_data["id2"]
        except:
            print("Error parsing the body of the request")
            return jsonify("Error parsing the body of the request")

        # # extract image id and download image
        # try:
        #     id1 = url1.split("/")[-1]
        #     id2 = url2.split("/")[-1]
        #
        #     print("image urls: " + id1 + id2)
        #
        #     r = req.get(url1)
        #     with open('./images/{}'.format(id1), 'w+b') as f:
        #         f.write(r.content)
        #
        #     r = req.get(url2)
        #     with open('./images/{}'.format(id2), 'w+b') as f:
        #         f.write(r.content)
        #
        # except:
        #     print("Error downloading the images")
        #     return jsonify("Error downloading the images")

        # generate new image
        try:
            # generator.generate_image("./images/{}".format(id1), "./images/{}".format(id2), img_id)
            new_id = generator.generate_image(id1, id2)

        except:
            print("Error generating new image")
            return jsonify("Error generating new image")

        file_path = "{}/api/static/cleaned-images/".format(os.getcwd())
        file_name = "{}.png".format(new_id)

        print(file_path)
        return send_from_directory(file_path, file_name, as_attachment=True)


@api.route('/image/<id>')
class Download(Resource):
    def get(self, id):
        file_path = "{}/api/static/images/".format(os.getcwd())
        file_name = "{}.png".format(id)
        return send_from_directory(file_path, file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
