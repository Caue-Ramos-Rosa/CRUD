from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

db = []

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/listar_paises':
            self._set_headers()
            self.wfile.write(json.dumps(db).encode('utf-8'))

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/salvar_pais':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            novo_pais = json.loads(post_data)
            db.append(novo_pais)
            self._set_headers()
            self.wfile.write('País salvo com sucesso!'.encode('utf-8'))

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/editar_pais':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            novos_dados = json.loads(post_data)
            self.editar_pais(parsed_path, novos_dados)

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/excluir_pais':
            params = parse_qs(parsed_path.query)
            pais_id = int(params['id'][0])
            global db
            db = [pais for pais in db if pais['id'] != pais_id]
            self._set_headers()
            self.wfile.write('País excluído com sucesso!'.encode('utf-8'))

    def editar_pais(self, parsed_path, novos_dados):
        pais_id = int(parse_qs(parsed_path.query)['id'][0])
        for idx, pais in enumerate(db):
            if pais['id'] == pais_id:
                db[idx] = novos_dados
                break
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write('País editado com sucesso!'.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servindo na porta {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
