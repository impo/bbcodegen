import requests
import logging


def getMovieInfo(tmdb_id, api_key):
    logging.info("Getting movie info for TMDB ID: {}".format(tmdb_id))
    url = r"https://api.themoviedb.org/3/movie/" + str(tmdb_id)
    payload = {"api_key": api_key}
    r = requests.get(url, params=payload)
    movie_info = r.json()
    return movie_info


def getMovieCast(tmdb_id, api_key):
    logging.info("Getting movie cast for TMDB ID: {}".format(tmdb_id))
    url = r"https://api.themoviedb.org/3/movie/" + str(tmdb_id) + r"/credits"
    payload = {"api_key": api_key}
    r = requests.get(url, params=payload)
    resp = r.json()
    # Pull first 8 cast members as top-billed cast
    (cast, crew) = (resp["cast"][:8], resp["crew"])
    directors = list(filter(lambda crew_member: crew_member["job"] == "Director", crew))
    return (cast, directors)


def getPosterUrl(tmdb_id, api_key, poster_path):
    logging.info("Getting poster url for TMDB ID: {}".format(tmdb_id))
    url = "https://api.themoviedb.org/3/configuration"
    payload = {"api_key": api_key}
    r = requests.get(url, params=payload)
    resp = r.json()["images"]

    """To build an image URL, you will need 3 pieces of data. The base_url, size and file_path. Simply combine them all and you will have a fully qualified URL."""

    base_url = resp["secure_base_url"]
    poster_size = resp["poster_sizes"][-1]
    return base_url + poster_size + poster_path
