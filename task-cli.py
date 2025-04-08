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

def update_task(id, new_desc):
    # Read json file
    with open("tasks.json", mode="r") as f:
        tasks = json.load(f)

    # Updating task
    updated = False
    now = datetime.datetime.now()
    updatedAt = now.strftime("%d-%b-%Y %H:%M:%S")
    for task in tasks["tasks"]:
        if task["id"] == id:
            task["description"] = new_desc
            task["updatedAt"] = updatedAt
            updated = True

    # Writing back json file
    with open("tasks.json", mode="w") as f:
        json.dump(tasks, f, indent=4)

    # User output
    if updated:
        print("Task updated successfully")
    else:
        print("Task not found")

def mark_task(id, mark):
    # Read json file
    with open("tasks.json", mode="r") as f:
        tasks = json.load(f)

    # Updating task
    updated = False
    now = datetime.datetime.now()
    updatedAt = now.strftime("%d-%b-%Y %H:%M:%S")
    for task in tasks["tasks"]:
        if task["id"] == id:
            updated = True
            if mark == "mark-in-progress":
                task["status"] = "in-progress"
                task["updatedAt"] = updatedAt
            else:
                task["status"] = "done"
                task["updatedAt"] = updatedAt

    # Writing back json file
    with open("tasks.json", mode="w") as f:
        json.dump(tasks, f, indent=4)

    # User output
    if updated:
        print("Task updated successfully")
    else:
        print("Task not found")

def delete_task(id):
    # Read json file
    with open("tasks.json", mode="r") as f:
        tasks = json.load(f)

    # Delete task
    new_tasks = {"current_id": tasks["current_id"], "tasks": []}
    for task in tasks["tasks"]:
        if task["id"] != id:
            new_tasks["tasks"].append(task)

    # Writing back json file
    with open("tasks.json", mode="w") as f:
        json.dump(new_tasks, f, indent=4)

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
    
    # update command
    update_parser = subparsers.add_parser("update", help="Update task description")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("new_desc", type=str, help="New task description")

    # mark-in-progress command
    mip_parser = subparsers.add_parser("mark-in-progress", help="Mark a task as in-progress")
    mip_parser.add_argument("id", type=int, help="Task ID")

    # mark-done command
    mip_parser = subparsers.add_parser("mark-done", help="Mark a task as done")
    mip_parser.add_argument("id", type=int, help="Task ID")

    # delete command
    del_parser = subparsers.add_parser("delete", help="Delete task")
    del_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.task)
    
    if args.command == "list":
        list_tasks(args.status)

    if args.command == "update":
        update_task(args.id, args.new_desc)

    if args.command == "mark-in-progress" or args.command == "mark-done":
        mark_task(args.id, args.command) 

    if args.command == "delete":
        delete_task(args.id)

if __name__ == "__main__":
    main()