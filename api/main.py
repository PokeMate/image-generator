from flask import Flask, escape, request, jsonify, abort, request
from flask_restplus import Api, Resource, reqparse
from generator import ImageGenerator
import json
import requests as req

import os

# flask app configuration
app = Flask(__name__)
api = Api(app, doc="/swagger/")

# image gnerator
generator = ImageGenerator()

# routes
@api.route("/home")
class Home(Resource):
    @api.doc("home")
    def get(self):
        return jsonify("Welcome to PokeMate image generator!")


# routes
@api.route("/image-generator")
class Generator(Resource):
    @api.doc("image-generator")
    def post(self):
        id1 = id2 = url1 = url2 = ""

        # parse the request
        try:
            jsonData = json.loads(request.data)
            url1 = jsonData["url1"]
            url2 = jsonData["url2"]
        except:
            print("Error parsing the body of the request")
            return jsonify("Error parsing the body of the request")

        # extract image id and download image
        try:
            id1 = url1.split("/")[-1]
            id2 = url2.split("/")[-1]

            print("image urls: " + id1 + id2)

            r = req.get(url1)
            with open('./images/{}'.format(id1), 'w+b') as f:
                f.write(r.content)

            r = req.get(url2)
            with open('./images/{}'.format(id2), 'w+b') as f:
                f.write(r.content)

        except:
            print("Error downloading the images")
            return jsonify("Error downloading the images")

        # generate new image
        try:
            # TODO generator code comes here: feed images into image generator
            generator.generate_image("./images/{}".format(id1), "./images/{}".format(id2))

        except:
            print("Error generating new image")
            return jsonify("Error generating new image")

        return jsonify("requesting new image for {} and {}".format(id1, id2))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
