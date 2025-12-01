from flask import Flask, request, redirect, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "flaskuser",
    "password": "StrongPassword123!",  # change if you picked a different password
    "database": "cicd_flask_db",
}


def get_db_connection():
    """Create and return a new DB connection."""
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/", methods=["GET"])
def home():
    # Fetch tasks from DB
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title FROM tasks ORDER BY id DESC;")
        tasks = cursor.fetchall()
    except Error as e:
        print(f"DB error: {e}")
        tasks = []
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if title:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))
            conn.commit()
        except Error as e:
            print(f"DB error inserting task: {e}")
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass

    return redirect("/")


if __name__ == "__main__":
    # Host 0.0.0.0 so it’s accessible from outside the EC2 instance if needed
    app.run(host="0.0.0.0", port=5000, debug=True)

