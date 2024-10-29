from flask import Flask
from flask_restful import Api, Resource
from config import DevConfig


app = Flask(__name__)

app.config.from_object(DevConfig)

api = Api(app)


# @api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}
    
# API's
api.add_resource(HelloResource, '/hello')
    


if __name__ == '__main__':
    app.run()
        