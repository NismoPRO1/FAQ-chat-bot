from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Your Google API key and Custom Search Engine ID
api_key = 'AIzaSyCHypa5gHM29KNDoa7Y6f17WhUV7MJ9t4I'
cse_id = '645b315c8a32c4605'

# Google Custom Search API
def google_search(query):
    service = build("customsearch", "v1", developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id, num=3).execute()
    return result['items'] if 'items' in result else []

# Route for handling search queries
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        query = data.get('query')
        logging.debug(f"Received query: {query}")

        if query:
            results = google_search(query)
            logging.debug(f"Search results: {results}")

            if results:
                snippets = []
                for result in results:
                    snippet = result.get('snippet', 'No snippet available.')
                    snippets.append(snippet)
                full_response = "\n\n".join(snippets)
                return jsonify(response=full_response)

        return jsonify(response="Sorry, I couldn't find anything relevant on the web.")
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify(response="An error occurred."), 500

if __name__ == '__main__':
    app.run()


