CS419 - Faculty Scheduling Tool
=====

Developer Enviornment: Please see the following How-To guide for setting up the project's intergrated development enviornment. https://www.evernote.com/shard/s292/sh/342bbe6c-6d54-4860-bee3-42a7dcdd73e5/2ee1ca0f0925f62bfe1029ac5c3a8bb2

HOW TO...

Start the app and populate the database for the first time:

Step 1: open pycharm and click the "terminal" tab at the base of the program window Step 2: navigate to project folder and look for the "manage.py" script inside the kalandar root folder. Step 3: type the following command without the quotes "rm db.sqlite3" Step 4: type "python manage.py syncdb" Step 5: follow the instructions to setup an admin account to log into the admin console of our app Step 6: type "python manage.py populate_db" Step 7: start the application and navigate to http://127.0.0.1/admin Step 8: login using the account you created in step 5 Step 9: once logged into, click the Facultys admin page to view all added Faculty Objects
