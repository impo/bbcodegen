import argparse
import logging
import pyperclip
from bbcodegen.config import load_config
from jinja2 import Environment, PackageLoader
from datetime import date
from bbcodegen.screenshot import mkScreenshots
from bbcodegen.util import get_mediainfo
from bbcodegen import tmdb
from bbcodegen import ptpimg_uploader


def get_args_bbgen():
    parser = argparse.ArgumentParser(
        description="Generate BBCode for movie based upon TMDB information and base media file."
    )
    parser.add_argument(
        "tmdb_id", metavar="TMDB_ID", type=int, help="ID for movie on TMDB"
    )
    parser.add_argument(
        "template", metavar="JINJA_TEMPLATE", help="BBCode template to render"
    )
    parser.add_argument("-i", "--input", dest="input", help="Input file")
    parser.add_argument(
        "--interval",
        dest="interval",
        action="store",
        type=int,
        default=600,
        help="Take screenshot of the video every <INTERVAL> seconds (default: 600)",
    )
    parser.add_argument(
        "-n",
        dest="num",
        action="store",
        type=int,
        default=8,
        help="Number of screenshots to upload (default: 8)",
    )
    return parser.parse_args()


def main():
    args = get_args_bbgen()
    config = load_config()

    tmdb_key = config["tmdb"]["api_key"]

    local_video_data = {}

    # Take and upload screenshots (screenshot dir will cleanup at program exit)
    if args.input:
        (tmpdir, screenshots) = mkScreenshots(args.input, args.interval, args.num)
        local_video_data["screenshots"] = ptpimg_uploader.upload(config['ptpimg']['api_key'], screenshots)
        local_video_data["mediainfo"] = get_mediainfo(args.input)

    # Pull movie_information from TMDB
    movie_info = tmdb.getMovieInfo(args.tmdb_id, tmdb_key)
    movie_year = date.fromisoformat(movie_info["release_date"]).year
    (movie_cast, movie_directors) = tmdb.getMovieCast(args.tmdb_id, tmdb_key)

    # Pull poster from TMDB
    poster_path = movie_info["poster_path"]
    if poster_path:
        cover_url = tmdb.getPosterUrl(args.tmdb_id, tmdb_key, poster_path)
    else:
        logging.warning("TMDB movie poster path not found! Inserting placeholder.")
        cover_url = "COVER_URL_HERE"

    # Load and render template
    env = Environment(
        loader=PackageLoader("bbcodegen", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(args.template + ".j2")
    rendered = template.render(
        movie_info=movie_info,
        movie_year=movie_year,
        movie_directors=movie_directors,
        cover_url=cover_url,
        movie_cast=movie_cast,
        local_video_data=local_video_data,
    )

    try:
        pyperclip.copy(rendered)
    except pyperclip.PyperclipException: # This may pop up if we're working on a headless system
        pass

    print(rendered)


if __name__ == "__main__":
    main()
