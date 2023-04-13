from filter import *
from recommendation import recommend_restaurant, recommend_tour, recommend_hotel
from rcmdweb import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# We assume that the user has already logged in

user_ID = 'vrKkXsozqqecF3CW4cGaVQ'
tour_ID = recommend_tour(user_ID, 450)
hotel_ID = recommend_restaurant(user_ID, 3600)
restaurant_ID = hotel_ID

# Display the welcome message
put_markdown('# Welcome to Travel Copilot!🎉')
put_markdown('### This is a ***travel recommendation system***📖. \n\n ### Fill in the following information according to the guidance.\n\n ### We will provide you with a **customized travel plan**✈️.')

# step 1 date schedule
put_markdown('## Step 1: Date Schedule📅')
put_markdown("### Choose your travel time, we will make a plan for you according to the time.🌞")
num_travel_days = select_date()
put_markdown(f'### You will travel for {num_travel_days} days.🌛 ')

# step 2 select city
put_markdown('## Step 2: Select City🌍')
put_markdown("### First you need to tell me which city you want to go to?🚗")

info = input_group("User info", [
    input('Input your name', name='name', stay=True),
    input('Input the city you want to travel', name='city', type=TEXT, stay=True)
])


city = info['city']
put_markdown(f'### You will travel to {city}.🏯This is a very good choice.🗺️')

# step 3 Choose the attractions you want to visit
put_markdown('## Step 3: Choose the attractions you want to visit🌉')
put_markdown("### There are many recommended attractions, what kind of preferences do you have?🏖")

# tour_categories = ['Aerial Tours', 'Boat Tours', 'Art Galleries']
tour_categories = sel_cate_for_tour()


filtered_tours = filter_businesses(tour_ID)
filtered_tours = filter_businesses_by_type(filtered_tours, tour_categories)
sorted_tours = sort_data_by_business_ids(tour_ID, filtered_tours)
sorted_tours = download_images(sorted_tours[:3])
display_results_for_user(sorted_tours)
put_markdown("### Here are the recommended attractions, you can choose the ones you like.⛰")
selected_tours = select_name(sorted_tours)
longitude = sorted_tours[0]['longitude']
latitude = sorted_tours[0]['latitude']

# step 4 Choose the hotel you want to stay
put_markdown('## Step 4: Choose the hotel you want to stay.🏨')
put_markdown("### Next, we recommend some hotels for you, and you can also choose some needs.💒")

filtered_hotels = filter_businesses(hotel_ID)
filtered_hotels = filter_businesses_by_type(filtered_hotels, ['Hotels'])
# hotel_attributes = {'WiFi': 'not required', 'HasTV': 'True', 'NoiseLevel': 'not required',
#                     'BusinessAcceptsCreditCards': 'not required'}
hotel_attributes = sel_attr_for_hotel()
filtered_hotel_attributes = {k: v for k, v in hotel_attributes.items() if v != 'not required'}
print(filtered_hotel_attributes)
filtered_hotels = filter_data_by_attributes(filtered_hotels, filtered_hotel_attributes)
filtered_hotels = filter_by_distance(longitude, latitude, filtered_hotels, 10000)
sorted_hotels = sort_data_by_business_ids(hotel_ID, filtered_hotels)
sorted_hotels = download_images(sorted_hotels[:3])
display_results(sorted_hotels)
put_markdown("### Here are the recommended hotels, you can choose the ones you like.🏠")
selected_hotel = select_name(sorted_hotels)

# step 5 Choose the restaurants you want to visit
put_markdown('## Step 5: Choose the restaurants you want to visit. 🍽')
put_markdown("### We will recommend some restaurants for you, there are very rich cuisines for you to choose from.🍔")
filtered_restaurants = filter_businesses(restaurant_ID)
# breakfast
put_markdown("### First of all, we recommend some breakfasts near the hotel for you.🥞")
filter_breakfast = filter_businesses_by_type(filtered_restaurants, ['Breakfast & Brunch'])
filter_breakfast = filter_by_distance(longitude, latitude, filter_breakfast, 5000)
sorted_breakfast = sort_data_by_business_ids(restaurant_ID, filter_breakfast)
sorted_breakfast = download_images(sorted_breakfast[:3])
display_results(sorted_breakfast)
put_markdown("### Here are the recommended breakfasts, you can choose the ones you like.🥓")
selected_breakfast = select_name(sorted_breakfast)

# lunch and dinner
put_markdown("### Next, we recommend some restaurants for you to have lunch and dinner.🍕")
# restaurant_categories = ['American (New)', 'French']
# restaurants_attributes = {'RestaurantsPriceRange2': '1', 'OutdoorSeating': 'True', 'RestaurantsReservations': 'True', 'RestaurantsDelivery': 'True'}
restaurant_categories, restaurants_attributes = sel_for_rst()
filtered_restaurants = filter_businesses_by_type(filtered_restaurants, restaurant_categories)
filtered_restaurants_attributes = {k: v for k, v in restaurants_attributes.items() if v != 'not required'}
filtered_restaurants = filter_data_by_attributes(filtered_restaurants, filtered_restaurants_attributes)
filtered_restaurants = filter_by_distance(longitude, latitude, filtered_restaurants, 10000)
sorted_restaurants = sort_data_by_business_ids(restaurant_ID, filtered_restaurants)
sorted_restaurants = download_images(sorted_restaurants[:3])
display_results(sorted_restaurants)
put_markdown("### Here are the recommended restaurants, you can choose the ones you like.🍟")
selected_restaurants = select_name(sorted_restaurants)

# step 6 Display the final plan
put_markdown('## Step 6: Display the final plan.📝')
put_markdown("### Here is your final plan.📝")
display_final_plan(selected_tours[0], selected_hotel[0], selected_breakfast[0], selected_restaurants[0], selected_restaurants[1])