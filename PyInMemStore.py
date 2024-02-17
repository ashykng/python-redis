from redis import Redis
from flask import Flask, request, abort
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Redis API"
    },
)

app.register_blueprint(swaggerui_blueprint)

client_connection = Redis(host='localhost', charset="utf-8", decode_responses=True)


@app.route("/set/<key>/<value>", methods=["PUT"])
def set_key(key, value):

    try:
        expire = request.args.get('expire', default=None, type=int)
        if expire is None:
            client_connection.set(key, value)
        else:
            client_connection.set(key, value, ex=expire)
        return "set successfully"

    except Exception as error:
        abort(400, f"Error:{error}")


@app.route("/get/<key>", methods=["GET"])
def get_key(key):
    try:
        return str(client_connection.get(key))

    except Exception as error:
        abort(400, f"Error:{error}")


@app.route("/get/ttl/<key>", methods=["GET"])
def get_key_ttl(key):
    try:
        return str(client_connection.ttl(key))

    except Exception as error:
        abort(400, f"Error:{error}")


@app.route("/del/<key>", methods=["DELETE"])
def delete_key(key):
    try:
        client_connection.delete(key)
        return "Key deleted successfully"

    except Exception as error:
        abort(400, f"Error:{error}")


@app.route("/get_all_keys", methods=["GET"])
def get_all_keys():
    try:
        response = client_connection.scan_iter("*")
        res = []

        for key in response:
            res.append(f"{res}: {client_connection.get(key)}")

        return res

    except Exception as error:
        abort(400, f"Error:{error}")


@app.route("/del_all_keys", methods=["DELETE"])
def delete_all_keys():
    try:
        response = client_connection.scan_iter("*")

        for key in response:
            client_connection.delete(key)

        return "All keys deleted successfully"

    except Exception as error:
        abort(400, f"Error:{error}")



if __name__ == "__main__":
    app.run()