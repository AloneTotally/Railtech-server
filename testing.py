# from flask import Flask, jsonify, request
# import json
# app = Flask(__name__)

# # Sample data to act as a database
# items = [
#     {"id": 1, "name": "Item 1"},
#     {"id": 2, "name": "Item 2"},
# ]
# # GET all items
# @app.route('/items', methods=['GET'])
# def get_items():
#     return jsonify(items)

# # GET a single item by ID
# @app.route('/items/<int:item_id>', methods=['GET'])
# def get_item(item_id):
#     item = next((item for item in items if item["id"] == item_id), None)
#     if item is None:
#         return jsonify({"error": "Item not found"}), 404
#     return jsonify(item)

# # POST a new item
# @app.route('/items', methods=['POST'])
# def create_item():
#     print(request.json)
#     new_item = request.json
#     new_item["id"] = len(items) + 1  # Simple ID assignment
#     items.append(new_item)
#     return jsonify(new_item), 201

#     #new_items = request.get_json
#     #new_item["id"] = len(items) + 1  # Simple ID assignment
#     # items.append({"id": 245, "name  ": "Item 3"})
#     #items.append(new_item)
#     # print("Request data is ", request.data)
#     # data = json.loads(request.data)
#     # print("data is ",data)
#     # return jsonify(items), 201

# # PUT to update an item
# @app.route('/items/<int:item_id>', methods=['PUT'])
# def update_item(item_id):
#     item = next((item for item in items if item["id"] == item_id), None)
#     if item is None:
#         return jsonify({"error": "Item not found"}), 404

#     updated_data = request.json
#     item.update(updated_data)
#     return jsonify(item)

# # DELETE an item
# @app.route('/items/<int:item_id>', methods=['DELETE'])
# def delete_item(item_id):
#     global items
#     items = [item for item in items if item["id"] != item_id]
#     return jsonify({"message": "Item deleted"}), 204

# if __name__ == '__main__':
#     app.run(debug=True)
taa_data = {
    "listItems": [
        {
            "title": 'Maintanence between Bukit Panjang and Cashew',
            "type": 'TAR',
            "id": 'SBST123456789A',
            "status": 'Ongoing',
            "workzones": [
                "Workzone A",
                "Workzone C",
                "Workzone E",
            ],
            "checkins": [
                {
                    "name": "alonzo",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Electrical Engineer"
                },
                {
                    "name": "Bob Smith",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Project Manager"
                },
                {
                    "name": "Charlie Davis",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Software Developer"
                },
                {
                    "name": "Dana Lee",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Data Analyst"
                },
                {
                    "name": "Evan Brown",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Mechanical Engineer"
                }
            ]
             ,
            "activitylog":[]
        },
        {
            "title": 'Not Maintanence between Bukit Panjang and Cashew',
            "type": 'EWR',
            "id": 'SMRT123456789A',
            "status": 'Not Started',
            "workzones": [
                "Workzone B",
                "Workzone D",
                "Workzone E",
            ],
            "checkins": [
                {
                    "name": "alonzo",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Electrical Engineer"
                },
                {
                    "name": "Bob Smith",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Project Manager"
                },
                {
                    "name": "Charlie Davis",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Software Developer"
                },
                
                # {
                #     "name": "Dana Lee",
                #     "Date": "-",
                #     "time": "-",
                #     "status": None,
                #     "job": "Data Analyst"
                # },
                # {
                #     "name": "Evan Brown",
                #     "Date": "-",
                #     "time": "-",
                #     "status": None,
                #     "job": "Mechanical Engineer"
                # }
            ]
            ,
            "activitylog":[{
            "title": "Checked in",
            "timestamp": "1.30pm",
            "alert": False,
            "origin": None,
            "note": "",
            "target": "checked in",
            "details":["alonzo"]
            }]
        },
        {
            "title": 'Testing Maintanence between Bukit Panjang and Cashew',
            "type": 'TAR',
            "id": 'SBST987654321A',
            "status": 'Finished',
            "workzones": [
                "Workzone A",
                "Workzone B",
                "Workzone C",
                "Workzone D",
                "Workzone E",
            ],
            "checkins": [
                {
                    "name": "alonzo",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Electrical Engineer"
                },
                {
                    "name": "Bob Smith",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Project Manager"
                },
                {
                    "name": "Charlie Davis",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Software Developer"
                },
                {
                    "name": "Dana Lee",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Data Analyst"
                },
                {
                    "name": "Evan Brown",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Mechanical Engineer"
                }
            ]
            ,
            "activitylog":[{
            "title": "Checked in",
            "timestamp": "1.30pm",
            "alert": False,
            "origin": None,
            "note": "",
            "target": "checked in",
            "details":["darius"]
            }]
        }
    ]
}
all_coordinates = {
        "inWorkzones": [{"workzone A":["alonzo"],"workzone B":["darius"]}]
    }
for taa in taa_data["listItems"]:
    breaker = False
    print("hi")
    for activity in taa["activitylog"]:
        if activity["title"] == "Checked in":
            name = activity["details"][0]
            print(name)
            for workzone in all_coordinates["inWorkzones"][0]:
                for user in all_coordinates["inWorkzones"][0][workzone]:
                    print(user)
                    if user == name:
                        activity["title"] += f" {workzone}"
                        breaker = True
                        break
                if breaker:
                    break
        if breaker:
            print(activity)
            break
    



                
