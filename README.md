# todo-api
A simple API for a "todo" app with user authentication.

This is a todo app API built using Flask(python framework), Postgresql as the database and Sqlalchemy as the ORM.

Features of the API:

1. User creation and login.

2. User can get to CREATE/RETRIEVE/UPDATE/DELETE the todo notes.

3. Basic security to the password is implemented using JWT tokens. Passwords are hashed with 'HS256' algorithm. (HMAC with SHA 256)

4. Tests are also written to check the endpoints.

**************************************************************************************************************
Environment while developing the API (developed inside a virtualenv):

- Mac OS High Sierra.
- python (v 2.7.10)
- package manager used: pip
- virtual environment for sandboxing and conflict-free development.
- all the other packages and requirements are specified in requirements.txt file.

**************************************************************************************************************

REQUIREMENTS AND SETUP TO RUN THE PROJECT:

1. Make sure you have 'pip' package manager installed on your computer.

2. If Postgres is not installed on your system, you can install it from the official link:

      https://www.postgresql.org/download/

3. A GUI tool to view the Postgres is psequel, which can be installed using this link:

      http://www.psequel.com/

4. Install POSTMAN to test endpoints and requests made to the API.

      https://www.getpostman.com/apps

5. Open up a terminal and install virtualenv:

      pip install virtualenv

6. Now, create your virtual environment inside a project folder:

      mkdir <project_folder>
      cd <project_folder>
      virtualenv <ENV>

7. Copy and paste the "todo_app" folder and ".env" file after unzipping the submitted assignment folder inside the <project_folder>.

8. The structure should now looks like this:

      - <project_folder>
          - <ENV>
          - todo_app
          - .env

9. In the <project_folder> , activate the virtual environment:

      source .env

10. Go inside the todo_app folder and install the dependencies.

      cd todo_app

      pip install -r requirements.txt

11. Make sure your postgres server is running on its default port (5432) and create two tables:

    1. CREATE TABLE TEST_DB;

    2. CREATE TABLE TODO_APP_API_DB;

12. Now, go back to the terminal, and after starting the virtualenv, its time to setup the tables and do the migrations.

    python manage.py db init

    python manage.py db migrate

    python manage.py db upgrade

    Now, you should see two tables called "todos" and "user" in your "todo_app_api_db" database.

    With the same state, continue to run the app as given below:

13. The .env file contains some setting which can be changed.

**************************************************************************************************************

TO RUN THE APP AND VERIFY THE RESULTS:

1.  With the postgres server running and the virtualenv activated, run the project using:

      python run.py

      This will run the project on port 5000.

2.  The project is designed to handle user registration and authentication.

**************************************************************************************************************
3.  Open up POSTMAN and register a user.

    url : http://localhost:5000/auth/register
    type: POST
    BODY PARAMETERS (email and password): If sending as a JSON, example is :

                      {
                      "email": "email_here",
                      "password": "password_here"
                      }

    If successful, you will receieve the message: "You have registered successfully. You may now login!"

**************************************************************************************************************

4.  Login as the user(almost the same request as "register" but a different URL):

    url : http://localhost:5000/auth/login
    type: POST
    BODY PARAMETERS (email and password): If sending as a JSON, example is :

                      {
                      "email": "email_here",
                      "password": "password_here"
                      }

    If successful, you will receive a JSON with an access token valid for 10 minutes and a message saying you logged in successfully.

**************************************************************************************************************

5.  To create a TODO note:

    url : http://localhost:5000/todos/
    type: POST

    headers: Authorization: Bearer <insert_access_token_here>

    BODY PARAMETERS (name (name of the note) and contents): If sending as a JSON, example is :

                      {
                      "name": "name of the todo note here",
                      "contents": "contents of the todo note here"
                      }

    You will be able to view the todo you created as a response.

**************************************************************************************************************

5. To get a TODO note / notes (descending order of date created):

    url : http://localhost:5000/todos/     --- > this gets all the TODOS for the particular user.
          http://localhost:5000/todos/<todo-id>  -- > if id is specified, it will fetch only the particular todo from the user.
    type: GET

    headers: Authorization: Bearer <insert_access_token_here>


    You will be able to view the todo as a response.

**************************************************************************************************************

6. To DELETE a todo note:

    url : http://localhost:5000/todos/<todo-id>    --- > this gets all the TODOS for the particular user.

    type: DELETE

    headers: Authorization: Bearer <insert_access_token_here>


    You will be able to view the deleted todo as a response.

**************************************************************************************************************

7. To MODIFY a todo note:


    url : http://localhost:5000/todos/

    type: PUT

    headers: Authorization: Bearer <insert_access_token_here>

    BODY PARAMETERS (name (name of the note) and contents): If sending as a JSON, example is :

                      {
                      "name": "name of the todo note here",
                      "contents": "contents of the todo note here"
                      }

    You will be able to view the todo you modified as a response.
**************************************************************************************************************



Testing the API:

There are also test cases to check for the endpoints:

1. To run all the tests together,

    python manage.py test


2. to check the user registration, login, and authentication test, go to manage.py and change line 19 to :

    tests = unittest.TestLoader().discover('./tests', pattern='test_auth.py')

3. To check the note creation tests, it will run , but will fail because they are authenticated endpoints.

    tests = unittest.TestLoader().discover('./tests', pattern='test_todo_app.py')


**************************************************************************************************************
