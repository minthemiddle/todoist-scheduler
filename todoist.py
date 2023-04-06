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


def get_labels(token):
    labels_url = 'https://api.todoist.com/rest/v2/labels'
    auth_string = "Bearer {}".format(token)
    response = requests.get(labels_url,
                            headers={"Authorization": auth_string})
    return response.json()


def get_projects(token):
    projects_url = 'https://api.todoist.com/rest/v2/projects'
    auth_string = "Bearer {}".format(token)
    response = requests.get(projects_url,
                            headers={"Authorization": auth_string})
    return response.json()


def get_tasks(token, day):
    tasks_url = 'https://api.todoist.com/rest/v2/tasks'
    auth_string = "Bearer {}".format(token)

    response = requests.get(tasks_url,
                            params={"filter": day},
                            headers={"Authorization": auth_string})
    return response.json()


def filter_tasks(tasks, label_id, project_id=None):
    if project_id is None:
        return [task for task in tasks if label_id in task["labels"]]
    else:
        return [task for task in tasks if task["project_id"] == project_id and label_id in task["labels"]]

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

    if not your_token:
        print("No API Key, did you set 'api_key' in .todoist_scheduler.conf?")
        sys.exit(1)

    day = input('Day (leave empty for today): ') or "today"   # Bcs usually it would be today
    project_name = input('Project (leave empty for all projects): ')

    # Get labels from Todoist API.
    labels = get_labels(your_token)
    projects = get_projects(your_token)

    # Get project ID from project name.
    project_id = [project["id"] for project in projects if project["name"] == project_name]
    if project_id:
        project_id = project_id[0]
    else:
        project_id = None

    # Detect labels like "25min".
    time_labels = {label["name"][:-3]: label["name"] for label in labels if label["name"].endswith("min") and label["name"][:-3].isdigit()}

    # Get all tasks for today from Todoist API.
    all_tasks = get_tasks(your_token, day)

    # Filter tasks by project and label.
    tasks_by_duration = {}
    for duration, label_id in time_labels.items():
        tasks_by_duration[duration] = filter_tasks(all_tasks, label_id, project_id)

    # Summarize tasks for user.
    print("Task Count: {}".format(count_tasks(tasks_by_duration)))
    print("Estimated Time: {}".format(sum_tasks(tasks_by_duration)))

