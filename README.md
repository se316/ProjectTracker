## ProjectTracker

Project Tracker is a locally hosted web tool built for assisting with project management.

## Description

Project Tracker is made up of 3 containers and launched with docker-compose. 

1. A flask web server handles user interactions and is where you'll be doing the project work.
1. A CA server generates the certificates required for a secure connection.
1. A mysql database stores user accounts, user settings as a json and created projects. 

Projects themselves can be broken up into Subtasks and Status Management is available at both levels with visual feedback like different colored icons for each status. Users are able to comment on their Subtasks.

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
- for a proper https connection, refer to section "*How to enable proper HTTPS in Project Tracker*".

## How to Use Project Tracker

When navigating to ProjectTracker for the first time, you'll need to create an account to login with. Using accounts makes it so multiple people on the local network can track their work separately. 

When logging in for the first time, a new project can be created using the New Project button in the top right corner. 

After creating and describing a project, you're able to go to its individual project page and create Subtasks for it in the Subtasks tab. 

On the individual subtask page, you're able to see the description in one tab and add comments in the other. 

Each subtask has a list of statuses they can be marked as, and when all subtasks are complete, the project can be marked as complete. 

There's nothing to stop you from changing the project status without marking all the subtasks as complete, how you use project tracker is up to you and a list of terms, statuses and references will be provided starting from the "*Terms and References*" section. A final note on basic usage is all descriptions and comments can [render markdown for greater organization](https://gist.github.com/jonschlinkert/5854601).

## How to enable proper HTTPS in Project Tracker

To avoid the browser warning shown when accessing Project Tracker, login and go to your Settings. The CA's certificate will be available for download in the Certificate setting. Once downloaded, apply the following workflows for installation. Once installed and the exception's been removed, the browser will trust ProjectTracker to handle secure connections.

How to add the CA certificate in Firefox:
1. Open the options menu in the top-right corner of your browser window, open Settings.
1. Select "Privacy & Security".
1. Scroll down to "Certificates" and select "View Certificates".
1. Click the "Authorities" tab and select "Import". Select and open the downloaded certificate.
1. Click the "Servers" tab and remove the exception made for the site. (e.g. localhost if it's running on your computer)

How to add the CA certificate in Chromium-based browsers:
1. Open the options menu in the top-right corner of your browser window, open Settings.
1. Select "Privacy & Security", then select "Security".
1. Scroll to the bottom and click "Manage certificates".
1. Select the "Trusted Root Certification Authorities" tab, then select "Import".
1. Select and open the downloaded certificate, be sure All filetypes are showing.
1. Restart the browser to have the new certificate applied to your connection.

### Additional notes on secure access

By default, Project Tracker creates a valid secure connection when an end user connects to it via https://localhost or https://projecttracker.io. Localhost can be used on the same computer it's running on with no modifications; there are different ways to access it by "projectracker.io" or an IP address for the computer PT's running from listed below. 

- If you have access to a DNS server (applies to everyone's access in your network):
    - Have the DNS server point "projecttracker.io" at the IP Address it's running on.
    - This makes it so every DNS request for projecttracker is directed towards the right place and the certificate's requirements are valid.
- If you know the IP Address before building for the first time (applies to everyone's access by IP on your network from the server's side):
    - Uncomment the last line in caroot/conf/server.cnf and replace ```<IP Address Project Tracker's on>``` with the IP Address.
    - This makes it so if anyone visits "https://[yourip]", the connection will be valid because the IP Address is listed as a valid name in the certificate.
- If you don't have access to a DNS server and don't want to rebuild everything by retroactively doing the last step (applies to an end user's access by hostname from their own system):
    - Modify the hosts file on your computer with a new line that says "[Project Tracker's IP Address]    projecttracker.io"
    - This makes it so when you type "projecttracker.io" in the browser, it connects to project tracker's IP Address by the name set which is a valid name in the certificate. 
    - The hosts file on linux is located at: /etc/hosts
    - The hosts file on windows is located at: C:\Windows\System32\drivers\etc\hosts (must open as admin to save changes)
    - The hosts file on mac os is located at: /etc/hosts (must edit as root, [see how to enable root on mac os](https://kinsta.com/knowledgebase/edit-mac-hosts-file/#how-to-find-and-edit-your-mac-hosts-file-in-4-steps))

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
* **Last N Comments** - this section shows the last N amount of comments made with links to their subtasks. Number of comments can be changed in Settings and defaults to 10.
* **Project/Subtask Stats** - a table containing a summary of your work. See what statuses are assigned, how many are in those statuses and what share they represent as a percentage of all projects or subtasks respectively. 


## MySQL DB Credentials

MySQL and the App get their credentials from the MySQL container's environment file. To change the default username/passwords to the database, modify the file located at ```ProjectTracker/mysqldb/.env```.
