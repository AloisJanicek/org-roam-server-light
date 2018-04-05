#Creating a Python3 Webserver From The Ground Up

Jumping into Python when your previous experience is mostly in web-based languages (PHP, Javascript, Ruby) can be a daunting task. Python has all of the tools available to make a strong HTTP Server or framework, as well as plenty of mature web frameworks to get started with, but the purpose of this tutorial/write-up isn't to show you how to leverage those, but how to build one from the ground up (similarly to how you'd start learning with NodeJS).

Throughout this tutorial, we'll go through a few different steps, the first of which is included today:
- Step 1) Setting up a basic HTTP server that will do the following:
    - Respond to requests at the appropriate HTTP method,
    - Allow you to respond to those requests and serve the following types of files:
        - HTML
        - CSS
        - Javascript
        - Images (PNG/JPG)
    - Display basic (static) HTML files that can import their own resources
    - Define routes to match to the appropriate HTML files you wish to import
- Step 2) Allow our routes to take parameters, and respond in-kind with the appropriate data and set up API routes
- Step 3) Add a view rendering library and incorporate a database into our application

The full source code is available on Git, with the appropriate versions tagged. Today's version is tagged as "basic-webserver."

Let's dive right in.

## Step 1 - Create the Basic Webserver