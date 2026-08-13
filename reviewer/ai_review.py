import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq() # reads GROQ_API_KEY from environment automatically

class ReviewFailedError(Exception):
    pass

def validate_comments(comments: list, files: list) -> list:
    """
    Filters out any comment whose (file, line) doesn't correspond to
    a real added line in the parsed diff. Protects against the model
    hallucinating file/line references that don't actually exist.
    Skips any comment that's missing expected fields entirely.
    """

    valid_locations = set()
    for file in files:
        filename = file["filename"]
        for line_num, _ in file["added_lines"]:
            valid_locations.add((filename, line_num))

    validated = []
    for comment in comments:
        
        try:
            file_name = comment["file"]
            line_num = comment["line"]

        except KeyError:
            continue

        if (file_name, line_num) in valid_locations:
            validated.append(comment)

    return validated

def review_diff(files: list) -> list:
    """
    Takes the parsed diff (from parse_diff()) and returns a list of review
    comment dicts: [{"file": ..., "line": ..., "severity": ..., "message": ...}, ...]
    """
    
    diff_summary = ""
    for file in files:
        diff_summary += f"File: {file['filename']}\n"
        for line_num, content in file["added_lines"]:
            diff_summary += f"line {line_num}: {content}\n"

    system_prompt = """You are a code reviewer. You must respond with ONLY a JSON object shaped like:
{"comments": [{"file": "...", "line": 12, "severity": "...", "message": "..."}]}

severity must be exactly one of: "critical", "warning", or "info". Do not use any other value.

If you find nothing worth flagging in the code, respond with {"comments": []} — do not invent minor or trivial issues just to have something to report."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diff_summary},
        ],
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content

    try:
        data = json.loads(raw_content)
        comments = data["comments"]
        return validate_comments(comments, files)
    except (json.JSONDecodeError, KeyError) as e:
        raise ReviewFailedError("The AI review response could not be parsed.") from e
