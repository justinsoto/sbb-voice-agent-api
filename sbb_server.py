from flask import Flask, request, jsonify
from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
import os

# Construct Flask server
app = Flask(__name__)

# Load virtual environment 
load_dotenv()

# Create Square client that interacts with Square API
client = Square(
    environment=SquareEnvironment.PRODUCTION,
    token=os.environ['SQUARE_TOKEN']
)

@app.route('/')
def root():
    return 'root'


# Search for customer profile records with a matching phone number 
@app.route('/customer/profile/<phone_number>', methods=['GET'])
def get_customer_profile(phone_number):
    try:
        # queries Square API for customer records with the matching phone number 
        response = client.customers.search(
            query={
                "filter": {
                    "phone_number": {
                        "fuzzy": phone_number
                    }
                }
            }
        )

        customers = []
        
        # prints unique Sqaure ID and full name
        for customer in response.customers:
            print(customer.id)
            print(f"{customer.given_name} {customer.family_name}")
            print(customer.email_address)
            print(customer.phone_number)

            customers.append({
                "customer_id": customer.id,
                "name": f'{customer.given_name} {customer.family_name}',
                "email": customer.email_address,
                "phone_number": customer.phone_number
            })

        print(customers)
        return jsonify(customers)

    except ApiError as e:
        for error in e.errors:
            print(error.category)
            print(error.code)
            print(error.detail)



if __name__ == "__main__":
    app.run(debug=True)