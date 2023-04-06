#!/usr/bin/python3

# Standard library imports.
import sys
import configparser
# Third-party imports.
import requests


def read_config():
    config = configparser.ConfigParser()
    config.read(".todoist_scheduler.conf")
    return config["todoist"]


def get_labels(token, labels_url):
    auth_string = "Bearer {}".format(token)
    response = requests.get(labels_url,
                            headers={"Authorization": auth_string})
    return response.json()


def get_tasks(token, tasks_url, day, label_id):
    auth_string = "Bearer {}".format(token)
    response = requests.get(tasks_url,
                            params={"filter": day, "label": label_id},
                            headers={"Authorization": auth_string})

    return response.json()


def count_tasks(task_dict):
    return sum(len(tasks) for tasks in task_dict.values())


def sum_tasks(task_dict):
    total_seconds = sum(len(tasks) * int(duration) * 60 for duration, tasks in task_dict.items())
    hours = total_seconds // 3600
    minutes = total_seconds // 60 - hours * 60

    my_len = "%d:%02d" % (hours, minutes)
    return my_len


if __name__ == "__main__":
    # Read config and get API key and default project name.
    config = read_config()
    your_token = config.get("api_key", "")
    default_project_name = config.get("default_project_name", "")

    if not your_token:
        print("No API Key, did you set 'api_key' in .todoist_scheduler.conf?")
        sys.exit(1)

    tasks_url = 'https://api.todoist.com/rest/v2/tasks'
    labels_url = 'https://api.todoist.com/rest/v2/labels'
    day = "today"   # Bcs usually it would be today

    # Get labels from Todoist API.
    labels = get_labels(your_token, labels_url)

    # Get tasks from Todoist API.
    # Detect labels like "25min".
    time_labels = {label["name"][:-3]: label["name"] for label in labels if label["name"].endswith("min") and label["name"][:-3].isdigit()}

    # Collect tasks from Todoist API.
    tasks_by_duration = {duration: get_tasks(your_token, tasks_url, day, label) for duration, label in time_labels.items()}
    for duration, tasks in tasks_by_duration.items():
        print("Duration: {}min".format(duration))
        for task in tasks:
            print("  {}".format(task["content"]))

    # Summarize tasks for user.
    print("Task Count: {}".format(count_tasks(tasks_by_duration)))
    print("Estimated Time: {}".format(sum_tasks(tasks_by_duration)))

