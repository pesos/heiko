from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

import requests


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'
    hostname = None

    def do_GET(self, body=True):
        try:
            # Parse request
            if self.hostname is not None:
                url = 'http://{}{}'.format(self.hostname, self.path)
                req_header = self.parse_headers()

                # Call the target service
                logging.info(f"Sending request to {url}")
                resp = requests.get(url, headers=req_header, verify=False)

                # Respond with the requested data
                self.send_response(resp.status_code)
                for k, v in resp.headers.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.content)
            else:
                logging.warning("No hostname set")
                self.send_response(404)
                self.wfile.write(b"Host not configured")
        finally:
            pass

    def parse_headers(self):
        req_header = {}
        for k, v in self.headers.items():
            req_header[k] = v
        return self.inject_auth(req_header)

    def inject_auth(self, headers):
        # headers['Authorization'] = 'Bearer secret'
        return headers


def start_http(port):
    logging.info("Starting server at 0.0.0.0:{}".format(port))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    logging.info('http server is running')
    httpd.serve_forever()
    return httpd


def set_host(host):
    logging.info("Setting hostname to %s", host)
    ProxyHTTPRequestHandler.hostname = host


def reset_host():
    logging.info("Resetting hostname to None")
    ProxyHTTPRequestHandler.hostname = None
