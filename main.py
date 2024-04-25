# get put post delete todolist
import hashlib
import secrets
import time

from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse
from fastapi.requests import Request
import sqlite3

app = FastAPI()


@app.get("/")
async def root(request: Request, response: Response):
    auth = request.cookies.get("auth")
    if auth is not None or auth != "":
        try:
            db = sqlite3.connect("todo.db")
            cursor = db.cursor()
            user_id = cursor.execute("SELECT id FROM Users WHERE session_token = ?", (auth,)).fetchone()[0]
            tasks = cursor.execute("SELECT * FROM Tasks WHERE owner = ?", (user_id,)).fetchall()
            cursor.close()
            db.close()
            tasks_dict = []

            if not tasks:
                return "You have no tasks yet."

            for i in tasks:
                task_dict = {}
                (task_dict["id"], task_dict["title"],
                 task_dict["status"], task_dict["description"], task_dict["owner"], task_dict["creation_date"]) = i
                tasks_dict.append(task_dict)
            return tasks_dict
        except Exception as e:
            return "Unexpected error."
    else:
        return RedirectResponse("/login")


@app.post("/register")
async def register(request: Request):
    user_login = request.headers.get("login")
    user_password = request.headers.get("password")
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO Users (login, password, creation_date) VALUES (?, ?, ?)"
                       , (user_login, user_password, time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()),))
        db.commit()
        cursor.close()
        db.close()
        return f"Successfully added user {user_login}"
    except Exception as e:
        print(e)
        return RedirectResponse("/")


@app.get("/register")
async def register():
    return "GET method is not supported to /register."


@app.put("/login")
async def login(request: Request, response: Response):
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    auth_cookie = request.cookies.get("auth")
    user_name = cursor.execute("SELECT * FROM Users WHERE session_token = ?", (auth_cookie, )).fetchone()
    if user_name is not None:
        cursor.close()
        db.close()
        return "You are already signed in."
    print(auth_cookie)
    user_login = request.headers.get("login")
    user_password = request.headers.get("password")

    try:
        cursor.execute("SELECT * FROM Users WHERE login = ?", (user_login,))
        user = cursor.fetchone()
        if user is not None:
            if user_password == user[2]:
                hash_func = secrets.token_hex(16)
                response.set_cookie("auth", hash_func, expires=3600)
                print(user[0])
                cursor.execute("UPDATE Users SET session_token = ? WHERE id = ?", (hash_func, user[0]))
                db.commit()
                cursor.close()
                db.close()
                print("Login success")
                return response.body
        else:
            return "Login failed."
    except Exception as e:
        return f"Login failed. {e}"


@app.get("/login")
async def login():
    return "Method is not supported to /login."


@app.put("/logout")
async def logout(request: Request, response: Response):
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    current_session = request.cookies.get("auth")
    try:
        user_id = cursor.execute("SELECT id "
                                 "FROM Users WHERE session_token = ?", (current_session,)).fetchone()[0]
        cursor.execute("UPDATE Users SET session_token = ? WHERE id = ?", (user_id, "",))
        response.set_cookie("auth", "")
        response.body = "Successfully logged out."
        cursor.close()
        db.close()
        return response
    except Exception as e:
        cursor.close()
        db.close()
        return "Something went wrong."


@app.get("/logout")
async def logout():
    return "Cannot send GET request to /logout. Please get the hell out."
