from flask import Flask, request
from flask_graphql import GraphQLView
from flask_restful import Api, Resource
import graphene

app = Flask(__name__)
api = Api(app)

loan_products = [
    {"id": 1, "name": "Tom's Loan", "interest_rate": 5.0, "maximum_amount": 10000},
    {"id": 2, "name": "Chris Wailaka", "interest_rate": 3.5, "maximum_amount": 500000},
    {"id": 3, "name": "NP Mobile Money", "interest_rate": 4.5, "maximum_amount": 30000}
]

loan_applications = []

class LoanProduct(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    interest_rate = graphene.Float()
    maximum_amount = graphene.Int()


class LoanApplicationObject(graphene.ObjectType):
    id = graphene.Int()
    full_name = graphene.String()
    email = graphene.String()
    loan_amount = graphene.Float()
    loan_purpose = graphene.String()

class Query(graphene.ObjectType):
    loan_products = graphene.List(LoanProduct)
    loan_applications = graphene.List(LoanApplicationObject)

    def resolve_loan_products(self, info):
        return loan_products

    def resolve_loan_applications(self, info):
        return loan_applications

schema = graphene.Schema(query=Query)

class LoanApplication(Resource):
    def post(self):
        data = request.get_json()
        full_name = data.get('full_name')
        email = data.get('email')
        loan_amount = data.get('loan_amount')
        loan_purpose = data.get('loan_purpose')

        if not all([full_name, email, loan_amount, loan_purpose]):
            return {"message": "All fields are required."}, 400

        application = {
            "id": len(loan_applications) + 1,
            "full_name": full_name,
            "email": email,
            "loan_amount": loan_amount,
            "loan_purpose": loan_purpose
        }
        loan_applications.append(application)
        return {"message": "Loan application submitted successfully."}, 201

api.add_resource(LoanApplication, '/apply-loan')

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.route('/')
def home():
    return "Welcome to the Loan Application API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
