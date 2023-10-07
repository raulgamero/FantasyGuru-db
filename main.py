import os
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

DATA = 'data'
PLAYERS = 'players'
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
CLUSTER = os.environ["CLUSTER"]


def mongo_connection():
    print(USER, PASSWORD, CLUSTER)
    uri = "mongodb+srv://" + USER + ":" + PASSWORD + "@" + CLUSTER + ".wocrudb.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print('-----------------------------------------------')
        print("You successfully connected to MongoDB!")
        print('-----------------------------------------------')
        return client
    except Exception as e:
        print('-----------------------------------------------')
        print("Connection error:")
        print(e)
        print('-----------------------------------------------')
    

def write_players(client):
    db = client[PLAYERS]
    # get all teams 
    os.chdir(PLAYERS)
    teams = os.listdir(os.getcwd())
    for team in teams:
        print('Inserting ' + team + ' data')
        # Create collection for the team
        Collection = db[str(team)]
        # Drop collectiuon if exists
        if Collection is not None:
            Collection.drop()
            Collection = db[str(team)]  
        os.chdir(str(team))
        # Get all players json from the team
        files = [f for f in os.listdir() if os.path.isfile(f)]
        for f in files:
            # Loading or Opening the json file
            with open(str(f)) as file:
                file_data = json.load(file)
            # Inserting the loaded data in the Collection
            if isinstance(file_data, list):
                Collection.insert_many(file_data)  
            else:
                Collection.insert_one(file_data)
        os.chdir('..')
    os.chdir('..')
    print('PLAYERS DATA INSERTED CORRECTLY!')
    print('-----------------------------------------------')


def write_teams(client):
    db = client[DATA]
    # get all teams 
    os.chdir(DATA)
    teams = os.listdir(os.getcwd())
    for team in teams:
        print('Inserting ' + team + ' data')
        # Create collection for the team
        Collection = db[str(team)]
        # Drop collectiuon if exists
        if Collection is not None:
            Collection.drop()
            Collection = db[str(team)] 
        # Loading or Opening the json file
        with open(str(team)) as file:
            file_data = json.load(file)
        # Inserting the loaded data in the Collection
        if isinstance(file_data, list):
            Collection.insert_many(file_data)  
        else:
            Collection.insert_one(file_data)
    os.chdir('..')
    print('TEAMS DATA INSERTED CORRECTLY!')
    print('-----------------------------------------------')


if __name__ == '__main__':
    # Execute scraper loco
    #with open("fantasy_scraper.py") as f:
    #    exec(f.read())
    # Connect to db and write
    client = mongo_connection()
    write_players(client)
    write_teams(client)
    print('DATABASE UPDATED CORRECTLY')
    print('-----------------------------------------------')