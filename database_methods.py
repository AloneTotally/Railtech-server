import firebase_admin
from firebase_admin import credentials, firestore
import time
# Firebase setup
path = "railtech-database-firebase-adminsdk-62eza-b93f1145aa.json"
try:
    cred = credentials.Certificate(path)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    print("Firebase Initialized")
except Exception as e:
    print(e)

'''------------------------FUNCTIONS----------------------------------------------------'''

db = firestore.client()

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

'''-------------------------------------------------Code-----------------------------------'''
start = time.time()
data = {"position": [1, 0], "tracking": True, "age": 30}
people = ["Nash", "Venti"]
x = query("Access Points", "age", ">", 9)
print(len(x))
print(time.time()-start)
# Sample query: Get users with age greater than 9


# Other function tests
# update("Users", "Nash", {"age": 31})
# print(get_document("Users", "Nash"))
# print(get_field("Users", "Nash", "position"))
=======
data = {"position":[1,0],"tracking": False,"age":10}
people = ["Alonzo","Isaac","Nash","Venti"]
for i in people:
    add("Users",i,data)
print(query("Users","age",9))
# update(collections[0],"Alonzo",data)
# print(getall("Users","Alonzo"))
# print(getfield(collections[0],"Alonzo","Position"))
# print(query("Users","Tracking","==",True))
>>>>>>> Stashed changes
