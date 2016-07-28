#==============================================================================#
# This file takes command line input to control the task manager.
#
# @author Nick Tripp
# @date July 2016
#
#TODO: prioritize tasks!
#TODO: print color?
#==============================================================================#
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Manages task list.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a, --add', dest='new_task', default=None, help='Add a task to the task list')
    group.add_argument('-d, --delete', dest='del_task', default=None, help='Delete a task from the task list')
    group.add_argument('-c, --complete', dest='comp_task', default=None, help='Mark a task as completed')

    args = parser.parse_args()

    if(args.new_task != None):
        add_task(args.new_task)
    elif(args.del_task != None):
        remove_task(args.del_task)
    elif(args.comp_task != None):
        # STRIKETHROUGH TASK
    else:
        # PRINT TASK LIST: file
        f = open(os.environ['TASKPATH'] + "tasks.txt")
        print("\n== CURRENT TASKS ==\n")
        for line in f:
            print(" - " + line),
        print("")

def add_task(new_task):
    f = open(os.environ['TASKPATH'] + 'tasks.txt', 'a')
    f.write(new_task + "\n")
    print("Wrote new task: " + new_task)

def remove_task(task):
    f = open(os.environ['TASKPATH'] + 'tasks.txt', 'r+')
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