# Note App

**Backend Setup**
First of all make sure that you are in \Note_app folder.
Yo must have installed Python, if you don't, you can download here: https://www.python.org/downloads/

## Create a virtual env to install the dependencies
```
python -m venv note_back/venv
```
## Active the virtual env
```
cd note_back/venv/Scripts
activate
```

## Install the dependencies
Go to the the backend folder of the app (note_back/notes) and install the dependencies:

```
pip install -r requeriments.txt
```

## Run the migrations
```
python manage.py makemigrations
python manage.py migrate
```

## Run the server
```
python manage.py runserver
```

## It's done, now you can setup the front of the app, register an user and use "Green Notes" 

**Frontend Setup**
Make sure you are in the frontend folder (/note_front)
Yo must have installed Node.js, if you don't, you can download here: https://nodejs.org/en/download/current

## Install Vue js in case you don't have it
```
npm i -g @vue/cli
```

## Install the dependencies
```
npm install
```

### run the development server
```
npm run serve
```

**Note:**
The backend of the app runs by default on http://127.0.0.1:8000 and the front on http://localhost:8080.
In case you change the default address and port that Django runs, 
put that address in the file settings.js, cause there is the route that the front use to fecth the api.

