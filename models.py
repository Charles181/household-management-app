from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(10), nullable=False, default="user")

class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(20), nullable=False)
    task_description = db.Column(db.String(200), nullable=False)

class Assignments(db.Model):
    assignment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False, default=datetime.now())
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Inventory(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    expire_date = db.Column(db.String, nullable=False, default='N/A')
    item_category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, default=1)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(35), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class ShoppingListHeaders(db.Model):
    list_id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # e.g., 'active', 'completed', etc.
    notes = db.Column(db.String(250), default="No notes.")

class ShoppingLists(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('shopping_list_headers.list_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)