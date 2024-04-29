# fastapi-todolist
## Short Description
This is a small todo project for testing out FastAPI capabilities and gaining the experience necessary to
work with web applications using front and back -end communication via frontend's JavaScript's fetches.<br>
This is also my university-related project.<br>
I know this project probably has massive security-related (and not only security-related) issues, which I might fix later,
however, if you wish (for some reason) to point some of 
them out to me, don't be shy and create an Issue. I might take a look at it later.
## How To Run
No matter the system you use, you must have 'uvicorn' and python 3.10+ installed.
(Next time I will try to understand how Docker works to make it easier for everybody,
but for now this will have to do).
Open terminal in the project's root folder and type:<br>
`uvicorn main:app --reload`<br>
This will start the server on `localhost:8000`.<br>
Now open up your favourite browser and go to the address mentioned above.<br>
That's basically it. The frontend is pretty intuitive.<br>
`python3 main.py` or `python main.py` will NOT work. Believe me, I tried.<br>
I guess if you make some minor changes to the code it will, but I was satisfied with
using uvicorn.
That's it. Thanks:)