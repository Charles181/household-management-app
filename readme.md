## Household Management app
#### Video Demo:  <URL HERE>
## Table of Contents
- [Description](#description)
- [Video Demo](#video-demo)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Future Features](#future-features)
- [Contributing](#contributing)
- [Contact Information](#contact-information)
## Description:
Household Management App is a web-based application designed to streamline household management tasks such as assigning tasks (TO-DO list), tracking inventory, and managing shopping lists. Built using Flask, the app provides users with an intuitive interface to organize household activities from any device with an internet connection.

### Inspiration

The idea for this app came from my personal experience as a busy father of two. With a full-time job and college classes in the evenings, my weekdays are packed, and I barely have time for household tasks. I leave home at 7:00 am and don’t get back until around 11:00 pm, which means the only time I can shop for groceries is on the weekend. However, I often find myself struggling to remember what I need to buy when I'm at the store.

My two sons, like many kids, love to snack between meals, and they don’t always tell me when we run out of something. This leads to constant confusion over what we actually have at home. I’ve lost count of the number of times I’ve had to call my wife or kids from the grocery store, asking them to check the fridge or pantry. Worse still, sometimes I’d come home only to realize I’d bought things we already had, or I’d forget to buy something important, only to discover later that it had expired!

On top of that, managing household tasks can be just as challenging. My wife and I often assign chores to our kids, but keeping track of what has or hasn’t been done requires constant reminders. I wanted a way for us to easily assign tasks, so the kids could see what they need to do directly on their phones, and we could check their progress without constant follow-up.

## Video Demo
Watch a demo of the app here: [Video Demo Link](<URL>)

## Features
- User registration (admin based) and login system.
- Role-based access (admin and user).
- Task management: create, assign, and mark tasks as completed.
- Inventory management: track household items and add items to a shopping list.
- Shopping list management: create, update, and mark shopping lists as completed.
- Mobile-friendly design.

## Technologies Used
- Flask (Python)
- SQLite (Database)
- SQLAlchemy (ORM)
- Bootstrap 5.3 (Frontend Framework)
- Jinja2 (Template Engine)
- JavaScript (for interactive features)

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/charles181/household-management-app.git
   ```
2. Navigate to the project directory:
   ```
   cd household-management-app
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the Flask app:
   ```
   flask run
   ```
6. Open your browser and go to `http://127.0.0.1:5000/`

## Usage
### Users:
1. Register an account (If not provided by an admin)
2. Login using your credentials
3. Logged in users can view or complete tasks assigned to them.

### Admins:
1. Login using your credentials
2. In the admin dashboard, admins can add users, add tasks, assign task to users, update inventory and create and manage shopping lists.

## File Structure
- `app.py`: The main Flask application file, contains the app’s routes.
- `helpers.py`: Helper functions (decorators @login_required and @admin_required).
- `models.py`: Defines the database models (Users, Tasks, Assignments, Inventory, etc.).
- `templates/`: Contains all HTML templates.
 - `layout.html`: Website's basic layout.
 - `assign.html`: Assign tasks to specific users and set due date.
 - `admin_dashboard.html`: Add users, add tasks, assign tasks to users, manage inventory and manage shopping lists.
 - `forbidden.html`: Page shown to unauthorized users that try to access an admin page.
 - `index.html`: Users's homepage where a summary of their activities and the pending activities for the current day are shown.
 - `inventory.html`: Inventory management, add and remove items. Sort items by quantity, category or item name.
 - `login.html`: Process user login.
 - `register.html`: Users registration form.
 - `shopping_list.html`: Shopping list management. Create shopping lists, sort lists by date. Displays most recent shopping list, with the option to mark as complete, which adds the items on it to the inventory.
 - `task_view.html`: Lets users select a date to view activities for selected date.
 - `view_shopping_list.html`: Detailed view of shopping lists.
- `static/`: Contains static files (bootstrap).
- `instance/`: Contains the app's database. 
- `requirements.txt`: Lists the Python dependencies required to run the project.

## Future Features
- Add task priority levels.
- Generate reports of completed tasks and shopping lists.
- Add email notifications for task assignments.
- Add email capabilities for shopping lists.
- More features.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## Contact Information
- Email: csantillanj@gmail.com
- GitHub: [charles181](https://github.com/charles181)