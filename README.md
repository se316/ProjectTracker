## ProjectTracker

Project Tracker is a locally hosted web tool built for assisting with project management.

## Description

Project Tracker is made up of 2 containers and launched with docker-compose. A flask web server handles user interactions and a mysql database stores user accounts, user settings as a json and created projects. Projects themselves can be broken up into Subtasks and Status Management is available at both levels with visual feedback like different colored icons for each status. 

The main purpose and benefit to using Project Tracker is to be able to answer with just a simple glance: 

- What am I doing? 
- What do I need to do to get this done? 
- Where did I leave off? 
- What do I need to do next? 

Each of these questions can involve a lot of reading, time and mental effort without having an effective means to track, and letting the tool do all the work in that regard allows you to focus all your mental energy on getting a given task done. 

## How to Install and Run ProjectTracker

To install project tracker you need to:

- download and install [git](https://git-scm.com/downloads).
- download and install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).
- download ProjectTracker by running ```git clone https://github.com/se316/ProjectTracker```.
- build the package the first time by running ```docker-compose build``` at the package's root directory.

To run Project Tracker:

- after building it the first time, run PT with ```docker-compose up```. Append the command with ```-d``` to run it in the background.
- once it's up and running, navigate to https://localhost in a browser to be taken to the login/register page.
- when you want to stop ProjectTracker, open a terminal in the project's root directory and run ```docker-compose stop```

## How to Use Project Tracker

When navigating to ProjectTracker for the first time, you'll need to create an account to login with. Using accounts makes it so multiple people on the local network can track their work separately. When logging in for the first time, a new project can be created using the New Project button in the top right corner. After creating and describing a project, you're able to go to its individual project page and create Subtasks for it in the Subtasks tab. On the individual subtask page, you're able to see the description in one tab and add comments in the other. Each subtask has a list of statuses they can be marked as, and when all subtasks are complete, the project can be marked as complete. There's nothing to stop you from changing the project status without marking all the subtasks as complete, how you use project tracker is up to you and a list of terms, statuses and references will be provided below. A final note on usage is all descriptions and comments can render markdown for greater organization.

## Terms and References

This section is meant to briefly discuss various aspects of the Project Tracker

|Level | What it's for
|:- |:-
| Project | Projects are functionally just tracking tickets. It's supposed to be the single entry point to all the work that revolves around getting that project done. Their descriptions are visible on the home page and a good project overview should help guide the project on a high level.
| Subtask | Subtasks always have a parent Project they come from. If Projects are considered what's being tracked on a high level, Subtasks would be the actual work that needs to be done for your Project. Keeping these well organized makes jumping in and out of a Project straight forward and helps break something big into small quick to work on pieces. 
| Comments | Comments can be left on the Subtask level. If an individual Subtask can be viewed as the task at hand, comments are the way you keep track of your work while working towards completion. If you're coming back to something, comments are a great way to see exactly what you've done so far and where you've left off at a glance. If you like leaving a note telling yourself what to do next, this makes it even easier to know what to do at a glance. 

**Statuses**: There are multiple statuses available that can be broken down into 3 categories: active, inactive, complete. A list of statuses and their usage is available below. "Projects" can be swapped out with "Subtasks" because their status management works the same way. 

**Active** - these are projects you are actively working on. 

|Status|Usage
|:-|:-
|In Progress| This is used for the project you are literally actively working on.
|Pending | You are working on the project, but have paused your work on it for whatever reason. It is going to be worked on after completing what's In Progress
|Review | You have finished working on the Project and are wrapping things up. Testing, code cleanup, and collecting final thoughts are done at this point before officially marking it as complete and moving on. 
|Researching | You are working on a Project but need to do more reading or experimentation before being able to proceed. 

**Inactive** - these are projects you have not started working on yet.

|Status|Usage
|:-|:-
| Not Started | These are projects you've created and plan on doing soon but have not been started. It is the default status for every created Project.
| Backlog | These are projects you want to keep on your radar and do at some point but they are low priority. 

**Complete** - these are the statuses used to close out your Project.

|Status|Usage
|:-|:-
|Complete | You have successfully completed the Project.
|Closed | You have willingly closed out the Project without completing the work. 
|Blocked | You are unable to complete the Project for reasons beyond your control. 

## Home Page Filters

After projects are created, the default behavior of the home page is to list all projects in order of status priority (active > inactive > complete) then last modified time. There are filter buttons that allow you to only see your active, inactive, complete or researching Projects, and there is a Home Page Filter preference that can be set in the Settings so whenever you navigate to the home page the specified filter will automatically be applied. 


## Profile Page

The profile page contains various information about your projects and subtasks. There are different features available on the profile page and they're summarized below:

* **Project Tree** - the project tree contains a breakdown of all your projects and their respective subtasks and statuses in a nested list format. Subtasks are nested within their projects.
* **Open Projects** - this section lists all of your open projects.
* **Open Subtasks** - this section lists all of your open subtasks.
* **Project/Subtask Stats** - a summary of projects, subtasks and their respective statuses.


## MySQL DB Credentials

MySQL and the App get their credentials from the MySQL container's environment file. To change the default username/passwords to the database, modify the file located at ```ProjectTracker/mysqldb/.env```.
