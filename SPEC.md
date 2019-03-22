# GPGI Specification v0.1.1

## Metadata

Author: Robert "khuxkm" Miles <khuxkm@tilde.team>  
WIP  
Errata probably exist, that's why this is zero-ver

Version history:

 - v0.1.0 - initial release
 - v0.1.1 - fix formatting

## Rationale

[WSGI][pep-3333] is Python's standard web gateway interface. However, to the 
best of the author's knowledge, no such specification has been made in any way 
for Gopher.

While the web dwarfs Gopher, the latter is still in use in many places. To help 
standardize this set of programs, the author has resolved to make this a 
publicly available specification for how one may go about such a thing.

Much like WSGI, since no production-ready applications can serve it, GPGI needs 
to be easy to implement.

## Gopher

The Gopher protocol is a TCP/IP application layer protocol designed for 
distributing, searching, and retrieving documents over the Internet. ([Wikipedia][1])

Originally built by Mark McCahill and his team of University of Minnesota, 
Gopher eventually lost to the World Wide Web. However, to this day, Gopher 
enthusiasts are still making "gopherholes" and keeping the protocol alive. Some 
even tout it as an alternative to the current state of the web.

While the author makes no claims about the effectiveness of the textual Gopher 
protocol to replace the visual World Wide Web, he does acknowledge that the 
protocol has its charm.

## A Note on String Types

All strings must be ASCII-representable. In Python 3, for example, `output.encode("ascii")`
cannot fail.

## Definitions

For the purposes of this specification:

 - `callable` - "an object that, should the server support it, can be utilized as a function would in Python"
 - `mapping` - "a Python dictionary, or equivalent type"

## GPGI

GPGI works in a similar way to WSGI, being based on a callable. However, the
definition of "callable" is changed. The new definition is intentionally vague
to support implementation of GPGI outside of the Python ecosystem.

The server, upon recieving a request, will set up an "environ" mapping
containing the following values:

 - `selector` - The selector utilized to access the function. (WSGI equivalent: `SCRIPT_NAME+PATH_INFO`?)
 - `query` - The raw query. (WSGI equivalent: providing a variable with the contents of `wsgi.input` pre-read)
 - `output` - A callable that will output the supplied string in ASCII encoding.
 - `log` - A callable of signature `callable(level,msg)` that will log `msg` at level `level`, preferably using standard library logging except where it doesn't exist.

The application MUST be able to modify the environ mapping to its liking. The
callable will be invoked with `environ` as its first and only argument. Once
the callable returns, any output sent via `output` must be sent to the
client in ASCII encoding. The server is responsible for terminating the Gopher
connection with a dot on its own line.

## An example app

In Python 3:

```python
# example app for GPGI spec
def gpgi_app(environ):
    write = environ["output"]
    write("iHello, world!\tnull.host\t1\r\n")
```

In Lua:

```lua
-- example app for GPGI spec
function gpgi_app(environ)
    environ.output("iHello, world! I'm Lua!\tnull.host\t1\r\n")
end
```

## Middleware (or, playing both parts)

As with WSGI, apps may be a server to some application(s) and an application to
some server(s). Generally, middleware MUST leave environ as is, unless there is
a reason to change. For example, the `output` entry SHOULD be changed to proxy
output through the middleware (if the middleware changes the output).

Here is an example of changing any lines that do not start with a listing char
to info lines. Please note that this can be done better, and that this is simply
an illustration.

```python
GOPHER_SPECIAL_CHARS = "i0137ghI"

# hello world app from earlier but redone to show off the middleware
def helloworld(environ):
	environ["output"]("Hello, world!")

def escape_lines(environ):
	def write(line):
		if line and line[0] not in GOPHER_SPECIAL_CHARS:
			environ["output"]("i{}\tnull.host\t1\r\n".format(line.rstrip()))
		elif line:
			environ["output"](line.rstrip()+"\r\n")
	fake_env = dict()
	fake_env.update(environ)
	fake_env["output"]=write
	helloworld(fake_env)
```

[pep-3333]: https://python.org/dev/peps/pep-3333/
[1]: https://en.wikipedia.org/Gopher_(protocol)
