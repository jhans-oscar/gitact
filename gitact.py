#!/usr/bin/env python3

import sys
from datetime import datetime

import requests

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"


def describe_push(event):
    commits = event.get("payload", {}).get("commits", [])
    count = len(commits)
    noun = "commit" if count == 1 else "commits"
    return f"Pushed {count} {noun}"


def describe_issue(event):
    payload = event.get("payload", {})
    action = payload.get("action", "updated").capitalize()
    issue = payload.get("issue", {})
    number = issue.get("number")
    title = issue.get("title")
    if number and title:
        return f"{action} issue #{number}: {title}"
    if number:
        return f"{action} issue #{number}"
    return f"{action} an issue"


def describe_pull_request(event):
    payload = event.get("payload", {})
    action = payload.get("action", "updated").capitalize()
    pr = payload.get("pull_request", {})
    number = pr.get("number")
    title = pr.get("title")
    if number and title:
        return f"{action} pull request #{number}: {title}"
    if number:
        return f"{action} pull request #{number}"
    return f"{action} a pull request"


def describe_generic(event):
    etype = event.get("type", "Event")
    cleaned = etype.replace("Event", "").strip()
    label = cleaned or "Activity"
    return f"{label} activity"


EVENT_STYLES = {
    "PushEvent": ("⬆", GREEN, describe_push),
    "IssuesEvent": ("❗", YELLOW, describe_issue),
    "PullRequestEvent": ("⇋", BLUE, describe_pull_request),
    "WatchEvent": ("★", MAGENTA, lambda _: "Starred the project"),
}


def describe_event(event):
    etype = event.get("type")
    icon, color, builder = EVENT_STYLES.get(etype, ("•", CYAN, describe_generic))
    message = builder(event)
    return icon, color, message


def format_timestamp(raw_timestamp):
    try:
        stamp = datetime.strptime(raw_timestamp, "%Y-%m-%dT%H:%M:%SZ")
        return stamp.strftime("%b %d, %Y %H:%M UTC")
    except (TypeError, ValueError):
        return "Unknown time"


def print_banner(username):
    title = f" GitAct • @{username} "
    border = "─" * len(title)
    print(f"{BOLD}{BLUE}┌{border}┐{RESET}")
    print(f"{BOLD}{BLUE}│{RESET}{BOLD}{title}{RESET}{BOLD}{BLUE}│{RESET}")
    print(f"{BOLD}{BLUE}└{border}┘{RESET}")


def get_username():
    if len(sys.argv) < 2:
        print(f"{RED}Usage:{RESET} python gitactiv.py <username>")
        sys.exit(1)
    else:
        username = sys.argv[1].lower()
    return username


def url_request(username):
    base_url = "https://api.github.com/users"
    url = f"{base_url}/{username}/events"

    response = requests.get(url)

    if response.status_code == 200:
        events = response.json()
        return events

    elif response.status_code == 404:
        print(f"{RED}Error:{RESET} User '{username}' not found.")
    
    elif response.status_code == 403:
        print(f"{RED}Error:{RESET} Rate limit exceeded. Try again later.")

    else:
        print(f"{RED}Error:{RESET} GitHub API returned {response.status_code}")


def print_activity(events, username):
    if not events:
        print(f"{YELLOW}No recent activity found for @{username}.{RESET}")
        return

    for event in events[:10]:
        repo = event.get("repo", {}).get("name", "Unknown repository")
        created_at = event.get("created_at")
        timestamp = format_timestamp(created_at)
        icon, color, message = describe_event(event)
        print(f"{color}{icon} {message}{RESET}")
        print(f"   {DIM}{repo} • {timestamp}{RESET}\n")


def main():
    username = get_username()
    print_banner(username)
    events = url_request(username)
    if events is None:
        print(f"{RED}Something went wrong.{RESET}")
    else:
        print_activity(events, username)


if __name__ == "__main__":
    main()

