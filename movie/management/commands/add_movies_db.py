from django.core.management.base import BaseCommand
from movie.models import Movie
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        json_file_path = 'movie/management/commands/movies.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)

        for i, item in enumerate(movies[:100]):
            # Mapea los campos reales del dataset
            title = item.get('Series_Title', 'Sin título')
            description = item.get('Overview', 'Sin descripción')
            genre = item.get('Genre', 'Desconocido')
            year = item.get('Released_Year', None)

            # Evita duplicados por título
            exist = Movie.objects.filter(title=title).first()
            if not exist:
                Movie.objects.create(
                    title=title,
                    description=description,
                    genre=genre,
                    year=year,
                    image='movie/images/default.jpg'  # imagen por defecto
                )

        self.stdout.write(self.style.SUCCESS('Se cargaron hasta 100 películas correctamente.'))


