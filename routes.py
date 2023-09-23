from app import app
from flask import redirect, render_template, request, session
from datetime import datetime, timedelta
import todos, users
#TODO tiivistä ja vähennä toistoa


#INDEX is same as LOGIN
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
			return redirect("/todolist") #AFTER LOGIN redirect to TODOLIST
		else:
			return render_template("login.html", error_message="Wrong username or password")

#LOGOUT
@app.route("/logout") 
def logout():
	users.logout()
	return redirect("/")

#REGISTER new user
@app.route("/register", methods=["GET", "POST"]) 
def register():
	if request.method == "GET":
		return render_template("register.html")
	if request.method == "POST":
		username = request.form["username_new"]
		password1 = request.form["password_new"]
		password2 = request.form["password2_new"]
		if password1 != password2:
			return render_template("register.html", username_post=username, error_message="Passwords were not the same.")
		if len(password1) < 4 or len(password1) >= 254:
			return render_template("register.html", username_post=username, error_message="Password must be between 4-254 characters.")		
		if len(username) < 2 or len(username) >= 254:
			return render_template("register.html", username_post=username, error_message="Username must be between 2-254 characters.")		
		#TODO puuttuu tarkistus ettei samaa nimeä kuin jo on kannassa
		if users.register(username, password1):
			return redirect("/todolist") #rekisteröimisen jälkeen ohjaus käyttäjän tehtävälistaan
		else:
			return render_template("register.html", error_message="Unable to create new user.")

#TODO LIST
@app.route("/todolist", methods=["GET", "POST"])
def todolist():
	list1 = todos.get_list('all')
	today = datetime.now().strftime("%d.%m.%Y")
	tomorrow = ( datetime.now() + timedelta(1)).strftime("%d.%m.%Y")

	if request.method == "GET":
		return render_template("todolist.html", todos_all=list1, today=today, tomorrow=tomorrow)

#DONE TODOs
	if request.method == "POST":
		todo_id = request.form["id"]
		#TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
		if todos.mark_done(todo_id):
			list1 = todos.get_list('all')
			return render_template("todolist.html", error_message=f"ToDo marked as done. {todo_id}", todos_all=list1, today=today, tomorrow=tomorrow)
		else:
			list1 = todos.get_list('all')
			return render_template("todolist.html", error_message=f"Unable mark a ToDo as done. {todo_id}",  todos_all=list1, today=today, tomorrow=tomorrow)


#MANAGING Projects, todos 
@app.route("/manage", methods=["GET", "POST"]) 
def manage():
	list = todos.get_projects()
	list2 = todos.get_project_todos()
	list3 = todos.get_types()


	if request.method == "GET":
		return render_template("manage.html", types=list3, project_todos=list2, projects=list)

	if request.method == "POST":
		type = request.form["form_type"]

#ADD PROJECT
		if type == "add_project":
			#TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			#TODO tarkista, että samaa nimeä ei jo ole

			project_name = request.form["project_name"]
			if len(project_name) < 3 or len(project_name) >= 254:
				return render_template("manage.html", error_message=f"Project name must be between 3-254 characters.", types=list3, project_todos=list2, projects=list)
			if todos.add_project(project_name):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("manage.html", error_message=f"New project added: {project_name}.", types=list3, project_todos=list2, projects=list)
			else:
				return render_template("manage.html", error_message=f"Unable to add new project.", types=list3, project_todos=list2, projects=list)

#ADD TODOs
		if type == "add_todo":		
			#TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			#TODO tarkista, päivämäärä

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

#DELETE TODOs
		if type == "delete_todo":
			#TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			#TODO tarkista, että id löytyy 

			todo_id = request.form["todo_id"]
			if todos.delete_todo(todo_id):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("manage.html", error_message=f"ToDo deleted.", types=list3, project_todos=list2, projects=list)
			else:
				return render_template("manage.html", error_message=f"Unable to delete a ToDo.", types=list3, project_todos=list2, projects=list)



		return render_template("manage.html", error_message=f"No actions done.", types=list3, project_todos=list2, projects=list)

#MANAGING types
@app.route("/types", methods=["GET", "POST"]) 
def types():
	list3 = todos.get_types()


	if request.method == "GET":
		return render_template("types.html", types=list3)

	if request.method == "POST":
		type = request.form["form_type"]

#ADD TYPE
		if type == "add_type":
			#TODO tarkista, että käyttäjällä on oikeus tehdä päivitys
			#TODO tarkista, että samaa nimeä ei jo ole

			type_name = request.form["type_name"]
			if len(type_name) < 3 or len(type_name) >= 254:
				return render_template("types.html", error_message=f"Type name must be between 3-254 characters.", types=list3)
			if todos.add_type(type_name):
				list = todos.get_projects()
				list2 = todos.get_project_todos()
				list3 = todos.get_types()
				return render_template("types.html", error_message=f"New type added: {type_name}.", types=list3)
			else:
				return render_template("types.html", error_message=f"Unable to add new type.", types=list3)

#DELETE TYPE
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

