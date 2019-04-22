from flask import Flask, render_template, url_for, jsonify, request, redirect, session
import os
SECRETE_KEY = os.urandom(24)

app = Flask(__name__, static_url_path='/static')
app.secret_key = SECRETE_KEY

keyword_list = ["friendly", "fresh", "chinese", "happy", "family",
              "japanese", "italian", "noodles", "freestyle", "pizza",
              "party", "zen", "BBQ", "curry", "spicy",
              "sports", "expensive", "tip", "homelike", "salty",
              "movie", "vacation", "comic", "sci-fi", "hen-tai",
              "high-end", "successful", "rich", "taylor-swift", "bitch"
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
    return render_template('template.html', my_string="Wheeeee!", my_list=keyword_list)


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
        return render_template('template.html', my_string="Wheeeee!", my_list=tmp_list)


if __name__ == '__main__':

    app.run(debug=True)
