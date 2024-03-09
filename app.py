from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import json
from main import main
from validate import validate

app = Flask(__name__)
api = Api(app)

put_args = reqparse.RequestParser()
put_args.add_argument("taskID", type=str, required=True)
put_args.add_argument("data", type=str, required=True)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/<string:taskID>/<string:data>')
def req(taskID, data):
    data = json.loads(data)
    response = main(taskID, data)
    return jsonify(response)


class HallBooking(Resource):
    # def get(self):
    
    def post(self):
        args =  put_args.parse_args()
        validate(args)
        if not args['Error']:
            # response = ['Fine']
            response = main(args['taskID'], args['data'])
        else:
            response = args['Error']
        return jsonify(response)

api.add_resource(HallBooking,'/')

if __name__ == "__main__":
    app.run(debug=True)