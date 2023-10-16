# ToDo Today
### Repo: ToDo list for Today (thsoha)

ToDo Today is a simple task management application for small projects. ToDos (tasks) with a deadline are linked to a project and a ToDo is classified with a type. 

For example a student can use this application to follow on a daily basis, which tasks, essays, reports, meetings, teamworks etc. are due today or tomorrow. From a simple view the student can see how the completing of different courses (= projects) is going. 

## Features
- Register a user account
- Login and logout with the account
- User can add/view/delete only his/hers projects, tasks and task types
- View of ToDos: "ToDos for Today", "ToDos for Tomorrow", "All Open ToDos" 
- View project status: done/total ToDos per project

## Screenshots from 23.9.2023 version
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_login2.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_registration2.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_todolist2.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_projects2.png">
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_types2.png">

## Database
See in detail schema.sql

Tables
- users
- projects
- project_users
- todos
- todo_types
- type_users

## How to use the app
1. Get project from github
2. Go to the application directory /todotoday/
3. On terminal create .env file with the following contents: 
    - DATABASE_URL="postgresql:///todotoday"
    - SECRET_KEY='key'
        - _key = a random 16-character string enclosed within ‘’-marks_
4. On terminal start venv (create a virtual environment): source venv/bin/activate 
5. On terminal install dependencies: pip install -r requirements.txt
6. On terminal start psql with command: psql
7. On psql create database: CREATE DATABASE todotoday
8. On terminal create tables to the database: psql -d todotoday < schema.sql
9. On psql write command: \connect todotoday 
10. On psql write command: \dt. The database should contain tables users, projects, project_users, todo_types, type_users and todos.
11. On terminal start the application with the command: flask run
12. Start a browser and go to url http://127.0.0.1:5000/ (or where Flask tells the app is running).
13. Begin using "ToDo today" application with registering a username. After login create some types first. Then you can create projects and add todos in them.
14. If you want to delete the database, on psql use command: DROP DATABASE todotoday;

## Status of the project: Development phase 
- [x] Database  
- [x] Login and logout with the account
- [x] User can add projects, todos and types
- [x] User can view projects, todos and types
- [x] User can delete projects, todos and types
- [x] Page: ToDo list: "ToDos for Today", "ToDos for Tomorrow", "All Open ToDos" 
- [x] Page: Manage projects, major usability issues:
    - [x] after POST-action, can error messages be shown next to where it occured?
    - [x] re-design layout: selection of projects, show only one project data at the time
    - [x] Add Done-button to here also 
- [x] Page: Manage types (add/delete)
- [x] Layout, minor issues:
    - [x] Page tab: User login, change to the right, so ToDo list is first tab on right
    - [ ] Set more precisely location of Submit-buttons 
- [ ] Evaluations on posted data from forms, some to be added:
    - [x] decline dates in the past
    - [ ] more issues commented on the code
- [x] CSRF vulnerability check
- [ ] Error handling clean up
- [ ] From issue report, find&fix: ToDo listan tomorrow-osion "No todos tomorrow!"-teksti kasautuu oudosti 

## Development log
- This project is made on "TKT20019 Tietokannat ja web-ohjelmointi" course in the University of Helsinki
- 6th Sep 2023 First draft of the plan
- 22nd Sep 2023 Second draft, most functionalities available
- 5th October 2023 Third draft, functionalities done, manage projects page to be redesigned
- 16th Oct 2023: finalising

### Future development / if there is time
- Sort with types
- Add multiple users on a project (noted in the database design)
- Assigning a ToDo to another user in the project (noted in the current code)
- Copy a project with tasks to another user 