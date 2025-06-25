from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
import os

load_dotenv()

client = Square(
    environment=SquareEnvironment.PRODUCTION,
    token=os.environ['SQUARE_TOKEN']
)

def search_customer_by_phone_number(phone_number :str):

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
        
        # prints unique Sqaure ID and full name
        for customer in response.customers:
            print(customer.id)
            print(f"{customer.given_name} {customer.family_name}")

    except ApiError as e:
        for error in e.errors:
            print(error.category)
            print(error.code)
            print(error.detail)


def book_appointment():
    reponse = client.bookings.list()
    print(reponse)
    

def get_items():
    response = client.catalog.list()

    services = []

    for i, item in enumerate(response.items):
        item_type = item.type
        if item_type == "ITEM":
        
            product_type = item.item_data.product_type

            if product_type == "APPOINTMENTS_SERVICE":
                services.append(item)
                # print(f"{i}. {item.item_data.name}: {product_type}")


    for service in services:
        if service.item_data.name == "Relaxer Touch Up":
            print(service)
            print(f'Service ID: {service.id}')
            # print(f'Service Variation ID: {service.item_data.variations[0].item_variation_data.item_id}')
            print(f'Service Variation ID: {service.item_data.variations[0].id}')


def get_location_id():
    location_profiles = client.bookings.location_profiles.list()
    print(location_profiles)


def get_team_member_ids():
    team_members = client.bookings.team_member_profiles.list()

    for member in team_members.items:
        if "Teresa" in member.display_name:
            print(member)

# search_customer_by_phone_number("631 316 6511")
# book_appointment()
# get_items()
# get_location_id()
get_team_member_ids()
