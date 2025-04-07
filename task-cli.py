import argparse, os, json, datetime

def add_task(task):
    # Read json file
    with open("tasks.json", mode="r") as f:
        tasks = json.load(f)

    # Creating new task
    now = datetime.datetime.now()
    createdAt = now.strftime("%d-%b-%Y %H:%M:%S")
    new_task = {"id": tasks["current_id"],
                "description": task,
                "status": "todo",
                "createdAt": createdAt,
                "updatedAt": createdAt}
    
    # Updating current_id in json file
    tasks["current_id"] += 1
    tasks["tasks"].append(new_task) 

    # Writing back json file
    with open("tasks.json", mode="w") as f:
        json.dump(tasks, f, indent=4)

    # User output
    print(f"Task added successfully (ID: {tasks["current_id"]-1})")

def list_tasks(status):
    # Read json file
    with open("tasks.json", mode="r") as f:
        tasks = json.load(f)

    # User output
    print(f"{"ID"[:3]:<4} {"Description"[:30]:<31} {"Status"[:11]:<12} {"Created at"[:20]:<21} {"Updated at"[:20]:<21}")
    print("-"*92)
    if status == "todo":
        for task in tasks["tasks"]:
            if task["status"] == "todo":
                print(f"{str(task["id"])[:3]:<4} {task["description"][:30]:<31} {task["status"][:11]:<12} {str(task["createdAt"])[:20]:<21} {str(task["updatedAt"])[:20]:<21}")

    elif status == "in-progress":
        for task in tasks["tasks"]:
            if task["status"] == "in-progress":
                print(f"{str(task["id"])[:3]:<4} {task["description"][:30]:<31} {task["status"][:11]:<12} {str(task["createdAt"])[:20]:<21} {str(task["updatedAt"])[:20]:<21}")

    elif status == "done":
        for task in tasks["tasks"]:
            if task["status"] == "done":
                print(f"{str(task["id"])[:3]:<4} {task["description"][:30]:<31} {task["status"][:11]:<12} {str(task["createdAt"])[:20]:<21} {str(task["updatedAt"])[:20]:<21}")

    else:
        for task in tasks["tasks"]:
            print(f"{str(task["id"])[:3]:<4} {task["description"][:30]:<31} {task["status"][:11]:<12} {str(task["createdAt"])[:20]:<21} {str(task["updatedAt"])[:20]:<21}")

def main():
    # Creating json file if it does not exist
    if os.path.exists("tasks.json") == False:
        with open("tasks.json", "w") as f:
            new_json = {"current_id": 0, "tasks": []}
            json.dump(new_json, f, indent=4)

    # Setup argparse
    parser = argparse.ArgumentParser(description="task-cli app")    
    subparsers = parser.add_subparsers(dest="command")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", type=str, help="Task description")

    # list command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("status",
                             nargs="?", # Status argument is optional
                             choices=["todo", "in-progress", "done"],
                             type=str,
                             help="List tasks by status")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.task)
    
    if args.command == "list":
        list_tasks(args.status)

if __name__ == "__main__":
    main()