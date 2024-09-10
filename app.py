from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Users, Tasks, Assignments, Inventory, ShoppingLists, Categories, ShoppingListHeaders
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, admin_required
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
migrate = Migrate(app, db)

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()

@app.before_first_request
def create_admin():
    admin_user = Users.query.filter_by(user_type='admin').first()
    if not admin_user:
        # Create a default admin user
        hashed_password = generate_password_hash("defaultadminpassword", method='pbkdf2:sha256')
        new_admin = Users(username="admin", password_hash=hashed_password, user_type='admin')
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created with username 'admin' and password 'defaultadminpassword'")

@app.route("/")
@login_required
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    user = Users.query.filter_by(id=session["user_id"]).first()
    existing_assignments = db.session.query(Assignments, Tasks).join(Tasks, Assignments.task_id == Tasks.task_id).filter(Assignments.user_id == session["user_id"]).filter(Assignments.due_date == today).first()
    if existing_assignments:
        assignments = db.session.query(Assignments, Tasks).join(Tasks, Assignments.task_id == Tasks.task_id).filter(Assignments.user_id == session["user_id"]).filter(Assignments.due_date == today)
    else:
        assignments = None
    completed = Assignments.query.filter_by(user_id=session["user_id"], completed=1).all()
    pending = Assignments.query.filter_by(user_id=session["user_id"], completed=0).all()
    return render_template("index.html", user=user, assignments=assignments, completed=completed, pending=pending, today=today)
    
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            flash("Password and confirmation do not match!")
            return redirect("/register")
        
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!")
            return redirect("/register")
        
        new_user = Users(username=username, password_hash=generate_password_hash(password), user_type='user')
        db.session.add(new_user)
        db.session.commit()
        flash(f"{username} added successfully!")
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"]) # This function code was taken from cs50x problem set 9 - Finance
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not username:
            flash("Must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not password:
            flash("Must provide password")
            return redirect("/login")

        # Query database for username
        user = Users.query.filter_by(username=username).first()
        # print(user)
        # Ensure username exists and password is correct
        if user == None or not check_password_hash(user.password_hash, password):
            flash("Invalid username and/or password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = user.id
        session["user_type"] = user.user_type

        # Redirect user to home page
        flash(f"Logged in as {user.username}")
        if user.user_type == 'user':
            return redirect("/")
        else:
            return redirect("/admin")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout") # This function code was taken from cs50x problem set 9 - Finance
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged out successfully.")
    return redirect("/")

@app.route("/admin", methods=["POST", "GET"])
@login_required
@admin_required
def admin():
    today = datetime.today().strftime('%Y-%m-%d')
    if request.method == "POST":
        selected_date = datetime.strptime(request.form.get("selected_date"), '%Y-%m-%d').strftime('%Y-%m-%d')
        if not selected_date:
            selected_date = today
        
        assignments = db.session.query(Assignments, Users, Tasks).join(Users, Assignments.user_id == Users.id).join(Tasks, Assignments.task_id == Tasks.task_id).filter(Assignments.due_date == selected_date).all()
        return render_template("admin_dashboard.html", selected_date=selected_date, assignments=assignments, today=today)
    else:
        return render_template("admin_dashboard.html", today=today)

@app.route("/add_task", methods=["POST", "GET"])
@login_required
@admin_required
def add_task():
    if request.method == "POST":
        task_name = request.form.get("task_name")
        task_description = request.form.get("task_description")

        # Check if task already exists in db
        existing_task = Tasks.query.filter_by(task_name=task_name).first()
        if existing_task:
            flash("Task already exists, please try adding a new one.")
            return redirect("/admin")
        
        new_task = Tasks(task_name=task_name, task_description=task_description)
        db.session.add(new_task)
        db.session.commit()
        flash(f"{task_name} added successfully!")
        return redirect("/admin")

@app.route("/add_item", methods=["POST"])
@login_required
@admin_required
def add_item():
    item_name = request.form.get("item_name")
    quantity = request.form.get("item_quantity")
    expire_date = request.form.get("expire_date")
    category = request.form.get("item_category")
    item_category = Categories.query.filter_by(category=category).first()
    if not expire_date:
        expire_date = 'N/A'

    existing_item = Inventory.query.filter_by(item_name=item_name).first()
    if existing_item:
        flash(f"{item_name} already exists in database.")
        return redirect("/inventory")
    
    new_item = Inventory(item_name=item_name, total_quantity=quantity, expire_date=expire_date, item_category=item_category.id)
    db.session.add(new_item)
    db.session.commit()
    flash(f"{item_name} added successfully.")
    return redirect("/inventory")
    
@app.route("/assign", methods=["GET", "POST"])
@login_required
@admin_required
def assign():
    today = datetime.today().strftime('%Y-%m-%d')
    users = Users.query.all()
    tasks = Tasks.query.all()

    if request.method == "POST":
        assigner = session["user_id"]
        username = request.form.get("user_name")
        task_name = request.form.get("task_name")
        due_date = datetime.strptime(request.form.get("due_date"), '%Y-%m-%d').date()
        user = Users.query.filter_by(username=username).first()
        task = Tasks.query.filter_by(task_name=task_name).first()

        if not user or not task:
            flash("Please select task AND user!")
            return redirect("/assign")
        
        existing_task = Assignments.query.filter_by(user_id=user.id, task_id=task.task_id, due_date=due_date).first()

        if existing_task:
            flash(f"{task_name} has already been assigned to {username} for this date.")
            return redirect("/assign")

        new_assignment = Assignments(user_id = user.id, task_id = task.task_id, due_date = due_date, assigned_by = assigner)
        db.session.add(new_assignment)
        db.session.commit()
        return redirect("/assign")
    else:
        return render_template("assign.html", users=users, tasks=tasks, today=today)
    
@app.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory(): # Sorting implementation achieved with help of chatgpt code copilot.
    sort_options = {
        'item_name': Inventory.item_name,
        'total_quantity': Inventory.total_quantity,
        'category_name': Categories.category
    }
    sort_by = request.args.get('sort_by', 'total_quantity')  # Default to sorting by quantity
    sort_column = sort_options.get(sort_by, Inventory.total_quantity)  # Default to sorting by quantity if sort_by is not recognized
    order = request.args.get('order', 'desc')  # Default to descending order

    # Order the list based on the sort_by and order parameters
    if order == 'asc':
        items = db.session.query(Inventory, Categories).join(Inventory, Inventory.item_category == Categories.id).order_by(sort_column).all()
    else:
        items = db.session.query(Inventory, Categories).join(Inventory, Inventory.item_category == Categories.id).order_by(db.desc(sort_column)).all()
    
    
    categories = Categories.query.all()
    if request.method == "POST":
        for item, _ in items:
            new_quantity = request.form.get(f"quantity_{item.item_id}")
            if new_quantity is not None:
                item.total_quantity = int(new_quantity)
        db.session.commit()
        flash("Inventory updated successfully!")
        return redirect("/inventory")
    return render_template("inventory.html", items=items, categories=categories, sort_by=sort_by, order=order)

@app.route("/update_task", methods=["POST"])
@login_required
def update_task():
    action = request.form.get("action")
    assignment_id = request.form.get("assignment_id")
    task_to_update = Assignments.query.filter_by(assignment_id=assignment_id).first()

    print(f"Received action: {action}")
    print(f"Received assignment_id: {assignment_id}")

    if task_to_update:
        if action == "done":
            task_to_update.completed = 1
        elif action == "undone":
            task_to_update.completed = 0
        db.session.commit()
        flash("Task status updated successfully!", "success")

    else:
        flash("Task not found!", "danger")
    return redirect("/")

@app.route("/tasks", methods=["POST", "GET"])
@login_required
def tasks():
    today = datetime.today().strftime('%Y-%m-%d')
    if request.method == "POST":
        selected_date = datetime.strptime(request.form.get("selected_date"), '%Y-%m-%d').strftime('%Y-%m-%d')
        user = Users.query.filter_by(id=session["user_id"]).first()
        assignments = db.session.query(Assignments, Tasks).join(Tasks, Assignments.task_id == Tasks.task_id).filter(Assignments.user_id == session["user_id"]).filter(Assignments.due_date == selected_date)
        if not selected_date:
            selected_date = today
        
        return render_template("task_view.html", today=today, user=user, assignments=assignments, selected_date=selected_date)

    else:
        return render_template("task_view.html", today=today)

@app.route("/shopping_list", methods=["GET", "POST"]) # Sorting implementation achieved with help of chatgpt code copilot.
@login_required
@admin_required    
def shopping_list():
    sort_by = request.args.get('sort_by', 'date')  # Default to sorting by date
    order = request.args.get('order', 'desc')  # Default to descending order

    # Order the list based on the sort_by and order parameters
    if order == 'asc':
        all_lists = ShoppingListHeaders.query.order_by(sort_by).all()
    else:
        all_lists = ShoppingListHeaders.query.order_by(db.desc(sort_by)).all()

    recent_list_header = all_lists[0] if all_lists else None
    if recent_list_header:
        recent_list = db.session.query(ShoppingLists, Inventory).join(Inventory, ShoppingLists.item_id == Inventory.item_id).filter(ShoppingLists.list_id == recent_list_header.list_id).all()
    else:
        recent_list = None

    items = Inventory.query.all()

    return render_template("shopping_list.html", recent_list=recent_list, recent_list_header=recent_list_header, all_lists=all_lists, items=items, today=datetime.today().strftime('%Y-%m-%d'), sort_by=sort_by, order=order)


@app.route("/create_shopping_list", methods=["POST"])
@login_required
@admin_required
def create_shopping_list():
    list_name = request.form.get("list_name")
    list_date = datetime.strptime(request.form.get("list_date"), '%Y-%m-%d').date()

    if not list_name:
        list_name = f"Shopping List for {list_date}"

    new_list = ShoppingListHeaders(list_name=list_name, date=list_date)
    db.session.add(new_list)
    db.session.commit()

    flash("Shopping list created successfully!")
    return redirect("/shopping_list")


@app.route("/modify_shopping_list", methods=["POST"])
@login_required
@admin_required
def modify_shopping_list():
    list_id = request.form.get("shopping_list_id")
    item_ids = request.form.getlist("item_id[]")
    quantities = request.form.getlist("quantity[]")
    # print(item_ids)

    for item_id, quantity in zip(item_ids, quantities):
        existing_entry = ShoppingLists.query.filter_by(list_id=list_id, item_id=item_id).first()

        if existing_entry:
            existing_entry.quantity += int(quantity)
        else:
            new_entry = ShoppingLists(list_id=list_id, item_id=item_id, quantity=int(quantity))
            db.session.add(new_entry)

    db.session.commit()
    flash("Shopping list updated successfully!")
    return redirect("/shopping_list")

@app.route("/view_shopping_list", methods=["POST"])
@login_required
@admin_required
def view_shopping_list():
    list_id = request.form.get("list_id")
    shopping_list = db.session.query(ShoppingLists, Inventory).join(Inventory, ShoppingLists.item_id == Inventory.item_id).filter(ShoppingLists.list_id == list_id).all()
    list_header = ShoppingListHeaders.query.filter_by(list_id=list_id).first()
    all_lists = ShoppingListHeaders.query.order_by(ShoppingListHeaders.date.desc()).all()

    return render_template("view_shopping_list.html", shopping_list=shopping_list, list_header=list_header, all_lists=all_lists)

@app.route("/delete_from_shopping", methods=["POST"])
@login_required
@admin_required
def delete_from_shopping():
    list_id = request.form.get("list_id")
    item_id = request.form.get("item_id")
    list_header = ShoppingListHeaders.query.filter_by(list_id=list_id).first()
    all_lists = ShoppingListHeaders.query.order_by(ShoppingListHeaders.date.desc()).all()

    item_to_delete = ShoppingLists.query.filter_by(list_id=list_id, item_id=item_id).first()
    db.session.delete(item_to_delete)
    db.session.commit()
    shopping_list = db.session.query(ShoppingLists, Inventory).join(Inventory, ShoppingLists.item_id == Inventory.item_id).filter(ShoppingLists.list_id == list_id).all()
    flash("Item removed successfully.")
    return render_template("/view_shopping_list.html", shopping_list=shopping_list, list_header=list_header, all_lists=all_lists)

@app.route("/complete_list", methods=["POST"])
@login_required
@admin_required
def complete_list():
    list_id = int(request.form.get("recent_list_header_id"))
    if request.form.get("notes") == "":
        notes = "No notes."
    else:
        notes = request.form.get("notes")
    list_to_complete = ShoppingListHeaders.query.filter_by(list_id=list_id).first()
    if list_to_complete:
        # Mark the shopping list as completed
        list_to_complete.status = 'completed'
        list_to_complete.notes = notes

        # Now, update the inventory based on the shopping list
        recent_list = db.session.query(ShoppingLists, Inventory).join(Inventory, ShoppingLists.item_id == Inventory.item_id).filter(ShoppingLists.list_id == list_id).all()

        for entry, inventory_item in recent_list:
            # Get the hidden form inputs for item_id and quantity
            item_id = request.form.get(f"item_id_{entry.entry_id}")
            quantity = request.form.get(f"quantity_{entry.entry_id}")

            if item_id and quantity:
                # Update the inventory's total quantity
                inventory_item.total_quantity += int(quantity)
        
        # Commit all changes to the database
        db.session.commit()

        flash("Shopping list marked as completed and inventory updated successfully!")
    else:
        flash("Error: Shopping list not found.")

    return redirect("/shopping_list")


if __name__ == "__main__":
    app.run(debug=True)