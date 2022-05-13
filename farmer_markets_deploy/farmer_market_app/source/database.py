"""
This is a file that works with database for a program that shows US farmer markets.
It includes functions that search for needed information or execute INSERT, UPDATE and DELETE commands
"""


import pyodbc
from source.config import cnxn, server, database, username, password


def change_config(config_file):
    """
    This function changes the configuration file back to the default set of options after application is stopped
    
    Parameters
    ----------


    Returns
    ---------
   
    """
    with open(config_file, "r") as f:        
        data = f.read()
        data = data.replace(f"username = '{username}'", "username = 'username'") \
            .replace(f"password = '{password}'", "password = 'password'") \
            .replace(f"server = '{server}'",
                     "server = 'server'") \
            .replace(f"database = '{database}'", "database = 'database'")
        with open(config_file, "w") as f:
            f.write(data)
                
                
def get_order_criteria(selected_criteria):
    """
    This function establishes an order criteria
    
    Parameters
    ----------
    selected_criteria: str

    Returns
    ---------
    str    
    """
    if selected_criteria == "Z-A":
        order_criteria = "LOWER([MarketName]) DESC"
    elif selected_criteria == "A-Z":
        order_criteria = "LOWER([MarketName])"
    else:
        order_criteria = selected_criteria
    return order_criteria
    

def get_all_markets(search_condition = "MarketName", name_city_state_or_zip = "", orderby_criteria = "LOWER([MarketName])"):
    """
    This function helps to get brief information about the market:
        MarketName, Street, County, State, Rank, Votes
    
    Parameters
    ----------
    search_condition: str
    name_city_state_or_zip: str or int
    orderby_criteria: str

    Returns
    ---------
    list with pyodbc.Row values
    """
    with cnxn.cursor() as cursor:              
        cursor.execute(f"SELECT mar.[FMID], LOWER(mar.MarketName) MarketName, \
                        ISNULL(LOWER(TRIM(mar.[street])), '') Street, ISNULL(LOWER(TRIM(mar.[city])), '') City, \
                        ISNULL(LOWER(TRIM(mar.[County])),'') County, \
                        ISNULL(LOWER(TRIM(mar.[State])), '') State, \
                        ROUND(AVG(ISNULL(c.rank, 0)), 0) Rank, \
                        COUNT(c.rank) Votes \
                        FROM [dbo].[FarmersInfo] mar \
                        FULL JOIN [dbo].[Comments] c \
                        ON mar.FMID = c.FMID \
                        WHERE UPPER({search_condition}) LIKE UPPER('{name_city_state_or_zip}%') \
                        GROUP BY mar.[FMID], LOWER(mar.MarketName), \
                        ISNULL(LOWER(TRIM(mar.[street])), ''), ISNULL(LOWER(TRIM(mar.[city])), ''), \
                        ISNULL(LOWER(TRIM(mar.[County])),''), \
                        ISNULL(LOWER(TRIM(mar.[State])), ''), zip  \
                        ORDER BY {orderby_criteria}\
                        ")
        row = cursor.fetchall()
    return row


def get_one_market_info(market_id):
    """
    This function helps to get full information about the market:
        MarketName, Website, Facebook, Other media like Twitter, Youtube or any other,
        Street, County, State, Latitude, Longitude, Rank
    
    Parameters
    ----------
    market_id: int

    Returns
    ---------
    pyodbc.Row
    """
    with cnxn.cursor() as cursor:   
        cursor.execute(f"SELECT mar.[FMID], LOWER(mar.MarketName) MarketName, ISNULL(mar.[Website], '') Website, \
                        ISNULL(mar.[Facebook], '') Facebook, \
                        COALESCE(mar.[Twitter], mar.[Youtube], mar.[OtherMedia], '') OtherMedia, \
                        ISNULL(LOWER(mar.[street]), '') Street, ISNULL(LOWER(mar.[city]), '') City, \
                        ISNULL(LOWER(mar.[County]),'') County, \
                        ISNULL(LOWER(mar.[State]), '') State, \
                        mar.[y] Latitude, \
                        mar.[x] Longitude,\
                        ROUND(AVG(ISNULL(c.rank, 0)), 0) Rank \
                        FROM [dbo].[FarmersInfo] mar \
                        FULL JOIN [dbo].[Comments] c \
                        ON mar.FMID = c.FMID \
                        WHERE mar.FMID = {market_id} \
                        GROUP BY mar.[FMID], LOWER(mar.MarketName), ISNULL(mar.[Website], ''), \
                        ISNULL(mar.[Facebook], ''), \
                        COALESCE(mar.[Twitter], mar.[Youtube], mar.[OtherMedia], ''), \
                        ISNULL(LOWER(mar.[street]), '') , ISNULL(LOWER(mar.[city]), '') , \
                        ISNULL(LOWER(mar.[County]),''), \
                        ISNULL(LOWER(mar.[State]), ''), \
                        mar.[y], mar.[x]")    
        row = cursor.fetchone()
    return row


def get_markets_comments(market_id):
    """
    This function helps to get comments about the market
    
    Parameters
    ----------
    market_id: int

    Returns
    ---------
    list with pyodbc.Row values
    """
    with cnxn.cursor() as cursor:   
        cursor.execute(f"SELECT v.nick_name Nickname, \
                        c.Comment Comment, \
                        c.Rank Ranked \
                        FROM Visitors v \
                        FULL JOIN [dbo].[Comments] c \
                        ON c.visitor_id = v.visitor_id \
                        FULL JOIN [FarmersInfo] mar \
                        ON mar.FMID = c.FMID \
                        WHERE mar.FMID = {market_id} \
                        ") 
        row = cursor.fetchall()
    return row
   

def get_markets_goods(market_id):
    """
    This function helps to get and sort information about goods sold in the market
    
    Parameters
    ----------
    market_id: int

    Returns
    ---------
    list
    """
    with cnxn.cursor() as cursor:   
        cursor.execute(f"SELECT case [Organic] when 'True' then 'Organic food' END, case [Bakedgoods] when 'True' then 'Baked goods' END, \
                        case [Cheese] when 'True' then 'Cheese' END, case [Crafts] when 'True' then 'Crafts' END,\
                        case[Flowers] when 'True' then 'Flowers' END, case [Eggs] when 'True' then 'Eggs' END,\
                        case[Seafood] when 'True' then 'Seafood' END, case [Herbs] when 'True' then 'Herbs' END,\
                        case[Vegetables] when 'True' then 'Vegetables' END, case [Honey] when 'True' then 'Honey' END,\
                        case[Jams] when 'True' then 'Jams' END, case [Maple] when 'True' then 'Maple' END,\
                        case[Meat] when 'True' then 'Meat' END, case [Nuts] when 'True' then 'Nuts' END,\
                        case[Plants] when 'True' then 'Plants' END, case [Poultry] when 'True' then 'Poultry' END,\
                        case[Prepared] when 'True' then 'Prepared food' END, case [Soap] when 'True' then 'Soap' END,\
                        case[Trees] when 'True' then 'Trees' END, case [Wine] when 'True' then 'Wine' END,\
                        case[Coffee] when 'True' then 'Coffee' END, case [Beans]when 'True' then 'Beans' END, \
                        case[Fruits] when 'True' then 'Fruits' END, case [Grains] when 'True' then 'Grains' END,\
                        case[Juices] when 'True' then 'Juices' END, case [Mushrooms] when 'True' then 'Mushrooms' END,\
                        case[PetFood] when 'True' then 'Pet food' END, case [Tofu] when 'True' then 'Tofu' END,\
                        case[WildHarvested] when 'True' then 'Wild harvested food' END \
                        FROM [FarmersInfo] WHERE FMID = {market_id}")
        row = cursor.fetchone()
    goods=[]
    index=0
    for r in row:
        if row[index] != None:
            goods.append(r)       
        index+=1
    goods.sort()
    return goods
    

def get_next_market(market_name):
    """
    This function helps to get id of the next market in the database
    
    Parameters
    ----------
    market_name: str

    Returns
    ---------
    pyodbc.Row
    """
    with cnxn.cursor() as cursor:   
        cursor.execute(f"SELECT TOP(1) FMID \
                        FROM [FarmersInfo] \
                        WHERE MarketName > '{market_name}' ORDER BY MarketName")
        next_market = cursor.fetchone()
    return next_market


def get_previous_market(market_name):
    """
    This function helps to get id of the previous market in the database
    
    Parameters
    ----------
    market_name: str

    Returns
    ---------
    pyodbc.Row
    """
    with cnxn.cursor() as cursor:  
        cursor.execute(f"SELECT TOP(1) FMID \
                        FROM [FarmersInfo] \
                        WHERE MarketName < '{market_name}' ORDER BY MarketName DESC")
        prev_market = cursor.fetchone()
    return prev_market


def get_markets_nearby(distance, market_id, order_criteria):
    """
    This function helps to get information about the markets found in the radius of N miles
    
    Parameters
    ----------
    distance: str
        N-miles radius
    market_id: int
        Id of the market that is the center of the radius
    order_criteria: str
        order criteria of the results

    Returns
    ---------
    list with pyodbc.Row values
    """
    with cnxn.cursor() as cursor:
        cursor.execute(f"SELECT a.FMID, LOWER(a.MarketName) MarketName, \
                        ISNULL(LOWER(a.city), '') City, \
                        ISNULL(LOWER(a.Street), '') Street, \
                        (6371000 * 2 * ASIN(SQRT( \
                        POWER(SIN((a.[y] - ABS((SELECT [y] FROM [FarmersInfo] WHERE FMID = {market_id}))) * PI() / 180 / 2), 2) \
                        + COS(a.[y] * PI() / 180) \
                        * COS(ABS((SELECT [y] FROM [FarmersInfo] WHERE FMID = {market_id})) * PI() / 180) \
                        * POWER(SIN((a.[x]- (SELECT [x] FROM [FarmersInfo] WHERE FMID = {market_id})) * PI() / 180 / 2), 2)))) AS dist, \
                        ROUND(AVG(ISNULL(c.rank, 0)), 0) Rank,  COUNT(c.rank) Votes \
                        FROM [FarmersInfo] a \
                        FULL JOIN [dbo].[Comments] c \
                        ON a.FMID = c.FMID \
                        WHERE \
                        (6371000 * 2 * ASIN(SQRT( \
                        POWER(SIN((a.[y] - ABS((SELECT [y] FROM [FarmersInfo] WHERE FMID = {market_id}))) * PI() / 180 / 2), 2) \
                        + COS(a.[y] * PI() / 180) \
                        * COS(ABS((SELECT [y] FROM [FarmersInfo] WHERE FMID = 1000709)) * PI() / 180) \
                        * POWER(SIN((a.[x]- (SELECT [x] FROM [FarmersInfo] WHERE FMID = {market_id})) * PI() / 180 / 2), 2)))) \
                        < {distance} * 1609.34 \
                        AND a.FMID != {market_id} \
                        GROUP BY a.FMID, a.MarketName, \
                        a.city, \
                        a.Street, a.x, a.y \
                        ORDER BY {order_criteria}")
        matkets_nearby = cursor.fetchall()
    return matkets_nearby


def get_user_comment(market_id, nick_name, user_password):        
    """
    This function helps to get the comment about the market of one particular user
    using his nickname and password
    
    Parameters
    ----------
    market_id: int
    nick_name: str
    user_password:str
    
    Returns
    ---------
    pyodbc.Row
    """             
    with cnxn.cursor() as cursor:
        cursor.execute(f"SELECT v.nick_name Nickname, ISNULL(c.Comment, '') Comment, c.rank Rank \
                       FROM Comments c \
                       JOIN Visitors v \
                       ON c.visitor_id = v.visitor_id \
                       WHERE c.FMID = {market_id} \
                       AND c.visitor_id = (SELECT visitor_id FROM Visitors \
                       WHERE nick_name = '{nick_name}' \
                       AND user_password = '{user_password}')")
        user_comment_from_db = cursor.fetchone()
    return user_comment_from_db


def delete_comment(market_id, nick_name, user_password):
    """
    This function deletes the comment about the market of one particular user
    from the database using his nickname and password
    
    Parameters
    ----------
    market_id: int
    nick_name: str
    user_password:str
    
    Returns
    ---------

    """ 
    with cnxn.cursor() as cursor:
        cursor.execute(f"DELETE \
                       FROM Comments \
                       WHERE FMID = {market_id} \
                       AND visitor_id = (SELECT visitor_id FROM Visitors \
                       WHERE nick_name = '{nick_name}' \
                       AND user_password = '{user_password}')")
        cnxn.commit()


def update_comment(market_id, nick_name, user_password, user_comment, user_rank):
    """
    This function updates the comment and/or rank about the market of one particular user
    using his nickname and password
    
    Parameters
    ----------
    market_id: int
    nick_name: str
    user_password: str
    user_comment: str
    user_rank: int
    
    Returns
    ---------

    """ 
    with cnxn.cursor() as cursor:
        cursor.execute(f"UPDATE Comments SET Comment = '{user_comment}', rank = {user_rank}\
                       WHERE FMID = {market_id} \
                       AND visitor_id = (SELECT visitor_id FROM Visitors \
                       WHERE nick_name = '{nick_name}' \
                       AND user_password = '{user_password}')\
                       ")                  
        cnxn.commit()           


def check_user_id_in_comments(market_id, nick_name):   
    """
    This function looks for visitor_id in the table 'Comments' using given market_id and nick_name
    
    Parameters
    ----------
    market_id: int
    nick_name: str
    
    Returns
    ---------
    pyodbc.Row
    """ 
    with cnxn.cursor() as cursor:
        cursor.execute(f"SELECT c.visitor_id \
                       FROM Visitors v \
                       JOIN Comments c \
                       ON v.visitor_id = c.visitor_id \
                       WHERE v.nick_name = '{nick_name}' \
                       AND c.FMID = {market_id}")
        user_id = cursor.fetchone()
    return user_id  


def check_user_id_in_visitors(nick_name):
    """
    This function looks for visitor_id in the table 'Visitors' using given nick_name
    
    Parameters
    ----------
    nick_name: str
    
    Returns
    ---------
    pyodbc.Row
    """ 
    with cnxn.cursor() as cursor:
        cursor.execute(f"SELECT visitor_id \
                   FROM Visitors \
                   WHERE nick_name = '{nick_name}'")
        user_id = cursor.fetchone()
    return user_id


def create_new_visitor(nick_name, user_password):
    """
    This function creates a new visitor using given nick_name and user_password
    
    Parameters
    ----------
    nick_name: str
    user_password: str
    
    Returns
    ---------

    """ 
    with cnxn.cursor() as cursor:
        cursor.execute(f"INSERT INTO Visitors(nick_name, user_password) \
                        VALUES('{nick_name}', '{user_password}')")
        cnxn.commit()


def create_new_comment(market_id, user_id, user_comment, user_rank):
    """
    This function creates a new entry with comment and rank given by a particular user
    
    Parameters
    ----------
    market_id: int
    user_id: int
    user_comment: str
    user_rank: int
    
    Returns
    ---------

    """
    with cnxn.cursor() as cursor:
        cursor.execute(f"INSERT INTO Comments (FMID, visitor_id, Comment, rank) \
                        VALUES ({market_id}, {user_id}, '{user_comment}', {user_rank})")
        cnxn.commit()
