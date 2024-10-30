import firebase_admin
from firebase_admin import credentials, firestore
import time
from easy_trilateration.model import Circle
# Firebase setup

'''------------------------FUNCTIONS----------------------------------------------------'''

#FirebaseS Setup
def setup():
    path = "railtech-database-firebase-adminsdk-62eza-2c3d383796.json"
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
def add_field(collection, document, data):
    try:
        db.collection(collection).document(document).set(data,merge = True)
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
        docref = db.collection(collection).document(document)
        doccheck = docref.get()
        if doccheck.exists:
            docref.update(data)
        else:
            docref.set(data)
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
def get_collection_names(collection):
    try:
        doc = db.collection(collection).stream()
        results = [x.id for x in doc]
        return results
    except Exception as e:
        return e  # returns exception
def get_collection_data(collection):
    try:
        doc = db.collection(collection).stream()
        results = [x.to_dict() for x in doc]
        return results
    except Exception as e:
        return e  # returns exception
def select_field(collection,field,identifier):
    try:
        x = db.collection(collection).get()
        data = [i.to_dict() for i in x]
        result = {}
        for i in data:
            result[i[identifier]] = i[field]
        return result
    except Exception as e:
        return str(e)
def classtodict(x):
    return {"x":x.x,"y":x.y,"radius":x.radius}
def dicttoclass(x):
    return Circle(x["x"],x["y"],x["radius"])
@firestore.transactional
def transactional_update(transaction,collection,document,data):
    ref = db.collection(collection).document(document)
    snapshot = ref.get(transaction = transaction)
    transaction.update(ref,data)
def exists(collection, document):
    docref = db.collection(collection).document(document)
    doccheck = docref.get()
    if doccheck.exists:
        return 1
    else:
        return 0
#--------- simple sorting function to take top 5 closes to user
from trilateration import signal_to_distance
def top5(array: list[dict], ascending: bool) -> list:
    x = array
    x.sort(key=lambda accessPoint: signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"])) #ascending in the case of rssi since its -0 to -90
    if len(x) <5:
        return x
    else:
        return x[:5]
'''-------------------------------------------------Code-----------------------------------'''
db = setup()
data = {"current_coordinates": {"x":0,"y":0},"previous_coordinates":{"x":None,"y":None},"tracking":False,"rssi":{},"name":"alonzo"}
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



