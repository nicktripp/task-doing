import os

import time
import json

### Structure of a Task List:
# {
#     'General': {
#         'color': color_str,
#         'desc': 'A description of this track'
#         'task_list': [
#             {'txt':'task1', 'completed':False, time_created:date_created, time_completed:time_cmpleted},
#         ]
#     }
# }

class Task:
    def __init__(self, txt, complete=False, time_created=None, time_complete=None):
        self.__task__= True
        self.txt= txt
        self.complete= complete
        self.time_created= time_created if time_created else time.time()
        self.time_complete= time_complete if time_complete else None

    def as_task(obj_dct):
        if '__task__' in obj_dct:
            del obj_dct['__task__']
            return Task(**obj_dct)
        return obj_dct

    class Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Task):
                return obj.__dict__

            return json.JSONEncoder.default(self, obj)

class TaskList:
    # Some dict constants:
    UNSORTED_TRACK='GENERAL'
    TASK_LIST = 'task_list'
    DESC = 'desc'
    COLOR = 'color'

    def __init__(self, file_path=None):
        if not file_path or not os.path.exists(file_path) or not os.path.isfile(file_path):
            self.tracks = {}
            self.add_track(self.UNSORTED_TRACK, 'General, unsorted tasks', '')
        else:
            self.load_from_file(file_path)

    def add_task(self, task, track=None):
        """
        Adds a task.
        Adds to the tasklist with the name 'track', if specified, otherwise,
            adds to 'General'
        """

        # If empty string, do nothing
        if not task:
            return

        # If track is unspecified, add to the unsorted track
        if not track:
            track = self.UNSORTED_TRACK

        track = track.upper()
        if track not in self.tracks:
            raise ValueError("Track '{}' does not exist".format(track))

        task_complete = False

        track_data = self.tracks[track]
        track_data[self.TASK_LIST].append(Task(task))

    def add_track(self, name, desc='', color=''):
        """
        Adds a task track with the specified name and description.
        Raises ValueError if the track already exists.
        """
        if name in self.tracks:
            raise ValueError("Track '{}' already exists".format(name))

        name = name.upper()
        self.tracks[name] = { self.DESC:desc, self.TASK_LIST:[], self.COLOR:color }

    def complete_task(self, task=None, track=None, t_idx=None):
        """
        Complete first task beginning with 'task' from track 'track'.
        If the track is unspecified, go through every task.
        If an t_idx AND a track is specified, complete the task at that index.

        NOTE: this runs in O(N) time.

        :return The text of the task if a task was found, None otherwise
        """
        if not task:
            if not track and not t_idx:
                raise ValueError("If no specified task, must specify a track and t_idx")
        elif t_idx:
            raise ValueError("Cannot specify both a task and a t_idx")

        if not track:
            for track_name in self.tracks:
                success = self.complete_task(task, track=track_name)
                if success:
                    return success
            return None

        else:
            track = track.upper()

            if track not in self.tracks:
                raise ValueError("Given track '{}' does not exist".format(track))
            track_data = self.tracks[track]

            if t_idx:
                # Find the task by index
                if idx >= len(track_data[self.TASK_LIST]):
                    raise ValueError("Index '{}' out of bounds for track '{}'".format(t_idx,track))

                task = track_data[self.TASK_LIST][t_idx]
                task.complete = True
                return task.txt
            else:
                # Search through the given track
                for curr_task in track_data[self.TASK_LIST]:
                    if curr_task.txt.lower().find(task.lower()) == 0:
                        # Task found. Complete:
                        curr_task.complete = True
                        return curr_task.txt

            return None

    def del_task(self, task=None, track=None, t_idx=None):
        """
        Delete first task beginning with 'task' from track 'track'.
        If the track is unspecified, go through every task.

        NOTE: this runs in O(N) time.

        :return The task that was found and removed, None otherwise
        """
        if not task:
            if not track and not t_idx:
                raise ValueError("If no specified task, must specify a track and t_idx")
        elif t_idx:
            raise ValueError("Cannot specify both a task and a t_idx")

        if not track:
            for track_name in self.tracks:
                success = self.del_task(task, track=track_name)
                if success:
                    return success
            return None
        else:
            track = track.upper()

            if track not in self.tracks:
                raise ValueError("Given track '{}' does not exist".format(track))

            track_data = self.tracks[track]

            if t_idx:
                if t_idx >= len(track_data[self.TASK_LIST]):
                    raise ValueError("Index '{}' out of bounds for track '{}'".format(t_idx,track))

                task = track_data[self.TASK_LIST].pop(t_idx)
                return task.txt

            for idx,curr_task in enumerate(track_data[self.TASK_LIST]):
                if curr_task.txt.lower().find(task.lower()) == 0:
                    # Task found. Remove:
                    task = track_data[self.TASK_LIST].pop(idx)
                    return task.txt

            return None

    def get_tasks_in_track(self, track):
        """ Return a list of task tuples, in the format (txt,is_complete,date_created). """
        track = track.upper()
        if track not in self.tracks:
            raise ValueError("Given track {} does not exist".format(track))
        return self.tracks[track][self.TASK_LIST]

    def get_tracks(self):
        """ Returns the list of active tracks of tasks. """
        return [track for track in self.tracks]

    def del_track(self, track):
        """ Deletes the track, and all data associated with it. """
        track = track.upper()
        if track not in self.tracks:
            raise ValueError("Given track {} does not exist".format(track))
        del self.tracks[track]

    def load_from_file(self, file_path):
        """
        Loads tasks from a specified JSON file.
        """
        try:
            f = open(file_path)
        except IOError as err:
            raise err

        data = json.load(f, object_hook=Task.as_task)

        self.tracks = data
        f.close()


    def write_to_file(self, file_path):
        """
        Writes all tasks to a specified JSON file.
        Creates the file if it does not exist.
        Overwrites that file.
        """
        try:
            f = open(file_path, 'w')
        except IOError as err:
            raise err

        json.dump(self.tracks, f, cls=Task.Encoder)
        f.truncate()
        f.close()

    def get_track_color(self, track):
        track = track.upper()
        if track not in self.tracks:
            raise ValueError("Given track '{}' does not exist".format(track))

        return self.tracks[track][self.COLOR]

    def get_track_desc(self, track):
        track = track.upper()
        if track not in self.tracks:
            raise ValueError("Given track '{}' does not exist".format(track))

        return self.tracks[track][self.DESC]


    def set_track_attr(self, track, new_name=None, new_color=None, new_desc=None):
        """
        Sets the attributes of a track.  If any of the attributes specified are "None", they are not modified.

        :Params:
        :new_name - the new name for the track
        :new_color - one of the colors specified in the imported 'color' class
        :new_desc - a new description for the track
        """
        track = track.upper()
        if track not in self.tracks:
            raise ValueError("Given track {} does not exist".format(track))

        if new_name:
            if new_name in self.tracks:
                raise ValueError("Track '{}' already exists".format(new_name))

            self.tracks[new_name] = self.tracks[track]
            del self.tracks[track]
            track = new_name

        if new_color:
            self.tracks[track][self.COLOR] = new_color

        if new_desc:
            self.tracks[track][self.DESC] = new_desc
