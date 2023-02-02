# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask_app.models import user
from flask import flash, session
import re	# the regex module
# create a regular expression object that we'll use later
import math 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Show:
    db = "tv_shows_schema"
    def __init__(self,db_data):
        self.id = db_data["id"]
        self.title = db_data["title"]
        self.network = db_data["network"]
        self.release_date = db_data["release_date"]
        self.description = db_data["description"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
        self.user_id = db_data["user_id"]
        self.likes = db_data["likes"]
        # None can represent a currently empty space for a single User dictionary to be placed here, as a Tweet is made by ONE User. We want a User instance and all their attributes to be placed here, so something like data['...'] will not work as we have to make the User instance ourselves.
        self.creator = None


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        show_data = connectToMySQL(cls.db).query_db(query)
        shows = []
        for show in show_data:
            shows.append( cls(show) )
        return shows


    @classmethod
    def get_by_id(cls,show_id):
        query ="SELECT * FROM shows LEFT JOIN users on shows.user_id = users.id WHERE shows.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,show_id)
        show = cls(results[0])
        for row in results:
            if row["users.id"] == None:
                break
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            # author.favorite_books.append(book.Book(data))
            show.creator = user.User(user_data)
        return show


    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows JOIN users on shows.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        # all_the_messages = cls(results[0])
        all_shows = []
        for row in results:
            # Create a Tweet class instance from the information from each db row
            one_show = cls(row)
            # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            # Create the User class instance that's in the user.py model file
            owner = user.User(user_data)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_show.creator = owner
            # Append the Tweet containing the associated User to your list of tweets
            all_shows.append(one_show)
        return all_shows




    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (title, network, release_date, description, created_at, user_id) VALUES ( %(title)s , %(network)s, %(release_date)s, %(description)s, NOW(), %(user_id)s);"
        # data is a dictionary that will be passed into the save method from server.py
        endresult = connectToMySQL(cls.db).query_db(query, data)
        return endresult

    @classmethod
    def like(cls,data):
        query = "UPDATE shows SET likes = likes+1  WHERE shows.id = %(id)s;"
        endresult = connectToMySQL(cls.db).query_db(query, data)
        return endresult

    @classmethod
    def dislike(cls,data):
        query = "UPDATE shows SET likes = likes-1  WHERE shows.id = %(id)s;"
        endresult = connectToMySQL(cls.db).query_db(query, data)
        return endresult

    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title = %(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        endresult = connectToMySQL(cls.db).query_db(query, data)
        return endresult

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM shows WHERE shows.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_show(show):
        is_valid = True # we assume this is true
        if len(show['title']) < 3:
            flash("Show Title must be at least 3 characters long!", "newshow")
            is_valid = False
        if len(show['network']) < 3:
            flash("Show Network must be at least 3 characters long!", "newshow")
            is_valid = False
        if show['release_date'] == '':
            flash("Show must have a release date!", "newshow")
            is_valid = False
        if len(show['description']) < 3:
            flash("Show Description must be at least 3 characters long!", "newshow")
            is_valid = False
        if len(show["title"]) <= 0 or len(show["network"]) <= 0 or show["release_date"] =='' or len(show["description"]) <= 0:
            flash("All fields are required, process incomplete!", "newshow")
        return is_valid


    def time_span(self):
        print(self.created_at)
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"






# -- UPDATE shows SET likes = likes+1 WHERE shows.id = 1;
# -- UPDATE shows SET likes = likes+2 WHERE shows.id = 1;
# SELECT * FROM shows;
