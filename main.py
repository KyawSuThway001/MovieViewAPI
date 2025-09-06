import requests
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ['API_KEY']
BASE_URL = "https://api.themoviedb.org/3/"
QUERY = {
    "api_key": API_KEY
}

img_url = "https://image.tmdb.org/t/p/w500"
watch_url = "https://www.youtube.com/watch?v="


app = Flask(__name__)


@app.route("/")
def home():


    now_playing_url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    now_playing_respond = requests.get(url=now_playing_url, params=QUERY)
    now_playing_movies = now_playing_respond.json()['results']

    popular_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=8"
    popular_respond = requests.get(url=popular_url, params=QUERY)
    popular_movies = popular_respond.json()['results']

    top_rated_url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=3"
    top_rated_respond = requests.get(url=top_rated_url, params=QUERY)
    top_rated_movies = top_rated_respond.json()["results"]

    up_coming_url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    up_coming_respond = requests.get(url=up_coming_url, params=QUERY)
    up_coming_movies = up_coming_respond.json()["results"]

    coming_url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=7"
    coming_respond = requests.get(url=coming_url, params=QUERY)
    coming_movies = coming_respond.json()["results"]

    return render_template("home.html",
                           now_playing_movie=now_playing_movies,
                           popular_movie=popular_movies,
                           top_rated_movie=top_rated_movies,
                           up_coming_movie=up_coming_movies,
                           coming_movie=coming_movies,
                           photo_path=img_url)


@app.route("/search", methods=["Get", "POST"])
def search():
    search_params = {
        "api_key": API_KEY,
        "query": request.form['search_data'],
        "include_adult": "false",
        "language": "en-US",
        "page": "1",

    }
    if request.method == "POST":
        search_url = f"https://api.themoviedb.org/3/search/movie"
        search_request = requests.get(url=search_url, params=search_params)
        # request_id = search_request.json()
        search_data = search_request.json()['results']
        return render_template("search_movie.html", data=search_data, photo=img_url)
    return render_template("home.html")


@app.route("/search_movie_detail/<int:m_id>", methods=["GET", "POST"])
def search_movie_detail(m_id):
    movie_id = m_id
    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    youtube = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US"

    respond = requests.get(url=youtube, params=QUERY)
    if "results" not in respond.json():
        return render_template("no_data.html")
    if not respond.json()['results']:
        return render_template("no_data.html")
    data = respond.json()['results'][-1]
    use_url = ""
    if data:
        use_url = data['key']
    detail_respond = requests.get(url=detail_url, params=QUERY)
    detail_data = detail_respond.json()
    return render_template("search_movie_detail.html", all_movie=data, all_data=detail_data, image=img_url, y_url=use_url, y_path=watch_url)

@app.route("/actor")
def actor_name():

    END_POINT = "person/popular?language=en-US&page="
    def get_data(id):
        url = f"{BASE_URL}{END_POINT}{id}"
        actor_data_respond = requests.get(url, params=QUERY)
        data = actor_data_respond.json()["results"]

        return data
    actor_one = get_data("4")
    actor_two = get_data("5")
    actor_three = get_data("8")
    actor_four = get_data("1")
    actor_five = get_data("2")


    return render_template('actor.html',
                           actor_one=actor_one,
                           actor_two=actor_two,
                           actor_three=actor_three,
                           actor_four=actor_four,
                           actor_five=actor_five,
                           image_path=img_url,
                           )


@app.route("/actor_detail/<string:actor_id>")
def actor_detail(actor_id):


    actor_detail_url = f"https://api.themoviedb.org/3/person/{actor_id}?language=en-US"
    actor_detail_respond = requests.get(url=actor_detail_url, params=QUERY)
    data = actor_detail_respond.json()

    actor_one_url = "https://api.themoviedb.org/3/person/popular?language=en-US&page=4"
    actor_one_respond = requests.get(url=actor_one_url, params=QUERY)
    actor_one_data = actor_one_respond.json()["results"]



    return render_template('actor_detail.html', data=data,
                           actor_one_datas=actor_one_data, image_path=img_url)


@app.route("/actor_search", methods=["GET", "POST"])
def actor_search():
    actor_search_url = "https://api.themoviedb.org/3/search/person"
    query = {
        "api_key": API_KEY,
        "query": request.form["search_data"],
        "include_adult": 'true',
        'language': 'en-US',
        'page': '1'
    }
    actor_search_respond = requests.get(url=actor_search_url, params=QUERY)
    data = actor_search_respond.json()['results']
    return render_template('search_actor.html', data=data, image_path=img_url)


@app.route("/series")
def series():
    END_POINT = "?language=en-US&page="
    channel = "tv/"
    def get_data(tv_data, id):
        url = f"{BASE_URL}{channel}{tv_data}{END_POINT}{id}"
        series_respond = requests.get(url, params=QUERY)
        data = series_respond.json()["results"]
        return data

    series_one = get_data("popular", 3)
    series_two = get_data("airing_today", 1)
    series_three = get_data("airing_today", 1)
    series_four = get_data("popular", 5)
    series_five = get_data("airing_today", 2)


    playing_url = "https://api.themoviedb.org/3/tv/airing_today?language=en-US&page=1"
    playing_respond = requests.get(url=playing_url, params=QUERY)
    playing_series = playing_respond.json()['results']

    return render_template("series.html",
                           series_one=series_one,
                           series_two=series_two,
                           series_three=series_three,
                           series_four=series_four,
                           series_five=series_five,
                           photo_path=img_url, all_movie=series_two)


if __name__ == "__main__":
    app.run(debug=True)
