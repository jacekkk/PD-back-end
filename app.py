from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from mongoengine import connect
from schema import schema


app = Flask(__name__)
CORS(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    connect('graphene-mongo-example', host='mongomock://localhost', alias='default')
    app.run()
