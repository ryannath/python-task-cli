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
            for task in app_data["tasks"]:
                print(task)
        elif sys.argv[1] == "add":
            new_task = Task(app_data["last_task"], sys.argv[2])
            app_data["last_task"] += 1
            app_data["tasks"].append(new_task)
        elif sys.argv[1] == "update":
            task_id = int(sys.argv[2])
            task: Task = next((v for v in app_data["tasks"] if v.id == task_id), None)
            if task:
                task.update(sys.argv[3])
            
    with open("data.json", "w") as save_file:
        json.dump(app_data, save_file, default=json_default)

# Function to handle custom serialization
def json_default(obj):
    if hasattr(obj, "__json__"):
        return obj.__json__()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

if __name__ == "__main__":
    main()