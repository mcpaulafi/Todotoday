# ToDo Today
### Repo: ToDo list for Today (thsoha)

ToDo Today is a simple task management application for small one user projects. ToDos (tasks) with a deadline are linked to a project and a ToDo is classified with a type. 

For example a student can use this application to follow on a daily basis, which tasks, essays, reports, meetings, teamworks etc. are due today or tomorrow. From a simple view the student can see how completing of different courses (= projects) is going. 

## Features
- Create a user account
- Login and logout with the account
- User can view/edit/delete only his/hers projects, tasks and task types
- View of ToDos: "ToDos for Today", "Late ToDos", "ToDos for Tomorrow" 
- View of all projects and their status: done/total ToDos
  
## Database

### User
- User_id INTEGER PRIMARY KEY
- Name VARCHAR(255)
- Password VARCHAR(255)
- Create_date DATETIME

### Project
- Project_id INTEGER PRIMARY KEY
- Name VARCHAR(255)
- Created_by INTEGER -- user_id
- Create_date DATETIME
- Deadline_date DATETIME

### Project_users
- Project_id INTEGER 
- User_id INTEGER

### Task
- Task_id INTEGER PRIMARY KEY
- Project_id INTEGER
- Assigned_id INTEGER -- user_id
- Type_id INTEGER 
- Name VARCHAR(255)
- Create_date DATETIME
- Created_by INTEGER -- user_id
- Deadline_date DATETIME
- Done_date DATETIME -- if null open
  
### Task_types
- Type_id INTEGER PRIMARY KEY
- Name VARCHAR(255)
- Created_by INTEGER -- user_id


## Implementation Plan / development log
- This project is made on "TKT20019 Tietokannat ja web-ohjelmointi" course in the University of Helsinki
- 6th Sep 2023 First draft of the plan
- Keeping it simple so editing is mostly create/delete
  
### Future development / if there is time
- Add multiple users on a project
- Assigning a ToDo to another user in the project
- Copy a project with tasks to another user
