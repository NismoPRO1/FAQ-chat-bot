# api/chatbot.py

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Get the length of the incoming data
        content_length = int(self.headers['Content-Length'])
        # Read and decode the data
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body)
        
        # Get the query from the request body
        query = data.get('query', '')

        # Example response from the chatbot logic
        response = f"Your search query was: {query}. This is a Batman-related response."

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Respond with the chatbot's reply
        self.wfile.write(json.dumps({'response': response}).encode('utf-8'))
