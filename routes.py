"""routes.py: pages and user input"""
# Application ToDo Today is made by Paula Meuronen 2023
# for Helsinki University course TKT20019

from datetime import datetime, timedelta
from flask import redirect, render_template, request, session, abort
from app import app
import todos
import users

@app.route("/")
def index():
    """Index page is login"""
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            # After login redirect to ToDo list
            return redirect("/todolist")
        return render_template("login.html", error_message="Wrong username or password")
	#GET
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout"""
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    if request.method == "POST":
        username = request.form["username_new"]
        password1 = request.form["password_new"]
        password2 = request.form["password2_new"]
        error_msg = ""
        #Check passwd and username requirements
        if password1 != password2:
            error_msg = "Passwords were not the same."
        if len(password1) < 4 or len(password1) >= 254:
            error_msg="Password must be between 4-254 characters."
        if len(username) < 2 or len(username) >= 254:
            error_msg="Username must be between 2-254 characters."
        if len(error_msg)>0:
            return render_template("register.html", username_post=username, \
                          error_message=error_msg)
        error_msg = ""
        #Do not accept duplicate usernames
        if users.check_name(username):
            #Register user
            if users.register(username, password1):
                # After registration redirect to ToDo list
                return render_template("/todolist")
            error_msg="Unable to create new user."
        else:
            error_msg="Username is already in use."
        if len(error_msg)>0:
            return render_template("register.html", error_message=error_msg)
    #GET
    return render_template("register.html")

@app.route("/todolist", methods=["GET", "POST"])
def todolist():
    """ToDo list"""
    list1 = todos.get_list('all')
    today = datetime.now().strftime("%d.%m.%Y")
    tomorrow = ( datetime.now() + timedelta(1)).strftime("%d.%m.%Y")

# Done ToDo
    if request.method == "POST":

        #CSRF vulnerability check
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        todo_id = request.form["id"]
        if todos.mark_done(todo_id):
            list1 = todos.get_list('all')
            return render_template("todolist.html", error_message="ToDo marked as done.", \
                                   todos_all=list1, today=today, tomorrow=tomorrow)
        list1 = todos.get_list('all')
        return render_template("todolist.html", error_message="Unable mark a ToDo as done.", \
                               todos_all=list1, today=today, tomorrow=tomorrow)
    # GET
    return render_template("todolist.html", todos_all=list1, today=today, tomorrow=tomorrow)


@app.route("/manage", methods=["GET", "POST"])
def manage():
    """Managing Projects and ToDos"""

    list1 = todos.get_projects(None)
    list2 = todos.get_project_todos()
    list3 = todos.get_types()
    list4 = todos.get_project_names()
    error_msg = ""
    if len(list3) == 0:
        error_msg = 'First create a Type on Type Management page.'

    if request.method == "POST":
        type1 = request.form["form_type"]

# Add project
        if type1 == "add_project":
            # TODO: tarkista, että samaa nimeä ei jo ole

            #CSRF vulnerability check
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

            project_name = request.form["project_name"]
            try:
                project_deadline = request.form["project_deadline"]
            except Exception:
                return render_template("manage.html", \
                error_message="Project not added. Check date format in deadline.", \
                    types=list3, project_todos=list2, projects=list1, project_names=list4)

            #Someday fix this to minute level
            if datetime.strptime(project_deadline, "%d.%m.%Y") < (datetime.now()-timedelta(1)):
                return render_template("manage.html", \
                error_message="Project not added. Deadline date is in the past.", \
                project_name=project_name, types=list3, project_todos=list2, projects=list1, \
                project_names=list4)

            if len(project_name) < 3 or len(project_name) >= 254:
                return render_template("manage.html", \
                error_message="Project name must be between 3-254 characters.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)

            if todos.add_project(project_name, project_deadline):
                # Latest project that user has created
                project_id = todos.get_latest_project_id()

                list1 = todos.get_projects(project_id)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", \
                error_message="New project added: {project_name}.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)

            return render_template("manage.html", \
            error_message="Unable to add new project.", \
            types=list3, project_todos=list2, projects=list1, project_names=list4)

# Select project
        if type1 == "get_project":
            project_id = request.form["project_id"]

            #CSRF vulnerability check
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

            try:
                list1 = todos.get_projects(project_id)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", \
                error_message="Project selected for editing.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)
            except Exception:
                return render_template("manage.html", \
                error_message="Unable to get the project.", types=list3, project_todos=list2, \
                projects=list1, project_names=list4)

# Delete Project
        if type1 == "delete_project":

            #CSRF vulnerability check
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

            project_id = request.form["project_id"]
            if todos.delete_project(project_id):
                list1 = todos.get_projects(None)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", error_message="Project deleted.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)

            list1 = todos.get_projects(None)
            list2 = todos.get_project_todos()
            list3 = todos.get_types()
            return render_template("manage.html", \
            error_message="Unable to delete a project.", \
            types=list3, project_todos=list2, projects=list1, project_names=list4)

# Add Todos
        if type1 == "add_todo":

            #CSRF vulnerability check
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

            todo_description = request.form["todo_description"]
            project_id = request.form["project_id"]
            type_id = request.form["type_id"]
            try:
                todo_deadline = datetime.strptime(request.form["todo_deadline"], '%d.%m.%Y')
            except Exception:
                list1 = todos.get_projects(project_id)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", \
                error_message="Todo not added. Check date format in deadline.", \
                todo_description=todo_description, types=list3, project_todos=list2, \
                projects=list1, project_names=list4)

            #Someday fix this to minute level
            if todo_deadline < (datetime.now()-timedelta(1)):
                list1 = todos.get_projects(project_id)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", \
                error_message="ToDo not added. Deadline date is in the past.", \
                todo_description=todo_description, types=list3, project_todos=list2, \
                projects=list1, project_names=list4)

            if todos.add_todo(todo_description, project_id, type_id, todo_deadline):
                list1 = todos.get_projects(project_id)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", \
                error_message=f"Added a new ToDo {todo_description}", types=list3, \
                project_todos=list2, projects=list1, project_names=list4)
# Done ToDo
        if type1 == "done_todo":

            #CSRF vulnerability check
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

            todo_id = request.form["todo_id"]
            project_id = request.form["project_id"]
            if todos.mark_done(todo_id):
                list1 = todos.get_projects(project_id)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", \
                error_message="ToDo marked as done.", types=list3, project_todos=list2, \
                projects=list1, project_names=list4)

            list1 = todos.get_projects(project_id)
            list2 = todos.get_project_todos()
            list3 = todos.get_types()
            list4 = todos.get_project_names()
            return render_template("manage.html", \
            error_message="Unable mark a ToDo as done.", types=list3, project_todos=list2, \
            projects=list1, project_names=list4)

# Delete ToDo
        if type1 == "delete_todo":

            #CSRF vulnerability check
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)

            todo_id = request.form["todo_id"]
            project_id = request.form["project_id"]
            if todos.delete_todo(todo_id):
                list1 = todos.get_projects(project_id)
                list2 = todos.get_project_todos()
                list3 = todos.get_types()
                list4 = todos.get_project_names()
                return render_template("manage.html", error_message="ToDo deleted.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)

            return render_template("manage.html", error_message="Unable to delete a ToDo.", \
            types=list3, project_todos=list2, projects=list1, project_names=list4)

        #If no project is selected
        return render_template("manage.html", error_message="No actions done.", types=list3, \
        project_todos=list2, projects=list1, project_name=list4)

    #GET
    return render_template("manage.html", types=list3, project_todos=list2, \
    projects=list1, project_names=list4, error_message=error_msg)


@app.route("/types", methods=["GET", "POST"])
def types():
    """#Managing types"""
    list3 = todos.get_types()

    if request.method == "POST":
        type1 = request.form["form_type"]

        #CSRF vulnerability check
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        error_msg = ""

# Add type
        if type1 == "add_type":
            #TODO tarkista, että samaa nimeä ei jo ole
            type_name = request.form["type_name"]

            if len(type_name) < 3 or len(type_name) >= 254:
                return render_template("types.html", \
                error_message="Type name must be between 3-254 characters.", \
                types=list3)
            if todos.add_type(type_name):
                list3 = todos.get_types()
                return render_template("types.html", \
                error_message="New type added: {type_name}.", types=list3)
            return render_template("types.html", \
            error_message="Unable to add new type.", types=list3)

# Delete type
        if type1 == "delete_type":
            type_id = request.form["type_id"]
            if todos.delete_type(type_id):
                list3 = todos.get_types()
                return render_template("types.html", error_message="Type deleted.", types=list3)

            return render_template("types.html", \
            error_message="Unable to delete a type.", types=list3)
        else:
            return render_template("types.html", error_message="Unable to delete type.", types=list3)
    #GET
    return render_template("types.html", types=list3)
