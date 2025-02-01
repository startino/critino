import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_content(transcript_file, chunk_size=1000, chunk_overlap=100):
    """Chunks a transcript based on speaker turns/segments."""
    try:
        with open(transcript_file, 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)

        segments = []
        current_segment = ""
        current_speaker = None

        for entry in transcript_data:
            speaker = entry.get("speaker")
            text = entry.get("text")

            if speaker != current_speaker:
                if current_segment:
                    segments.append(current_segment)
                current_segment = text
                current_speaker = speaker
            else:
                current_segment += " " + text if current_segment else text

        if current_segment:
            segments.append(current_segment)

        all_chunks = []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )

        for segment in segments:
            chunks = splitter.split_text(segment)
            all_chunks.extend(chunks)

        return all_chunks

    except FileNotFoundError:
        print(f"Error: Transcript file not found: {transcript_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in transcript file: {transcript_file}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def chunk_content_streaming(transcript_file, chunk_size=1000, chunk_overlap=100):
    """Chunks a transcript in a streaming fashion."""
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )

    try:
        with open(transcript_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    speaker = entry.get("speaker")
                    text = entry.get("text")

                    if speaker and text:  # Check for missing keys
                        if speaker != current_speaker:
                            if current_segment:
                                chunks = splitter.split_text(current_segment)
                                all_chunks.extend(chunks)
                            current_segment = text
                            current_speaker = speaker
                        else:
                            current_segment += " " + text if current_segment else text

                except json.JSONDecodeError:
                    print(f"Warning: Skipping invalid JSON line: {line.strip()}")
                except Exception as e:
                    print(f"An unexpected error occurred in streaming: {e}")
                    return None

            if current_segment:
                chunks = splitter.split_text(current_segment)
                all_chunks.extend(chunks)
            return all_chunks

    except FileNotFoundError:
        print(f"Error: Transcript file not found: {transcript_file}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred in streaming file open: {e}")
        return None