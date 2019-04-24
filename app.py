from flask import Flask, render_template, url_for, jsonify, request, redirect, session
import os
import json
from flaskext.mysql import MySQL


SECRETE_KEY = os.urandom(24)

app = Flask(__name__, static_url_path='/static')
app.secret_key = SECRETE_KEY
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'ds504'
mysql = MySQL(app)

keyword_list_tmp = ["friendly", "fresh", "chinese", "happy", "family",
              "japanese", "italian", "noodles", "freestyle", "pizza",
              "party", "zen", "BBQ", "curry", "spicy",
              "sports", "expensive", "tip", "homelike", "salty",
              "movie", "vacation", "comic", "sci-fi", "hen-tai",
              "high-end", "successful", "rich", "taylor-swift", "bitch"
              ]

keyword_list = ["pricy", "cream", "dog", "clean", "chicken", "fish", "sushi", "spicy", "music", "party", "appointment",
               "italian", "fresh", "cheese", "sandwich", "wine", "drinks", "bar", "night", "rose", "shrimp", "specials",
               "happy"
               ]

b_ids = ["1SWheh84yJXfytovILXOAQ",
         "xvX2CttrVhyG2z1dFg_0xw",
         "Y6iyemLX_oylRpnr38vgMA",
         "1Dfx3zM-rW4n-31KeC8sJg",
         "giC3pVVFxCRR89rApqklyw",
         ]

_b_list_updated = False

_topic_list = [[]]

_chosen_index = []


def __api_get_topic_list(topic_list):
    '''
    get topic list from beckend recommendation system
    and set the local topic list variable.
    :param topic_list: topic list should be a 2d list/array that has 5 topics and each topic contains 6 keywords
    :return: nothing
    '''
    _topic_list = topic_list
    _b_list_updated = True


def get_entry_by_id(b_id):
    '''
    get MySQL entry by business ID
    :param b_id: a string id of yelp business
    :return: json structured entry of data to send back to front end.
    '''
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM yelp WHERE business_id = %s''', b_id)
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

@app.route("/chosen_list", methods=['POST', 'GET'])
def get_list():
    if request.method == 'GET':
        return "success"
    if request.method == 'POST':
        _chosen_index_jason = request.get_json()
        _tmp_list = _chosen_index_jason["chosen_list"]
        _chosen_index = list(map(int, _tmp_list))
        print(_chosen_index)
        session['_chosen_index'] = _chosen_index
        return jsonify("success")
    # return render_template('template.html', my_string="Wheeeee!", my_list=keyword_list)


@app.route('/', methods=['GET', 'POST'])
def template_test():
    return render_template('index.html', my_string="Wheeeee!", kw_list=keyword_list)

@app.route('/recommend_page', methods=['GET', 'POST'])
def rec_frame():
    if '_chosen_index' in session:
        idx = session['_chosen_index']
        # print(idx)
        tmp_list = [keyword_list[a] for a in idx]
        # print(tmp_list)
        return render_template('recc.html', my_string="Wheeeee!", my_list=tmp_list)


if __name__ == '__main__':

    app.run(debug=True)
