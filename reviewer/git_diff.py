import subprocess
import re

def get_staged_diff() -> str:
    """
    Runs `git diff --staged` and returns the diff output as a string.
    """
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,   
        text=True
    )

    return result.stdout

def parse_diff(diff_text: str) -> list:
    """
    Parses git diff text into a list of dicts:
    [{"filename": ..., "added_lines": [(line_num, content), ...]}, ...]
    """
    files = []
    current_file = None
    current_new_line = None

    lines = diff_text.split("\n")

    for line in lines:
        if line.startswith("diff --git"):
            if current_file is not None:
                files.append(current_file)
                
            parts = line.split()
            if len(parts) >= 4:
                new_filename = parts[3][2:] # Strip the "b/" prefix
                current_file = {"filename": new_filename, "added_lines": []}
            else:
                current_file = None
            

        elif line.startswith("@@"):
            # This is a hunk header line (@@ -1,3 +1,4 @@) — extract the starting line number
            match = re.search(r"\+(\d+)", line)
            current_new_line = int(match.group(1)) if match else None

        elif line.startswith("+++"):
            # This is a file header line (+++ b/README.md), not a real added line — skip it
            continue

        elif line.startswith("+"):
            if current_file is not None and current_new_line is not None:
                current_file["added_lines"].append((current_new_line, line[1:]))
                current_new_line += 1
                
        elif line.startswith("-"):
            # Removed line — doesn't exist in the new file, so no line-number bookkeeping needed
            pass

        else:
            if current_new_line is not None:
                current_new_line += 1

    if current_file is not None:
        files.append(current_file)

    return files

