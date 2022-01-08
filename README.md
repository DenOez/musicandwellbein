# musicandwellbeing
This project was done during my bachelor thesis. It's a web application that is collecting information of Spotify users with the help of the Spotify API. The aim of this project was to investigate the correlaction between music listening habits of Spotify users and their personal well-being. For that I designed a survey to messure the personal well-being of the participants. Then I analyzed the correlation between the results of the survey and the data that were collected by the web application. 

Here is the instruction, how to use the web-application:

**Step 1: Spotify credentials**

To work with the Spotify API first of all you need a Spotify account. When you already have one, go to the Dashboad page on Spotify Developers website and log in. Create an application and enter a name and description for your application. Then copy your Client ID and your Client Secret Key and store it on your computer.
If you want to run the application also on your local machine, you should enter a local redirect URL in the Spotify settings: 

https://localhost:8888/callback

**Step 2: Software installation**

As our application is written in Python you should download and install a new Python version on your computer. To run our web-application we recommend PyCharm as IDE, but if you prefer another IDE you can also use that one. Git is also required and helps you with version control. Download, install and create a Git account from Git’s website. In this tutorial we will deploy the application on the Heroku web server. Therefore, create an Heroku account and install the Heroku Command Line Interface (CLI) from Heroku’s website. Once installed, you can use the Heroku command from your command shell. Use the “heroku login” command to log in to the Heroku CLI. This command opens your web browser to Heroku login page. If your browser is already logged in to Heroku, simply click the log in button that is displayed on the page. Finally download and install PostgreSQL to manage your databases later. During the installation you will be asked for a listening port. Enter here port 1080, if you want to run the application locally on this port.

Links:

https://www.python.org/downloads

https://www.jetbrains.com/pycharm/

https://git-scm.com/downloads

https://devcenter.heroku.com/articles/getting-started-with-python#set-up

https://www.postgresql.org/download

**Step 3: Preparing environment**

Before you can deploy the web application to Heroku, you need to prepare the environment. For that, create a new project folder for your application and **copy all files of this application** in this folder. Then install a virtual environment with some libraries. Declare the process type and the starting point of your application in a Procfile. After installing all libraries save the dependencies in a requirements.txt file:

$ cd project-folder\
$ py -m venv venv\
$ venv\Scripts\activate\
$ pip install flask\
$ set Flask_APP=app\
$ pip install gunicorn\
$ echo web: gunicorn app:app > Procfile\
$ pip install SQLAlchemy\
$ pip install Flask_SQLAlchemy\
$ pip install flask-Bootstrap\
$ pip install psycopg2\
& pip install requests\
$ python -m pip install PyMySQL\
$ pip freeze > requirements.txt

**Step 4: Deploy the frontend to Heroku**

To deploy the frontend web-application to Heroku you need to set your Git user name and email address. This is important because every Git commit uses this information. If you already own a Git user account, you can skip the first and second step. Then initialize a Git repository and log in to the Heroku CLI. Create an Heroku app with a specify name for your application. If you don’t enter a name, Heroku generates a random name for your app. In our case we named our Heroku app “musicandwellbeing2021”. Then deploy your code to the server and open the website with the last command:

($ git config –global user.name “John Doe”)\
($ git config –global user.email johndoe@example.com)\
$ git init\
$ git commit\
$ heroku login\
$ heroku create musicandwellbeing2021\
$ heroku git:remote -a musicandwellbeing2021\
$ git add .\
$ git commit -am “first deploy”\
$ git push heroku master\
$ heroku ps:scale web=1\
$ heroku open

**Step 5: Create and connect app with database**

There are two options to store data from your application in a database. First one is on your local machine and the second one is on a cloud-based database. Both options can be managed by the PostgreSQL GUI. In this tutorial we will show you how to use the PostgreSQL GUI to work with the cloud-based database. The standard convention to connect a SQLAlchemy database in your Flask-App looks like this:

    dialect://username:password@host:port/database

To create a PostgreSQL database enter these commands in your CLI:

$ heroku login\
$ heroku addons:create heroku-postgresql:hobby-dev

You can view your existing databases with:

$ heroku addons

The addons command also shows you in violet the name of your created database. Copy and save this for the next command. The credentials and location of your new database you can view with:

$ heroku pg:credentials:url NAME_OF_DATABASE

NAME_OF_DATABASE is the name of database you have just created. This command will give you all information you need to enter in the pgAdmin GUI. Copy and insert the whole last line in your Python app.py script (line 26). Notice that you need to edit the dialect name of your database. It should look like this “postgresql”.\
(Complete documentation: https://devcenter.heroku.com/articles/heroku-postgresql)

**Work with Heroku database:**

The pgAdmin GUI allows you to interact with the PostreSQL database server. Launch the pgAdmin application from Windows start menu.

![alt text](https://github.com/DenOez/musicandwellbeing/blob/b0b91533ac012b92be4cc898ad7d7ca4bef25c57/instruction1.jpg)

Then right-click the Servers node and select **Create > Server…** to create a server.

![alt text](https://github.com/DenOez/musicandwellbeing/blob/b0b91533ac012b92be4cc898ad7d7ca4bef25c57/instruction2.jpg)

Then enter a name for your server, host name/address, port, maintenance database, username, password and click the **Save** button:

![alt text](https://github.com/DenOez/musicandwellbeing/blob/b0b91533ac012b92be4cc898ad7d7ca4bef25c57/instruction3.jpg)

Now your database should be listed in your pgAdmin GUI on the left side. You can find your tables by clicking on **NAME_OF_DATABASE > database > Schemas > Tables**. After clicking on **Databases** we recommend to search for your Heroku database with **Strg + F** key combination. To view a table right-click the table and select **View/Edit Data > All Rows**. You can delete a table with **Delete/Drop** and with **Truncate** only the table content will be deleted.

But by default there should be no tables available. To create a tables follow the instructions in step 6.

(Complete documentation: https://www.postgresqltutorial.com/connect-to-postgresql-database)

**Step 6: Create tables**

Now your database is connected with your application and you can access to your database via pgAdmin GUI. You can create the tables user and playlist_favorite_tracks with these commands:

$ cd project-folder\
$ py -m venv venv\
$ venv\Scripts\activate\
$ python\
$ from app import db\
$ db.create_all()\
$ exit()

**Step 7: Edit Python and HTML scrips**

Then you need to edit some parts in your Python and HTML scripts. The Redirect URIs and your Spotify credentials you can change with:

1. By heroku open command you can run your web-application. Copy the URL for the next step.\
2. Open the templates folder in your IDE and open the login.html script. You need to edit the personal Client ID and redirect URI in line 43. Before you change the redirect URI you need to encode it with any online URL to URI encoder. The value of this parameter must match with the value of the redirect_uri parameter your app supplied when requesting the authorization code.

The URI we used in the login.html page looks like this:
    
    https%3A%2F%2Fmusicandwellbeing2021.herokuapp.com%2Fcallback
    
Then go to **Edit Settings** in your Spotify application settings and enter the redirect URL of your application and don’t forget to save the settings.

The URL we used in Spotify settings looks like this:

    https://musicandwellbeing2021.herokuapp.com/callback
  
3. Open the callback.html script in the templates folder. Enter the URL (in line 43) of the website you want the website visitor redirect to, after he clicks on the last button in your web-application.

4. Open the exchange_auth.py script and change first the redirect_uri in line 28. Then enter in line 33 and 68 your spotify credentials. This line must have the format:
Authorization: Basic *<base64 encoded client_id:client_secret>*
  
**Step 8: Last Steps**
    
Now you just need to push your code to the Heroku with:
  
$ cd project-folder\
$ py -m venv venv\
$ venv\Scripts\activate\
$ git add .\
$ git commit -m “push to heroku”\
$ git push heroku master
  
  
Finally run the backend application (that is exchanging the authorization code with an access and refresh token) locally on your machine. For that, open your IDE and run the exchange_auth.py script.
