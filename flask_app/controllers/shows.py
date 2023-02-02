from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Show
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/show_wall")
def recipe_wall():
    if "user_id" not in session:
        return redirect("/logout")
    print(session["user_id"])
    user = User.get_by_id(session["user_id"])
    users = User.get_all() 
    shows = Show.get_all_shows()
    return render_template("show_wall.html", user=user, users=users, shows=shows)

@app.route("/shows/like/<int:show_id>")
def likeshow(show_id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : show_id
    }
    Show.like(data)
    return redirect("/show_wall")

@app.route("/shows/dislike/<int:show_id>")
def dislikeshow(show_id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : show_id
    }
    Show.dislike(data)
    return redirect("/show_wall")

@app.route("/shows/new")
def showsnew():
    if "user_id" not in session:
        return redirect("/logout")
    return render_template("new_show.html")


@app.route("/shows/new/save", methods=["POST"])
def saveshow():
    valid_show = Show.validate_show(request.form)
    if 'user_id' not in session:
        return redirect('/')
    if not valid_show:
        return redirect("/shows/new")
    data ={ "title":request.form["title"],
        "network":request.form["network"],
        "release_date":request.form["release_date"],
        "description":request.form["description"],
        "user_id":session["user_id"]
    }
    Show.save(data)
    return redirect("/show_wall")



@app.route("/shows/edit/<int:show_id>")
def editrecipe(show_id):
    if "user_id" not in session:
        return redirect("/logout")
    show_id = {"id":show_id}
    show = Show.get_by_id(show_id)
    return render_template("edit_show.html", show = show)


@app.route("/shows/update/<int:show_id>",methods=["POST"])
def update(show_id):
    valid_show = Show.validate_show(request.form)
    if 'user_id' not in session:
        return redirect('/')
    if not valid_show:
        return redirect(f"/shows/edit/{show_id}")
    data ={ "id":show_id,
        "title":request.form["title"],
        "network":request.form["network"],
        "release_date":request.form["release_date"],
        "description":request.form["description"],
    }
    Show.update(data)
    return redirect("/show_wall")


@app.route("/shows/view/<int:show_id>")
def viewshow(show_id):
    if "user_id" not in session:
        return redirect("/logout")
    user = User.get_by_id(session["user_id"])
    show_id = {"id":show_id}
    show = Show.get_by_id(show_id)
    return render_template("view_show.html", show = show, user=user)

@app.route("/shows/delete/<int:show_id>")
def deleteshow(show_id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : show_id
    }
    Show.delete(data)
    return redirect("/show_wall")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")