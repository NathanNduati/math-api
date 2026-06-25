from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

class MathHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        operations = {'/add': 'addition', '/subtract': 'subtraction', '/multiply': 'multiplication'}
        
        if path in operations:
            try:
                a = float(query_params.get('a', [0])[0])
                b = float(query_params.get('b', [0])[0])
                
                if path == '/add':
                    result = a + b
                elif path == '/subtract':
                    result = a - b
                elif path == '/multiply':
                    result = a * b
                
                response_data = {
                    'a': a,
                    'b': b,
                    'operation': operations[path],
                    'result': result
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                return

            except (ValueError, TypeError):
                self.send_error_response(400, "Invalid query parameters. 'a' and 'b' must be numbers.")
                return
        
        self.send_error_response(404, "Endpoint not found.")

    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode('utf-8'))

def run(port=5000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MathHandler)
    print(f"Starting math API server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()

if __name__ == '__main__':
    run()