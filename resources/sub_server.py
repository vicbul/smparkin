from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from iotdm import iotdm_api
import json, sys, ast
from cStringIO import StringIO

class MyBaseHTTPRequestHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        print 'GET request.'
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write('Conected to server.')
        return

    def do_POST(self):
        print 'Getting post info.'
        print self.client_address
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
        })
        print form.headers, form.value
        form_to_dict = ast.literal_eval(form.value)
        # target_URI = form_to_dict['nev']['rep']['rn']
        data = form_to_dict['nev']['rep']
        print data
        # self.get_instance_data('http://localhost:8282',target_URI)
        return

    def get_instance_data(self, target_host, target_URI):
        iotdm_api.retrieve(target_host+target_URI)


def run(server_class=HTTPServer, handler_class=MyBaseHTTPRequestHandler):
    server_address = ('localhost', 8586)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    return httpd


run()
