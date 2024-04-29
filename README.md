# FastAPI "To Do" Web Application
## Short Description
This is a small todo project for testing out FastAPI capabilities and gaining the experience necessary to
work with web applications using front and back -end communication via frontend's JavaScript's fetches.<br>
This is also my university-related project.<br>
I know this project probably has massive security-related (and not only security-related) issues, which I might fix later,
however, if you wish (for some reason) to point some of 
them out to me, don't be shy and create an Issue. I might take a look at it at some point.
## How To Run
No matter the system you use, you must have 'uvicorn' and python 3.10+ installed.<br>
If something isn't installed, `pip install "fastapi[all]"` should do the trick.<br>
(Next time I will try to understand how Docker works to make it easier for everybody,
but for now this will have to do).<br>
Open terminal in the project's **root folder** and type:<br>
`uvicorn main:app --reload`<br>
This will start the server on `localhost:8000`.<br>
Now open up your favourite browser and go to the address mentioned above.<br>
That's basically it. The frontend is pretty intuitive.<br>
`python3 main.py` or `python main.py` will NOT work. Believe me, I tried.<br>
I guess if you make some minor changes to the code it will, but I was satisfied with
using uvicorn.
That's it. Thanks:)
## How It Works
Basically, you have a backend.<br>
When you try to go the "/", you will first be redirected to "/login" and asked to sign in OR to log in, since
you don't have an active session (yes, I am using cookies for this).
Then you log in or register (after registration you will be asked to log in) and you are once
again redirected back to "/", where you will have your tasks! Your session lasts exactly 3600 seconds === 1 hour. After that you will be asked to log in.<br> To add a task you simply click
on a button on the right bottom corner (which is a plus sign) and write in a title and a description
and then press "Add".<br>
Now you have your first task, and you can mark it as complete using the "Mark As Complete" button.
<br>You can log out using the button in the bottom left corner.<br>
<br>That's basically it.
## What was used
- `Python 3.10`;
- `SQLite`;
- `SQL` requests;
- `CSS`;
- `HTML`;
- `JavaScript`;
- `.svg images`.
## _Maybe_ I will do this later
- Make the application safer to use;
- Add the ability to edit the ToDos;
- Add a profile page;
- Show completed ToDos at the end;
- Code style changes.
