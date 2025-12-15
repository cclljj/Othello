import http.server
import socketserver
import json
import os
from othello import OthelloGame

PORT = 8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

game = OthelloGame()

class OthelloHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/state":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            state = self._get_game_state()
            self.wfile.write(json.dumps(state).encode())
            return

        # URL normalization
        path = self.path
        if path == "/" or path == "":
            path = "/index.html"
        
        # Remove query parameters if any
        path = path.split('?')[0]
        
        # Security check: prevent directory traversal
        if ".." in path:
            self.send_error(403, "Forbidden")
            return

        # Try to find the file in the static directory
        # Remove leading slash to make it relative
        relative_path = path.lstrip("/")
        file_path = os.path.join(STATIC_DIR, relative_path)
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.serve_file(file_path)
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        try:
            if self.path == "/api/new_game":
                game.reset_game()
                self._send_json(self._get_game_state())
            elif self.path == "/api/move":
                content_len_header = self.headers.get('Content-Length')
                if not content_len_header:
                     self._send_json_error(400, "Missing Content-Length")
                     return
                
                try:
                    content_length = int(content_len_header)
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data)
                except (ValueError, json.JSONDecodeError):
                    self._send_json_error(400, "Invalid JSON or Content-Length")
                    return
                
                print(f"DEBUG: Processing move {data}")
                success, msg = game.place_disc(data['row'], data['col'])
                
                if not success:
                    print(f"DEBUG: Move failed: {msg}")
                    self._send_json_error(400, msg)
                else:
                    print("DEBUG: Move successful")
                    self._send_json(self._get_game_state())
            else:
                self._send_json_error(404, "Endpoint not found")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self._send_json_error(500, f"Internal Server Error: {str(e)}")

    def _send_json_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"detail": message}).encode())

    def _get_game_state(self):
        return {
            "board": game.get_board(),
            "current_turn": game.current_turn,
            "game_over": game.game_over,
            "winner": game.winner,
            "scores": game.get_score(),
            "valid_moves": [list(m) for m in game.get_valid_moves()]
        }

    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def serve_file(self, path):
        self.send_response(200)
        # simplistic mime type detection
        if path.endswith(".html"):
            self.send_header('Content-type', 'text/html')
        elif path.endswith(".css"):
            self.send_header('Content-type', 'text/css')
        elif path.endswith(".js"):
            self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        with open(path, 'rb') as f:
            self.wfile.write(f.read())

class ReusableThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    # Ensure we are compliant with how do_GET serves files
    # We will verify file existence in static folder explicitly
    with ReusableThreadingTCPServer(("", PORT), OthelloHandler) as httpd:
        print(f"Serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
