"""
This is a views file for a program that shows US farmer markets.
There are two views: index or home page of the application and info.
Home page shows all the markets from the database with a brief information aboout them.
It also gives opportunity to search for markets by name, city, state or zip and
order results by name from A to Z or Z to A, by city, state, ranks and votes.
Info-view is devoted to the market chosen by a user.
It gives all the details about the market and 
allows reading and adding comments and ranks 
and changing and deleting them if you log in using password.
You can also search for markets situated in the radius of N miles
"""


from flask import Flask, render_template, request
from source import app
from source import database
from source import exiting
import os


@app.route('/', methods=['GET', 'POST'])
def index():
    search_entry = ''
    search_criteria = 'MarketName'
    order_criteria = "LOWER([MarketName])"
       
    if request.method == 'POST':
        if 'search-input' in request.form:
            search_entry = request.form['search-input']
            search_criteria = order_criteria = request.form['searching']

        sort_criteria = request.form['order_markets']
        if sort_criteria != "Sort":
            order_criteria = database.get_order_criteria(sort_criteria)        
    
    markets = database.get_all_markets(search_criteria, search_entry, order_criteria)

    return render_template('index.html', markets=markets, search_entry=search_entry, search_criteria=search_criteria)


@app.route('/info', methods=['GET', 'POST'])
def info():
    distance = 0
    new_markets = ''
    user_comment_from_db = ''
    order_criteria = 'LOWER([MarketName])'
    market_id = request.args.get('market_id')
    user_password = ''
    user_comment = ''
    user_rank = ''
    
    if request.method == 'POST':
        if request.form.get("form_type") == 'formOne':
            distance = request.form['search-distance']
            if 'order_markets' in request.form:
                sort_criteria = request.form['order_markets']
                if sort_criteria != "Sort":
                    order_criteria = database.get_order_criteria(sort_criteria)
            
        elif request.form.get("form_type") == 'formTwo':
            nick_name = request.form['nickname-input'].replace("'", "''")
            
            if 'password-input' in request.form:
                user_password = request.form['password-input']
            if 'comment-input' in request.form:
                user_comment = request.form['comment-input'].replace("'", "''")
            if 'star-rating' in request.form:
                user_rank = request.form['star-rating']
                    
            if 'show_comment' in request.form:
                if user_password != '':             
                    user_comment_from_db = database.get_user_comment(market_id, nick_name, user_password)
            
            elif 'delete_comment' in request.form:
                if user_password != '': 
                    database.delete_comment(market_id, nick_name, user_password)
                    
            elif 'add_comment' in request.form:
                if nick_name != '' and user_rank != '':
                    user_id = database.check_user_id_in_comments(market_id, nick_name)
                    if user_id:
                        if user_password != '': 
                            database.update_comment(market_id, nick_name, user_password, user_comment, user_rank)
                    else:
                        user_id = database.check_user_id_in_visitors(nick_name)
                        if not user_id:
                            database.create_new_visitor(nick_name, user_password)
                            user_id = database.check_user_id_in_visitors(nick_name)                
                        database.create_new_comment(market_id, user_id[0], user_comment, user_rank)
            
    market = database.get_one_market_info(market_id)
    market_name = market[1].replace("'", "''")
    comments = database.get_markets_comments(market_id)
    markets_goods = database.get_markets_goods(market_id)
    next_market = database.get_next_market(market_name)
    prev_market = database.get_previous_market(market_name)

    if distance != '':
        new_markets = database.get_markets_nearby(distance, market_id, order_criteria)

    return render_template('info.html', market=market, distance=distance, markets_goods=markets_goods, 
                            next_market=next_market, prev_market=prev_market, 
                            new_markets=new_markets, 
                            comments=comments, user_comment_from_db=user_comment_from_db)


@app.route('/exit')
def exit():
    config_file = r'farmer_market_app/source/config.py'
    global exiting
    exiting = True
    database.change_config(config_file)
    return "Exit"


@app.teardown_request
def teardown(exception):
    if exiting:
        os._exit(1)