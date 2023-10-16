# Application ToDo Today is made by Paula Meuronen 2023 for Helsinki University course TKT20019
# routes.py: pages and user input
 
from app import app
from flask import redirect, render_template, request, session, abort
from datetime import datetime, timedelta
import todos, users

# index is same as login
# ##############################################################################
@app.route("/")
def index():
	return render_template("login.html")

@app.route("/login", methods=["GET", "POST"]) 
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username, password):
			# After login redirect to ToDo list
			return redirect("/todolist") 
		else:
			return render_template("login.html", error_message="Wrong username or password")

# Logout
# ##############################################################################
@app.route("/logout") 
def logout():
	users.logout()
	return redirect("/")

# Register new user
###############################################################################
@app.route("/register", methods=["GET", "POST"]) 
def register():
	if request.method == "GET":
		return render_template("register.html")
	if request.method == "POST":
		username = request.form["username_new"]
		password1 = request.form["password_new"]
		password2 = request.form["password2_new"]

		#Check passwd and username requirements (very simple criteria)
		if password1 != password2:
			return render_template("register.html", username_post=username, error_message="Passwords were not the same.")
		if len(password1) < 4 or len(password1) >= 254:
			return render_template("register.html", username_post=username, error_message="Password must be between 4-254 characters.")		
		if len(username) < 2 or len(username) >= 254:
			return render_template("register.html", username_post=username, error_message="Username must be between 2-254 characters.")		

		#Do not accept duplicate usernames
		if users.check_name(username):
			#Register user
			if users.register(username, password1):
				# After registration redirect to ToDo list
				return render_template("/todolist") 
			else:
				return render_template("register.html", error_message="Unable to create new user.")
		else:
			return render_template("register.html", error_message="Username is already in use.")


# ToDo list
###############################################################################
@app.route("/todolist", methods=["GET", "POST"])
def todolist():
	list1 = todos.get_list('all')
	today = datetime.now().strftime("%d.%m.%Y")
	tomorrow = ( datetime.now() + timedelta(1)).strftime("%d.%m.%Y")

	if request.method == "GET":
		return render_template("todolist.html", todos_all=list1, today=today, tomorrow=tomorrow)

# Done ToDo
###############################################################################
	if request.method == "POST":

		#CSRF vulnerability check
		if session["csrf_token"] != request.form["csrf_token"]:
			abort(403)

		todo_id = request.form["id"]
		if todos.mark_done(todo_id):
			list1 = todos.get_list('all')
			return render_template("todolist.html", error_message=f"ToDo marked as done.", todos_all=list1, today=today, tomorrow=tomorrow)
		else:
			list1 = todos.get_list('all')
			return render_template("todolist.html", error_message=f"Unable mark a ToDo as done.",  todos_all=list1, today=today, tomorrow=tomorrow)


# Managing Projects and ToDos 
###############################################################################
@app.route("/manage", methods=["GET", "POST"]) 
def manage():
#	print(f"MANAGE ")

	list = todos.get_projects(None)
	list2 = todos.get_project_todos()
	list3 = todos.get_types()
	list4 = todos.get_project_names()
	error = ""
	if len(list3) == 0:
		error = 'First create a Type on Type Management page.'

	if request.method == "GET":
		return render_template("manage.html", types=list3, project_todos=list2, projects=list, project_names=list4, error_message=error)

	if request.method == "POST":
		type = request.form["form_type"]

# Add project
###############################################################################
		if type == "add_project":
			# KESKEN: tarkista, että päivämäärä ei ole menneisyydessä
			# KESKEN: tarkista, että samaa nimeä ei jo ole

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			project_name = request.form["project_name"]
			try:
				project_deadline = request.form["project_deadline"]
			except:		
				return render_template("manage.html", error_message=f"Project not added. Check date format in deadline.", types=list3, project_todos=list2, projects=list, project_names=list4)
			
			#Someday fix this to minute level
			if datetime.strptime(project_deadline, "%d.%m.%Y") < (datetime.now()-timedelta(1)):
				return render_template("manage.html", error_message=f"Project not added. Deadline date is in the past.", project_name=project_name, types=list3, project_todos=list2, projects=list, project_names=list4)
			
			if len(project_name) < 3 or len(project_name) >= 254:
				return render_template("manage.html", error_message=f"Project name must be between 3-254 characters.", types=list3, project_todos=list2, projects=list, project_names=list4)
			
			if todos.add_project(project_name, project_deadline):
				# Latest project that user has created 
				project_id = todos.get_latest_project_id()

				list = todos.get_projects(project_id)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				list4 = todos.get_project_names()
				return render_template("manage.html", error_message=f"New project added: {project_name}.", types=list3, project_todos=list2, projects=list, project_names=list4)
			else:
				return render_template("manage.html", error_message=f"Unable to add new project.", types=list3, project_todos=list2, projects=list, project_names=list4)

# Select project
###############################################################################
		if type == "get_project":
			project_id = request.form["project_id"]

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			try:			
				list = todos.get_projects(project_id)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				list4 = todos.get_project_names()
				return render_template("manage.html", error_message=f"Project selected for editing.", types=list3, project_todos=list2, projects=list, project_names=list4)
			except Exception as e:
#				print("Errori", e)
				return render_template("manage.html", error_message=f"Unable to get the project.", types=list3, project_todos=list2, projects=list, project_names=list4)

# Delete Project
# ###############################################################################
		if type == "delete_project":

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			project_id = request.form["project_id"]
#			print(f"route project id {project_id}")
			if todos.delete_project(project_id):
				list = todos.get_projects(None)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				list4 = todos.get_project_names()
				return render_template("manage.html", error_message=f"Project deleted.", types=list3, project_todos=list2, projects=list, project_names=list4)
			else:
				list = todos.get_projects(None)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("manage.html", error_message=f"Unable to delete a project.", types=list3, project_todos=list2, projects=list, project_names=list4)

# Add Todos
# ##############################################################################
		if type == "add_todo":		
			# TODO tarkista, että päivämäärä ei ole menneisyydessä

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			todo_description = request.form["todo_description"]
			project_id = request.form["project_id"]
			type_id = request.form["type_id"]
			try:
				todo_deadline = datetime.strptime(request.form["todo_deadline"], '%d.%m.%Y')
			except:		
				return render_template("manage.html", error_message=f"Todo not added. Check date format in deadline.", types=list3, project_todos=list2, projects=list)

			if todos.add_todo(todo_description, project_id, type_id, todo_deadline):
				list = todos.get_projects(project_id)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				list4 = todos.get_project_names()
				return render_template("manage.html", error_message=f"Added a new ToDo {todo_description}", types=list3, project_todos=list2, projects=list, project_names=list4)
# Done ToDo
# ###############################################################################
		if type == "done_todo":

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			todo_id = request.form["todo_id"]
			project_id = request.form["project_id"]
			if todos.mark_done(todo_id):
				list = todos.get_projects(project_id)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				list4 = todos.get_project_names()
				return render_template("manage.html", error_message=f"ToDo marked as done.", types=list3, project_todos=list2, projects=list, project_names=list4)
			else:
				list = todos.get_projects(project_id)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				list4 = todos.get_project_names()
				return render_template("manage.html", error_message=f"Unable mark a ToDo as done.",  types=list3, project_todos=list2, projects=list, project_names=list4)

# Delete ToDo
# ###############################################################################
		if type == "delete_todo":

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			todo_id = request.form["todo_id"]
			project_id = request.form["project_id"]
			if todos.delete_todo(todo_id):
				list = todos.get_projects(project_id)
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				list4 = todos.get_project_names()
				return render_template("manage.html", error_message=f"ToDo deleted.", types=list3, project_todos=list2, projects=list, project_names=list4)
			else:
				return render_template("manage.html", error_message=f"Unable to delete a ToDo.", types=list3, project_todos=list2, projects=list, project_names=list4)

		#If no project is selected
		return render_template("manage.html", error_message=f"No actions done.", types=list3, project_todos=list2, projects=list, project_name=list4)

# Managing types
# ##############################################################################
@app.route("/types", methods=["GET", "POST"]) 
def types():
	list3 = todos.get_types()

	if request.method == "GET":
		return render_template("types.html", types=list3)

	if request.method == "POST":
		type = request.form["form_type"]

# Add type
# ##############################################################################
		if type == "add_type":
			#TODO tarkista, että samaa nimeä ei jo ole

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			type_name = request.form["type_name"]
			if len(type_name) < 3 or len(type_name) >= 254:
				return render_template("types.html", error_message=f"Type name must be between 3-254 characters.", types=list3)
			if todos.add_type(type_name):
				list3 = todos.get_types()
				return render_template("types.html", error_message=f"New type added: {type_name}.", types=list3)
			else:
				return render_template("types.html", error_message=f"Unable to add new type.", types=list3)

# Delete type
# ##############################################################################
		if type == "delete_type":

			#CSRF vulnerability check
			if session["csrf_token"] != request.form["csrf_token"]:
				abort(403)

			type_id = request.form["type_id"]
			if todos.delete_type(type_id):
				list3 = todos.get_types()
				return render_template("types.html", error_message=f"Type deleted.", types=list3)
			else:
				return render_template("types.html", error_message=f"Unable to delete a type.", types=list3)


		return render_template("types.html", error_message=f"No actions done.", types=list3)

