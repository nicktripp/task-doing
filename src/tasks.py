#==============================================================================#
# This file takes command line input to control the task manager.
#
# @author Nick Tripp
# @date July 2016
#
#TODO: prioritize tasks!
#TODO: print color?
#TODO: make multiple lists, that aggregate
#TODO: make distributed
#TODO: redo pathing to remove env vars
#TODO: DOCUMENT!
#==============================================================================#
import argparse
import os

def get_data_path():
    """Returns the path of the data directory, which should be a sibling to this file's parent directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def data_dir_exists():
    data_path = get_data_path()
    return os.path.exists(data_path) and os.path.isdir(data_path)

def generate_data_dir():
    """ Create the data directory, if it doesn't exist. """
    data_path = get_data_path()
    os.mkdir(data_path)


def main():
    parser = argparse.ArgumentParser(description='Manages task list.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a, --add', dest='new_task', default=None, help='Add a task to the task list')
    group.add_argument('-d, --delete', dest='del_task', default=None, help='Delete a task from the task list')
    group.add_argument('-c, --complete', dest='comp_task', default=None, help='Mark a task as completed')
    group.add_argument('-n', action='store_true', dest='show_num')

    args = parser.parse_args()


    if not data_dir_exists():
        generate_data_dir()

    if(args.new_task != None):
        add_task(args.new_task)

    elif(args.del_task != None):
        try:
            del_num = int(args.del_task)
            remove_task_by_num(del_num)
        except ValueError:
            remove_task(args.del_task)

    elif(args.comp_task != None):
        strike_task(args.comp_task)

    else:
        # PRINT TASK LIST: file
        data_path = get_data_path()
        f = open("{}/{}".format(data_path, "tasks.txt"))
        print("\n== CURRENT TASKS ==\n")
        for i,line in enumerate(f):
            line_marker = "{}.".format(str(i) + 1) if args.show_num else "-"
            print(" {} {}".format(line_marker, line))
        print("")

def strike_task(task):
    print("Woops this doesn't work yet")

def add_task(new_task):
    data_path = get_data_path()
    f = open("{}/{}".format(data_path, "tasks.txt"), 'a')
    f.write(new_task + "\n")
    print("Wrote new task: {}".format(new_task))

def remove_task_by_num(del_num):
    data_path = get_data_path()
    f = open("{}/{}".format(data_path, "tasks.txt"), 'r+')
    lines = f.readlines()
    f.seek(0)

    found = None
    line_num = 1
    for line in lines:
        if(not found and line_num == del_num):
            found = line
        else:
            f.write(line)
            line_num += 1

    f.truncate()
    f.close()

    if(found):
        print("Deleted task: " + found),
    else:
        print("Task number doesn't exist: " + del_num)

def remove_task(task):
    data_path = get_data_path()
    f = open("{}/{}".format(data_path, "tasks.txt"), 'r+')
    lines = f.readlines()
    f.seek(0)
    found = None
    for line in lines:
        if(not found and line.lower().find(task.lower()) == 0):
            found = line
        else:
            f.write(line)

    f.truncate()
    f.close()

    if(found):
        print("Deleted task: " + found),
    else:
        print("Could not find task: " + task)



if __name__ == '__main__': main()