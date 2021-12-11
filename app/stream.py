from vidgear.gears import WriteGear

from app import settings

# Define required FFmpeg optimizing parameters for `writer`.
output_params = {
    "-i": "app/resources/silence.mp3",
    "-acodec": "aac",
    "-ar": 44100,
    "-b:a": 712000,
    "-vcodec": "libx264",
    "-preset": "medium",
    "-b:v": "4500k",
    "-bufsize": "64k",
    "-pix_fmt": "yuv420p",
    "-f": "flv",
}

# Define writer with defined parameters and
stream = WriteGear(
    output_filename=f"rtmp://a.rtmp.youtube.com/live2/{settings.youtube_stream_key}",
    **output_params
)
