#!/usr/bin/env python
import sys
import json
from datetime import datetime
from Task import Task

def main():
    app_data = {}
    app_data["last_task"] = 0
    app_data["tasks"] = []
    try:
        with open("data.json", "r") as save_file:
            data = json.load(save_file)
            if "tasks" in data:
                tasks = []
                for task in data["tasks"]:
                    tasks.append(Task.from_dict(task))
                app_data["tasks"] = tasks
            if "last_task" in data:
                app_data["last_task"] = data["last_task"]
    except FileNotFoundError:
        print("No save file, creating a new one")
    except json.JSONDecodeError:
        print("Warning json save file is corrupted")
    except Exception as e:
        print(e)
        return

    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            tasks = []
            if len(sys.argv) < 3:
                tasks = app_data["tasks"]
            elif sys.argv[2] == "done":
                completed_tasks = list(filter(lambda task: task.completed == "completed", app_data["tasks"]))
                tasks = completed_tasks
            elif sys.argv[2] == "in-progress":
                inprogress_tasks = list(filter(lambda task: task.completed == "inprogress", app_data["tasks"]))
                tasks = inprogress_tasks
            else:
                incomplete_tasks = list(filter(lambda task: task.completed == "incomplete", app_data["tasks"]))
                tasks = incomplete_tasks
            for task in tasks:
                print(task)
        elif sys.argv[1] == "add":
            new_task = Task(app_data["last_task"], sys.argv[2])
            app_data["last_task"] += 1
            app_data["tasks"].append(new_task)
        elif sys.argv[1] == "update":
            task_id = int(sys.argv[2])
            task: Task = find_task(task_id, app_data["tasks"])[0]
            if task:
                task.update(sys.argv[3])
        elif (sys.argv[1] == "mark-done" or
                sys.argv[1] == "mark-in-progress" or 
                sys.argv[1] == "mark-incomplete"):

            task_id = int(sys.argv[2])
            task = find_task(task_id, app_data["tasks"])[0]
            if task:
                if (sys.argv[1] == "mark-done"):
                    task.mark_as_completed()
                elif (sys.argv[1] == "mark-in-progress"):
                    task.mark_as_inprogress()
                else:
                    task.mark_as_incomplete()
        elif sys.argv[1] == "delete":
            task_id = int(sys.argv[2])
            task_index = find_task(task_id, app_data["tasks"])[1]
            if task_index > -1:
                del app_data["tasks"][task_index]

    with open("data.json", "w") as save_file:
        json.dump(app_data, save_file, default=json_default)

# Function to handle custom serialization
def json_default(obj):
    if hasattr(obj, "__json__"):
        return obj.__json__()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def find_task(taskId, tasks):
    for i, task in enumerate(tasks):
        if task.id == taskId:
            return [task, i]
    return [None, -1]

if __name__ == "__main__":
    main()