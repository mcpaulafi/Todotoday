# Application ToDo Today is made by Paula Meuronen 2023 for Helsinki University course TKT20019
# routes.py: pages and user input
 
from app import app
from flask import redirect, render_template, request, session
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
				return redirect("/todolist") 
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

# Dode ToDos
###############################################################################
	if request.method == "POST":
		todo_id = request.form["id"]
		# TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
		if todos.mark_done(todo_id):
			list1 = todos.get_list('all')
			return render_template("todolist.html", error_message=f"ToDo marked as done. {todo_id}", todos_all=list1, today=today, tomorrow=tomorrow)
		else:
			list1 = todos.get_list('all')
			return render_template("todolist.html", error_message=f"Unable mark a ToDo as done. {todo_id}",  todos_all=list1, today=today, tomorrow=tomorrow)


# Managing Projects and ToDos 
###############################################################################
@app.route("/manage", methods=["GET", "POST"]) 
def manage():
	list = todos.get_projects()
	list2 = todos.get_project_todos()
	list3 = todos.get_types()


	if request.method == "GET":
		return render_template("manage.html", types=list3, project_todos=list2, projects=list)

	if request.method == "POST":
		type = request.form["form_type"]

# Add project
###############################################################################
		if type == "add_project":
			# TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			# TODO tarkista, että samaa nimeä ei jo ole

			project_name = request.form["project_name"]
			try:
				project_deadline = request.form["project_deadline"]
			except:		
				return render_template("manage.html", error_message=f"Project not added. Check date format in deadline.", types=list3, project_todos=list2, projects=list)

			if len(project_name) < 3 or len(project_name) >= 254:
				return render_template("manage.html", error_message=f"Project name must be between 3-254 characters.", types=list3, project_todos=list2, projects=list)
			if todos.add_project(project_name, project_deadline):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("manage.html", error_message=f"New project added: {project_name}.", types=list3, project_todos=list2, projects=list)
			else:
				return render_template("manage.html", error_message=f"Unable to add new project.", types=list3, project_todos=list2, projects=list)
# Delete Project
# ###############################################################################
		if type == "delete_project":
			# TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			# TODO tarkista, että id löytyy 
			project_id = request.form["project_id"]
			print(f"route project id {project_id}")
			if todos.delete_project(project_id):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("manage.html", error_message=f"Project deleted.", types=list3, project_todos=list2, projects=list)
			else:
				return render_template("manage.html", error_message=f"Unable to delete a project.", types=list3, project_todos=list2, projects=list)

# Add Todos
# ##############################################################################
		if type == "add_todo":		
			# TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			# TODO tarkista, päivämäärä

			todo_description = request.form["todo_description"]
			project_id = request.form["project_id"]
			type_id = request.form["type_id"]
			try:
				todo_deadline = datetime.strptime(request.form["todo_deadline"], '%d.%m.%Y')
			except:		
				return render_template("manage.html", error_message=f"Todo not added. Check date format in deadline.", types=list3, project_todos=list2, projects=list)

			if todos.add_todo(todo_description, project_id, type_id, todo_deadline):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("manage.html", error_message=f"Added a new ToDo.", types=list3, project_todos=list2, projects=list)

# Delete ToDo
# ###############################################################################
		if type == "delete_todo":
			# TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			# TODO tarkista, että id löytyy 

			todo_id = request.form["todo_id"]
			if todos.delete_todo(todo_id):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("manage.html", error_message=f"ToDo deleted.", types=list3, project_todos=list2, projects=list)
			else:
				return render_template("manage.html", error_message=f"Unable to delete a ToDo.", types=list3, project_todos=list2, projects=list)



		return render_template("manage.html", error_message=f"No actions done.", types=list3, project_todos=list2, projects=list)

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
			#TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			#TODO tarkista, että samaa nimeä ei jo ole

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
			#TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			#TODO tarkista, että id löytyy 

			type_id = request.form["type_id"]
			if todos.delete_type(type_id):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("types.html", error_message=f"Type deleted.", types=list3)
			else:
				return render_template("types.html", error_message=f"Unable to delete a type.", types=list3)


		return render_template("types.html", error_message=f"No actions done.", types=list3)

