from flask import Flask, request, jsonify
from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
import uuid
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


# Book an appointment with the given customer ID
@app.route('/booking/new', methods=['GET', 'POST'])
def book_new_appointment():
    try:
        # get a list of all available services from the salon
        appointment_services = client.catalog.search_items(
            product_types=[
                "APPOINTMENTS_SERVICE"
            ]
        )

        # genrate a unique idempotency key
        idempotency_key = uuid.uuid4()

        services = []

        # filter out all non-bookable services
        # NOTE: "[Wash Only]" is the only hidden service that passes through the filter
        for service in appointment_services.items:
            if len(service.item_data.variations) == 1:
                services.append(service)

        # list that will only contain bookable services and id numbers 
        # that are relevant to the booking api call 
        final_services_list = []

        # extract three key fields from each service
        # - service_name
        # - service_variation_id
        # - service_variation_version
        for service in services:
            final_services_list.append(
                {
                    "service_name": service.item_data.name,
                    "service_variation_id": service.item_data.variations[0].id,
                    "service_variation_version": service.item_data.variations[0].version,
                }
            )

        # constants for testing
        test_customer_id = "56JV2KW4G4MVVCQVGZ5J76FGGM"     # customer id for Zakia Amazing
        team_member_id = os.environ['TERESA_TEAM_ID']       # Teresa Hernandez team member id
        sbb_location_id = os.environ['SBB_LOCATION_ID']     # SBB location id
        appointment_time = "2025-07-16T12:00:00-04:00"      # July 16, 2025 at 12PM EDT in ISO 8601
        test_service = final_services_list[15]              # Random service 

        # create the appointment
        client.bookings.create(
        booking={
            "appointment_segments": [
                {
                    "team_member_id": team_member_id,
                    "service_variation_id": test_service['service_variation_id'],
                    "service_variation_version": test_service['service_variation_version']
                }
            ],
            "start_at": appointment_time,
            "location_id": sbb_location_id,
            "customer_id": test_customer_id
        },
        idempotency_key=idempotency_key
    )

        return final_services_list
    
    except ApiError as e:
        for error in e.errors:
            print(error)
            print(error.category)
            print(error.code)
            print(error.detail)



if __name__ == "__main__":
    app.run(debug=True)
