import ffmpeg
import srt
from datetime import timedelta

def extract_audio(video_path: str, output_audio_path: str):
    """
    Extract audio from a video file as a WAV file.
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_audio_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr}")
        raise e

def create_srt_file(segments: list, output_srt_path: str):
    """
    Create an SRT subtitle file from transcription segments.
    """
    subtitles = []
    for i, segment in enumerate(segments):
        start = timedelta(seconds=segment['start'])
        end = timedelta(seconds=segment['end'])
        text = segment.get('translated_text', segment['text']).strip()

        subtitles.append(
            srt.Subtitle(index=i+1, start=start, end=end, content=text)
        )

    with open(output_srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitles))

def merge_audio_video(video_path: str, audio_path: str, output_video_path: str):
    """
    Merge the new translated audio with the original video.
    """
    try:
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        # Replace audio stream, map video from original and audio from new file
        (
            ffmpeg
            .output(input_video.video, input_audio.audio, output_video_path, vcodec='copy', acodec='aac')
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        print(f"Error merging audio/video: {e.stderr}")
        raise e
