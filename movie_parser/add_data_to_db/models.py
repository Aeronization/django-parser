from django.db import models

# (R. Friel - January 12, 2021) - I am creating the models here based on the Schema present in the README.txt available from the zip file. - 
# Because a movie can have multiple generes I created a second model for Genre, and will reference it to the Movie model
# via ManyToMany field. As a Movie can have many genres, and a Genre can be related to many different movies.


class Genre(models.Model):
    genre_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_id = models.CharField(max_length=128)
    movie_title = models.CharField(max_length=128)
    movie_year = models.CharField(max_length=128)
    imbd_rating = models.FloatField()
    number_of_imdb_votes = models.IntegerField()
    genre = models.ManyToManyField(Genre, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_title