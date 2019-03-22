# A hello world GPGI app.

def helloworld(environ):
	environ["output"]("iHello, world!\tnull.host\t1\r\n")
