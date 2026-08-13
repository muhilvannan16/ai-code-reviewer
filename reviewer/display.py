from rich.console import Console
from rich.markup import escape

def display_review(comments: list) -> None:
    """
    Pretty-prints review comments to the terminal, color-coded by severity,
    grouped by file and sorted by line number.
    """
    console = Console()

    if not comments:
        console.print("[green]No issues found.[/green]")
        return

    severity_colors = {
        "critical": "red",
        "warning": "yellow",
        "info": "cyan"
    }

    sorted_comments = sorted(comments, key=lambda comment: (comment["file"], comment["line"]))

    for comment in sorted_comments:
        color = severity_colors.get(comment["severity"], "white")

        raw_text = f"[{comment['file']}:{comment['line']}] {comment['severity'].upper()}: {comment['message']}"

        safe_text = escape(raw_text)

        console.print(f"[{color}]{safe_text}[/]")