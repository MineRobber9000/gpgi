import socketserver, exampleapps, time

APP = exampleapps.helloworld

HOST = "127.0.0.1"
PORT = 7071

def output(f):
	def _output(out):
		f.write(out.encode("ascii"))
	return _output

def log(level,message):
	"""Logger. Technically conforms with GPGI v0.1.0 spec."""
	print("[{}] <{}> {}".format(time.strftime("%Y-%m-%dT%H:%M:%S"),level,message))

class GPGIHandler(socketserver.StreamRequestHandler):
	def handle(self):
		selector = self.rfile.readline().decode("ascii").strip()
		query = None
		if "\t" in selector:
			selector, query = selector.split("\t",1)
		environ = dict(selector=selector,query=query,output=output(self.wfile),log=log)
		APP(environ)
		self.wfile.write(".\r\n".encode("ascii"))
		return

if __name__=="__main__":
	server = socketserver.TCPServer((HOST,PORT),GPGIHandler)
	server.serve_forever()
