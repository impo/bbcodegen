from os.path import join as path_join
import subprocess
import tempfile
import logging
from bbcodegen.util import absoluteFilePaths, largestFiles


def mkScreenshot(file, outputDir, offset):
    """ Make a screenshot from file in specified output dir, with the specified offset

    Keyword arguments:
    file -- input file (full path)
    outputDir -- directory to write screenshot to
    offset -- how many seconds into the file to pull the screenshot from
    """

    ffmpeg_args = [
        "ffmpeg",
        "-loglevel",
        "fatal",
        "-ss",
        str(offset),
        "-i",
        file,
        "-vf",
        "scale=\'iw:trunc(iw/dar)\',setsar=1/1", # Make sure we output square pixels
        "-frames:v",
        "1",
        path_join(outputDir, "ss" + str(offset).zfill(5) + ".png"),
    ]

    try:
        subprocess.run(ffmpeg_args, check=True)
    except subprocess.CalledProcessError:
        logging.critical(
            "Error running ffmpeg! Check if ffmpeg is installed and in your PATH."
        )
        raise

    return True


def getDuration(file_path, interval):
    """ Get duration of video file (in seconds)
    """

    ffprobe_args = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]

    # Run ffprobe to query duration of file
    try:
        p = subprocess.run(ffprobe_args, capture_output=True, check=True)
        duration = p.stdout.decode()
    except subprocess.CalledProcessError:
        logging.critical(
            "Error running ffprobe! Check if ffprobe is installed and in your PATH."
        )
        raise

    parsed_duration = int(float(duration.strip()))

    # Check if interval is too long.
    if parsed_duration < interval:
        raise ValueError(
            "The input file ("
            + str(parsed_duration)
            + " seconds) must be longer than the "
            "interval (" + str(interval) + " seconds)."
        )

    return parsed_duration


def getDurationCount(file_path, interval):
    duration = getDuration(file_path, interval)
    count = duration // interval
    logging.info(
        "Input file is " + str(duration) + " seconds long. "
        "This will generate " + str(count) + " screenshots."
    )

    return (duration, count)


def mkScreenshots(file_path, interval, max_shots):
    """ Make screenshots from file, with the specified interval between screenshots

    Keyword arguments:
    file -- input file (full path)
    interval -- interval between screenshots (seconds)
    max_shots -- upper limit imposed by user on number of shots
    """

    # Counts number of shots to generate and prints message with max # of shots
    (_, count) = getDurationCount(file_path, interval)

    # Generate screenshots in tmpdir and remove tmpdir
    tmpdir = tempfile.TemporaryDirectory()
    for i in range(1, count + 1):
        mkScreenshot(file_path, tmpdir.name, i * interval)

    # Get the largest screenshots limited to args.num
    screenshots = absoluteFilePaths(tmpdir.name)
    if max_shots:
        screenshots = largestFiles(screenshots, max_shots)

    logging.info("Done making and processing screenshots.")

    return (tmpdir, screenshots)