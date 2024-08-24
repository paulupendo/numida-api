from flask import request
from flask_restful import Resource
import logging

loan_applications = []


class LoanApplication(Resource):
    def post(self):
        try:
            data = request.get_json()

            if not data:
                logging.warning("No input data provided.")
                return {"message": "No input data provided."}, 400

            full_name = data.get('full_name')
            email = data.get('email')
            loan_amount = data.get('loan_amount')
            loan_purpose = data.get('loan_purpose')

            if not all([full_name, email, loan_amount, loan_purpose]):
                logging.warning("Missing fields in the request.")
                return {"message": "All fields are required."}, 400

            application = {
                "id": len(loan_applications) + 1,
                "full_name": full_name,
                "email": email,
                "loan_amount": loan_amount,
                "loan_purpose": loan_purpose
            }
            loan_applications.append(application)
            logging.info("Loan application submitted successfully.")
            return {"message": "Loan application submitted successfully."}, 201

        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return {"message": "Failed to submit loan application."}, 500
