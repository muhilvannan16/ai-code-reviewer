import sys

from reviewer.git_diff import get_staged_diff, parse_diff
from reviewer.ai_review import review_diff, ReviewFailedError
from reviewer.display import display_review


def main():
    diff_text = get_staged_diff()

    if not diff_text:
        sys.exit(0)

    parsed_files = parse_diff(diff_text)

    try:
        comments = review_diff(parsed_files)
    except ReviewFailedError:
        print("⚠️  Code review failed to run. Proceeding without review.")
        sys.exit(0)

    display_review(comments)

    has_critical = any(comment["severity"] == "critical" for comment in comments)

    if has_critical:
        print("❌ Critical issue found. Commit blocked. Use `git commit --no-verify` to override.")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
