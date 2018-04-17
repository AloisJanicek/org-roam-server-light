# Part 2

In part one we took a look at setting up the basic infrastructure for a web framework - namely serving up HTML files at specific route reponses. If you haven't ready Part 1(https://medium.com/@andrewklatzke/creating-a-python3-webserver-from-the-ground-up-4ff8933ecb96), I'd start there to get up to speed.

## Setting Up a Static Request Handler

In the previous section, we set up two different types of request handlers: a `BadRequestHandler` to manage 404s and other types of errors, and a `TemplateHandler` to send back our HTML file requests at specific URLs. We're going to expand that now by adding a third type of handler, a `StaticHandler`.

First, let's stub out the file so that it properly utilizes our `RequestHandler` parent class:

<script src="https://gist.github.com/aklatzke/371b26c6e986acc3fa44a2469af92461.js"></script>

Within this class, we've set up three methods:
 - `__init__`, which we'll add to in a moment,
 - `find` which if we remember from the last article, is responsible for actually finding the file,
 - and finally, `setContentType` which will work in tandem with the `__init__` to set the appropriate content type depending on the file extension

 We know from our `TemplateHandler` that we currently have the `server.py` set up to pass the entire path to a given request into the handler for that request. As such, we can go ahead and fill out these methods based on the incoming request, and then we'll add the handling logic to our `server.py` so that it routes to this handler when appropriate.

Go ahead and create a folder called "public" within your directory. This is going to house all public assets for the site (CSS, Images, Javascript, etc.). By using a specific folder we can insure that:
1. No one can request files outside that folder
2. We can consistently access the files from a simple path - e.g. treating our "public" folder as the server root

As such, a request for "/main.css" would translate (on our server) to "/public/main.css". This makes it easy for us to reason about where our requests should be routed, and restricts all of the access on our server to a single folder (helping with possible security issues).

Let's go ahead and fill out the `StaticHandler`'s `find` method.

Before we do, go ahead and add the following line to the top of your `StaticHandler` file:

`import os`

We'll be using this to grab files from the filesystem.

As for the `StaticHandler`:

<script src="https://gist.github.com/aklatzke/e357cf5534332b3bbade9f78c3e3f030.js"></script>

Within this method we've done a few things:
- First, we split the path into its individual parts using the `os` package so that we can pull the extension
- Next, we pull that extension from `split_path[1]`
- Our conditional checks if it's of certain filetypes (images) which are already in `bytes` format
  - If they are in bytes format, we open them with 'rb',
  - if not, we open them with just 'r'
- We're using the built-in string formatting to build out the path, prefixing it with "public"
  - _It would be wise to add some logic surrounding this to ensure that no one can include `..` in the request path to give them access to more than what is intended. For now, we're going to skip that part_.
- Next, we pass the extension to `self.setContentType` (which we'll see in a moment)
- Finally, if we got to this point, we set the status code to 200
- If there is an exception (e.g. the file does not exist) then we set the contenttype to 'notfound' and send a 404 code
  - _Again, there is significant room here for better error handling, but I don't want to bore you with the details, so we've excluded it for the time being. When the final source is posted, I'll adjust for these so that they're better handled._
- We return a boolean in either case to let the consumer of this method know that the file was either found or not.

Next, let's look at how we'll figure out the `Content-Type` (I'm including the entire `StaticHandler` here so you can see it all in tandem):

<script src="https://gist.github.com/aklatzke/b298432b0bdbe8064d7fa348aa859575.js"></script>

We're setting up a hash table within our `__init__` to handle the whitelisted file types available. For now, we'll allow the processing of: js, css, png, and jpg files. This can obviously be expanded to handle additional file types like videos, gifs, etc..

In our `setContentType` method, we're simply doing a lookup on this hash table to set the content type to the appropriate value:

`self.contentType = self.filetypes[ext]`

Now that the contentType member is set, when we run `getContentType` in our `server.py` we'll be able to get the appropriate content type. 

## Adding our New Handler

In the last article we went through the hassle of setting up the `RequestHandler` class, and we're now seeing how it benefits us; by having each of these classes extend our base `RequestHandler` we're allowing the a "plug and play" interface for a new handler without having to drastically change the code in our base `server.py` file. Pretty soon, we won't have to interact with `server.py` at all, but first, we need to go ahead and add our `StaticHandler` into the mix to handle non-html requests:

We know that requests for static assets will always be "GET" requests, so that's the method we want to zero in on:

<script src="https://gist.github.com/aklatzke/fbfec7c7db66b5d54c85b886b1b0401a.js"></script>

First we add the import for our new file:

`from response.staticHandler import StaticHandler`

Next, let's look at the changes to the `do_GET` method:

<script src="https://gist.github.com/aklatzke/fd597c05a4fc06fce93393e518b8f585.js"></script>

They're fairly straightforward, but let's document them here:
- The firs thing: we've added an `elif` to our conditional that checks if the request file's extension is ".py". This is just a security addition to make sure that if someone is (for some reason) trying to request a source file, that it immediately ends the request and sends back a 404
- Next, we turn the previous `BadRequestHandler` in the `else` into a call to the `StaticHandler` instead
  - _Since the `StaticHandler` takes care of a 404 if it cannot find the file, this basically means that it will look for a file in __public__ and if it cannot return it, will send the same 404 it would have previously_ 
- We pass the path into the `StaticHandler`'s `.find` method, and that's basically it. The  data will be pulled out in the same manner as it is for our `TemplateHandler` because they're using the same parent class

Next, there are a few quick changes we need to make to the `handle_http` method:

<script src="https://gist.github.com/aklatzke/42d414601dfa469ddb308f5540296f00.js"></script>

This is a simple one - because some of our files will now be coming back to us in `bytes` format (e.g. images) we need to account for the fact that they do not need to be converted into a `bytes` type.

We set up a conditional to check if the `content` from the handler is already a `bytes` or `bytearray` object - if it is, we go ahead and return that data, otherwise we return the data converted into the bytes type object.

## Seeing It In Action

Visit your "templates/index.html" file and add the following in the `<head>`:

`<link rel="stylesheet" href="/main.css">`

Create a file in the public folder called "main.css".

Add the following to that file:

`body{
    background-color: #222
}`

Restart your server, clear your cache on your browser, and you should see the background color applied to your index page.

You can go ahead and add some Javascript links too (remember, everything is linked from public/) and see that in action as well. 

Our 












        

