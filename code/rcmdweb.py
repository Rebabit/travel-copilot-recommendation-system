from datetime import datetime
from pywebio import STATIC_PATH
from pywebio.input import *
from pywebio.output import *


def select_date():
    # Prompt the user for a start and end date
    data = input_group("Enter the start and end dates", [
        input(name='start_date', type='date', label='Start Date', stay=True),
        input(name='end_date', type='date', label='End Date', stay=True)
    ])

    # Extract start and end dates from input
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

    # Calculate the number of travel days
    delta = end_date - start_date
    num_travel_days = delta.days

    # Return the number of travel days to be used in step 2
    return num_travel_days

def sel_cate_for_tour():
    # Define the list of available categories
    categories = [
        'Art Galleries',
        'Museums',
        'Attraction Farms',
        'Observatories',
        'Aerial Tours',
        'Architectural Tours',
        'Art Tours',
        'Beer Tours',
        'Bike tours',
        'Boat Tours',
        'Bus Tours',
        'Historical Tours',
        'Walking Tours',
        'Whale Watching Tours',
        'Wine Tours'
    ]

    # Prompt the user to select categories
    selected_categories = checkbox("Select categories", options=categories, stay=True)


    return selected_categories

def sel_attr_for_hotel():
    # Define the available attribute options
    wifi_options = ['not required', 'free']
    tv_options = ['not required', 'True']
    parking_options = ['not required', 'True']
    noise_options = ['not required', 'quiet', 'average', 'loud', 'very_loud']
    credit_options = ['not required', 'True']

    # Prompt the user to select attributes
    data = input_group("Select attributes", [
        select(name='wifi', label='WiFi', options=wifi_options),
        select(name='tv', label='HasTV', options=tv_options),
        select(name='parking', label='Business Parking', options=parking_options),
        select(name='noise', label='NoiseLevel', options=noise_options),
        select(name='credit', label='BusinessAcceptsCreditCards', options=credit_options),
    ])

    # Build a dictionary of selected attributes
    attributes = {
        'WiFi': data['wifi'],
        'HasTV': data['tv'],
        'BusinessParking': data['parking'],
        'NoiseLevel': data['noise'],
        'BusinessAcceptsCreditCards': data['credit']
    }

    # Return the dictionary of attributes
    return attributes

def sel_for_rst():
    categories = ["Asian Fusion", "Japanese", "American (Traditional)", "American (New)", "Chinese",
                  "Mexican", "Indian", "Italian", "French", "Vegetarian", "Vegan", "Halal", "Gluten-Free"]
    selected_categories = checkbox("Select preferences", options=categories, required=False)

    data = input_group("Select attributes", [
        select(name='price_range', label='Price Range', options=["1", "2", "3", "4"]),
        select(name='business_parking', label='Business Parking', options=['not required', 'True']),
        select(name='outdoor_seating', label='Outdoor Seating', options=['not required', 'True']),
        select(name='alcohol', label='Alcohol', options=['not required', 'full_bar', 'beer_and_wine']),
        select(name='reservations', label='Reservations', options=['not required', 'True']),
        select(name='delivery', label='Delivery', options=['not required', 'True'])
    ])

    selected_attributes = {"RestaurantsPriceRange2": data['price_range'],
                            "BikeParking": data['business_parking'],
                            "OutdoorSeating": data['outdoor_seating'],
                            "Alcohol": data['alcohol'],
                            "Reservation": data['reservations'],
                            "Delivery": data['delivery']
                            }


    return selected_categories, selected_attributes


def display_results(results):
    put_html(
        "<style>table{border-collapse: collapse;width: 100%;}th, td{padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}th{background-color: #04AA6D;color: white;}</style>")
    table_data = [["Name", "Address", "Stars", "Distance", "Photo"]]
    for result in results:
        table_data.append([
            result['name'],
            result['address'],
            str(result['stars']),
            f"{round(result['distance'] / 1000, 1)} km",
            put_image(open(result['PhotoPath'], 'rb').read(), width="200px", height="200px")
        ])
    put_table(table_data)



def display_results_for_user(results):
    put_html(
        "<style>table{border-collapse: collapse;width: 100%;}th, td{padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}th{background-color: #04AA6D;color: white;}</style>")
    table_data = [["Name", "Address", "Stars", "Photo"]]
    for result in results:
        table_data.append([
            result['name'],
            result['address'],
            str(result['stars']),
            put_image(open(result['PhotoPath'], 'rb').read(), width="200px", height="200px")
        ])
    put_table(table_data)



def select_name(results):
    selected_result = []
    options = [r['name'] for r in results]
    selected_name = checkbox('Select a name:', options)
    for result in results:
        if result['name'] in selected_name:
            selected_result.append(result)
    return selected_result

def display_final_plan(tour, hotel, restaurant1, restaurant2, restaurant3):
    put_html(
        "<style>table{border-collapse: collapse;width: 100%;}th, td{padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}th{background-color: #04AA6D;color: white;}</style>")
    table_data = [["Plan", "Photo", "Info"]]
    table_data.append([
        "Tour",
        put_image(open(tour['PhotoPath'], 'rb').read(), width="200px", height="200px"),
        f"Name: {tour['name']}" + "\n" + f"Address: {tour['address']}" + "\n" + f"Stars: {tour['stars']}" + "\n"  + "\n"])
    table_data.append([
        "Hotel",
        put_image(open(hotel['PhotoPath'], 'rb').read(), width="200px", height="200px"),
        f"Name: {hotel['name']}" + "\n" + f"Address: {hotel['address']}" + "\n" + f"Stars: {hotel['stars']}" + "\n"  ])
    table_data.append([
        "Breakfast",
        put_image(open(restaurant1['PhotoPath'], 'rb').read(), width="200px", height="200px"),
        f"Name: {restaurant1['name']}" + "\n" + f"Address: {restaurant1['address']}" + "\n" + f"Stars: {restaurant1['stars']}" + "\n"])
    table_data.append([
        "Lunch",
        put_image(open(restaurant2['PhotoPath'], 'rb').read(), width="200px", height="200px"),
        f"Name: {restaurant2['name']}" + "\n" + f"Address: {restaurant2['address']}" + "\n" + f"Stars: {restaurant2['stars']}" + "\n"])
    table_data.append([
        "Dinner",
        put_image(open(restaurant3['PhotoPath'], 'rb').read(), width="200px", height="200px"),
        f"Name: {restaurant3['name']}" + "\n" + f"Address: {restaurant3['address']}" + "\n" + f"Stars: {restaurant3['stars']}" + "\n"])

    put_table(table_data)




if __name__ == '__main__':
    # Example data
    data = [
        {'image': '../downloads/A Love Letter for You Philadelphia/Image_1.jpg', 'text': 'Item 1'},
        {'image': '../downloads/A Love Letter for You Philadelphia/Image_1.jpg', 'text': 'Item 2'},
        {'image': '../downloads/A Love Letter for You Philadelphia/Image_1.jpg', 'text': 'Item 3'},
        {'image': '../downloads/A Love Letter for You Philadelphia/Image_1.jpg', 'text': 'Item 4'},
        {'image': '../downloads/A Love Letter for You Philadelphia/Image_1.jpg', 'text': 'Item 5'}
    ]

    # Loop through the data and display each item in a row
    for i in range(0, len(data), 2):
        # Create a row with three columns
        with put_row():
            pass

        with put_row():
            # Display the first item in the row
            put_image(open(data[i]['image'], 'rb').read(), width='150px', height='150px')
            put_text(data[i]['text'])

            # Display the second item in the row
            if i + 1 < len(data):
                put_image(open(data[i + 1]['image'], 'rb').read(), width='150px', height='150px')
                put_text(data[i + 1]['text'])











