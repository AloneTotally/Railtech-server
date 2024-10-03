import firebase_admin
from firebase_admin import credentials, firestore
collections = ["Users","Access Points"]
try:
    cred = credentials.Certificate("railtech-database-firebase-adminsdk-62eza-29a228774f.json")
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(e)

'''------------------------FUNCTIONS----------------------------------------------------'''

db = firestore.client()
def add(collection, document, data):
    #will replace doccument if it exists
    try:
        x = db.collection(collection).document(document).set(data)
        return 1   # worked
    except Exception as e:
        return e # returns exception
def delete(collection, document):
    try:
        x = db.collection(collection).document(document).delete()
        return 1   # worked
    except Exception as e:
        return e # returns exception
def update(collection, document,data):
    try:
        x = db.collection(collection).document(document).update(data)
        return 1   # worked
    except Exception as e:
        return e # returns exception
def getall(collection,document):
    # get all
    try:
        x = db.collection(collection).document(document).get()
        return x.to_dict()
    except Exception as e:
        return e # returns exception
def getfield(collection,document,field):
    try:
        x = db.collection(collection).document(document).get().to_dict().get(field,"Field not found")
        return x
        
    except Exception as e:
        return e # returns exception

# cant get this to work??????
def query(collection,check,val):
    try:
        x = db.collection(collection).where(check,">",val).stream()
        results = [doc.to_dict().get("position") for doc in x]

        return results
    except Exception as e:
        return e

'''-------------------------------------------------Code-----------------------------------'''
# data = {"position":[1,0],"tracking": False,"age":10}
# people = ["Alonzo","Isaac","Nash","Venti"]
# for i in people:
#     add("Users",i,data)
print(query(collections[0],"age",9))
# update(collections[0],"Alonzo",data)
# print(getall("Users","Alonzo"))
# print(getfield(collections[0],"Alonzo","Position"))
# print(query("Users","Tracking","==",True))