from os import getenv
from enum import Enum
from bcrypt import hashpw, gensalt, checkpw
from pymongo import  MongoClient
from bson.objectid import ObjectId
from dataclasses import dataclass
from typing import List, Literal
from re import compile, IGNORECASE
from dotenv import load_dotenv

load_dotenv()

conn = MongoClient(getenv("MONGO_URI"))
db = conn.FoodTracker
users = db.users
recipes = db.recipes


def oid(data: str):
    return data if isinstance(data, ObjectId) else ObjectId(data)

@dataclass
class Ingredient:
    name: str
    amount: str
    unit: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def to_dict(self):
        return self.__dict__


@dataclass
class Recipe:
    _id: ObjectId
    owner: ObjectId
    name: str
    desc: str
    ingredients: List[Ingredient]
    steps: list

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def to_dict(self, convert: bool = None):
        if convert is True:
            return {**self.__dict__, "_id": str(self._id), "owner": str(self.owner)}
        return self.__dict__
    
    @classmethod
    def find(cls, _id: ObjectId):
        recipe = recipes.find_one({"_id": oid(_id)})
        if not recipe:
            return None
        return cls.from_dict(recipe)
    
    @classmethod
    def find_all(cls):
        return [cls.from_dict(data) for data in recipes.find({})]
    
    def update(self):
        recipes.update_one({"_id": self._id}, {"$set": self.to_dict()})

    @classmethod
    def create_new(cls, owner: ObjectId, name: str, desc: str, ingredients: list, steps: list):
        data = recipes.insert_one({"owner": owner, "name": name, "desc": desc, "ingredients": ingredients, "steps": steps})
        return cls.find(data.inserted_id)

    def get_url(self, type: Literal["edit", "view"]):
        return f"/@user/recipes/{self._id}/edit"

    @staticmethod
    def search(term: str):
        term = compile(term, IGNORECASE)
        return [Recipe.from_dict(data) for data in recipes.find({"name": term})]

    def delete(self):
        recipes.delete_one({"_id": self._id})

class FindBy(Enum):
    ID = 1
    NAME = 2
    EMAIL = 3


@dataclass
class User:
    _id: ObjectId
    uname: str
    passw: str
    email: str

    def get_reciepies(self):
        return [Recipe.from_dict(data) for data in recipes.find({"owner": self._id})]

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def find_by(cls, find_by: FindBy, value: str):
        user = None
        match find_by:
            case FindBy.ID:
                user = users.find_one({"_id": ObjectId(value)})
            case FindBy.NAME:
                user = users.find_one({"uname": value})
            case FindBy.EMAIL:
                user = users.find_one({"email": value.lower()})
        if not user:
            return None
        return cls.from_dict(user)

    @staticmethod
    def _hash_pw(passw: str):
        return hashpw(passw.encode("utf-8"), gensalt()).decode("utf-8")

    def verify_pw(self, passw: str):
        return checkpw(passw.encode("utf-8"), self.passw.encode("utf-8"))

    @classmethod
    def create_new(cls, uname: str, passw: str, email: str):
        data = users.insert_one({"uname": uname.lower(), "passw": cls._hash_pw(passw), "email": email.lower()})
        return cls(data.inserted_id, uname, passw, email)

if __name__ == "__main__":
    # testing
    found = []
    reps = list(Recipe.find_all())
    for recipe in reps:
        if recipe.name in found:
            print("DUPLICATE")
        else:
            found.append(recipe.name)
    print(len(reps) - len(found))
