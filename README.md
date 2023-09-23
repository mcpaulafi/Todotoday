# ToDo Today
### Repo: ToDo list for Today (thsoha)

ToDo Today is a simple task management application for small projects. ToDos (tasks) with a deadline are linked to a project and a ToDo is classified with a type. 

For example a student can use this application to follow on a daily basis, which tasks, essays, reports, meetings, teamworks etc. are due today or tomorrow. From a simple view the student can see how the completing of different courses (= projects) is going. 

## Features
- Create a user account
- Login and logout with the account
- User can view/edit/delete only his/hers projects, tasks and task types
- View of ToDos: "ToDos for Today", "ToDos for Tomorrow", "Late ToDos" 
- View of status: done/total ToDos per project

## Screenshots 
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_login.png" border=1>
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_registration.png" border=1>
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_todolist.png" border=1>
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_projects.png" border=1>
<img src="https://github.com/mcpaulafi/Todotoday/blob/main/Drafts/2023-09-23_types.png" border=1>

## Database
See schema.sql

## Status of the project: Development phase
- Database ready, visible atribute not yet placed everywhere in SQL inquiries
- User interphase: plan did not fully work in practise, not intuitive and smooth enough, requires development especially on Management-page 
- Python code: missing a lot of checking on data from forms, and if the user has enough permissions  
- Python code: overall requires more compacting and tidying
- User Account: missing check for same usernames on registration
- User Account: logged in name comes from session, replace with inquiry from db
- Index -page: login serves as a "frontpage", needs to be rethinked if it is fine or not
- ToDo list -page: OK 
- Status -page: add status-info to the Manage projects -page and delete this page
- Manage projects -page: make Add new-sections visually different from other content
- Manage projects - page: after POST-action, can error messages be shown next to that project
- Manage projects - page: re-design usability: can there be quick links to project names or filter or some search? 
- Manage projects - should a project have a deadline too, should it pe possible to view also todos description
- Manage projects -page: move Types management to another page
- Type management -page: create this new page and move functionalities for this from Manage projects-page  

## Development log
- This project is made on "TKT20019 Tietokannat ja web-ohjelmointi" course in the University of Helsinki
- 6th Sep 2023 First draft of the plan
- 22nd Sep 2023 Second draft, most functionalities available

### Future development / if there is time
- Add multiple users on a project
- Assigning a ToDo to another user in the project
- Copy a project with tasks to another user