# Todoist Scheduler

You may want to schedule your (work) day. Therefore, you need to know how many tasks you can get done on a particular day.

Todoist has no time estimation built in.
Luckily, there are labels. And 4 different time slots are enough for most use cases: 5, 15, 30, 45min (if any task takes more than 45min, you should split it up anyway).

## How to estimate time in Todoist?

- Just add `@m5`, `@m15`, `@m30` or `@m45` to any given task

## How to get a sum of estimates for your whole day?

- (Bash) `EXPORT TODOIST_KEY = 'your_key_here'` (or add to `.zshrc` or the like)
- `git clone git@github.com:minthemiddle/todoist-scheduler.git`
- `cd todoist-scheduler`
- (Create new virtualenv) `python3 -m venv myvenv`
- (Activate on Linux/Mac) `source myvenv/bin/activate`
- (Install `requests`) `pip3 install requests`
- `python3 todoist.py`

It will ask for a project name (e.g. `work`) and will calculate all estimations within this project and its subprojects.

## Status und Contributions

This is still a very basic script to solve my problem. I don't like that I have to type in the project name (correctly) and that the label names `m…` are hard-coded.

Totally open to pull requests to improve the code quality and extend the functionality!

