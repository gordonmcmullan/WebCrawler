import platform
from threading import Thread
import http.server
import socketserver

class Platform:

    @classmethod
    def file_scheme_prefix(cls):
        if platform.system() == "Windows":
            file_prefix = "//"
        else:
            file_prefix = ""
        return file_prefix


class TestHttpServer():

    def __init__(self):
        self.thread = Thread(group=None, target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        self.start_server()



    @classmethod
    def start_server(cls):
        server_started = False
        port = 9999
        handler = http.server.SimpleHTTPRequestHandler
        while not server_started:
            try:
                cls.httpd = socketserver.TCPServer(("", port), handler)
                cls.httpd.serve_forever()
                server_started = True
            except(OSError):
                pass

    @classmethod
    def stop_server(cls):
        try:
            cls.httpd.server_close()
            cls.httpd.shutdown()
        except:
            pass

