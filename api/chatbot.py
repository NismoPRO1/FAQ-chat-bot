from http.server import BaseHTTPRequestHandler
import json
from googleapiclient.discovery import build

# Your Google API Key and Custom Search Engine ID
api_key = 'AIzaSyCHypa5gHM29KNDoa7Y6f17WhUV7MJ9t4I'
cse_id = '645b315c8a32c4605'

# Function to perform Google search
def google_search(query):
    service = build("customsearch", "v1", developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id, num=3).execute()  # Fetch more results
    return result['items'] if 'items' in result else []

# Handler for Vercel's serverless function
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the incoming data
        content_length = int(self.headers['Content-Length'])
        # Read and decode the data
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body)
        
        # Get the query from the request body
        query = data.get('query', '')

        # Perform the Google search
        results = google_search(query)
        if results:
            snippets = [result['snippet'] for result in results]
            response = "\n\n".join(snippets)
        else:
            response = "Sorry, I couldn't find anything relevant on the web."

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Respond with the search results
        self.wfile.write(json.dumps({'response': response}).encode('utf-8'))
