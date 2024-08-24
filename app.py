from flask import Flask, jsonify
from flask_graphql import GraphQLView
from flask_restful import Api, Resource

from schemas.loans import schema

app = Flask(__name__)
api = Api(app)

loan_applications = []


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
