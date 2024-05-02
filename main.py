import json
from secrets import token_hex
from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse, FileResponse
from fastapi.requests import Request

import sqlite3

from starlette.staticfiles import StaticFiles

app = FastAPI(static_dir="static", )

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

"""
backend -> json -> frontend

3 layers: controller, service, repository (folders) (look up mvc)

auth function

on first line: with db connection...
------------------------
.../tasks

GET -- все

/tasks/{id}

PUT
{
  "action": "CLOSE" | "OPEN"
}

/tasks
POST
{
  "title": "...",
  "description": "...",
}

/tasks/{id}
DELETE
no-content
------------------------
try page-request

try jwt

lookup multiple connections to db (connection pool)

from pydantic import BaseModel 

(data classes possibly) other library
----------------------- js frameworks
react.js / vue.js / typescript
----------------------- web-server
nginx if frontend reworked
-----------------------
"""

@app.get("/")
async def root(request: Request):
    # connecting to the db
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    auth = request.cookies.get("auth")
    # if authorized
    if auth is not None and auth != "":
        expire_date = cursor.execute("SELECT session_expire_date FROM Users WHERE session_token = ?",
                                     (auth,)).fetchone()
        if expire_date is not None:
            # if session token hasn't expired yet
            if datetime.now() < datetime.strptime(expire_date[0], "%Y-%m-%d %H:%M:%S.%f"):
                try:
                    user_id = cursor.execute("SELECT id FROM Users WHERE session_token = ?", (auth,)).fetchone()[0]
                    tasks = cursor.execute("SELECT * FROM Tasks WHERE owner = ?", (user_id,)).fetchall()
                    cursor.close()
                    db.close()
                    tasks_dict = []
                    # get all tasks
                    for i in tasks:
                        task_dict = {}
                        (task_dict["id"], task_dict["title"],
                         task_dict["status"], task_dict["description"], task_dict["owner"],
                         task_dict["creation_date"]) = i
                        tasks_dict.append(task_dict)
                    r = json.dumps(tasks_dict)
                    return FileResponse("static/home.html", media_type="text/html", headers={"tasks": f"{r}"})
                except Exception as e:
                    cursor.close()
                    db.close()
                    return f"Unexpected error. {e}"
            else:
                cursor.close()
                db.close()
                return FileResponse("static/login.html", media_type="text/html")
    else:
        cursor.close()
        db.close()
        return FileResponse("static/login.html", media_type="text/html")


@app.post("/")
async def root(request: Request):
    # connecting to the db
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    auth = request.cookies.get("auth")
    # if authorized
    if auth is not None and auth != "":
        expire_date = cursor.execute("SELECT session_expire_date FROM Users WHERE session_token = ?",
                                     (auth,)).fetchone()
        if expire_date is not None:
            # if session token hasn't expired yet
            if datetime.now() < datetime.strptime(expire_date[0], "%Y-%m-%d %H:%M:%S.%f"):
                try:
                    user_id = cursor.execute("SELECT id FROM Users WHERE session_token = ?", (auth,)).fetchone()[0]
                    tasks = cursor.execute("SELECT * FROM Tasks WHERE owner = ?", (user_id,)).fetchall()
                    cursor.close()
                    db.close()
                    tasks_dict = []
                    # get all tasks
                    for i in tasks:
                        task_dict = {}
                        (task_dict["id"], task_dict["title"],
                         task_dict["status"], task_dict["description"], task_dict["owner"],
                         task_dict["creation_date"]) = i
                        tasks_dict.append(task_dict)
                    r = json.dumps(tasks_dict)
                    return FileResponse("static/home.html", media_type="text/html", headers={"tasks": f"{r}"})
                except Exception as e:
                    cursor.close()
                    db.close()
                    return f"Unexpected error. {e}"
            else:
                cursor.close()
                db.close()
                return FileResponse("static/login.html", media_type="text/html")
    else:
        cursor.close()
        db.close()
        return FileResponse("static/login.html", media_type="text/html")


@app.post("/register")
async def register(request: Request):
    auth = request.cookies.get("auth")
    if auth is not None and auth != "":
        return Response("400 Bad Request", status_code=400)
    b = await request.json()
    # pydantic
    try:
        user_login = b["login"]
        user_password = b["password"]
    except Exception as e:
        print(e)
        return Response("400 Bad Request", status_code=400)
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


@app.put("/logout")
async def logout(request: Request, response: Response):
    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    current_session = request.cookies.get("auth")
    expire_date = cursor.execute("SELECT session_expire_date FROM Users WHERE session_token = ?",
                                 (current_session,)).fetchone()
    if current_session is None or current_session == "":
        return Response("400 Bad Request", status_code=400)
    elif expire_date is not None and datetime.now() >= datetime.strptime(expire_date[0], "%Y-%m-%d %H:%M:%S.%f"):
        return Response("403 Forbidden", status_code=403)
    try:
        user_id = cursor.execute("SELECT id "
                                 "FROM Users WHERE session_token = ?", (current_session,)).fetchone()
        print(user_id[0])
        cursor.execute("UPDATE Users SET session_token = ?,"
                       " session_expire_date = ? WHERE id = ?", ("", "", int(user_id[0])))
        response.delete_cookie("auth")
        response.body = "Successfully logged out."
        db.commit()
        cursor.close()
        db.close()
        print("LOGGED OUT")
        return response.body
    except Exception as e:
        print(f"EXCEPTION {e}")
        cursor.close()
        db.close()
        return "Something went wrong. {e}".format(e=e)


@app.get("/login")
async def login():
    return "Method is not supported to /login."


@app.get("/logout")
async def logout():
    return "Cannot send GET request to /logout. Please get the hell out."


@app.put("/change_task")
async def complete_task(request: Request):
    r = await request.json()
    try:
        task_id = r["id"]
        new_status = r["new_status"]
        if int(new_status) != 0 and int(new_status) != 1:
            return Response("400 Bad Request", status_code=400)
    except Exception as e:
        return Response(content="400 Bad Request", status_code=400)
    auth = request.cookies.get("auth")
    if auth is not None and auth != "":
        db = sqlite3.connect("todo.db")
        cur = db.cursor()
        expire_date = cur.execute("SELECT session_expire_date FROM Users WHERE session_token = ?", (auth,)).fetchone()
        if expire_date is not None and datetime.now() < datetime.strptime(expire_date[0], "%Y-%m-%d %H:%M:%S.%f"):
            user_id = cur.execute("SELECT id FROM Users WHERE session_token = ?", (auth,)).fetchone()[0]
            task_owner = cur.execute("SELECT owner FROM Tasks WHERE id = ?", (task_id,)).fetchone()[0]
            if user_id != task_owner:
                return Response("403 Forbidden", status_code=403)
            cur.execute("UPDATE Tasks SET status = ? WHERE id = ?", (new_status, task_id,))
            db.commit()
            cur.close()
            db.close()
            return Response("200 Success", status_code=200)
    return Response("403 Forbidden", status_code=403)


@app.post("/create_task")
async def create_task(request: Request):
    auth = request.cookies.get("auth")
    if auth is None or auth == "":
        return Response("403 Forbidden", status_code=403)

    db = sqlite3.connect("todo.db")
    cursor = db.cursor()
    expire_date = cursor.execute("SELECT session_expire_date FROM Users WHERE session_token = ?", (auth,)).fetchone()
    if datetime.now() >= datetime.strptime(expire_date[0], "%Y-%m-%d %H:%M:%S.%f"):
        return Response("403 Forbidden", status_code=403)

    r = await request.json()
    try:
        title = r["title"]
        description = r["description"]
        owner = cursor.execute("SELECT id FROM Users WHERE session_token = ?", (auth,)).fetchone()[0]
        cursor.execute("INSERT INTO Tasks (title, description, owner, creation_date) "
                       "VALUES (?, ?, ?, ?)", (title, description, owner, datetime.now()))
        db.commit()
        cursor.close()
        db.close()
        return Response("200 Success", status_code=200)
    except Exception as e:
        return Response("400 Bad Request", status_code=400)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
