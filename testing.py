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
