# get put post delete todolist
import json
from secrets import token_hex
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse, FileResponse
from fastapi.requests import Request

import sqlite3

from starlette.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(static_dir="static", )

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.get("/")
async def root(request: Request):
    auth = request.cookies.get("auth")
    if auth is not None and auth != "":
        try:
            db = sqlite3.connect("todo.db")
            cursor = db.cursor()
            user_id = cursor.execute("SELECT id FROM Users WHERE session_token = ?", (auth,)).fetchone()[0]
            tasks = cursor.execute("SELECT * FROM Tasks WHERE owner = ?", (user_id,)).fetchall()
            cursor.close()
            db.close()
            tasks_dict = []

            for i in tasks:
                task_dict = {}
                (task_dict["id"], task_dict["title"],
                 task_dict["status"], task_dict["description"], task_dict["owner"], task_dict["creation_date"]) = i
                tasks_dict.append(task_dict)
            r = json.dumps(tasks_dict)
            return FileResponse("static/home.html", media_type="text/html", headers={"tasks": f"{r}"})
        except Exception as e:
            return f"Unexpected error. {e}"
    else:
        return FileResponse("static/login.html", media_type="text/html")


@app.post("/")
async def root(request: Request):
    auth = request.cookies.get("auth")
    if auth is not None and auth != "":
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
            return f"Unexpected error. {e}"
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
                       , (user_login, user_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
        db.commit()
        cursor.close()
        db.close()
        return RedirectResponse("/", headers={"status": "success"}, status_code=307)
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
    expire_date = cursor.execute("SELECT session_expire_date FROM Users WHERE session_token = ?",
                                 (auth_cookie,)).fetchone()
    if expire_date is not None:
        if datetime.now() < datetime.strptime(expire_date[0], "%Y-%m-%d %H:%M:%S.%f"):
            cursor.close()
            db.close()
            return "You are already signed in."
        else:
            return "Session expired"

    # get the user data from headers
    user_login = request.headers.get("login")
    user_password = request.headers.get("password")

    """
    the code below is for authentication purposes
    """
    try:
        cursor.execute("SELECT * FROM Users WHERE login = ?", (user_login,))  # this tries to find user with given login
        user = cursor.fetchone()
        if user is not None:  # if user was found, proceed further
            if user_password == user[2]:  # this line checks whether the given password checks out with the actual one
                hash_func = token_hex(16)  # here we create session token for cookie
                response.set_cookie("auth", hash_func, expires=3600)  # expires in 3600s = 1 hour
                cookie_expiration = datetime.now() + timedelta(hours=1)
                cursor.execute("UPDATE Users SET session_token = ?, session_expire_date = ? WHERE id = ?"
                               , (hash_func, cookie_expiration, user[0]))
                db.commit()
                cursor.close()
                db.close()
                return response.body
        else:
            return "Login failed."  # if user was not found then this user does not exist
    except Exception as e:
        return f"Login failed. {e}"


@app.post("/login")
async def login(request: Request, response: Response):
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    auth_cookie = request.cookies.get("auth")
    expire_date = cursor.execute("SELECT session_expire_date FROM Users WHERE session_token = ?",
                                 (auth_cookie,)).fetchone()
    if expire_date is not None:
        if datetime.now() < datetime.strptime(expire_date[0], "%Y-%m-%d %H:%M:%S.%f"):
            cursor.close()
            db.close()
            return "You are already signed in."
        else:
            cursor.close()
            db.close()
            return "Session expired"

    # get the user data from headers
    user_login = request.headers.get("login")
    user_password = request.headers.get("password")

    """
        the code below is for authentication purposes
    """
    try:
        cursor.execute("SELECT * FROM Users WHERE login = ?",
                       (user_login,))  # this tries to find user with given login
        user = cursor.fetchone()
        if user is not None:  # if user was found, proceed further
            if user_password == user[2]:  # this line checks whether the given password checks out with the actual one
                hash_func = token_hex(16)  # here we create session token for cookie
                response.set_cookie("auth", hash_func, expires=3600)  # expires in 3600s = 1 hour
                cookie_expiration = datetime.now() + timedelta(hours=1)
                cursor.execute("UPDATE Users SET session_token = ?, session_expire_date = ? WHERE id = ?"
                               , (hash_func, cookie_expiration, user[0]))
                db.commit()
                cursor.close()
                db.close()
                return response.body
        else:
            return "Login failed."  # if user was not found then this user does not exist
    except Exception as e:
        return f"Login failed. {e}"


@app.put("/logout")
async def logout(request: Request, response: Response):
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    current_session = request.cookies.get("auth")
    try:
        user_id = cursor.execute("SELECT id "
                                 "FROM Users WHERE session_token = ?", (current_session,)).fetchone()[0]
        cursor.execute("UPDATE Users SET session_token = ?, session_expire_date = ? WHERE id = ?", ("", "", user_id))
        response.set_cookie("auth", "")
        response.body = "Successfully logged out."
        cursor.close()
        db.close()
        return response
    except Exception as e:
        cursor.close()
        db.close()
        return "Something went wrong."


@app.get("/login")
async def login():
    return "Method is not supported to /login."


@app.get("/logout")
async def logout():
    return "Cannot send GET request to /logout. Please get the hell out."
