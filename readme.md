#Creating a Python3 Webserver From The Ground Up

Jumping into Python when your previous experience is mostly in web-based languages (PHP, Javascript, Ruby) can be a daunting task. Python has all of the tools available to make a strong HTTP Server or framework, as well as plenty of mature web frameworks to get started with, but the purpose of this tutorial/write-up isn't to show you how to leverage those, but how to build one from the ground up (similarly to how you'd start learning with NodeJS).

Throughout this tutorial, we'll go through a few different steps, the first of which is included today:
1. Setting up a basic HTTP server that will respond to basic GET requests with a stock message ("Hello World")
2. Incorporate appropriate file responses for requests (HTML, images, CSS, Javascript) and allow them to automatically import their own resources
3. Allow our routes to take parameters, and respond in-kind with the appropriate data and set up API routes
4. Add a view rendering library and incorporate a database into our application

A basic understanding of Python3's syntax and OOP components will help you through this tutorial. Components important to the server will be explained as we move through, but basic syntax will not be explained. 

The full source code is available on Git, with the appropriate versions tagged. Today's version is tagged as "basic-webserver."

Let's dive right in.

##Setting Up

###Python3

First and foremost, let's make sure we're running the right version - we'll be building this on Python3, which you'll need to have installed. 

You can run a `which python3` on a Linux box to make sure it's available, if not, follow the appropriate steps to install the latest `python3` binary.

Note - on Macs, the version that ships out of the box (i.e. what happens when you run `python`) is version 2, which means you'll need to install the latest version. Homebrew makes this easy.

###Setting Up Our Editor

You can use your editor of choice for this, but I'd recommend at least the following:
- The syntax package for your editor
- A linter (pylint is a good choice)

###Setting Up Our Project

#### `main.py`

Create the directory in which you want the webserver to live. 

I'm going to call mine "http-py".

Once you have a new directory, create two files in the root - the initial will be `main.py` to house our execution script, and `server.py` which will contain the class that will be running our server.

First, let's fill out our `main.py`. Where needed, I'll fill out comments about the code after the presented code blocks.

```python
#!/usr/bin/env python3
import time
from http.server import HTTPServer
from server import Server

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
```
First, we're importing the necessary packages that we'll be using in this file:

The `time` package simply writes timestamps for when our server goes up or down.
The `http.server` package contains the HTTP server boilerplate from the Python3 standard library. We're importing a single module from this - `HTTPServer`.
The `server` module is the other file we'll be filling out here in a moment, as of now, it's going to show an error for the improper import. We're importing a single class, `Server` from our module.

Next, we define two constants we'll be using when we launch the server:

`HOST_NAME=localhost` which will launch our server on our localhost and `PORT_NUMBER=8000` which is the port we want it to run on (feel free to change this port if your 8000 is occupied).

Next up, we have the boilerplate for running our server. The first line `if __name__ == '__main__':` is assuring that we ran this file specifically. If that's the case, we'll execute the rest of the code.

Next, we create the HTTP object by passing the following parameters to the `HTTPServer` object that we imported earlier:
- We pass a tuple containing the `HOST_NAME` and `PORT_NUMBER`
- As a second argument, we pass the server handling class `Server`, imported from our own file, that we'll fill out in a moment

The next line simply prints our "Server UP" with the timestamp to the console. We're using the Python string formatting operator to pass in the constants as well.

This next block actually starts up the server and runs it:

```python
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
```

This tells our created `httpd` object to serve until it receives a keyboard interrupt. Once that happens, it closes out the server connection with `httpd.server_close()`.

Our last `print` line simply outputs a message when the server is closed.

Next, let's set up our server handler.

####`server.py`

Let's go ahead and stub out the file with the following class:

```python
from http.server import BaseHTTPRequestHandler

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_POST(self):
        return

    def do_GET(self):
        return

    def handle_http(self):
        return
        
    def respond(self):
        return
```

We'll be using these four basic methods to handle the responses. On our first line, we import the `BaseHTTPRequestHandler` from the `http.server` package. This is going to be the class that ours will subclass. There are some important things to note:

- When a request comes in, the BaseHTTPRequestHandler will automatically route the request to the appropriate request method (either `do_GET` or `do_POST`) which we've defined on our subclass

- We'll use `handle_http` to send our basic http handlers and then return the content.

- `respond` will be in charge of sending the actual response out

In order to first respond, our class will need to be able to send, at minimum, three things: 

- the response's `Content-type`,
- the response's `status code`,
- and finally the actual content of the site

Let's add this to our class now so that it can send a basic "Hello World" response to a GET request in plain text to make sure our server is working as intended:

```python
from http.server import BaseHTTPRequestHandler

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def do_POST(self):
        return

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes("Hello World", "UTF-8")

    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)
```

Let's look at the changes, starting at our `handle_http` method.

```python
    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes("Hello World", "UTF-8")
```

As stated before, this method is going to take care of sending our header and generally putting the response in a format where it's ready to be sent. All arguments in our `handle_http` method will be pased in from the `respond` method. The flow of data will look like this when a request is received:

`do_* Method` -> `respond Method` -> `handle_http Method`

In the first line, we're sending the status code through the `send_response` method inherited from the `BaseHTTPRequestHandler`. 

In the next line, we're sending the `Content-type` header with `send_headers`, also passed in from our `respond` method. We end the headers we're sending (for now!) with the `self.end_headers` method.

Next, we return the content we want to send ("Hello World" for now), converted into a `bytes` object with UTF-8 encoding. Anything you send back in your response will need to be in this format. We'll add additional handling later to take care of objects that are already in this byte format (for example, images).

Next, let's look at the `respond` method. 

```python
    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)
```

For now, it's passing through a 200 success code and the content type ('text/html') to the handle_http method. Finally we run the `self.wfile.write` method to send the finalized content out as the response.

Our `do_get` method simply kicks off this process as it will be the one the `BaseHTTPRequestHandler` triggers when a GET request is received.

```python
    def do_GET(self):
        self.respond()
```


At this point, our server is ready to run. Navigate to the directory your project is housed in and run `python3 main.py` to start up the server. Navigate to your chosen port (8000) in the above instructions, and you should see a "Hello World" response.










