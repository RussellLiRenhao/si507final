# si507final

#First, let me say that my goal with this project was to explore the relationship between weather and businesses, and to visualize that relationship.

To achieve this, I started by using the Yelp API to search for businesses in different locations and categories. I then used the OpenWeather API to fetch weather data for each locations.

Next, I processed the data by creating a tree structure that organized businesses by location and category. I used this data structure to calculate various statistics, such as average ratings and review counts for businesses in good weather vs. bad weather.

However, I encountered an unexpected issue while analyzing businesses in the "food" category during bad weather. It seemed that the rating and review count for these businesses were 0. Upon further investigation, I discovered that this was likely due to a bias in Yelp's review system, where reviews are more likely to be negative during bad weather. This bias may have led to the apparent lack of positive reviews during bad weather for the "food" category.

While working on this project, I encountered a few errors, such as KeyError and ZeroDivisionError. I had to debug these errors by carefully examining the code and the API responses. I also made use of caching to minimize API requests and speed up the program.

Overall, I'm happy with how the project turned out. It allowed me to practice working with APIs, data processing, and I was able to gain some insights into the relationship between weather and businesses, despite the unexpected issue with the "food" category.

# API keys
yelp_api_key = '0C3hEulLGZgZltaMUVregmiySEXyXEdRT6r6wuaskGwtoePkE8UY4aBlDIEEjbjXOvS8HqU7hBP281OB-Y9VP0Dpf8aq1v2Jjp_0dL00cDFEoVbxTGD5vt87MeU2ZHYx'
openweather_api_key = '30099990cbd27c1d3bb0f6e057256e94'
WEATHER_API_KEY = '30099990cbd27c1d3bb0f6e057256e94'
