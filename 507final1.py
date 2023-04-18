import requests
import json
from collections import defaultdict
from plotly.subplots import make_subplots
import plotly.graph_objs as go
CACHE_FILE = 'cache.json'
data_tree = defaultdict(lambda: defaultdict(list))

# API keys
yelp_api_key = '0C3hEulLGZgZltaMUVregmiySEXyXEdRT6r6wuaskGwtoePkE8UY4aBlDIEEjbjXOvS8HqU7hBP281OB-Y9VP0Dpf8aq1v2Jjp_0dL00cDFEoVbxTGD5vt87MeU2ZHYx'
openweather_api_key = '30099990cbd27c1d3bb0f6e057256e94'
WEATHER_API_KEY = '30099990cbd27c1d3bb0f6e057256e94'

# Headers for Yelp API
headers = {
    'Authorization': 'Bearer %s' % yelp_api_key,
}

# Data tree structure
data_tree = defaultdict(lambda: defaultdict(list))

# Cache
cache_file = 'cache.json'
try:
    with open(cache_file, 'r') as file:
        cache = json.load(file)
except FileNotFoundError:
    cache = {}

# Save cache
def save_cache(cache, cache_file_name):
    cache_file = open(cache_file_name, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

# Fetch businesses from Yelp API
def fetch_businesses(location, term):
    cache_key = f'businesses_{location}_{term}'
    if cache_key in cache:
        return cache[cache_key]

    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'location': location, 'term': term, 'limit': 50}

    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    cache[cache_key] = data['businesses']
    save_cache()

    return data['businesses']

# Fetch weather data from OpenWeather API
def fetch_weather_data(lat, lon):
    cache_key = f"weather_{lat}_{lon}"
    if cache_key in cache:
        return cache[cache_key]

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    data = response.json()

    if 'main' not in data:
        print(f"Error: Weather data not found for lat {lat} and lon {lon}")
        return None

    weather_data = {
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity']
    }

    cache[cache_key] = weather_data
    save_cache(cache, CACHE_FILE)
    return weather_data

# Add the search_businesses function here
def search_businesses(location, term):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': f'Bearer {yelp_api_key}'}
    params = {'location': location, 'term': term, 'limit': 50}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()['businesses']

# Process data
def process_data(businesses, location):
    for business in businesses:
        category = business['categories'][0]['title']
        weather_data = fetch_weather_data(business['coordinates']['latitude'], business['coordinates']['longitude'])

        if weather_data:
            business.update(weather_data)
            data_tree[location][category].append(business)


# Generate visualizations
def generate_visualizations():
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Temperature vs Rating", "Humidity vs Rating", "Temperature vs Review Count", "Humidity vs Review Count"))

    for city, categories in data_tree.items():
        for category, businesses in categories.items():
            temperature = [b['temperature'] for b in businesses]
            humidity = [b['humidity'] for b in businesses]
            ratings = [b['rating'] for b in businesses]
            review_counts = [b['review_count'] for b in businesses]

            fig.add_trace(go.Scatter(x=temperature, y=ratings, mode='markers', name=f'{city} - {category}', text=[b['name'] for b in businesses]), row=1, col=1)
            fig.add_trace(go.Scatter(x=humidity, y=ratings, mode='markers', name=f'{city} - {category}', text=[b['name'] for b in businesses]), row=1, col=2)
            fig.add_trace(go.Scatter(x=temperature, y=review_counts, mode='markers', name=f'{city} - {category}', text=[b['name'] for b in businesses]), row=2, col=1)
            fig.add_trace(go.Scatter(x=humidity, y=review_counts, mode='markers', name=f'{city} - {category}', text=[b['name'] for b in businesses]), row=2, col=2)

    fig.update_layout(height=1000, width=1500, title_text="Weather and Business Analysis")
    fig.show()

# Main program
def main():
    while True:
        location = input("Enter the location you want to search (type 'exit' to quit): ")
        if location.lower() == 'exit':
            break

        term = input("Enter the term you want to search (e.g., food, drink, hotel, etc.): ")

        businesses = search_businesses(location, term)
        process_data(businesses, location)  # Pass location as an argument

        good_weather_ratings = []
        good_weather_review_counts = []
        bad_weather_ratings = []
        bad_weather_review_counts = []

        # Define your criteria for good and bad weather
        def is_good_weather(temperature, humidity):
            return 60 <= temperature <= 80 and humidity < 60

        for category, category_businesses in data_tree[location].items():
            for business in category_businesses:
                if 'temperature' in business and 'humidity' in business:
                    if is_good_weather(business['temperature'], business['humidity']):
                        good_weather_ratings.append(business['rating'])
                        good_weather_review_counts.append(business['review_count'])
                    else:
                        bad_weather_ratings.append(business['rating'])
                        bad_weather_review_counts.append(business['review_count'])

        average_good_weather_rating = sum(good_weather_ratings) / len(good_weather_ratings) if good_weather_ratings else 0
        average_bad_weather_rating = sum(bad_weather_ratings) / len(bad_weather_ratings) if bad_weather_ratings else 0
        average_good_weather_review_count = sum(good_weather_review_counts) / len(good_weather_review_counts) if good_weather_review_counts else 0
        average_bad_weather_review_count = sum(bad_weather_review_counts) / len(bad_weather_review_counts) if bad_weather_review_counts else 0

        print("Average rating for businesses with good weather:", average_good_weather_rating)
        print("Average rating for businesses with bad weather:", average_bad_weather_rating)
        print("Average review count for businesses with good weather:", average_good_weather_review_count)
        print("Average review count for businesses with bad weather:", average_bad_weather_review_count)

    # Save the tree structure to a JSON file after processing the data
    with open('results.json', 'w') as outfile:
        json.dump(data_tree, outfile)

    # Add your visualization code here

if __name__ == "__main__":
    main()





