import socketserver, http.server, logging
from os import listdir
from os.path import isfile, join

PORT = 80
UPLOAD_PATH = 'uploads/'

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.error(self.headers)
        print(self.path)
        files = []
        if self.path == '/getPitResultNames':
            files = [f for f in listdir(UPLOAD_PATH) if isfile(join(UPLOAD_PATH, f)) and f.startswith('pit-') and f.endswith('.json')]
        elif self.path == '/getMatchResultNames':
            files = [f for f in listdir(UPLOAD_PATH) if isfile(join(UPLOAD_PATH, f)) and f.startswith('match-') and f.endswith('.json')]
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(str.encode(','.join(files)))

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info('POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n',
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write('POST request for {}'.format(self.path).encode('utf-8'))
        upload = post_data.decode('utf-8').split('|||')
        with open(UPLOAD_PATH + upload[0] + '.json', 'w') as f:
            f.write(upload[1])

Handler = ServerHandler

httpd = socketserver.TCPServer(('', PORT), Handler)

print('Serving at port: ', PORT)
httpd.serve_forever()