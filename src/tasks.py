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
#TODO: DOCUMENT!
#TODO: import tasks from file
#==============================================================================#
import argparse
import os

from task_list import TaskList

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

    data_file = os.path.join(get_data_path(), 'tasks.JSON')
    task_list = TaskList(data_file)

    if(args.new_task != None):
        task_list.add_task(args.new_task)
        print("Wrote new task: {}".format(args.new_task))

    elif(args.del_task != None):
        arg_is_num = False
        try:
            del_num = int(args.del_task)
            arg_is_num = True
        except ValueError:
            arg_is_num = False

        if arg_is_num:
            track = 'General'
            success = task_list.del_task(t_idx=del_num, track=track)
            if(success):
                print("Deleted task: #{} in track '{}'".format(del_num, track))
            else:
                print("Task number doesn't exist: {}".format(del_num))
        else:
            success = task_list.del_task(task=args.del_task)
            if(success):
                print("Deleted task: {}".format(args.del_task))
            else:
                print("Task doesn't exist: {}".format(args.del_task))

    elif(args.comp_task != None):
        strike_task(args.comp_task)

    else:
        # Print task list
        print("\n== CURRENT TASKS ==")
        task_tracks = task_list.get_tracks()
        for track in task_tracks:
            print("\n\t-{}-".format(track))
            for task in task_list.get_tasks_in_track(track):
                line_marker = "{}.".format(str(i)) if args.show_num else "-"
                print(" {} {}".format(line_marker, task.txt))
        print("")

    task_list.write_to_file(data_file)

def strike_task(task):
    print("Woops this doesn't work yet")


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
