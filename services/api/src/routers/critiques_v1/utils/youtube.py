from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re
import json
def get_video_id(url: str) -> str:
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)

def get_transcript(url: str) -> list: 
    try:
        video_id = get_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['en']  
        )
        return transcript 
    except NoTranscriptFound:
        raise ValueError("No English captions available for this video")
    except TranscriptsDisabled:
        raise ValueError("Captions are disabled for this video")
    except Exception as e:
        raise RuntimeError(f"Transcript error: {str(e)}") 

