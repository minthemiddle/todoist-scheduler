#!/usr/bin/python3

# Standard library imports.
import os
import sys
# Third-party imports.
import requests
from dotenv import load_dotenv
# No local imports.


def get_tasks(token, tasks_url, day, project, label):
    filter_string = '{} & @{} & ##{}'.format(day, label, project)
    auth_string = "Bearer {}".format(token)
    response = requests.get(tasks,
                            params={"filter": filter_string},
                            headers={"Authorization": auth_string})
    return response.json()


def count_tasks(i5,i15,i30,i45):
    return len(i5)+len(i15)+len(i30)+len(i45)


def sum_tasks(i5, i15, i30, i45):
    s5 = len(i5) * 5
    s15 = len(i15) * 15
    s30 = len(i30) * 30
    s45 = len(i45) * 45
    total_seconds = (s5 + s15 + s30 + s45)*60

    hours = total_seconds // 3600
    minutes = total_seconds // 60 - hours * 60

    my_len = "%d:%02d" % (hours, minutes)
    return my_len


if __name__ == "__main__":
    # Collect script variables from user.
    load_dotenv()
    your_token = os.getenv('TODOIST_KEY', '')
    if not your_token:
        print("No API Key, did you set 'TODOIST_KEY' environment variable?")
        sys.exit(1)
    tasks = 'https://api.todoist.com/rest/v2/tasks'
    project = input('Project: ')
    day = input('Day: ')

    # Collect tasks from Todoist API.
    m5 = get_tasks(your_token, tasks, day, project, label="m5")
    m15 = get_tasks(your_token, tasks, day, project, label="m15")
    m30 = get_tasks(your_token, tasks, day, project, label="m30")
    m45 = get_tasks(your_token, tasks, day, project, label="m45")

    # Summarize tasks for user.
    print("Task Count: {}".format(count_tasks(m5,m15,m30,m45)))
    print("Estimated Time: {}".format(sum_tasks(m5,m15,m30,m45)))


