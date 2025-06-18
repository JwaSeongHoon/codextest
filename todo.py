import json
import argparse
from pathlib import Path

TASKS_FILE = Path('tasks.json')


def load_tasks():
    if TASKS_FILE.exists():
        with TASKS_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with TASKS_FILE.open('w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(description):
    tasks = load_tasks()
    tasks.append({'description': description, 'completed': False})
    save_tasks(tasks)
    print(f"Added task: {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for idx, task in enumerate(tasks, start=1):
        status = '[x]' if task.get('completed') else '[ ]'
        print(f"{idx}. {status} {task.get('description')}")


def complete_task(index):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        tasks[index - 1]['completed'] = True
        save_tasks(tasks)
        print(f"Completed task {index}")
    else:
        print("Invalid task number")


def delete_task(index):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f"Deleted task: {removed.get('description')}")
    else:
        print("Invalid task number")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple To-Do List Application')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')

    list_parser = subparsers.add_parser('list', help='List all tasks')

    complete_parser = subparsers.add_parser('complete', help='Mark a task as completed')
    complete_parser.add_argument('index', type=int, help='Task number to complete')

    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('index', type=int, help='Task number to delete')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'complete':
        complete_task(args.index)
    elif args.command == 'delete':
        delete_task(args.index)
    else:
        parser.print_help()
