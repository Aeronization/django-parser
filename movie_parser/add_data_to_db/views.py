import requests
from bs4 import BeautifulSoup
import os
import zipfile
import io
import csv

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin

# (R. Friel - January 12, 2021) - import all constants and models.
from .constants import CLIENT_URL, CLIENT_DELIMITER
from .models import Movie, Genre

# Create your views here.
class HomeView(SuccessMessageMixin, TemplateView):
    template_name = "add_data_to_db/home.html"
    success_message = "New movies added to the database!"

    def get(self, request, *args, **kwargs):
        # (R. Friel - January 12, 2021) - Make a simple GET request to the url provided by client to retrieve movie data.
        zip_url = ""
        response = requests.get(CLIENT_URL)

        # (R. Friel - January 12, 2021) - Ensure response has a status code of 200.
        if not response.status_code == 200:
            response.raise_for_status()

        # (R. Friel - January 12, 2021) - Inside of the response content should be another zip file url,
        # which will contain the data we need.
        # Use beautiful soup to find the href.
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            if ".zip" in link['href']:
                zip_url = link['href']

        # (R. Friel - January 12, 2021) - Call the other methods to download zip contents, then add new entries to db.
        self.download_zip_contents(url=zip_url)
        self.add_new_movies_to_database()

        return super().get(request, *args, *kwargs)


    def download_zip_contents(self, url,  *args, **kwargs):
        """
        (R. Friel - January 12, 2021)
        Will download and save all zip contents to the current directory.

        Args:
            url ([str]): [The url pointing to zip file.]
        """

        save_path = os.getcwd() + "/zip_contents"

        if url:

            # (R. Friel - January 12, 2021) - This will save contents from the get request to the zip_contents directory.
            response = requests.get(url)
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            zip_file.extractall(save_path)


    def add_new_movies_to_database(self, *args, **kwargs):
        """
        (R. Friel - January 12, 2021)
        Will download and save all zip contents to the current directory.
        """

        # (R. Friel - January 12, 2021) - Get the path to the text file we require.
        file_location = os.getcwd() + "/zip_contents/cornell movie-dialogs corpus/movie_titles_metadata.txt"

        # (R. Friel - January 12, 2021) - Was returning an error without the iso-8859-1 encoding.
        with open(file_location, 'r', newline='', encoding = 'iso-8859-1') as opened_file:
            reader = csv.reader(opened_file, delimiter='\n')

            for row in reader:

                # (R. Friel - January 12, 2021) - This will take the current row and return an updated row
                # that is a string. Better than using str(row).
                updated_row = ''.join([str(character) for character in row])
                split_row = updated_row.split(CLIENT_DELIMITER)

                # (R. Friel - January 12, 2021) - Print out raw data from file.
                # for part in split_row:
                #     print(part)
                #     print(type(part))

                # (R. Friel - January 12, 2021) - For this part, we need to assume that our Schema has not changed to be successful.
                # Ensure values are of the right type.
                movie_id = str(split_row[0])
                movie_title = str(split_row[1])
                movie_year = str(split_row[2]) # Must be a string to account for /I in some movie years.
                movie_rating = float(split_row[3])
                number_of_votes = int(split_row[4])

                # (R. Friel - January 12, 2021) - The genres come back as a string, we need to split back into a set.
                # and remove any bad characters.
                updated_genres: list = []
                genres = split_row[5].split(",")
                for genre in genres:
                    genre = genre.replace("[","")
                    genre = genre.replace("]","")
                    genre = genre.replace('"', "")
                    genre = genre.replace("'", "")
                    genre = genre.replace(" ", "")
                    updated_genres.append(genre)


                # (R. Friel - January 12, 2021) - Print everything out if you want to check the values.
                # print(f"{movie_id}, {movie_title}, {movie_year}, {movie_rating}, {number_of_votes}, {updated_genres}")

                movie, created = Movie.objects.get_or_create(
                    movie_id = movie_id,
                    movie_title = movie_title,
                    movie_year = movie_year,
                    imbd_rating = movie_rating,
                    number_of_imdb_votes = number_of_votes
                )

                for genre in updated_genres:
                    found_genre, created = Genre.objects.get_or_create(
                        genre_name = genre
                    )
                    movie.genre.add(found_genre)
