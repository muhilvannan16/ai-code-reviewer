import argparse

from reviewer.git_diff import get_staged_diff, parse_diff
from reviewer.ai_review import review_diff, ReviewFailedError
from reviewer.display import display_review


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered code reviewer for staged git changes."
    )

    args = parser.parse_args()

    diff_text = get_staged_diff()

    if not diff_text:
        print("No staged changes found. Stage something with `git add` first.")
        return

    parsed_files = parse_diff(diff_text)
    try:
        comments = review_diff(parsed_files)
    except ReviewFailedError:
        print("⚠️  Code review failed to run. Proceeding without review.")
        return
    display_review(comments)


if __name__ == "__main__":
    main()
