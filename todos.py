"""todos.py: database queries"""
# Application ToDo Today is made by Paula Meuronen 2023
# for Helsinki University course TKT20019

from datetime import datetime, timedelta
from sqlalchemy.sql import text
from db import db
import users

# ToDos
def get_list(time1):
    """Query of ToDos assigned_to user (atm same as creator)"""
    user_id = users.user_id()
    today = datetime.now()
    tomorrow = today + timedelta(1)

    get_time = today.strftime("%Y-%m-%d")

    if time1=="today":
        get_time = today.strftime("%Y-%m-%d")
    if time1=="tomorrow":
        get_time = tomorrow.strftime("%Y-%m-%d")

    # Select for today or tomorrow
    sql = "SELECT T.deadline_date, P.project_name, TT.type_name, T.todo_description, \
    T.done_date, T.todo_id FROM todos T LEFT JOIN projects P ON T.project_id=P.project_id \
    LEFT JOIN todo_types TT ON T.type_id=TT.type_id  WHERE T.assigned_id=:user_id AND \
    T.visible=TRUE AND T.deadline_date=:deadline AND T.done_date IS NULL"
    result = db.session.execute(text(sql), {"user_id":user_id, "deadline":get_time})

    if time1=="all":
        sql = "SELECT T.deadline_date, P.project_name, TT.type_name, T.todo_description, \
        T.done_date, T.todo_id FROM todos T LEFT JOIN projects P ON T.project_id=P.project_id \
            LEFT JOIN todo_types TT ON T.type_id=TT.type_id  WHERE T.assigned_id=:user_id AND \
            T.done_date IS NULL AND T.visible=TRUE ORDER BY T.deadline_date"
        result = db.session.execute(text(sql), {"user_id":user_id})

    return result.fetchall()

def get_list_type(type_id):
    """Query of ToDos assigned_to user (atm same as creator) filter type"""
    user_id = users.user_id()
    if type_id != "all":
        sql = "SELECT T.deadline_date, P.project_name, TT.type_name, T.todo_description, \
            T.done_date, T.todo_id FROM todos T LEFT JOIN projects P ON T.project_id=P.project_id \
                LEFT JOIN todo_types TT ON T.type_id=TT.type_id  WHERE T.assigned_id=:user_id AND \
                T.done_date IS NULL AND T.visible=TRUE AND T.type_id=:type_id ORDER BY T.deadline_date"
        result = db.session.execute(text(sql), {"user_id":user_id, "type_id":type_id})
    else:
        sql = "SELECT T.deadline_date, P.project_name, TT.type_name, T.todo_description, \
        T.done_date, T.todo_id FROM todos T LEFT JOIN projects P ON T.project_id=P.project_id \
            LEFT JOIN todo_types TT ON T.type_id=TT.type_id  WHERE T.assigned_id=:user_id AND \
            T.done_date IS NULL AND T.visible=TRUE ORDER BY T.deadline_date"
        result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()

def add_todo(todo_description, project_id, type_id, deadline_date):
    """Adding ToDo and it is assigned to creator"""
    user_id = users.user_id()
    try:
        sql = "INSERT INTO todos (project_id, type_id, todo_description, deadline_date, \
            assigned_id, created_by, create_date) VALUES (:project_id, :type_id, \
            :todo_description, :deadline_date, :assigned_id, :created_by, NOW())"
        db.session.execute(text(sql), {"project_id":project_id, "type_id":type_id, \
                                       "todo_description":todo_description, \
                                        "deadline_date":deadline_date, \
                                        "assigned_id":user_id, "created_by":user_id})
        db.session.commit()
    except Exception:
        return False
    return True

def delete_todo(todo_id):
    """ToDo can be deleted by created_by user"""
    created_by = users.user_id()
    try:
        sql = "DELETE FROM todos WHERE todo_id=:todo_id AND created_by=:created_by"
        db.session.execute(text(sql), {"todo_id":todo_id, "created_by":created_by})
        db.session.commit()
    except Exception:
        return False
    return True

def mark_done(todo_id):
    """"ToDo can be marked done by assigned_user"""
    user_id = users.user_id()
    try:
        sql = "UPDATE todos SET done_date=NOW() WHERE todo_id=:todo_id AND assigned_id=:assigned_id"
        db.session.execute(text(sql), {"todo_id":todo_id, "assigned_id":user_id})
        db.session.commit()
    except Exception:
#        print (e)
        return False
    return True

# Projects

def check_project_name(project_name):
    """Is the new name already registered?"""
    created_by = users.user_id()
    sql = "SELECT project_name FROM projects WHERE project_name=:project_name AND created_by=:created_by AND visible=TRUE"
    result = db.session.execute(text(sql), {"project_name":project_name, "created_by":created_by})
    project_name_sql = result.fetchone()
    if project_name_sql:
        return True
    return False

def get_latest_project_id():
    """Get the project which user created latest"""
    user_id = users.user_id()
    try:
        sql = "SELECT p1.project_id FROM projects p1 WHERE p1.created_by=:user_id \
            ORDER BY p1.create_date DESC LIMIT 1"
        result = db.session.execute(text(sql), {"user_id":user_id})
        return result.fetchone()[0]
    except Exception:
#        print("errori", e)
        return False

def get_project_names():
    """Get projects on which user is listed"""
    user_id = users.user_id()
    try:
        sql = "SELECT p1.project_id, p1.project_name FROM project_users pu, projects p1 \
            WHERE p1.project_id=pu.project_id AND pu.user_id=:user_id ORDER BY p1.project_name"
        result = db.session.execute(text(sql), {"user_id":user_id})
        return result.fetchall()
    except Exception:
        return False

def get_projects(project_id):
    """Get projects on which user is listed"""
    user_id = users.user_id()
    if project_id is not None:
        try:
            sql = "SELECT p1.project_id, p1.project_name, (SELECT COUNT(*) \
                FROM todos t2 WHERE t2.done_date IS NOT NULL AND t2.visible=TRUE \
                AND p1.project_id=t2.project_id AND t2.assigned_id=:user_id), \
                COUNT(t1.todo_id), p1.deadline_date FROM project_users pu, projects p1  \
                LEFT JOIN todos t1 ON p1.project_id=t1.project_id AND t1.visible=TRUE \
                WHERE p1.project_id=pu.project_id AND pu.user_id=:user_id AND p1.project_id=:project_id \
                GROUP BY p1.project_id ORDER BY p1.project_name"
            result = db.session.execute(text(sql), {"user_id":user_id, "project_id":project_id})
            return result.fetchall()
        except Exception:
            return False
    # If no project_id
    return 0

def get_project_todos(project_id):
    """Get project on which user is listed and its ToDos where user is the assigned_user"""
    user_id = users.user_id()
    try:
        sql = "SELECT p1.project_id, p1.project_name, t1.todo_id, t1.deadline_date, tt.type_name, \
            t1.todo_description, t1.done_date FROM projects p1, project_users pu, todos t1 \
            LEFT JOIN todo_types tt ON tt.type_id=t1.type_id WHERE p1.project_id=pu.project_id \
            AND p1.project_id=t1.project_id AND pu.user_id=:user_id AND t1.assigned_id=:user_id \
            AND p1.project_id=:project_id \
            ORDER BY p1.project_name, t1.deadline_date"
        result = db.session.execute(text(sql), {"user_id":user_id, "assigned_user":user_id, "project_id":project_id})
        return result.fetchall()
    except Exception:
        return False

def add_project(project_name, project_deadline):
    """User is project creator and member of project users"""
    created_by = users.user_id()
    try:
        sql = "INSERT INTO projects (project_name, created_by, create_date, deadline_date) \
            VALUES (:project_name, :created_by, NOW(), :deadline_date) RETURNING project_id"
        result = db.session.execute(text(sql), {"project_name":project_name, \
                                                "created_by":created_by, \
                                                "deadline_date":project_deadline})
        project_id = result.fetchone()[0]
        sql2 = "INSERT INTO project_users (project_id, user_id) VALUES (:project_id, :user_id)"
        db.session.execute(text(sql2), {"project_id":project_id, "user_id":created_by})
        db.session.commit()
    except Exception:
        return False
    return True

def delete_project(project_id):
    """Creator can delete"""
    created_by = users.user_id()
    try:
        sql = "DELETE FROM projects WHERE project_id=:project_id AND created_by=:created_by"
        db.session.execute(text(sql), {"project_id":project_id, "created_by":created_by})
        db.session.commit()
    except Exception:
        return False

    return True

# Types

def check_type_name(type_name):
    """Get list of types"""
    user_id = users.user_id()
    sql = "SELECT t1.type_id FROM todo_types t1 WHERE t1.visible = TRUE \
        AND t1.created_by=:user_id AND t1.type_name=:type_name"
    result = db.session.execute(text(sql), {"user_id":user_id, "type_name":type_name})
    type_name_sql = result.fetchone()
    if type_name_sql:
        return True
    return False

def get_types():
    """Get list of types"""
    user_id = users.user_id()
    try:
        sql = "SELECT t1.type_id, t1.type_name,  \
        (SELECT COUNT(*) FROM todos t2 WHERE t2.type_id=t1.type_id) \
        FROM todo_types t1 WHERE t1.visible = TRUE \
            AND t1.created_by=:user_id ORDER BY t1.type_name"
        result = db.session.execute(text(sql), {"user_id":user_id})
        return result.fetchall()
    except Exception:
        return False

def add_type(type_name):
    """Add new type"""
    created_by = users.user_id()
    try:
        sql = "INSERT INTO todo_types (type_name, created_by) VALUES (:type_name, :created_by) \
            RETURNING type_id"
        result = db.session.execute(text(sql), {"type_name":type_name, "created_by":created_by})
        type_id = result.fetchone()[0]
        sql2 = "INSERT INTO type_users (type_id, user_id) VALUES (:type_id, :user_id)"
        db.session.execute(text(sql2), {"type_id":type_id, "user_id":created_by})
        db.session.commit()
    except Exception:
        return False
    return True

def delete_type(type_id):
    """Creator can delete"""
    created_by = users.user_id()
    try:
        sql = "DELETE FROM todo_types WHERE type_id=:type_id AND created_by=:created_by"
        db.session.execute(text(sql), {"type_id":type_id, "created_by":created_by})
        db.session.commit()
    except Exception:
        return False
    return True
