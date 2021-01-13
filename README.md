# django movie parser
This project will send an HTTP request to http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html

### Logic
After recieving a response, the project will then parse the HTML and find any ".zip" urls that are available.
Then send a http request to the zip file url and save the contents.

### Logic Continued
Once the zip file contents are saved, the project will then search for the "movie_titles_metadata.txt" file.
Next the file will be opened and parsed to retrieve all of the movie details available.
The details will then be saved to the database in two different models. Movie & Genre.

#### Requirements
The requirements for this project can be found in the requirements.txt file.
However the following modules are needed to run this project.
django
requests
beautifulsoup4

#### Running this project
To run this project locally please follow these steps.
1) Please clone this repository.
2) Create a virtual environment and activate it. Use this code:
```python
python3 venv -m venv
source venv/bin/activate
```
3) Now that the virtual environment is created and active, make sure to install the requirments. Use this code:
```python
pip3 install -r requirements.txt
```
4) Now that all requirements are met, we are ready to run our application. The migrations should already be handled, but if you need to start fresh please run this code to handle migrations.
```python
python3 manage.py makemigrations
python3 manage.py migrate
```
5) All requirements and migrations have been run, We now need a super user. Use this code and follow the prompts:
```python
python3 manage.py createsuperuser
```
6) We can now run our server. There is only two pages available. The home page and the admin page. Run this code:
```python
python3 manage.py runserver
```
7) The server is now running, visit localhost:8000 and you should see some text prompting you to visit the admin interface. You can confirm that the movies have been added to the database here.
8) Go to localhost:8000/admin and login with the super user credentials you made earlier.
9) Look at the Movies and Genres, there should be plenty that are populated.
