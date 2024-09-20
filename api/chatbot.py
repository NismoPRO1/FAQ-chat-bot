from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

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
    data = request.get_json()
    query = data.get('query')
    
    if query:
        results = google_search(query)
        if results:
            snippets = []
            for result in results:
                snippet = result.get('snippet', 'No snippet available.')
                snippets.append(snippet)
            full_response = "\n\n".join(snippets)
            return jsonify(response=full_response)
    
    return jsonify(response="Sorry, I couldn't find anything relevant on the web.")

if __name__ == '__main__':
    app.run(debug=True)


