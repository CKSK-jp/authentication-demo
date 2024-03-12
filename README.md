# User Authentication App with Flask

This is a simple user authentication web application built with Flask. It allows users to register, log in, and perform various actions based on their authentication status.

## Features

- User Registration: Users can create new accounts by providing a unique username and a secure password. Passwords are hashed using bcrypt for enhanced security.
- User Login: Registered users can log in securely using their username and password credentials.
- User Authentication: The app authenticates users using their stored credentials and provides access to restricted content and features.
- Account Management: Registered users can view and manage their account details, including updating their profile and deleting their account.
- Feedback System: Users can provide feedback by submitting text entries, which are stored and displayed on the website.
- Password Hashing: The app uses the bcrypt hashing algorithm to securely store user passwords in the database.

## Technologies Used

- Flask: Python web framework used for building the application.
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapping (ORM) library used for database operations.
- psycopg2: PostgreSQL adapter for Python used to interact with the PostgreSQL database.
- bcrypt: Password hashing library used to securely hash user passwords.
- HTML/CSS: Frontend markup and styling for web pages.
- Jinja2: Templating engine for rendering dynamic content in HTML templates.

## Getting Started

To run the application locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies listed in `requirements.txt` using `pip install -r requirements.txt`.
3. Set up a PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database connection string.
4. Run the Flask application by executing `python app.py` in your terminal.
5. Open your web browser and navigate to `http://localhost:5000` to access the application.

## File Structure

- `app.py`: Main Flask application file containing the routes and logic for user authentication and other functionalities.
- `forms.py`: Python file defining the WTForms for user registration, login, and feedback submission.
- `models.py`: Python file defining the database models using SQLAlchemy, including the `AuthUser` and `Feedback` models.
- `templates/`: Directory containing HTML templates for rendering web pages.
- `static/`: Directory containing static files such as CSS stylesheets and client-side JavaScript files.

