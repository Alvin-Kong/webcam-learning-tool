import flask
from flask import request
from flask_cors import CORS

import asyncio
import json
import sys

import util

app = flask.Flask(__name__)
cors = CORS(app)


# Main function to respond to requests
@app.route("/", methods=["GET"])
def home():
    response = asyncio.run(build_response())
    return json.dumps(response), {"Content-Type": "application/json"}


# Build a response to send to the client
# asynchronously waiting for external APIs
async def build_response():
    response = {}
    response["results"] = await get_position()
    return response


# Function to ge the
async def get_position():
    response = {}
    bbox = util.getBBox()
    response["center"] = util.getCenter(bbox)
    response["x"] = util.getXCenter(bbox)
    response["y"] = util.getYCenter(bbox)
    return response.json()


# Generate an JSON error response
def generateError(reason):
    return {
        "reasons": [
            {
                "language": "en",
                "message": reason
            }
        ]
    }


# Main method to run API
if __name__ == "__main__":
    PORT = 5000  # port to run the server on
    DEBUG = False  # whether to run in debug mode
    SSL_CONTEXT = None  # indicates whether to use HTTPS

    if "--debug" in sys.argv:
        DEBUG = True

    if "--https" in sys.argv:
        SSL_CONTEXT = "ahdoc"

    app.config["DEBUG"] = DEBUG
    app.run(port=PORT, ssl_context=SSL_CONTEXT)
