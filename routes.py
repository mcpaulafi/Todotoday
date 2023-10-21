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
        if users.check_name(username):
            """Do not accept duplicate usernames"""
            error_msg="Username is already registered."

        if len(error_msg)>0:
            return render_template("register.html", username_post=username, \
                          error_message=error_msg)
        else:
            if users.register(username, password1):
                """ Register user"""
                # After registration redirect to ToDo list
                return render_template("todolist.html")
        # Unknown error
        error_msg="Unable to create a new user."
        if len(error_msg)>0:
            return render_template("register.html", error_message=error_msg)
    # GET
    return render_template("register.html")

@app.route("/todolist", methods=["GET", "POST"])
def todolist():
    """ToDo list"""
    list1 = todos.get_list('all')
    list2 = todos.get_list('today')
    list3 = todos.get_list('tomorrow')
    get_types = todos.get_types()

    if request.method == "POST":

        list1 = todos.get_list('all')
        list2 = todos.get_list('today')
        list3 = todos.get_list('tomorrow')
        form_type = request.form["form_type"]

        #CSRF vulnerability check
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        # Get types
        if form_type == "get_types":
            type_id = request.form["type_id"]
            list4 = todos.get_list_type(type_id)
            confirm_message_type = "Type selected."
            if type_id == "all":
                confirm_message_type = ""

            return render_template("todolist.html", confirm_message_type=confirm_message_type, \
                                todos_all=list4, today=list2, tomorrow=list3, get_types=get_types)

        # Done ToDo
        if form_type == "done_todo":
            todo_id = request.form["todo_id"]
            if todos.mark_done(todo_id):
                list1 = todos.get_list('all')
                list2 = todos.get_list('today')
                list3 = todos.get_list('tomorrow')

                return render_template("todolist.html", confirm_message="ToDo marked as done.", \
                                    todos_all=list1, today=list2, tomorrow=list3, get_types=get_types)
            #Error
            return render_template("todolist.html", error_message="Unable mark a ToDo as done.", \
                                todos_all=list1, today=list2, tomorrow=list3, get_types=get_types)
    # GET
    return render_template("todolist.html", todos_all=list1, today=list2, tomorrow=list3, get_types=get_types)

@app.route("/manage", methods=["GET", "POST"])
def manage():
    """Managing Projects and ToDos"""

    list1 = todos.get_projects(None)
    list2 = None                        # No project_id available
    list3 = todos.get_types()
    list4 = todos.get_project_names()
    error_msg = ""

    if len(list3) == 0:
        error_msg = 'First create a Type on Type Management page.'

    # POST
    if request.method == "POST":
        type1 = request.form["form_type"]

        #CSRF vulnerability check
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        # Add project
        if type1 == "add_project":
            project_name = request.form["project_name"]
            error_msg = ""
            try:
                project_deadline = request.form["project_deadline"]
            except:
                error_msg = "Project not added. Check date format in deadline."

            #Someday fix this to minute level
            try:
                project_deadline = datetime.strptime(request.form["project_deadline"], '%d.%m.%Y')
            except:
                error_msg = "Project not added. Check the deadline date."

            if error_msg!="Project not added. Check the deadline date.":
                if project_deadline < (datetime.now()-timedelta(1)):
                    error_msg = "Project not added. Deadline date is in the past."

            if len(project_name) < 3 or len(project_name) >= 254:
                error_msg = "Project name must be between 3-254 characters."

            if todos.check_project_name(project_name):
                error_msg = "Project name is already in use."

            if error_msg == "":
                if todos.add_project(project_name, project_deadline):
                    # Latest project that user has created
                    project_id = todos.get_latest_project_id()

                    list1 = todos.get_projects(project_id)
                    list2 = todos.get_project_todos(project_id)
                    list3 = todos.get_types()
                    list4 = todos.get_project_names()
                    return render_template("manage.html", \
                    confirm_message=f"New project added: {project_name}.", \
                    types=list3, project_todos=list2, projects=list1, project_names=list4)
                else:
                    error_msg = "Unable to add new project."

            return render_template("manage.html", \
            types=list3, project_todos=list2, projects=list1, project_names=list4, project_name=project_name, error_message_add=error_msg)

        # Select project
        if type1 == "get_project":
            project_id = request.form["project_id"]

            list1 = todos.get_projects(project_id)
            list2 = todos.get_project_todos(project_id)
            list3 = todos.get_types()
            list4 = todos.get_project_names()

            try:
                return render_template("manage.html", \
                confirm_message_add="Project selected for editing.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)
            except:
                return render_template("manage.html", \
                error_message_add="Unable to get the project.", types=list3, project_todos=list2, \
                projects=list1, project_names=list4)

        # Delete Project
        if type1 == "delete_project":
            project_id = request.form["project_id"]

            list1 = todos.get_projects(project_id)
            list2 = todos.get_project_todos(project_id)
            list3 = todos.get_types()
            list4 = todos.get_project_names()

            if todos.delete_project(project_id):
                list1 = todos.get_projects(None)
                list2 = None
                list4 = todos.get_project_names()
                return render_template("manage.html", confirm_message="Project deleted.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)

            return render_template("manage.html", \
            error_message="Unable to delete a project.", \
            types=list3, project_todos=list2, projects=list1, project_names=list4)

        # Add Todos
        if type1 == "add_todo":
            project_id = request.form["project_id"]
            todo_description = request.form["todo_description"]
            type_id = request.form["type_id"]

            list1 = todos.get_projects(project_id)
            list2 = todos.get_project_todos(project_id)
            list3 = todos.get_types()
            list4 = todos.get_project_names()

            error_msg_todo = ""

            try:
                todo_deadline = datetime.strptime(request.form["todo_deadline"], '%d.%m.%Y')
            except:
                error_msg_todo = "Todo not added. Check date format in deadline."

            if error_msg_todo != "Todo not added. Check date format in deadline.":
                #Someday fix this to minute level
                if todo_deadline < (datetime.now()-timedelta(1)):
                    error_msg_todo = "ToDo not added. Deadline date is in the past."

            if error_msg_todo == "":
                if todos.add_todo(todo_description, project_id, type_id, todo_deadline):
                    list1 = todos.get_projects(project_id) # status count update
                    list2 = todos.get_project_todos(project_id)

                    return render_template("manage.html", \
                    confirm_message_todo=f"Added a new ToDo {todo_description}", types=list3, \
                    project_todos=list2, projects=list1, project_names=list4)
                else:
                    error_msg_todo = "Unable to add ToDo."

            return render_template("manage.html", \
            error_message_todo=error_msg_todo, types=list3, \
            project_todos=list2, projects=list1, project_names=list4)


# Done ToDo
        if type1 == "done_todo":

            todo_id = request.form["todo_id"]
            project_id = request.form["project_id"]

            list1 = todos.get_projects(project_id)
            list2 = todos.get_project_todos(project_id)
            list3 = todos.get_types()
            list4 = todos.get_project_names()
 
            if todos.mark_done(todo_id):
                list2 = todos.get_project_todos(project_id)

                return render_template("manage.html", \
                confirm_message_todo="ToDo marked as done.", types=list3, project_todos=list2, \
                projects=list1, project_names=list4)

            return render_template("manage.html", \
            error_message="Unable mark a ToDo as done.", types=list3, project_todos=list2, \
            projects=list1, project_names=list4)

# Delete ToDo
        if type1 == "delete_todo":
            todo_id = request.form["todo_id"]
            project_id = request.form["project_id"]

            list1 = todos.get_projects(project_id)
            list2 = todos.get_project_todos(project_id)
            list3 = todos.get_types()
            list4 = todos.get_project_names()

            if todos.delete_todo(todo_id):
                list2 = todos.get_project_todos(project_id)
                return render_template("manage.html", confirm_message_todo="ToDo deleted.", \
                types=list3, project_todos=list2, projects=list1, project_names=list4)

            return render_template("manage.html", error_message_todo="Unable to delete a ToDo.", \
            types=list3, project_todos=list2, projects=list1, project_names=list4)

        #If no project is selected
        return render_template("manage.html", error_message_todo="No actions done.", types=list3, \
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
            type_name = request.form["type_name"]
            error_message = ""
            confirm_message = ""

            if todos.check_type_name(type_name):
                error_message="Type name is already in use."

            if len(type_name) < 3 or len(type_name) >= 254:
                error_message="Type name must be between 3-254 characters." 
            
            if len(error_message)==0:
                if todos.add_type(type_name):
                    confirm_message=f"New type added: {type_name}."
                else:
                    error_message="Unable to add new type."
            
            list3 = todos.get_types()
            return render_template("types.html", \
            error_message=error_message, confirm_message=confirm_message, types=list3)

# Delete type
        if type1 == "delete_type":
            type_id = request.form["type_id"]
            if todos.delete_type(type_id):
                list3 = todos.get_types()
                return render_template("types.html", confirm_message="Type deleted.", types=list3)

            return render_template("types.html", \
            error_message="Unable to delete a type.", types=list3)

    #GET
    return render_template("types.html", types=list3)
