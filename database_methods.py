import firebase_admin
from firebase_admin import credentials, firestore
import time
# Firebase setup


'''------------------------FUNCTIONS----------------------------------------------------'''

#FirebaseS Setup
def setup():
    path = "railtech-database-firebase-adminsdk-62eza-b93f1145aa.json"
    try:
        cred = credentials.Certificate(path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except Exception as e:
        return 0

def add(collection, document, data):
    try:
        db.collection(collection).document(document).set(data)
        return 1  # worked
    except Exception as e:
        return e  # returns exception

def delete(collection, document):
    try:
        db.collection(collection).document(document).delete()
        return 1  # worked
    except Exception as e:
        return e  # returns exception

def update(collection, document, data):
    try:
        db.collection(collection).document(document).update(data)
        return 1  # worked
    except Exception as e:
        return e  # returns exception
def update_field(collection, document, field, data):
    try:
        db.collection(collection).document(document).update({field: data})
        return 1  # worked
    except Exception as e:
        return e  # returns exception
def get_document(collection, document):
    try:
        doc = db.collection(collection).document(document).get()
        return doc.to_dict()
    except Exception as e:
        return e  # returns exception

def get_field(collection, document, field):
    try:
        doc = db.collection(collection).document(document).get().to_dict()
        return doc.get(field, "Field not found")
    except Exception as e:
        return e  # returns exception

def query(collection, check, operator, val):
    try:
        x = db.collection(collection).where(check, operator, val).stream()
        results = [doc.to_dict() for doc in x]
        return results
    except Exception as e:
        return e
def get_collection(collection):
    try:
        doc = db.collection(collection).stream()
        results = [x.id for x in doc]
        return results
    except Exception as e:
        return e  # returns exception
'''-------------------------------------------------Code-----------------------------------'''
db = setup()
data = {"current_coordinates": {"x":0,"y":0},"previous_coordinates":{"x":None,"y":None},"tracking":False,"rssi":{}}
users = ["Isaac","Nash","Venti","Darius"]
for i in users:
    data["name"] = i  
    add("Users",i,data)
# data = {"position": [1, 0], "tracking": True, "age": 30}
# # people = ["Nash", "Venti"]
# for i in range(100):
#     delete("Access Points",str(i))
# print(time.time()-start)
# Sample query: Get users with age greater than 9


# Other function tests
# update("Users", "Nash", {"age": 31})
# print(get_document("Users", "Nash"))
# print(get_field("Users", "Nash", "position"))
