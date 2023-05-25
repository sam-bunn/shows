from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "shows"
class Show:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.network = db_data['network']
        self.date_made = db_data['date_made']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM shows
                JOIN users on shows.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        shows = []
        for row in results:
            this_show = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_show.creator = user.User(user_data)
            shows.append(this_show)
        return shows
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM shows
                JOIN users on shows.user_id = users.id
                WHERE shows.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_show = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_show.creator = user.User(user_data)
        return this_show

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO shows (name,description,network,date_made,user_id)
                VALUES (%(name)s,%(description)s,%(network)s,%(date_made)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE shows
                SET name = %(name)s,
                description = %(description)s,
                network = %(network)s ,
                date_made = %(date_made)s,
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM shows
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_show(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(form_data['network']) < 3:
            flash("network must be at least 3 characters long.")
            is_valid = False
        if form_data['date_made'] == '':
            flash("Please input a date.")
            is_valid = False


        return is_valid