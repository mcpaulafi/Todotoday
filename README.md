# ToDo Today
### Repo: ToDo list for Today (thsoha)

ToDo Today is a simple task management application for small projects. ToDos (tasks) with a deadline are linked to a project and a ToDo is classified with a type. 

For example a student can use this application to follow on a daily basis, which ToDos, essays, reports, meetings, teamworks etc. are due today or tomorrow. From a simple view the student can see how the completing of different courses (= projects) is going. 

## Features
- Register a user account
- Login and logout with the account
- User can add/view/delete only his/hers projects, ToDos and ToDo types
- View of ToDo list: ToDos for Today / Tomorrow / All Open ToDos and filter ToDos per Type
- View project status: done/total ToDos per project

## Database
See in detail schema.sql

### Tables
- users
- projects
- project_users
- todos
- todo_types
- type_users

## How to use the app
1. Get project from github
2. On terminal start psql with command: psql
3. On psql create database: CREATE DATABASE todotoday
4. On terminal create tables to the database: psql -d todotoday < schema.sql
5. On psql write command: \connect todotoday 
6. On psql write command: \dt. The database should contain tables users, projects, project_users, todo_types, type_users and todos.
7. Go to the application directory /todotoday/
8. On terminal create .env file with the following contents: 
    - DATABASE_URL="postgresql:///todotoday"
    - SECRET_KEY='key'
        - _key = a random 16-character string enclosed within ''-marks_
9. On terminal create a virtual environment: python3 -m venv venv
10. On terminal start venv: source venv/bin/activate 
11. On terminal install dependencies: pip install -r requirements.txt
12. On terminal start the application with the command: flask run
13. Start a browser and go to url http://127.0.0.1:5000/ (or where Flask tells the app is running).
14. Begin using "ToDo today" application with registering a username. After login create some types first. Then you can create projects and add todos in them.
15. If you want to delete the database, on psql use command: DROP DATABASE todotoday;

## Status of the project: First version available

## Development log
- This project is made on "TKT20019 Tietokannat ja web-ohjelmointi" course in the University of Helsinki
- 6th Sep 2023 First draft of the plan
- 22nd Sep 2023 Second draft, most functionalities available
- 5th October 2023 Third draft, functionalities done, manage projects page to be redesigned
- 16th Oct 2023: finalising
- 21st Oct 2023: first version ready for grading

### Future development possibilities
- Add multiple users on a project (noted in the database design)
- Assigning a ToDo to another user in the project (noted in the current code)
- Copy a project with tasks to another user 
- Admin role

## Screenshots from 21.10.2023 version
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-10-21_login.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-10-21_register.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-10-21_todolist.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-10-21_projects.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-10-21_types.png">
