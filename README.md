## Overview

What was I doing? Where did I leave off? What do I need to do next? The Project Tracker was created to help answer these questions. When it comes to project work, answering each question can be a time and energy consuming task depending on the complexity of things. It's much better to have a tool one can use to have those questions answered for them at a glance, making it easier to step away from or jump back into any given project at any given time. 

## How does Project Tracker work? 

There are 3 levels to managing a given project in the Project Tracker:

| Level | Purpose
|:- |:-
| Project | The project level is a high level "What do I want to do" kind of document. It is used to distinctly separate projects that have their own different tasks that need to be completed and serve different purposes. 
| Subtask | Every project will have its own subtasks. If projects are the answer to "What do I want to do?", subtasks are the answer to "What do I need to do to get this done?". Typically, there are many different things to do or consider when working on a given project and subtasks help keep those to-do items organized. 
| Comments | When working through a subtask, one should help themselves by leaving comments of what they've done. Doing this allows one to easily step in and out of a particular project/subtask. When coming back, comments are the answer to "Where did I leave off?", and if you tell yourself what the next step should be it'll also be a fast way to see what needs to be done next. 

Using those 3 levels together helps keep things organized while reducing how much mental effort it takes to work through a project. To help assist with the state of things, Project Tracker also has a status management mechanism. Projects and Subtasks can be marked as one of five different statuses:

- Not Started
- Pending
- In Progress
- Review
- Complete

Each status has its own corresponding color and icon to make differentiating between things even easier. To get started with project tracker, go to ```https://<"localhost" or ip address it's running on>``` and it'll take you to the login/register page. Make yourself an account then you're ready to login and get started. 

## Is the data used in registration used or shared with anyone?

No, only a username and password are asked for on the registration page and their only purposes are to:

- Help you login to ProjectTracker.
- Separate your project work from anyone elses (if you wanted to share it as a resource on your network).
- Give you a user id that is used to grab just your work from the database.

## Installation

In order to install this you'll need to make sure you have [Docker](https://docs.docker.com/get-docker/) and [Git](https://git-scm.com/downloads) installed as a prerequisite. If those are installed, then this package can be downloaded via

```
git clone https://github.com/se316/ProjectTracker.git
```

## Starting the App

After cloning the package onto your host, cd into the project's root directory "ProjectTracker" and use the following to start the servers

```
# do this once so it's faster to start in the future
docker-compose --build

# this is how to start the app, add " -d" to run it in the background
docker-compose up

# these are two ways to stop the app, you can also Ctrl+C if you only have one terminal open
docker-compose stop
docker-compose down
```

Once you see that the web server is listening on port 443, in a browser go to ```https://localhost``` to be taken to the ProjectTracker's home page. The current version uses a self signed cert, so accept the risk and continue to the site. This will be replaced with a trusted certificate in a future update.

## What are the different servers launched in this package? 

There are two nodes that get launched. One is a mysql server that will host the database required to make everything work, the second contains the web server you'll be logging into and interacting with. 
