from tkinter import filedialog
from threading import Thread
import datetime as dt
import tkinter as tk
import socket
import shutil
import time
import json
import sys
import os


class Cleaner:


    def __init__(self):
        if  __name__ != '__main__':
            self.config = 'config.json'
        elif socket.gethostname() == 'Aperture-Two':  # sets to my personal config instead of the example config on my pc
            self.config = 'personal_config.json'
        else:
            self.config = 'config.json'
        with open(self.config) as json_file:
            self.data = json.load(json_file)
        self.threads = []  # Initializes the thead list for use in move_by_name() and main()
        '''
        These variables, lists and disctionaries are pulled from
        the config file to allow for easier customization without touching the main code.
        '''
        # Settings
        self.watched_folder = self.data['settings']['watched_folder']  # Default watcher folder.
        self.autostart = self.data['settings']['autostart']  # Autostart using default folder toggle.
        # Dictionaries
        self.file_type_groups = self.data['dictionaries']['file_type_groups']  # Sets file types into groups.
        self.file_group_dest = self.data['dictionaries']['file_group_dest']  # Sets destination based on file group.
        self.keywords_dest = self.data['dictionaries']['keywords_dest']  # Checks for keywords in file names.
        self.special_case_dest = self.data['dictionaries']['special_case_dest']  # Lists special cases for file type destinations.
        self.delete_def = self.data['dictionaries']['delete_def']  # Lists file types that you might want to delete.


    def run_delete_empty_folders(self):
        '''
        Deletes empty folders in the watched_folder entered as an argument.

        Keyword arguments:

        f -- file that is being checked for file extension and keyword matches
        '''
        # checks config setting for deleting empty folders - enable/disable
        delete_empty_folders = self.data['settings']['delete_empty_folders']
        if delete_empty_folders == 1:
            delete_total = 0  # init var for total empty folders deleted
            for f in os.scandir(self.watched_folder):
                if os.path.exists(f.path) and not os.path.isfile(f.path):  # checks if f is a folder instead of a file
                    if len(os.listdir(f.path)) == 0:  # detects if folder is empty
                        try:
                            os.rmdir(f.path)
                        except OSError:  # error check in case of unseen circumstance
                            print(f'Failed to delete {f.name}\nIt is not empty.')
                        delete_total += 1
                if delete_total > 0: # prints info if empty folders were deleted
                    print('Deleted empty folders.')


    @staticmethod
    def get_file_type(f):
        '''Gets file type from the given file name. It only uses the last period separating extension.'''
        file_type = ''
        split_string = f.name.split(".")
        file_type = f'.{split_string[-1]}'
        return file_type


    def set_destination(self, f):
        '''
        This function looks for matches in file extensions and keywords.
        It sets the destination for the file or sets it to skip if the file was deleted.

        Keyword arguments:

        f -- file that is being checked for file extension and keyword matches
        '''
        destination = 'skip'
        file_type = self.get_file_type(f)
        for file_group, file_type_list in self.file_type_groups.items():  # for loop that checks for file group matches
            if file_type in file_type_list:
                destination = self.file_group_dest[file_group]  # sets destination based on file group
                if file_type in self.delete_def: # checks for file types in delete whitelist
                    del_resp = input(f'{f.name} found.\nDo you want to delete it? (Will skip recycle bin)\n')
                    if del_resp == 'yes' or del_resp == 'y':
                        # TODO Add recycle bin support for windows
                        os.remove(f.path)
                        print('Deleted File.')
                        return 'skip' #  prevents file from being copied if it was deleted
                if file_type in self.special_case_dest:
                    destination = self.special_case_dest[file_type] # sets destination based on special case
                for keyword, keyword_data in self.keywords_dest.items():  # for loop that checks for keyword matches
                    if keyword.lower() in f.name.lower(): # checks for match with upper case removed
                        if file_type in keyword_data[0]:
                            destination = keyword_data[1]
                        elif file_group == keyword_data[0][0]:
                            destination = keyword_data[1]
        return destination  # end destination for file entered as f argument


    @staticmethod
    def file_move(target, destination):
        '''
        Moves Target file to Destination after making the destination directory if it does not exist.
        It will also leave the file where it is if it already exists at the destination.

        Keyword arguments:

        target -- file to move

        destination -- destination of target file
        '''
        if os.path.isdir(destination) is False:  # checks if destination directory exist
            os.mkdir(destination) # makes directory if it does not exist
        if os.path.exists(os.path.join(destination, target.name)): # checks if file was moved previously and cancels move
            print(f'{target.name} already exists at destination.\nLeaving file as is.')
        else:
            shutil.move(target.path, destination)


    # TODO Add progress bar.
    def move_by_name(self):
        '''
        This function checks each file in the watched folder and figures out the destination if any exist.
        Once a destinations are found, it moves the files via threads. It also returns a count of the total files moved.
        '''
        files_moved_count = 0
        for f in os.scandir(self.watched_folder):
            if not f.name.startswith('.') and f.is_file():
                destination = self.set_destination(f)
                if destination != 'skip':  # skips file move if file was deleted in set_destination function
                    files_moved_count += 1
                    file_move_thread = Thread(target=self.file_move, args=(f, destination))
                    file_move_thread.start()
                    self.threads.append(file_move_thread)
        return files_moved_count  # returns total files moved for use later


    def set_watched_folder(self):
        '''
        Sets the Watched folder via tkinter Directory Dialog if you type cd.
        Otherwise it uses default for the watched folder.
        '''
        tk.Tk().withdraw() # hides blank tkinter window that pop up otherwise
        response = input("Press Enter to continue with default\nType cd to enter new directory\n")
        if response == 'cd':  # change directory command
            self.watched_folder = filedialog.askdirectory(initialdir="C:/", title="Select Directory")


    def main(self):
        '''
        This is the main function that introduces the script and sets up the backbone for everything.
        '''
        print('Auto Folder Cleaner')
        if self.autostart != 1:  # determines if program asks to change directory or not
            self.set_watched_folder()
        else:
            print(f'Autostarting in {self.watched_folder}.')
        overall_start = time.perf_counter() # start time for checking elaspsed runtime
        file_moved_count = self.move_by_name()
        for thread in self.threads:
            thread.join()
        print(f'\nFinished file check of {self.watched_folder}.\n{file_moved_count} files moved.')
        self.run_delete_empty_folders()
        overall_finish = time.perf_counter() # stop time for checking elaspsed runtime
        elapsed_time = round(overall_finish-overall_start, 2)
        if elapsed_time != 0:  # converts elapsed seconds into readable format
            converted_elapsed_time = str(dt.timedelta(seconds=elapsed_time))
        else:
            converted_elapsed_time = 'Instant'
        print(f'Overall Time Elapsed: {converted_elapsed_time}\n')
        input("Press Enter to Exit\n")
        sys.exit()


if __name__ == '__main__':
    App = Cleaner()
    App.main()
