import unittest
from graphene.test import Client
from unittest.mock import patch
from schemas.loans import schema, loan_products


class TestLoanSchema(unittest.TestCase):

    def setUp(self):
        # Set up the GraphQL client
        self.client = Client(schema)

    def test_query_loan_products(self):
        query = '''
        query {
            loanProducts {
                id
                name
                interestRate
                maximumAmount
            }
        }
        '''
        executed = self.client.execute(query)
        self.assertIn('data', executed)
        self.assertIn('loanProducts', executed['data'])
        self.assertEqual(
            len(executed['data']['loanProducts']), len(loan_products))

    @patch('schemas.loans.logging.warning')
    def test_query_empty_loan_products(self, mock_logger_warning):
        global loan_products
        loan_products.clear()

        query = '''
        query {
            loanProducts {
                id
                name
                interestRate
                maximumAmount
            }
        }
        '''
        executed = self.client.execute(query)
        self.assertIn('data', executed)
        self.assertIn('loanProducts', executed['data'])
        self.assertEqual(len(executed['data']['loanProducts']), 0)
        mock_logger_warning.assert_called_once()
        mock_logger_warning.assert_called_with("No loan products available.")

        loan_products.extend([
            {"id": 1, "name": "Tom's Loan",
                "interest_rate": 5.0, "maximum_amount": 10000},
            {"id": 2, "name": "Chris Wailaka",
                "interest_rate": 3.5, "maximum_amount": 500000},
            {"id": 3, "name": "NP Mobile Money",
                "interest_rate": 4.5, "maximum_amount": 30000}
        ])

    @patch('schemas.loans.logging.warning')
    def test_query_loan_applications(self, mock_logger_warning):
        query = '''
        query {
            loanApplications {
                id
                fullName
                email
                loanAmount
                loanPurpose
            }
        }
        '''
        executed = self.client.execute(query)
        self.assertIn('data', executed)
        self.assertIn('loanApplications', executed['data'])
        self.assertEqual(len(executed['data']['loanApplications']), 0)
        mock_logger_warning.assert_called_once()
        mock_logger_warning.assert_called_with("No loan applications found.")


if __name__ == '__main__':
    unittest.main()
