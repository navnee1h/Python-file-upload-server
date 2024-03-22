from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import shutil
import cgi

# Define the port for your server
PORT = 8000

# Define the directory where uploaded files will be stored
UPLOAD_DIR = "uploads"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'}
        )

        # Create the uploads directory if it doesn't exist
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        # Save each uploaded file
        for field in form.keys():
            field_item = form[field]
            if isinstance(field_item, list):
                # Handle multiple files with the same field name
                for item in field_item:
                    if item.filename:
                        file_path = os.path.join(UPLOAD_DIR, os.path.basename(item.filename))
                        with open(file_path, "wb") as f:
                            # Write file data in chunks to handle large files
                            shutil.copyfileobj(item.file, f, length=131072)  # Adjust chunk size as needed
            else:
                # Handle single file upload
                if field_item.filename:
                    file_path = os.path.join(UPLOAD_DIR, os.path.basename(field_item.filename))
                    with open(file_path, "wb") as f:
                        # Write file data in chunks to handle large files
                        shutil.copyfileobj(field_item.file, f, length=131072)  # Adjust chunk size as needed

        # Send response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"All files uploaded successfully")

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()