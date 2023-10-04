# Application ToDo Today is made by Paula Meuronen 2023 for Helsinki University course TKT20019
# todos.py: database queries

from db import db
from sqlalchemy.sql import text
from datetime import datetime, timedelta
import users

# TODO lisää visible atribuutti kaikkiin


# ToDos
# ##############################################################################

def get_list(time):
    # Query of ToDos assigned_to user (atm same as creator)  
    user_id = users.user_id()
    today = datetime.now()
    tomorrow = today + timedelta(1)

    get_time = today.strftime("%Y-%m-%d")
 
    if time=="today":
        get_time = today.strftime("%Y-%m-%d")
    if time=="tomorrow":
        get_time = tomorrow.strftime("%Y-%m-%d")

    # Select for today or tomorrow
    sql = "SELECT T.deadline_date, P.project_name, TT.type_name, T.todo_description, T.done_date, T.todo_id FROM todos T LEFT JOIN projects P ON T.project_id=P.project_id LEFT JOIN todo_types TT ON T.type_id=TT.type_id  WHERE T.assigned_id=:user_id AND T.visible=TRUE AND T.deadline_date=:deadline AND T.done_date IS NULL"
    result = db.session.execute(text(sql), {"user_id":user_id, "deadline":get_time})
 
    if time=="all":
        sql = "SELECT T.deadline_date, P.project_name, TT.type_name, T.todo_description, T.done_date, T.todo_id FROM todos T LEFT JOIN projects P ON T.project_id=P.project_id LEFT JOIN todo_types TT ON T.type_id=TT.type_id  WHERE T.assigned_id=:user_id AND T.done_date IS NULL AND T.visible=TRUE ORDER BY T.deadline_date"
        result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()

def add_todo(todo_description, project_id, type_id, deadline_date):
    user_id = users.user_id()
    # ToDo is assigned to creator
    try:
        sql = "INSERT INTO todos (project_id, type_id, todo_description, deadline_date, assigned_id, created_by, create_date) VALUES (:project_id, :type_id, :todo_description, :deadline_date, :assigned_id, :created_by, NOW())"
        db.session.execute(text(sql), {"project_id":project_id, "type_id":type_id, "todo_description":todo_description, "deadline_date":deadline_date, "assigned_id":user_id, "created_by":user_id})
        db.session.commit()
    except:
        return False
    return True

def delete_todo(todo_id):
    # ToDo can be deleted by created_by user 
    created_by = users.user_id()
    try:
        sql = "DELETE FROM todos WHERE todo_id=:todo_id AND created_by=:created_by"
        db.session.execute(text(sql), {"todo_id":todo_id, "created_by":created_by})
        db.session.commit()
    except:
        return False
    return True

def mark_done(todo_id):
    # ToDo can be marked done by assigned_user 
    user_id = users.user_id()
    try:
        sql = "UPDATE todos SET done_date=NOW() WHERE todo_id=:todo_id AND assigned_id=:user_id"
        db.session.execute(text(sql), {"todo_id":todo_id, "assigned_id":user_id})
        db.session.commit()
    except:
        return False
    return True

# Projects
# ##############################################################################

def get_projects():
    # Get projects on which user is listed
    user_id = users.user_id()
    try:
        sql = "SELECT p1.project_id, p1.project_name, (SELECT COUNT(*) FROM todos t2 WHERE t2.done_date IS NOT NULL AND t2.visible=TRUE AND p1.project_id=t2.project_id AND t2.assigned_id=:user_id), COUNT(t1.todo_id) FROM project_users pu, projects p1  LEFT JOIN todos t1 ON p1.project_id=t1.project_id AND t1.visible=TRUE WHERE p1.project_id=pu.project_id AND pu.user_id=:user_id GROUP BY p1.project_id ORDER BY p1.project_name"
        result = db.session.execute(text(sql), {"user_id":user_id})
        return result.fetchall()
    except:
        return False

def get_project_todos():
    # Get projects on which user is listed and its ToDos there user is the assigned_user
    user_id = users.user_id()
    try:
        sql = "SELECT p1.project_id, p1.project_name, t1.todo_id, t1.deadline_date, tt.type_name, t1.todo_description, t1.done_date FROM projects p1, project_users pu, todos t1 LEFT JOIN todo_types tt ON tt.type_id=t1.type_id WHERE p1.project_id=pu.project_id AND p1.project_id=t1.project_id AND pu.user_id=:user_id AND t1.assigned_user=:user_id ORDER BY p1.project_name, t1.deadline_date"
        result = db.session.execute(text(sql), {"user_id":user_id, "assigned_user":user_id})
        return result.fetchall()
    except:
        return False

def add_project(project_name):
    # TODO add deadline date
    # Add user also on project_users
    created_by = users.user_id()
    try:
        sql = "INSERT INTO projects (project_name, created_by, create_date) VALUES (:project_name, :created_by, NOW()) RETURNING project_id"
        result = db.session.execute(text(sql), {"project_name":project_name, "created_by":created_by})
        project_id = result.fetchone()[0]
        sql2 = "INSERT INTO project_users (project_id, user_id) VALUES (:project_id, :user_id)"
        db.session.execute(text(sql2), {"project_id":project_id, "user_id":created_by})
        db.session.commit()
    except:
        return False
    return True

# Types
# ##############################################################################

def get_types():
    user_id = users.user_id()
    try:
        sql = "SELECT t1.type_id, t1.type_name FROM todo_types t1 WHERE t1.visible = TRUE AND t1.created_by=:user_id ORDER BY t1.type_name"
        result = db.session.execute(text(sql), {"user_id":user_id})
        return result.fetchall()
    except:
        return False
    
def add_type(type_name):
    created_by = users.user_id()
    try:
        sql = "INSERT INTO todo_types (type_name, created_by) VALUES (:type_name, :created_by)"
        result = db.session.execute(text(sql), {"type_name":type_name, "created_by":created_by})
        type_id = result.fetchone()[0]
        sql2 = "INSERT INTO type_users (type_id, user_id) VALUES (:type_id, :user_id)"
        db.session.execute(text(sql2), {"project_id":type_id, "user_id":created_by})
        db.session.commit()
    except:
        return False
    return True

def delete_type(type_id):
    # Creator can delete
    created_by = users.user_id()
    try:
        sql = "DELETE FROM todo_types WHERE type_id=:type_id AND created_by=:created_by"
        db.session.execute(text(sql), {"type_id":type_id, "created_by":created_by})
        db.session.commit()
    except:
        return False
    return True
