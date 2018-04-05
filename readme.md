# Creating a Python3 Webserver From The Ground Up

Jumping into Python when your previous experience is mostly in web-based languages (PHP, Javascript, Ruby) can be a daunting task. Python has all of the tools available to make a strong HTTP Server or framework, as well as plenty of mature web frameworks to get started with, but the purpose of this tutorial/write-up isn't to show you how to leverage those, but how to build one from the ground up (similarly to how you'd start learning with NodeJS).

Throughout this tutorial, we'll go through a few different steps, the first of which is included today:
1. Setting up a basic HTTP server that will respond to basic GET requests with a stock message ("Hello World") and then expand that to have a router that allows us to request different HTML files.
2. Incorporate appropriate file responses for requests (HTML, images, CSS, Javascript) and allow them to automatically import their own resources
3. Allow our routes to take parameters, and respond in-kind with the appropriate data and set up API routes
4. Add a view rendering library and incorporate a database into our application

A basic understanding of Python3's syntax and OOP components will help you through this tutorial. Components important to the server will be explained as we move through, but basic syntax will not be explained. 

The full source code is available on Git, with the appropriate versions tagged. Today's version is tagged as "v1-webserver".

Let's dive right in.

## Setting Up

### Python3

First and foremost, let's make sure we're running the right version - we'll be building this on Python3, which you'll need to have installed. 

You can run a `which python3` on a Linux box to make sure it's available, if not, follow the appropriate steps to install the latest `python3` binary.

Note - on Macs, the version that ships out of the box (i.e. what happens when you run `python`) is version 2, which means you'll need to install the latest version. Homebrew makes this easy.

### Setting Up Our Editor

You can use your editor of choice for this, but I'd recommend at least the following:
- The syntax package for your editor
- A linter (pylint is a good choice)

### Setting Up Our Project

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

```python
import time
from http.server import HTTPServer
from server import Server
```

The `time` package simply writes timestamps for when our server goes up or down.
The `http.server` package contains the HTTP server boilerplate from the Python3 standard library. We're importing a single module from this - `HTTPServer`.
The `server` module is the other file we'll be filling out here in a moment, as of now, it's going to show an error for the improper import. We're importing a single class, `Server` from our module.

Next, we define two constants we'll be using when we launch the server:

```python
HOST_NAME = 'localhost'
PORT_NUMBER = 8000
```

`HOST_NAME=localhost` which will launch our server on our localhost and `PORT_NUMBER=8000` which is the port we want it to run on (feel free to change this port if your 8000 is occupied).

Next up, we have the boilerplate for running our server. The first line `if __name__ == '__main__':` is assuring that we ran this file specifically. If that's the case, we'll execute the rest of the code.

Next, we create the HTTP object:
```python
httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
```
We pass the following parameters to the `HTTPServer` object that we imported earlier:
- We pass a tuple containing the `HOST_NAME` and `PORT_NUMBER`
- As a second argument, we pass the server handling class `Server`, imported from our own file, that we'll fill out in a moment

The next line simply prints our "Server UP" with the timestamp to the console. We're using the Python string formatting operator to pass in the constants as well.

```python
print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
```

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

```python
print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
```

Next, let's set up our server handler.

#### `server.py`

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

We'll be using these methods to handle the responses. On our first line, we import the `BaseHTTPRequestHandler` from the `http.server` package. This is going to be the class that ours will subclass. There are some important things to note:

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

`do_*` receives request &rarr; `respond` invoked &rarr; `handle_http` bootstraps request, returns  content &rarr; `respond` sends the response

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

We now have a webserver!

### Adding a Router

Obviously, right now, this is not much of a webserver - we're just passing "Hello World" out to the user. 

One of the most important facets of a websever is being able to respond to requests at different URLs - it's not really useful without it. So next, we're going to go ahead and create a router.

A router, at its core, just allows us to map a given request to a given resource on our webserver. This sounds very similar to a given structure in Python (the dictionary) which allows us to map keys to their specific values. 

Let's create a new folder (routes) and create a file inside that directory (`main.py`).

![alt text](docs/routes.png "Routes Directory Structure")

Since we're currently working with text, we're going to set up our router to just respond with text data when a given route is hit.

Let's fill this out:

```python
routes = {
    "/" : "Hello World",

    "/goodbye" : "Goodbye World"
}
```
This is very simple at the moment, but we'll be filling it out further in our examples.

Next, let's import the routes file into our `server.py`:

```python
from http.server import BaseHTTPRequestHandler
from routes.main import routes

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes("Hello World", "UTF-8")

    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)
```

Next, let's adjust our `handle_http` to grab content from the routes file dependent on the current path:

```python
    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        route_content = routes[self.path]
        return bytes(route_content, "UTF-8")
```

All we need to do is pull the `self.path` member from the class and then pass it into the `routes[]` dictionary that we pulled from our routes file. It's pretty straightforward - we're just looking it up by key at the moment. We then pass the `route_content` into our return in order to pass it on to the `respond` method.

### Sending HTML

Next we're going to make the routes file respond with HTML rather than just text - far more useful.

Let's create a few more files. Start by creating a "templates" folder which will house our HTML (for now, index.html and goodbye.html) and (in the future) assets:

![alt text](docs/templates.png "Template Directory Structure")

You can put whatever you want in these files for now, but leave out any references to CSS or JS because our server will not be able to handle those right now (though we'll be getting to that).

Here's our index.html file:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>Simple Python HTTP Server</h1>
</body>
</html>
```

We also need to change our routes file - we're going to go ahead and nest another dictionary within our current keys:

```python
routes = {
    "/" : {
        "template" : "index.html" 
    },

    "/goodbye" : {
        "template" : "goodbye.html"
    }
}
```

The `template` key within our nested dictionary is going to handle pointing out to our specific template file for a given route.

Next, we'll adjust our `server.py` file to pull those specific files:

```python
from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def handle_http(self):
        status = 200
        content_type = "text/plain"
        response_content = ""

        if self.path in routes:
            print(routes[self.path])
            route_content = routes[self.path]['template']
            filepath = Path("templates/{}".format(route_content))
            if filepath.is_file():
                content_type = "text/html"
                response_content = open("templates/{}".format(route_content))
                response_content = response_content.read()
            else:
                content_type = "text/plain"
                response_content = "404 Not Found"
        else:
            content_type = "text/plain"
            response_content = "404 Not Found"

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_content, "UTF-8")

    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)
```

We'll cover the changes starting with our new import:

```python
from pathlib import Path
```

We're importing the `Path` module from `pathlib` to make sure that our HTML files exist before we attempt to read their contents.

Next, we'll go down to our handle_http method:

```python
    def handle_http(self):
        status = 200
        content_type = "text/plain"
        response_content = ""

        if self.path in routes:
            route_content = routes[self.path]['template']
            filepath = Path("templates/{}".format(route_content))
            if filepath.is_file():
                content_type = "text/html"
                response_content = open("templates/{}".format(route_content))
                response_content = response_content.read()
            else:
                status = 404
                content_type = "text/plain"
                response_content = "404 Not Found"
        else:
            status = 404
            content_type = "text/plain"
            response_content = "404 Not Found"

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_content, "UTF-8")
```

We're doing a few things differently now:

- The method no longer takes any arguments, instead we'll be building out the response type and status code within our function so that we can respond with a 404 or other status code if necessary
- We're doing a check to ensure that our path exists within our routes to ensure that the path actually exists. If it doesn't, we'll send a 404 with a text/plain response
- Within this check, we're pulling the given route's template into the route_content variable and then passing it to `open`
- Once this is pulled, we use `.read` to get the HTML file's content. If the file doesn't exist, we throw a 404.
- After this, the only changes are that the `content_type` is now dynamic, and the `response_content` is equivalent to what we set it to earlier.

Go ahead and fire up the server and check your index page - you should now we be able to see the content you put in your `index.html` file. Next, go to /goodbye and you'll be able to see the content in the `goodbye.html` file.

### Handling Non-HTML File Requests and Some Refactoring

Okay, so, we've created a server that is capable of returning HTML files for a specific URL, but we haven't yet built something that can handle everything else an HTML file needs to do, namely, being able to include CSS, Javascript and Image files from the server. 

We're going to be building that out, but the first thing we want to do is some refactoring. In the current files, we're handling everything on a case-by-case basis which will very quickly baloon into a massive `handle_http` function.

Go ahead and create a new folder, named "response". This response folder is going to house a few classes that will allow us to tailor the response for specific types of files (e.g. templates vs static assets) in a much cleaner way.

Within this folder, let's create the base `Response` class and name it `requestHandler.py`:

```python
class MockFile():
    def read(self):
        return False
        
class RequestHandler():
    def __init__(self):
        self.contentType = ""
        self.contents = MockFile()

    def getContents(self):
        return self.contents.read()

    def read(self):
        return self.contents

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getContentType(self):
        return self.contentType 

    def getType(self):
        return 'static'
```

Within this file, we're going to do two things:

- Create a `MockFile` class - this is a placeholder object that will take care of requests where we won't have a `.read` function on the `self.contents` member.
    - If we don't have this, Python will yell at us, despite the fact that we'll be supplying the results of `open` calls later that have a `read` function.
- We're also declaring our `RequestHandler` here that will be the class we extend to handle each type of request. There are a number of different methods we're delclaring on this object which are mostly getters and setters for the various atributes that each request type will have. Also important to note is what we're not declaring here:
    - We have no mechanism to actually retrieve the file - this is because we're going to delegate that to the child classes so that they can each individually handle where the files should be imported from, as well as any specific handling that needs to happen to those files.

Next, let's go ahead and define a child class that will extend this to handle our templates and get our server back up and running:

```python
from response.requestHandler import RequestHandler

class TemplateHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'text/html'

    def find(self, routeData):
        try:
            template_file = open('templates/{}'.format(routeData['template']))
            self.contents = template_file
            self.setStatus(200)
            return True
        except:
            self.setStatus(404)
            return False
```

Within our `TemplateHandler` class, the first thing we're doing is importing our `RequestHandler` from the previous file. We pass it into the constructor for the class so that it inherits from that class:

`class TemplateHandler(RequestHandler):`

Next up, we define two methods - within our `__init__` we set the content-type for our HTML templates (which will always be `text/html`).

We define the `find` method which will allow the template to find the specific file and set the contents so that we can pull them out within our server file.

We now have a class that will handle our templates, but in our `server.py` we currently have two different types of requests that need handled - the templates, and "bad" requests, such as a 404 if the file is not found. Let's go ahead and implement a `BadRequestHandler` as well.

```python
from response.requestHandler import RequestHandler

class BadRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__(self)
        self.contentType = 'text/plain'
        self.setStatus(404)
```

Simple enough - this one doesn't need a `find` method because there's nothing to find, it's just a 404 so the content-type can be simple, and the status will be a 404.

Let's change up our `server.py` to reflect the changes we made - for now we'll only be handling HTML requests and sending 404s for everything else:

```python
import os

from http.server import BaseHTTPRequestHandler

from routes.main import routes

from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if request_extension is "" or request_extension is ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()

        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
```

We've changed some of the logic around - our `do_GET` will now be handling the actual request with our `RequestHandler` objects.

First, let's look at the new imports:

```python
import os
...
from response.templateHandler import TemplateHandler
from response.staticHandler import StaticHandler
from response.badRequestHandler import BadRequestHandler
```

Here we're importing the `os` package that will allow us to split the extension from the request path so that we can match against the extension and use the appropriate handler.

Let's look at our `do_GET` method:

```python
    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if request_extension is "" or request_extension is ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()

        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })
```

First, we split the path into its parts using `os.path.splitext`. We then pull the file extension from the array we just created.

We then have a conditional to check if our extension is either "" or ".html". This will handle requests for both .html files directly, and for simple URL requests (e.g. localhost:8000/, localhost:8000/goodbye).

Next, we have the same logic we previously did to see if the path exists in our routes file. If the path is valid, we create a new `TemplateHandler()` and then use the handler's `.find` method, passing in the routes object which looks like this:

```json
{
    "template" : "templateName.html"
}
```

In our `else` we use a `BadRequestHandler()` to signal the 404 on the file.

In our next `else` (if the route isn't found) we create another `BadRequestHandler()` to handle the 404.

Finally, we use `self.respond` and send the created `handler` through to the respond method which will then be passed into our `handle_http` method.

Let's look at `respond` next:

```python
    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
```

The only change here is that we're passing through an `opts` argument that contains the handler, and then passing that through to the `handle_http` method call.

Finally, let's check out the new `handle_http`:
```python
    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        return bytes(content, 'UTF-8')
```

First, we pull the `status_code` from the handler. If a `BadRequestHandler` made its way through, it'll be a 404, otherwise a 200 in the `TemplateHandler` unless the handler was unable to find the file, in which case it will also respond with a 404 (check out the `TemplateHandler`'s logic to see this in action).

We go ahead and send the status code, and then if the status code is 200 (OK) we go ahead and pull the contents of the file with `handler.getContents()`. This does an internal call to `.read` on the file that we opened.

Next, we send a header with the content type, again pulled from our `handler`.

We end the headers, and then go ahead and send our result. 

We're now reading files using our `RequestHandler` class, and we've cleaned up our `server.py` quite a bit (or at least made it more understandable and extensible).

That's it for today's tutorial - when the second part of this is published, we'll take a look at how we can add other resources (css, javascript, etc) and have the HTML pages automatically request them (like, how, you know, the web actually works).

Thanks for reading, and I hope you'll check back in for part 2!







