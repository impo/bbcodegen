# bbcodegen
Generate BBCode for a given movie based upon its TMDB ID and its corresponding video file.

## Requirements:
* ffmpeg, ffprobe, mediainfo

## Usage:
```
usage: bbcodegen.py [-h] [-i INPUT] [--interval INTERVAL] [-n NUM] TMDB_ID

Generate BBCode for a movie based upon TMDB information and base media file.

positional arguments:
  TMDB_ID               ID for movie on TMDB

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file
  --interval INTERVAL   Take screenshot between each <INTERVAL> seconds of the video (default: 600)
  -n NUM                Number of screenshots to upload (default: 8)
  ```

## Example BBCode:
```
[center][size=4]Lady Audley's Secret (2000)[/size]
[size=3]Director: Betsan Morris Evans[/size]
[thumb=500]https://image.tmdb.org/t/p/original/cXSWxSTuTZKxWxa8DMydgnkxU1V.jpg[/thumb][/center]

[size=3][b]Plot: [/b][/size]
When Lucy Graham (Neve McIntosh) weds the much older Sir Michael Audley (Kenneth Cranham), his nephew Robert (Steven Mackintosh) is suspicious of the lovely young woman's motives. Soon, Robert's friend disappears, and Robert believes Lucy may be involved. But as he attempts to unearth the truth about Lucy's past, he finds himself irresistibly drawn to her dangerous allure. Betsan Morris Evans's period drama is based on the novel by Mary Elizabeth Braddon's.

[size=3][b]Cast: [/b][/size]
[pre]
Neve McIntosh              ... Lucy / Lady Audley
Juliette Caton             ... Alicia Audley
Melanie Clark Pullen       ... Phoebe
Kenneth Cranham            ... Sir Michael Audley
Steven Mackintosh          ... Robert Audley
Jamie Bamber               ... George Talboys
Bev Willis                 ... Duffield
David Glover               ... Marriner
[/pre]

[center][size=3][b]Screenshots:[/b][/size]
[thumb=300]https://ptpimg.me/87w12c.png[/thumb][thumb=300]https://ptpimg.me/si4rv8.png[/thumb][thumb=300]https://ptpimg.me/p4u95m.png[/thumb][thumb=300]https://ptpimg.me/h0x34t.png[/thumb][thumb=300]https://ptpimg.me/1f70p3.png[/thumb] [thumb=300]https://ptpimg.me/gy9l63.png[/thumb][thumb=300]https://ptpimg.me/777f00.png[/thumb][thumb=300]https://ptpimg.me/vcr877.png[/thumb]
[/center]
```