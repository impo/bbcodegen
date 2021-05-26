import os
import logging
import subprocess

def absoluteFilePaths(directory):
    """Get full file paths within a specific directory

    Keyword arguments:
    directory -- directory path containing files
    """
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for f in sorted(filenames):
            files.append(os.path.abspath(os.path.join(dirpath, f)))
    return files


def largestFiles(files, limit=8):
    """Trims the files list to the specified limit, discarding the smallest files from the list
        Thanks to LeFirstTimer for the suggestion and sample code!

    Keyword arguments:
    files -- list of files (full paths)
    limit -- Maximum number of files
    """
    if len(files) <= limit:
        return files
    pairs = []
    for file in files:
        size = os.path.getsize(file)
        pairs.append((file, size))
    pairs.sort(key=lambda s: s[1], reverse=True)
    pairs = pairs[:limit]
    pairs.sort(key=lambda s: s[0])
    return [x[0] for x in pairs]


def get_mediainfo(file):
    mediainfo_args = [
        "mediainfo",
        file,
    ]
    try:
        p = subprocess.run(mediainfo_args, capture_output=True, check=True)
        result = p.stdout.decode()
    except subprocess.CalledProcessError:
        logging.critical(
            "Error running mediainfo! Check if mediainfo is installed and in your PATH."
        )
        raise
    return result.rstrip()
