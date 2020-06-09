# Sluggo Usage
The following is a tutorial on how to use Sluggo.

## What is Sluggo?
Sluggo is a simple issue tracker aiming to bring the core features of issue trackers such as GitHub Issues, JIRA,
and Trello to smaller teams. Compared to these other issue trackers, however, Sluggo aims to be more flexible and also
much simpler to understand. 

### Basic Concepts
Sluggo revolves around several different items of interest, namely:
* Tickets
* Tags
* Users

These different items all play their own role.

### Tickets
Tickets are how you store different issues or tasks which need to be completed on your team. Each ticket is designed to
represent one unit of work, and can encompass multiple dependency subtasks. Tickets have the following properties:

* **Title** - name of the ticket
* **Tags** - associated categories of the ticket (described later)
* **Description** - description of the ticket's task
* **Due Date** - date when a ticket is due
* **Progress** - whether a ticket is not started, in progress, or complete
* **Assignee** - who is assigned to be in charge of the task (only one person is allowed to be in charge of any
given task; large tasks should be broken into subtasks)
* **Subticket** - tickets that are blocking the completion of the task, or are "under" the task. (e.g. a ticket could
denote a milestone, and its subtickets' completion mark the successful completion of the milestone)

New tickets default to "Not Started" and have no subtickets; these can be changed from the Ticket Details screen.

### Tags
Tags are how a user may group different tasks together in Sluggo. This is useful for categorizing different tasks to
different groups of members on a project.

For example, consider a robotics team. There may be a Mechanical team in charge of designing the robot in CAD and 
fabricating different pieces for the device. There may also be an Electronics team in charge of designing and ordering
relevant PCBs. Finally, there could be a Software team in charge of programming the robot. These fit neatly into the 
notion of tags - where different concerns can be grouped together.

Each tag is a simple string. Many tickets can be associated to a tag, and multiple tags can be associated to a ticket.

Tags can be created by anyone, but admins will need to approve a tag before it can be used in a ticket. More on tag 
addition and approval can be found below on the section on the Admin dashboard.

### Users
Finally, each team will have different members. These members are kept track of on Sluggo as users. These users can be
assigned to tasks, and each will have their own set of interests (tags), pinned tickets, etc.

You can manage Users from the Admin dashboard, which will be seen below on the sectio on the Admin dashboard.

## Getting Started
When you first start Sluggo, authenticate using py4web's authentication system. You will then see the following
screen:

TODO SCREENSHOT

This screen will appear for all new accounts added to Sluggo, and enables you to choose your interests from what's
in Sluggo. If you are an Admin, it will also enable you to create new interests. These interests are stored as
tags in the database.

## Homepage
TODO homepage screenshot

After creating your profile, you'll be redirected to the homepage, which acts as a summary of information relevant
to you. The homepage holds five different sections:

### Your Tickets
This shows currently active tickets that are assigned to you. You can click on a ticket to view its details.

### Recent Updates
This shows recent updates to tickets that are relevant to you, such as status changes, added comments, and more. You can
click to be taken to the relevant ticket.

### Pinned Tickets
This is a section where you can pin tickets of interest to you. You can click on any ticket to view its details.

To pin a ticket, go to any ticket's details and click the pin button. This will add the pinned ticket to your homepage,
and subscribe you to comments and status changes in the Recent Updates section.

### Your Tags
This is a section which contains your interest. Clicking on any tag will bring you to the Tickets screen filtered by
that tag.

You can modify your tags from your page in the Users tab, which will be described below.

## Tickets
TODO Tickets screenshot

The tickets screen shows you all of your tickets, sorted in order of oldest to newest. You can search for tickets using
the search box at the top of the screen.

To add a ticket, click the add ticket button at the top of the screen.

TODO ADD TICKET MODAL SCREENSHOT

Here, you can set some initial properties of the ticket. Click "Save Changes" to save the ticket. It will appear in
your Tickets list.

Clicking on the ticket will bring you to the details screen.

TODO ADD TICKET DETAILS SCREENSHOT

Here, you can modify various aspects of the ticket, such as its current status, description, due date, tags,
assignees, and subtickets. You can also leave comments on the ticket to discuss the ticket status with
others, or leave important information. If you are the creator of a ticket or an admin, you may also delete the ticket.

To modify the tags or description, you must click the "Edit" button on the ticket.

You can also add subtickets to act as subtasks or dependencies on a ticket. Subticket completion will be reflected in
the progress bar at the top of the ticket. To do this, click the "+" button under Subtickets. This will add a 
subticket

## Users
TODO USERS SCREENSHOT

To access your profile, and information about others on the team, click the "Users" tab on the top of the screen.
You will be taken to the Users screen.

Clicking on your profile, you can see and modify information about yourself, such as your name, project tags,
role, and bio. You can modify these by changing the fields, and clicking the "Update" button.

Your project tags on this page are synchronized with your homepage, so any tags you add here will be added to your
homepage under the "Your Tags" section. You are also able to suggest new tags here for an Admin to approve.

To modify your profile picture, click the "Change Profile Picture" button, and choose a picture from your system.
The picture must be less than 1MB.

You can also view other users' information, although you will not be able to modify the contents of their profile.

## Admin
TODO ADMIN PAGE DEFAULT SCREENSHOT

If you are an Admin, you will be able to use the Admin dashboard. The Admin dashboard gives you the ability to modify
various characteristics about your team.

Firstly, a user may approve tags. This can be seen under the Approve Tags screen:

If a non-Admin tries to add a custom tag through their user, it will show up in the Approve screen. An Admin may
approve the tag here.

Next is the Tags screen, shown here:

TODO TAGS PAGE SCREENSHOT

This page allows you to modify what tags are on your Sluggo instance, including renaming or deleting them, as well
as modifying their approval status.

Next is the Members approval screen, shown here:

TODO APPROVE A MEMBER SCREENSHOT

New members will need to be approved before they can begin using Sluggo. Simply click the Approve button in order to
approve the member onto the team.

Finally, the team's bios can be exported, shown here:

TODO EXPORT BIOS SCREEN

This will export a screen of bios, shown here:

TODO BIOS EXPORT EXAMPLE

This is useful for exporting information to an external webpage about your team. The items stored on this page are
independent of the Sluggo instance and thus do not require Sluggo to be running in order to access the export.

