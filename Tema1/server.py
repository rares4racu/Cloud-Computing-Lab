import http.server
import json
from urllib.parse import urlparse, parse_qs
from database import *

PORT = 8000
init_db()


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Funcție pentru headers.
    """

    def _send_headers(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    """
    Funcție pentru citirea json-ului.
    """

    def _read_json(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return None
        body = self.rfile.read(content_length)
        try:
            return json.loads(body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return None

    """
    GET
    """

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        if path != "/clients":
            self._send_headers(404, {"error": "Route not found"})
            return
        if not query_params:
            clients = get_clients()
            self._send_headers(200, clients)
            return
        if "id" in query_params:
            client_by_id = get_client_id(query_params["id"][0])
            self._send_headers(200, client_by_id)
            return
        elif "name" in query_params:
            client_by_name = get_client_name(query_params["name"][0])
            self._send_headers(200, client_by_name)
            return

    """
    POST
    """

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        if path != "/clients":
            self._send_headers(404, {"error": "Route not found"})
            return
        data = self._read_json()
        if data is None:
            self._send_headers(400, {"error": "Invalid request"})
            return
        required = ["id", "status", "name", "emailAddress"]
        if not all(field in data for field in required):
            self._send_headers(400, {"error": "Missing fields"})
            return
        try:
            insert_client(data)
        except Exception as e:
            self._send_headers(400, {"error": str(e)})
            return
        self._send_headers(201, {"message": "Client created"})

    """
    PUT
    """

    def do_PUT(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        if path != "/clients":
            self._send_headers(404, {"error": "Route not found"})
            return
        if "id" not in query_params:
            data = self._read_json()
            if data is None:
                self._send_headers(400, {"error": "Invalid request"})
            required = ["id", "status", "name", "emailAddress"]
            if not all(field in data for field in required):
                self._send_headers(400, {"error": "Missing fields"})
                return
            try:
                insert_client(data)
            except Exception as e:
                self._send_headers(400, {"error": str(e)})
                return
            self._send_headers(200, {"message": "Client added"})
            return
        else :
            client_id = query_params["id"][0]
            data = self._read_json()
            if data is None:
                self._send_headers(400, {"error": "Invalid request"})
                return
            required = ["status", "name", "emailAddress"]
            if not all(field in data for field in required):
                self._send_headers(400, {"error": "Missing fields"})
                return
            try:
                update_client(client_id, data)
            except Exception as e:
                self._send_headers(400, {"error": str(e)})
                return
            self._send_headers(200, {"message": "Client updated"})
            return

    """
    DELETE
    """

    def do_DELETE(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        if path != "/clients":
            self._send_headers(404, {"error": "Route not found"})
            return
        if "id" not in query_params:
            self._send_headers(400, {"error": "Missing id parameter"})
            return
        client_id = query_params["id"][0]
        try:
            delete_client(client_id)
        except Exception as e:
            self._send_headers(400, {"error": str(e)})
            return
        self._send_headers(200, {"message": "Client deleted"})


"""
Funcție pentru rularea server-ului.
"""


def run():
    server_address = ("", PORT)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print("Serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the server")
    finally:
        httpd.server_close()
        print("Server stopped")


if __name__ == '__main__':
    run()
