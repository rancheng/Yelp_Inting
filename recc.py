import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize

# Input example
'''
Given a list of strings and top_n restaurants, return top_n recommendation bussiness id
recommendation_input = ["homework", "beef", "pizza", "chicken", "clean", "beer", "sushi", "price"]
output = ['xDHuJaOQ5HqaLP0zgpJD9w', '9eY5ZfKPc_oz6Co5WCPynQ', 'OTMKPz-000UxEN-jBFMA9w', '1QFT7S3Q2ZsS-lPz0CmubA', 'uRM3EfeXd3Dy8yt6xhZkVg', '4w8XXtssRDmggksGeCPy7Q', 'Os16U1qPeLuAJW5dqBdJPw', '9b7hXMrZqCRzUFVjxpiqbg', 't09msA0MsNsTZCn5eTPzLw', 'OLNplh1sp54BOdFxe0OXNg']

'''

def recommend_restaurants(recommendation_input=["homework", "beef", "pizza", "chicken", "clean", "beer", "sushi", "price"], top_n=10):

    # Topic list
    weight_df = pd.read_csv("vectors_rest.csv")


    str0 = "best food place great love amazing favorite ve pho good service bbq delicious phoenix family try worth valley restaurant definitely town friendly brisket authentic time gem wait staff awesome thai far eat just come fresh places arizona scottsdale area az absolutely like recommend pork tried hands times years stop drive"
    str1 = "food place just service time like order good minutes people don table really wait didn bar got location came great night went bad drink come asked room drinks ve nice restaurant server said staff took know going long manager pretty did 10 experience way ordered times want busy waited waiting"
    str2 = "pizza good great place food breakfast delicious salad coffee menu like sandwich love fresh service just wine really bread try cheese ordered nice amazing little time best lunch restaurant friendly perfect patio ve sandwiches definitely bacon italian dinner chocolate got chicken crust eggs dessert meal cake tasty order vegan favorite"
    str3 = "chicken good food place burger ordered like tacos great fries sauce rice just fried cheese really delicious try service fish sushi got order flavor spicy fresh meat time restaurant salad hot beef menu steak shrimp lunch rolls salsa roll best mexican little ve taco chips eat soup pretty taste meal"
    str4 = "great recommend staff dr highly professional amazing friendly job time work best love care hair helpful experience thank years did knowledgeable dog ve feel service place office clean really definitely wonderful going new salon looking awesome store team like family help happy extremely nice thanks comfortable easy make look super"
    str5 = "fun great beer ice music cream kids place bar beers selection games cool game good play love night lots atmosphere birthday watch drinks food awesome party friends nice environment live playing flavors vibe yummy choices friendly really date staff group enjoy family event plenty variety pricey loved definitely little unique"
    str6 = "great food service place friendly good love staff prices awesome sushi happy atmosphere excellent amazing fast hour nice definitely recommend delicious best pizza super clean reasonable wings spot breakfast fresh quick highly favorite really selection lunch price customer drinks attentive fantastic specials quality come menu time beat restaurant location bar"
    str7 = "car time service called told did company customer just said work day got new went don didn phone like business appointment job took great going came know store money price use experience needed home asked hours place ve days make need pay minutes nail massage people way manager come right"

    topics = {
                "topic_0" : str0.split(" "),
                "topic_1" : str1.split(" "),
                "topic_2" : str2.split(" "),
                "topic_3" : str3.split(" "),
                "topic_4" : str4.split(" "),
                "topic_5" : str5.split(" "),
                "topic_6" : str6.split(" "),
                "topic_7" : str7.split(" ")
            }

    restaurant_weight = []
    r_index_list = []
    for r_index, w in enumerate(weight_df['vector'].values):
        if 'nan' not in w[1:-1]:
            temp = (w[1:-1].replace("\n", ''))
            weight_temp = np.fromstring(temp, dtype=float, sep=' ')
            assert len(weight_temp) == 8
            restaurant_weight.append(weight_temp)
            r_index_list.append(r_index)

    # Construct User vector
    user_v = []
    for key, value in topics.items():
        count = 0
        for i in recommendation_input:
            if i in value:
                count += 1
        user_v.append(count)

    random_index = np.sum(user_v)/ len(user_v)
    alpha = 0.95
    # User Vector
    user_v = np.array(user_v) * alpha + random_index * (1-alpha)


    # Create weight restaurants

    restaurant_with_no_nan = weight_df['business_id'].values[r_index_list]

    b_id = restaurant_with_no_nan

    # Create and Normalize Restaurant weight

    w = normalize(np.array(restaurant_weight))
    restaurants_scores = np.dot(user_v, w.T)
    b_index = np.argsort(restaurants_scores.flatten())[::-1].tolist()
    return b_id[b_index].tolist()[:top_n]

# Print top_n result_id
# print(recommend_restaurants(['authentic', 'pho', 'family', 'birthday'], 20))
# print(recommend_restaurants(["chichen", "burger", "taco", "pricey", "vegan", "sushi", "price"], 20))
