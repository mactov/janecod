import http.server
import socketserver
import os
import threading

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return   

class WebServer(object):


    def __init__(self, project):
        self.project = project
        self.port = 29172


    def start(self):
        os.chdir(self.project)
        Handler = MyRequestHandler
        httpd = socketserver.TCPServer(("", self.port), Handler)
        thread = threading.Thread(target = httpd.serve_forever)
        thread.daemon = True
        try:
            thread.start()
            print('Server started')
        except:
            print('Server stopped')

