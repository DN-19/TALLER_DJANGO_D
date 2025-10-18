from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie
# Create your views here.

def home(request):
   # return HttpResponse('<h1>Welcome to Home Page</h1>')
   #return render(request, 'home.html')
   # return render(request, 'home.html', {'name':'Daniel Nohava'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})


def about(request):
    #return HttpResponse('<h1>Welcome to About page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64 

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}

    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # -------------------- FALTANTE: gráfica por género (primer género) --------------------
    # Contar películas por primer género
    movies_by_genre = {}
    for movie in all_movies:
        first_genre = (movie.genre or 'Unknown').split(',')[0].strip()
        movies_by_genre[first_genre] = movies_by_genre.get(first_genre, 0) + 1

    # Crear gráfica de barras por género
    plt.figure()
    g_positions = range(len(movies_by_genre))
    plt.bar(g_positions, movies_by_genre.values(), align='center')
    plt.title('Movies per genre (first genre)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(g_positions, movies_by_genre.keys(), rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)

    # Convertir segunda gráfica a base64
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()
    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic_genre = base64.b64encode(image_png2).decode('utf-8')
    # --------------------------------------------------------------------------------------

    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {'graphic': graphic, 'graphic_genre': graphic_genre})
