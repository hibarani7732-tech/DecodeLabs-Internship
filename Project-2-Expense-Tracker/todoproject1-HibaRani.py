def initialize_tasks():
    return [
        {"id": 1, "title": "Complete Python assignment", "status": "Pending"},
        {"id": 2, "title": "Attend online session", "status": "Pending"},
        {"id": 3, "title": "Work on final project", "status": "Pending"},
        {"id": 4, "title": "Make lecture notes", "status": "Pending"}
    ]


def display_tasks(tasks):
    if not tasks:
        print("\n⚠️ No tasks available.")
        return

    print("\n📋 TASK DATABASE:")
    print("-" * 50)
    for task in tasks:
        print(f"ID: {task['id']} | {task['title']} | {task['status']}")
    print("-" * 50)


def add_task(tasks):
    title = input("Enter new task: ").strip()
    if title:
        new_id = tasks[-1]["id"] + 1 if tasks else 1
        tasks.append({"id": new_id, "title": title, "status": "Pending"})
        print("✅ Task added successfully!")
    else:
        print("❌ Task cannot be empty.")


def remove_task(tasks):
    display_tasks(tasks)
    if not tasks:
        return

    confirm = input("Are you sure you want to delete a task? (y/n): ").strip().lower()
    if confirm != 'y':
        return

    try:
        task_id = int(input("Enter ID to delete: ").strip())
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                print("🗑 Task removed.")
                return
        print("❌ ID not found.")
    except ValueError:
        print("❌ Invalid input.")


def mark_done(tasks):
    display_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("Enter ID to mark as done: ").strip())
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "Done"
                print("✅ Task marked as done!")
                return
        print("❌ ID not found.")
    except ValueError:
        print("❌ Invalid input.")


def search_task(tasks):
    keyword = input("Enter keyword to search: ").strip().lower()
    found = False

    for task in tasks:
        if keyword in task["title"].lower():
            print(f"🔍 Found → ID: {task['id']} | {task['title']} | {task['status']}")
            found = True

    if not found:
        print("❌ No matching task found.")


def main():
    tasks = initialize_tasks()

    while True:
        print("\n===== STUDENT TASK SYSTEM =====")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Mark Task Done")
        print("5. Search Task")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_tasks(tasks)

        elif choice == '2':
            add_task(tasks)

        elif choice == '3':
            remove_task(tasks)

        elif choice == '4':
            mark_done(tasks)

        elif choice == '5':
            search_task(tasks)

        elif choice == '6':
            print("👋 Exiting program...")
            break

        else:
            print("❌ Invalid choice. Try again.")


main()