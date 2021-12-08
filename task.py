from sys import argv
import os

tasks_files_path = os.getcwd()


def print_help():
    help_text = """Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics"""
    print(help_text, end="")


def ls():
    """
    ./task.sh ls -> lists tasks
    """
    try:
        with open(f"{tasks_files_path}/task.txt", "r") as file:
            lines = file.read().splitlines()
            for i, line in enumerate(lines):
                index = line.find(" ")
                priority = line[0:index]
                task = line[index + 1 :]
                ls_out = f"{i+1}. {task} [{priority}]"
                print(ls_out)
    except Exception:
        print("There are no pending tasks!")


def add_task(priority, task):
    """
    ./task.sh add priority "task" -> lists tasks
    """
    with open(f"{tasks_files_path}/task.txt", "a+") as file:

        # Check file is empty or not
        if os.stat(f"{tasks_files_path}/task.txt").st_size == 0:
            file.write(f"{priority} {task}\n")

        # Tasks already present in file
        else:
            with open(f"{tasks_files_path}/task.txt", "r+") as file:
                lines = file.readlines()
                flag = False
                for i, line in enumerate(lines):
                    file_task_prior = int(line.split(" ")[0])
                    if file_task_prior > priority:
                        lines.insert(i, f"{priority} {task}\n")
                        flag = True
                        break
                    elif file_task_prior == priority:
                        lines.insert(i + 1, f"{priority} {task}\n")
                        flag = True
                        break
                    else:
                        continue

                # If last task
                if not flag:
                    lines.append(f"{priority} {task}\n")

                open(f"{tasks_files_path}/task.txt", "w").close()

                with open(f"{tasks_files_path}/task.txt", "w") as file:
                    file.writelines(lines)

        print(f'Added task: "{task}" with priority {priority}')


def delete_task(del_index_int, del_index):
    """
    ./task.sh del index -> "del" tasks based on index
    """
    with open(f"{tasks_files_path}/task.txt", "r+") as file:
        lines = file.readlines()
        if del_index_int <= len(lines) and del_index_int >= 1 and del_index.isdigit():
            # Del line by index
            del lines[del_index_int - 1]

            # Erase file content
            open(f"{tasks_files_path}/task.txt", "w").close()

            # Rewrite tasks
            with open(f"{tasks_files_path}/task.txt", "w") as file:
                file.writelines(lines)

            print(f"Deleted task #{del_index_int}")
        else:
            print(
                f"Error: task with index #{del_index} does not exist. Nothing deleted."
            )


def done_task(done_index_int, done_index):
    """
    ./task.sh done index -> "done" tasks based on index
    """
    with open(f"{tasks_files_path}/task.txt", "r+") as file:
        lines = file.readlines()
        if (
            done_index_int <= len(lines)
            and done_index_int >= 1
            and done_index.isdigit()
        ):

            # Store done task
            done_task_line = lines[done_index_int - 1]
            index = done_task_line.find(" ")
            done_task = done_task_line[index + 1 :]

            with open(f"{tasks_files_path}/completed.txt", "a+") as done_file:
                done_file.write(done_task)

            # Del line by index
            del lines[done_index_int - 1]

            # Erase file content
            open(f"{tasks_files_path}/task.txt", "w").close()

            # Rewrite tasks
            with open(f"{tasks_files_path}/task.txt", "w") as file:
                file.writelines(lines)

            print(f"Marked item as done.")
        else:
            print(f"Error: no incomplete item with index #{done_index} exists.")


def report():
    """
    ./task.sh report -> Pending and incomplete tasks
    """
    with open(f"{tasks_files_path}/task.txt", "r") as task_file:
        tasks_count = len(task_file.readlines())
        print(f"Pending : {tasks_count}")
        ls()
        print()

    with open(f"{tasks_files_path}/completed.txt", "r") as comp_file:
        completed_tasks = comp_file.read().splitlines()
        completed_tasks_count = len(completed_tasks)
        print(f"Completed : {completed_tasks_count}")

        for i, completed_task in enumerate(completed_tasks):
            print(f"{i+1}. {completed_task}")


def priority_list():
    """
    Main CLI App Execution
    """
    single_args_list = ["ls", "help", "report", "done", "del"]
    input_len = len(argv)

    if input_len == 1:
        print_help()

    elif input_len == 2:
        args = argv[1].lower()

        if args in single_args_list:
            if args == "help":
                print_help()
            elif args == "ls":
                ls()
            elif args == "done":
                print("Error: Missing NUMBER for marking tasks as done.")

            elif args == "del":
                print("Error: Missing NUMBER for deleting tasks.")
            else:
                report()
        else:
            print("Error: Missing tasks string. Nothing added!")

    elif input_len == 3:
        args = argv[1].lower()
        del_index = argv[2]
        done_index = argv[2]
        print(del_index)

        if args == "del":
            del_index_int = int(del_index)
            delete_task(del_index_int, del_index)

        elif args == "done":
            done_index_int = int(done_index)
            done_task(done_index_int, done_index)

    # Add a new item
    elif input_len == 4:
        args = argv[1].lower()
        priority = argv[2]
        task = argv[3]

        if args == "add" and priority.isdigit() and int(priority) >= 0:
            add_task(int(priority), task)
        else:
            print('Error : Invalid "add item command"')


if __name__ == "__main__":
    priority_list()
