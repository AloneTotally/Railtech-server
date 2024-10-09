from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/post-data', methods=['POST'])
def post_data():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Process the data (here we just print it)
        print("Received data:", data)

        # Example of response (echoing back the received data)
        response = {
            "status": "success",
            "received_data": data
        }

        return jsonify(response), 200  # Return a JSON response with a 200 status
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400  # Return an error message with a 400 status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the server on port 5000
