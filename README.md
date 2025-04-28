# HMCTS-Coding-Challenge

This is a small application that can be used to manage casework as tasks.
It is currently only set up so that it will work locally.
It has only been tested using a Mac, so usage in Windows or Linux may be buggy.

This application allows the creation of task tickets.
Each ticket will contain a unique ID, a title, a status (unstarted, in progress and completed) and a deadline (YYYY-MM-DD).
They may also include a description of the ticket.
Once a ticket has been created, the ticket can be viewed, updated and deleted using its unique ID.
All existing tickets can be viewed in a table format, showing the task's ID, title and deadline.
This table format does not currently allow filtering or sorting, though these may be added in future releases.

To set your mahine up to use this application, a few things need to be done:

- Ensure that you have Postgresql installed

- To set up the database, open this folder in a terminal and run ```./databaseCreation.sh```.

- Ensure you have a version of Python 3 installed

- To ensure the necessary Python modules are installed, open this folder in a terminal and run ```./PythonImports.sh```.

Once the above two commands have been run, then open this folder in a terminal and run ```python3 taskmanager.py``` to open the GUI window.
