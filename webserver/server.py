from os import curdir
from os.path import join as pjoin
from pprint import pprint
from urlparse import urlparse
import cgi
import os
import pynet
import deepdream
import json
import time

import sys
sys.path.insert(0,'../')

#from http.server import BaseHTTPRequestHandler, HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi

class StoreHandler(BaseHTTPRequestHandler):
    mime = {
        ".html":  "text/html",
        ".htm":   "text/html",
        ".css":   "text/css",
        ".png":   "image/png",
        ".jpg":   "image/jpeg",
        ".jpeg":  "image/jpeg",
        ".js":    "application/javascript",
        ".json":  "application/json",
        "":       "application/octet-stream"
    }

    # Handle static files
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_path = parsed_path.path

        if parsed_path == '/':
            parsed_path = '/index.html'
        parsed_path = parsed_path.lstrip('./\\')

        _, path_ext = os.path.splitext(parsed_path)
        path_ext = path_ext.lower()
        if path_ext in self.mime.keys():
            path_mime = self.mime[path_ext]
        else:
            path_mime = self.mime[""]

        try:
            fn = pjoin(curdir, parsed_path)
            #print("FILENAME: %s\n" % fn)
            with open(fn, 'rb') as fh:
                self.send_response(200)
                self.send_header('Content-type', path_mime)
                self.end_headers()
                self.wfile.write(fh.read())
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    # Handle file upload
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)

                fn = pjoin(curdir, 'inbox', field_item.filename)
                with open(fn, 'w') as fh:
                    fh.write(file_data)
                    
                val, label = pynet.classify_bytes_label(file_data)
		image = deepdream.deepdream_case1(file_data)
		image = 'data:image/jpeg;base64,' + image
                result = {"confidence":float(val), "class":label, "image":image}
                json_line = json.dumps(result)
                self.wfile.write(json_line)

                del file_data    

            # else:
            #     # Regular form value
            #     self.wfile.write(('\t%s=%s\n' % (field, form[field].value)).encode())
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 1488), StoreHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
