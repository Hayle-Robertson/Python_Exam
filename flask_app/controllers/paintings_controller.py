from flask_app import app
from flask import render_template, request, redirect, session, flash 
from flask_app.models.paintings import Painting 
from flask_app.models.users import User

@app.route('/add_painting')
def add_painting():

    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")



    data = {
        "user_id" : session["user_id"]
    }

    user = User.get_by_id(data)

    return render_template("add_painting.html", user = user)

@app.route('/new_painting', methods=["POST"])
def new_painting():

    if not Painting.validate_painting(request.form):
        return redirect ("/add_painting")

    data={
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "users_id": session ["user_id"]
    } 

    Painting.save_painting(data)

    return redirect('/dashboard')

@app.route("/painting/<int:id>/edit")
def edit_painting(id):

    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")

    data = {
        "id" : id 
    }
    painting = Painting.get_one_painting(data)
    return render_template("edit_painting.html", painting=painting)

@app.route("/edit_painting<int:id>", methods=["POST"])
def edit_painting_info(id):
    data = {
        "id" : id,
        "title": request.form["title"],
        "description" : request.form["description"],
        "price" : request.form["price"]
    }

    Painting.edit_painting_info(data)

    return redirect(f"/painting/{id}")

@app.route("/painting/<int:id>/delete")
def delete_painting(id):
    data = {
        "id" : id
    }
    Painting.delete_one_painting(data)

    return redirect("/dashboard")

@app.route('/painting/<int:id>')
def show_one_painting(id):

    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")

    data ={
        "id" : id
    }

    painting = Painting.get_one_painting_with_user(data)
    
    return render_template("show_painting.html", painting = painting)