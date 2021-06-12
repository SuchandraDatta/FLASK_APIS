from http.server import BaseHTTPRequestHandler, HTTPServer
import json
#What is BaseHTTPRequestHandler --> Handle HTTP reqs that arrive at server. Must be subclassed to handle each request. Important instance var of this class is server and client-address which is a tuples of the form (host, port), rfile and wfile(IO streams)

#What is HTTPServer -->Class that builds on the TCPServer class by storing server address as instance vars named server_name and server_port. The server is accessed by the handler through the handlers server instance var.

#Format --> HTTPServer(server_address, req_handler_class)
#BaseHTTPRequestHandler(request, client_address, server)

#json load --> from string, bytes or bytes_array
#json loads --> from file
#json dump --> to file
#json dumps --> to string

hostName = "localhost"
server_port = 8000

'''
SimpleHTTPRequestHandler (now called just http.server) defines methods like do_GET() if you get a GET request then do this. wfile is an instance var and write is a function from class BufferedIOBase with format write(bytes-like object) and returns # of bytes written. Similarly, read(N bytes). read and write returns bytes
self.headers["content-length"] --> Data from form POST
'''
class MySimpleServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><form  action = '#' method='POST'><input type='text' name='firstname'></input><input type='text' name='lastname'></input><input type='submit' value='Submit'></input></form></html>", "utf-8"))

	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		print("Content Length: ", int(self.headers["Content-Length"]))
		data = self.rfile.read(int(self.headers["Content-Length"]))
		print(data.decode("utf-8"))
		try:
			print(json.loads(data))
		except:
			pass



def run(server_class=HTTPServer, handler_class=MySimpleServer, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    try:
    	httpd.serve_forever()
    except KeyboardInterrupt:
    	httpd.socket.close()

run()