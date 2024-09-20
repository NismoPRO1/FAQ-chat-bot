from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json  # Get the JSON data from the request
        query = data.get('query')  # Extract the 'query' field
        
        # Add your logic to process the query and get a response
        # For demonstration, we'll just echo back the query
        response = f"This is a response to your query: {query}"  # Example response
        
        return jsonify(response=response), 200  # Send back a JSON response
    except Exception as e:
        return jsonify(error=str(e)), 500  # Handle errors

if __name__ == '__main__':
    app.run(debug=True)
