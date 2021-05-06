from DAO import DAO
import pymongo

class game_history_DAO(DAO):
    def __init__(self):
        self.connection()
        self.get_next_id()
    
    def connection(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Chess_Gambyte"]
        self.collection = self.db["Game_History"]

    def get_next_id(self):
        self.next_id = self.collection.count() + 1
        return self.next_id

    def save_game(self, game_info):
        self.collection.insert_one(game_info)

    def get_all_games(self):
        all_games = []
        for game in self.collection.find():
            all_games.append(game)
        return all_games

