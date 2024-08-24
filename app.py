from flask import Flask
from flask_graphql import GraphQLView
from flask_restful import Api

from schemas.loans import schema
from resources.loan_application import LoanApplication

app = Flask(__name__)
api = Api(app)

# Adding the LoanApplication resource
api.add_resource(LoanApplication, '/apply-loan')

# Adding the GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.route('/')
def home():
    return "Welcome to the Loan Application API"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
