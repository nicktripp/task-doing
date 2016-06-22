import argparse
import os

parser = argparse.ArgumentParser(description='Manages task list.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-a, --add', dest='new_task', default=None, help='Add a task to the task list')
group.add_argument('-d, --delete', dest='del_task', default=None, help='Delete a task from the task list')

args = parser.parse_args()

if(args.new_task != None):
    # ADD TASK TO LIST
    f = open(os.environ['TASKPATH'] + 'tasks.txt', 'a')
    f.write(args.new_task + "\n");
    print("Wrote new task: " + args.new_task)
elif(args.del_task != None):
    # REMOVE TASK FROM LIST
    f = open(os.environ['TASKPATH'] + 'tasks.txt', 'r+')
    lines = f.readlines()
    f.seek(0)
    found = None
    for line in lines:
        if(not found and line.lower().find(args.del_task.lower()) == 0):
            found = line
        else:
            f.write(line)

    f.truncate()
    f.close()

    if(found):
        print("Deleted task: " + found),
    else:
        print("Could not find task: " + args.del_task)
else:
    # PRINT TASK LIST: file
    f = open(os.environ['TASKPATH'] + "tasks.txt")
    print("\n== CURRENT TASKS ==\n")
    for line in f:
        print(" - " + line),
    print("")

#TODO: prioritize tasks!
#TODO: print color?

