import graphene
import logging
from graphql import GraphQLError

loan_products = [
    {"id": 1, "name": "Tom's Loan", "interest_rate": 5.0, "maximum_amount": 10000},
    {"id": 2, "name": "Chris Wailaka", "interest_rate": 3.5, "maximum_amount": 500000},
    {"id": 3, "name": "NP Mobile Money",
        "interest_rate": 4.5, "maximum_amount": 30000}
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
        try:
            if not loan_products:
                logging.warning("No loan products available.")
                return []
            return loan_products
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")
            raise GraphQLError("Failed to fetch loan products.")

    def resolve_loan_applications(self, info):
        try:
            if not loan_applications:
                logging.warning("No loan applications found.")
                return []
            return loan_applications
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")
            raise GraphQLError("Failed to fetch loan applications.")


schema = graphene.Schema(query=Query)
