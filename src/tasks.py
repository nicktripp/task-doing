#==============================================================================#
# This file takes command line input to control the task manager.
#
# @author Nick Tripp
# @date July 2016
#
#TODO: prioritize tasks!
#TODO: make distributed
#TODO: DOCUMENT!
#TODO: import tasks from file
#TODO: Handle delete collisions by asking to clarify
#TODO: Undo action button (via another JSON file!)
#TODO: Switch from task lists to task sets, and from delete by index to delete by ID
#TODO: multiple task add
#TODO: Rewrite for SQLite Database to store data
#TODO: add subtasks
#==============================================================================#
import argparse
import os

from color import color
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

def print_track_header(task_list, track, is_color=True):
    rows, columns = os.popen('stty size', 'r').read().split()
    head_str=  "{:-^" + columns + "}"
    if is_color:
        head_str = task_list.get_track_color(track) + head_str + color.END
    print(head_str.format(" {} ".format(track)))

def print_header(title):
    rows, columns = os.popen('stty size', 'r').read().split()
    head_str= color.BOLD + "{:=^" + columns + "}\n" + color.END
    print(head_str.format(" {} ".format(title)))

def main():
    data_file = os.path.join(get_data_path(), 'tasks.JSON')
    task_list = TaskList(data_file)

    parser = argparse.ArgumentParser(description='Manages task list.')
    parser.add_argument('-v','--verbose', action='count', help='display more information') # TODO: connect parser

    subparsers = parser.add_subparsers(required=True, dest='subcommand')

    ### List
    parser_list = subparsers.add_parser('list', help='List all tasks.', aliases=['ls','l'])
    parser_list.add_argument('-m', '--merge', action='store_true', dest='list_merge', help='merges all tracks into one large list')
    parser_list.add_argument('--nocolor','-n', action='store_false', dest='list_is_color', default=True, help='turns off terminal coloring')
    parser_list.add_argument('-t','--track', action='append', dest='list_tracks', choices=task_list.get_tracks(), help='the track to list')
    parser_list.add_argument('-e', '--enumerate', action='store_true', dest='list_is_enum', help='lists the tasks by their index within a track')
    parser_list.add_argument('-a','--all',  action='store_true', help='show all tasks, including completed') # TODO connect parser
    parser_list.add_argument('-c','--complete', action='store_true', help='show only complete tasks') #TODO connect parser
    parser_list.add_argument('-r','--random', action='store_true', dest='list_is_rand', help='randomize task order (cannot be used with the -e flag)') #TODO connect parser

    ### Add
    parser_add = subparsers.add_parser('add', help='Add a new task to the task list', aliases=['a'])
    parser_add.add_argument('new_task', help='the new task to add')
    parser_add.add_argument('-t','--track', dest='add_track', choices=task_list.get_tracks(), help='the track this task belongs to')

    ### Delete
    parser_del = subparsers.add_parser('delete', help='Delete a task', aliases=['del','d'])
    parser_del.add_argument('del_task_txt', nargs='?', type=str, help='the text of the task to delete')
    parser_del.add_argument('-n','--num', dest='del_task_num', type=int, help='delete a task by its index within a track instead of by text')
    parser_del.add_argument('-t','--track', dest='del_track', choices=task_list.get_tracks(), help='the track this task belongs to')
    parser_del.add_argument('--ignore_collisions', action='store_true', help='ignore task collisions, deleting the first found entry') #TODO

    ### Complete
    parser_comp = subparsers.add_parser('complete', help='Mark a task complete', aliases=['com','comp','c'])
    parser_comp.add_argument('comp_task_txt', nargs='?', type=str, help='the text of the task to complete')
    parser_comp.add_argument('-n','--num', dest='comp_task_num', type=int, help='complete a task by its index within a track instead of by text')
    parser_comp.add_argument('-t','--track', dest='comp_track', choices=task_list.get_tracks(), help='the track this task belongs to')
    parser_comp.add_argument('-u','--uncomplete', dest='is_incomplete', help='mark a task as incomplete') # TODO connect parser
    parser_comp.add_argument('--ignore_collisions', action='store_true', help='ignore task collisions, deleting the first found entry') #TODO




    ### Tracks #TODO connect parser
    parser_tracks = subparsers.add_parser('tracks', help='Manipulate task tracks', aliases=['track','tr'])
    track_subparsers = parser_tracks.add_subparsers(required=True, dest='tracks_action')

    # List tracks
    parser_list_track = track_subparsers.add_parser('list', help='List tracks', aliases=['ls','l'])
    parser_list_track.add_argument('-n','--nocolor', action='store_false', default=True, dest='color_track_list', help='flag to display colors of tracks.')

    # Add track #TODO connect parser
    parser_add_track = track_subparsers.add_parser('add', help='Add new task tracks', aliases=['a'])
    parser_add_track.add_argument('new_track', help='the new track to add')
    parser_add_track.add_argument('-d','--desc', dest='track_desc', help='description of the new track')
    parser_add_track.add_argument('-c','--color', dest='track_color', choices=color.COLORS, help='color of the new track')

    # Delete track #TODO connect parser
    parser_del_track = track_subparsers.add_parser('delete', help="Delete a task track. Fails if tasks are still inside unless forced; consider first transfering with 'tracks transfer'", aliases=['del','d'])
    parser_del_track.add_argument('del_track', help='the track to delete')
    parser_del_track.add_argument('-f','--force', action='store_true', dest='track_force_del', help='forces deletion, even if the given track still has tasks')

    # Transfer track #TODO make, connect parser
    # Rename track #TODO make, connect parser

    # Modify track
    parser_track_mod = track_subparsers.add_parser('modify', help='Modify a task track', aliases=['mod','m'])
    parser_track_mod.add_argument('mod_track', help='the track to modify')
    parser_track_mod.add_argument('-n','--name', dest='track_new_name', choices=color.COLORS, help='new name of the track')
    parser_track_mod.add_argument('-c','--color', dest='track_new_color', choices=color.COLORS, help='new color of the track')
    parser_track_mod.add_argument('-d','--desc', dest='track_new_desc', help='new description of the track')


    args = parser.parse_args()
    dargs = vars(args)
    print(args)

    print("")

    if not data_dir_exists():
        generate_data_dir()

    # Connect 'list' parser
    if args.subcommand.find('l') == 0:
        # Print task list
        print_header("TASKS")
        task_tracks = agrs.list_tracks if args.list_tracks else task_list.get_tracks()

        for track in task_tracks:
            if not args.list_merge:
                print_track_header(task_list, track, is_color=args.list_is_color)

            if args.list_is_color:
                print(task_list.get_track_color(track), end='')

            if not args.list_merge:
                print("")

            for i,task in enumerate(task_list.get_tasks_in_track(track)):
                line_marker = "{}.".format(str(i)) if args.list_is_enum else "-"
                line = " {} {}".format(line_marker, task.txt)
                if task.complete:
                    line = color.FAINT + line + color.END
                print(line)

            print(color.END, end='' if args.list_merge else '\n')

    # Connect 'add' parser
    elif 'new_task' in dargs:
        task_list.add_task(args.new_task, track=args.add_track)
        track = TaskList.UNSORTED_TRACK if not args.add_track else args.add_track
        print("Wrote new task: {} to track '{}{}{}'".format(args.new_task, task_list.get_track_color(track),track,color.END))

    # Connect 'del' parser
    elif args.subcommand.find('d') == 0:
        if args.del_task_txt and args.del_task_num:
            parser.error('delete: conflicting args: specify exactly one of -n DEL_TASK_NUM or DEL_TASK_TXT')

        elif args.del_task_num:
            if not args.del_track:
                parser.error('delete: if delete index -n specified, --track is required')

            try:
                success = task_list.del_task(t_idx=args.del_task_num, track=args.del_track)
            except ValueError as err:
                print("Failed to delete task: {}".format(err))
                exit(0)
            if(success):
                print("Deleted task: #{} in track '{}': '{}'".format(args.del_task_num, args.del_track, success))
            else:
                print("Task #{} doesn't exist in track '{}'".format(args.del_task_num, args.del_track))
        elif args.del_task_txt:
            success = task_list.del_task(task=args.del_task_txt)
            if(success):
                print("Deleted task: '{}'".format(success))
            else:
                print("Could not find task: '{}'".format(args.del_task_txt))
        else:
            parser.error('delete: missing args: specify exactly one of -n DEL_TASK_NUM or DEL_TASK_TXT')

    # Connect 'comp' parser
    elif args.subcommand.find('c') == 0:
        if args.comp_task_txt and args.comp_task_num:
            parser.error('delete: conflicting args: specify exactly one of -n DEL_TASK_NUM or DEL_TASK_TXT')

        elif args.comp_task_num:
            if not args.comp_track:
                parser.error('complete: if delete index -n specified, --track is required')

            try:
                success = task_list.complete_task(t_idx=args.comp_task_num, track=args.comp_track)
            except ValueError as err:
                print("Failed to delete task: {}".format(err))
                exit(0)
            if(success):
                print("Completed task: #{} in track '{}': '{}'".format(args.comp_task_num, args.comp_track, success))
            else:
                print("Task #{} doesn't exist in track '{}'".format(args.comp_task_num, args.comp_track))
        elif args.comp_task_txt:
            success = task_list.complete_task(task=args.comp_task_txt)
            if(success):
                print("Completed task: '{}'".format(success))
            else:
                print("Could not find task: '{}'".format(args.comp_task_txt))
        else:
            parser.error('complete: missing args: specify exactly one of -n DEL_TASK_NUM or DEL_TASK_TXT')

    # Connect 'tracks' parser
    elif args.subcommand.find('tr') == 0:

        # List tracks
        if args.tracks_action.find('l') == 0:
            # TODO: Verbosity
            # TODO: #complete count

            print_header("TRACKS")
            raw_tracks = task_list.get_tracks()

            if args.color_track_list:
                tracks = [task_list.get_track_color(track) + track + color.END for track in raw_tracks]
            else:
                tracks = raw_tracks

            row = "\t{}\t\t{}\t{}\n"
            print(row.format(color.UNDERLINE + "NAME", "#TASKS", "DESCRIPTION" + color.END))

            for i,track in enumerate(tracks):
                print( row.format(track, len(task_list.get_tasks_in_track(raw_tracks[i])), task_list.get_track_desc(raw_tracks[i])) )


        # Add track
        elif args.tracks_action.find('a') == 0:
            color_code = color.__dict__[args.track_color] if args.track_color else None

            try:
                task_list.add_track(args.new_track, desc=args.track_desc, color=color_code)
            except ValueError as err:
                exit("tracks add: {}".format(err))

            print("Added track: '{}{}{}'".format(color_code,args.new_track.upper(), color.END))

        # Del track
        elif args.tracks_action.find('d') == 0:
            task_cnt = len(task_list.get_tasks_in_track(args.del_track))
            color_code = task_list.get_track_color(args.del_track)

            if task_cnt == 0 or args.track_force_del:
                try:
                    task_list.del_track(args.del_track)
                except ValueError as err:
                    exit("tracks add: {}".format(err))

                if args.track_force_del and task_cnt > 0:
                    print("Deleted {} tasks".format(task_cnt))
                print("Deleted track: '{}{}{}'".format(color_code, args.del_track, color.END))

            else:
                exit("tracks delete: track '{}{}{}' still has {} task(s); transfer task(s) or rerun with 'tracks delete --force'".format(color_code,args.del_track,color.END, task_cnt))

        # Mod track
        elif args.tracks_action.find('m') == 0:
            if args.track_new_name or args.track_new_color or agrs.track_new_desc:
                color_code = color.__dict__[args.track_new_color] if args.track_new_color else None

                task_list.set_track_attr(args.mod_track, new_color=color_code, new_name=args.track_new_name, new_desc=args.track_new_desc)

                name = args.track_new_name if args.track_new_name else args.mod_track
                color_code = color_code if color_code else task_list.get_track_color(name)
                print("Modified track: '{}{}{}'".format(color_code, name, color.END))
            else:
                parser.err("tracks modify: must specify some attributes to modify")

    print("")
    task_list.write_to_file(data_file)

if __name__ == '__main__': main()
