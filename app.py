from flask import Flask,jsonify
from pymongo import MongoClient 
import requests
import os

app =Flask(__name__)
#get mangoDB connect details from the enviroment variable 
mongo_host =os.environ.get('MONGO_HOST','mongo')
mongo_port =int(os.environ.get('MONGO_PORT',27017))
mongo_url = f'mongodb://{mongo_host}:{mongo_port}/'

#conect to mongodb
client =MongoClient('mongodb://mongo:27017/')
db =client['nba_analytics']
players_collection = db['players']

@app.route('/api/3point-analytics',methods= ['GET'] )

def get_3point_analytics():
    #check if data is already in database
    if players_collection.count_documents == 0:
        nba_api_url ='free-nba.p.rapidapi.com'
        response = requests.get(nba_api_url)
        player_data =response.json()

        #insert data into mongoDB
        players_collection.insert_many(player_data)
   # Extract 3-point shooting data
    three_point_data = [{"player": player["name"], "three_point_percentage": player["3pt_percentage"]} for player in players_collection.find()]
    return jsonify(three_point_data)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')