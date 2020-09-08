from threading import Thread
from pyfiglet import Figlet
import tkinter.filedialog
import tkinter as tk
import fnmatch
import socket
import shutil
import time
import json
import sys
import os

if socket.gethostname() == 'Aperture-Two':
    config = 'personal_config.json'
else:
    config = 'config.json'
with open(config) as json_file:
    data = json.load(json_file)

# Default watcher folder
watched_folder = data['config']['settings']['watched_folder']

# Autostart using default folder toggle.
autostart = data['config']['settings']['autostart']

# Checks for keywords in file names.
keyword_def = data['config']['dictionaries']['keywords']
# TODO Set to only count keywords for certain file types.

file_type_def = data['config']['dictionaries']['file_type_defs']

# Checks for specific file types.
file_def_loc = data['config']['dictionaries']['file_def_loc']

# These file types will cause the script to ask if you want to delete them.
delete_def = data['config']['dictionaries']['delete_def']


def Set_Destination(watched_folder, f):
    '''This function checks for matches for file extensions and keywords.
    Using what is found, it sets the destination for the file.'''
    destination = 'skip'
    for file_type in file_def_loc:
        if f.endswith(file_type):
            destination = file_def_loc[file_type]
            for to_delete in delete_def:
                if fnmatch.fnmatch(f, f'*{to_delete}*'):
                    del_resp = input(f'{f} found.\nDo you want to delete it?\n')
                    if del_resp == 'yes' or del_resp == 'y':
                        os.remove(os.path.join(watched_folder, f))
                        print('Deleted File.')
                        return 'skip'
                    else:
                        print(f'Ok, copying {f} to the {file_type} default folder.\n')
                        destination =  file_def_loc[file_type]
            for keyword in keyword_def:
                if fnmatch.fnmatch(f, f'*{keyword}*'):
                    destination = keyword_def[keyword]
                    print(keyword_def[keyword])
    return destination


def File_Move(watched_folder, target, destination):
    '''Moves Target file to Destination after making the destination directory if it does not exist.
    It will also leave the file where it is if it already exists at the destination.'''
    if os.path.isdir(destination) is False:
        os.mkdir(destination)
    if os.path.exists(os.path.join(destination, target)):
        print(f'{target} already exists.\nLeaving file as is.')
    else:
        shutil.move(os.path.join(watched_folder, target), destination)


# Initializes the thead list for use in Move_By_Name() and Main()
threads = []


def Move_By_Name(watched_folder):
    '''This script checks each file in the watched folder and figures out the destination if any exist.
    Once a destinations are found, it moves the files via threads. It also returns a count of the total files moved.'''
    file_moved_count = 0
    for f in os.listdir(watched_folder):
        destination = Set_Destination(watched_folder, f)
        if destination != 'skip':
            file_moved_count += 1
            file_move_thread = Thread(target=File_Move, args=(watched_folder, f, destination))
            file_move_thread.start()
            threads.append(file_move_thread)
    return file_moved_count


def Set_Watched_Folder(watched_folder):
    '''Sets the Watched folder via tkinter Directory Dialog if you type cd. otherwise it uses what you entered for the watched folder.'''
    tk.Tk().withdraw()
    response = input("Press Enter to continue with default\nType cd to enter new directory\n")
    if response == 'cd':
        watched_folder = tk.filedialog.askdirectory(initialdir="C:/", title="Select Directory")
    if response == '':
        watched_folder = watched_folder
    return watched_folder


def Main(watched_folder):
    '''This is the main function that introduces the script and sets up backbone for everything.'''
    title = 'Auto Folder Cleaner'
    try:
        text = Figlet(font='slant')
        print(text.renderText(title))
    except:
        print(title)
    if autostart != 1:
        watched_folder = Set_Watched_Folder(watched_folder)
    else:
        print(f'Autostarting in {watched_folder}.')
        overall_start = time.perf_counter()
        file_moved_count = Move_By_Name(watched_folder)
    for thread in threads:
        thread.join()
    print(f'\nFinished file check of {watched_folder}.\n{file_moved_count} files moved.')
    overall_finish = time.perf_counter()
    elapsed_time = round(overall_finish-overall_start, 2)
    if elapsed_time != 0:
        converted_elapsed_time = f'{int(elapsed_time/60)}:{int(str(elapsed_time%60).zfill(2))}'
    else:
        converted_elapsed_time = 'Instant'
    print(f'Overall Time Elapsed: {converted_elapsed_time}\n')
    input("Press Enter to Exit\n")
    sys.exit()


if __name__ == '__main__':
    Main(watched_folder)
