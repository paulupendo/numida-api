import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from resources.loan_application import LoanApplication, loan_applications


class TestLoanApplication(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(LoanApplication, '/apply-loan')
        self.client = self.app.test_client()

        loan_applications.clear()

    def test_successful_loan_application(self):
        # Simulate a valid loan application request
        response = self.client.post('/apply-loan', json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "loan_amount": 1000,
            "loan_purpose": "Business expansion"
        }, headers={"Content-Type": "application/json"})

        # Check response status code and message
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json, {"message": "Loan application submitted successfully."})

        self.assertEqual(len(loan_applications), 1)
        self.assertEqual(loan_applications[0]["full_name"], "John Doe")

    @patch('resources.loan_application.loan_applications', [])
    def test_missing_fields(self):
        # Simulate a loan application request with missing fields
        response = self.client.post('/apply-loan', json={
            "full_name": "John Doe",
            "email": "john@example.com"
            # Missing loan_amount and loan_purpose
        })

        # Check response status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "All fields are required."})
        self.assertEqual(len(loan_applications), 0)

    def test_no_input_data(self):
        # Simulate a loan application request with no input data (empty JSON object)
        response = self.client.post(
            '/apply-loan', json={}, headers={"Content-Type": "application/json"})

        # Check response status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "No input data provided."})
        self.assertEqual(len(loan_applications), 0)

    def test_unexpected_error(self):
        # Simulate a loan application request without the Content-Type header
        response = self.client.post('/apply-loan')

        # Check that the response indicates an error due to missing Content-Type header
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json, {"message": "Failed to submit loan application."})
        self.assertEqual(len(loan_applications), 0)


if __name__ == '__main__':
    unittest.main()
