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
from math import log10
def signal_to_distance(mhz, dbm):
    # Free-Space Path Loss adapted avarage constant for home WiFI routers and following units
    # A source like does abs(dbm) to get I
    FSPL = 27.55 # For now it is an approximation that mainly works with routers and access points
    n = 3  # Path loss exponent for indoor environments (FOR TESTING PURPOSES, this constant will differ for the tunnel)
    m = 10 ** (( FSPL - (20 * log10(mhz)) + abs(dbm)) / (10 * n) )
   
    return m
def top5(array: list[dict], ascending: bool) -> list:
    x = array
    x.sort(key=lambda accessPoint: signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"]),reverse=ascending) #ascending in the case of rssi since its -0 to -90
    if len(x) <5:
        return x
    else:
        return x[:5]
'''-------------------------------------------------Code-----------------------------------'''
db = setup()
# x = get_document("Users","alonzo")
# print(x)
# data = [{'ssid': 'ArthurHome', 'signalStrength': -61, 'bssid': '58:ef:68:32:a1:3b', 'frequency': 5765}, {'ssid': '', 'signalStrength': -77, 'bssid': 'e8:9c:25:ac:d2:48', 'frequency': 5745}, {'ssid': '', 'signalStrength': -90, 'bssid': '8c:3b:ad:c2:63:72', 'frequency': 5580}, {'ssid': 'ArthurHome', 'signalStrength': -51, 'bssid': '58:ef:68:32:a2:0c', 'frequency': 5200}, {'ssid': 'CKGJS_5G-1', 'signalStrength': -85, 'bssid': 'e8:9c:25:ac:d2:44', 'frequency': 5180}, {'ssid': 'ArthurHome', 'signalStrength': -59, 'bssid': '80:69:1a:87:b3:7c', 'frequency': 2472}, {'ssid': '', 'signalStrength': -85, 'bssid': 'de:ec:5e:7c:0a:b1', 'frequency': 2467}, {'ssid': '', 'signalStrength': -86, 'bssid': '72:a0:67:53:e9:8d', 'frequency': 2462}, {'ssid': '', 'signalStrength': -84, 'bssid': '7e:e9:31:02:3e:4b', 'frequency': 2457}, {'ssid': 'TP-Link_AH_Home', 'signalStrength': -83, 'bssid': '5c:e9:31:02:3e:4b', 'frequency': 2457}, {'ssid': 'ArthurHome', 'signalStrength': -42, 'bssid': '58:ef:68:32:a2:0b', 'frequency': 2452}, {'ssid': 'ArthurHome', 'signalStrength': -63, 'bssid': '58:ef:68:32:a1:39', 'frequency': 2452}, {'ssid': '', 'signalStrength': -42, 'bssid': '5e:ef:68:32:a2:0b', 'frequency': 2452}, {'ssid': 'Razarusu_Room', 'signalStrength': -75, 'bssid': '34:60:f9:d3:84:97', 'frequency': 2427}, {'ssid': 'Razarusu_Room', 'signalStrength': -60, 'bssid': '08:bf:b8:b6:13:98', 'frequency': 2427}, {'ssid': 'alone iphone', 'signalStrength': -19, 'bssid': 'e2:e2:41:3c:f6:be', 'frequency': 5745}]
# x = top5(data,False)
# print(x,len(x))
# data = {"current_coordinates": {"x":0,"y":0},"previous_coordinates":{"x":None,"y":None},"tracking":False,"rssi":{},"name":"alonzo"}
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
