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

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.task)

if __name__ == "__main__":
    main()