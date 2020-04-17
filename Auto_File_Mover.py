import os
import sys
import shutil
import fnmatch
from tkinter import Tk, Label, Button, Frame, Entry, filedialog
# import tkinter as tk


# Checks for keywords in file names.
# Todo Set to only count keywords for certain file types.
KeywordDef = {
    'Wallpaper': 'D:/Downloads/Wallpapers',
}

# Checks for specific file types.
FileTypeDef = {
    '.docx': 'D:/Downloads/Documents',
    '.mp4': 'D:/Downloads/Video',
    '.png': 'D:/Downloads/Images',
    '.jpg': 'D:/Downloads/Images',
    '.txt': 'D:/Downloads/Documents',
    '.exe': 'D:/Downloads/Installers',
    '.wav': 'D:/Downloads/Audio Files',
}

# These file types will cause the script to ask if you want to delete them.
# Inputting yes/y deletes the .exe file.
# Inputting no/n means it reverts to moving to FileTypeDef.
DeleteDef = {'.exe', '.test'}


def FileMove(Target, Dest):
    if Dest == 'cancel':
        pass
    else:
        if os.path.isdir(Dest) is True:
            pass
        else:
            os.mkdir(Dest)
        shutil.move(WatchedFolderDef + '/' + Target, Dest)
        print('Move Complete.')
        print()  # Blank line for Spacing


def FileDelete(Target, Type):
    MoveDestination = ''
    InstallerDelResp = input('Do you want to delete it?')
    if InstallerDelResp == 'yes' or InstallerDelResp == 'y':
        os.remove(WatchedFolderDef + '/' + Target)
        print('Deleted File.')
    else:
        print('Ok, copying ' + Target + 'to the ' + Type + ' default folder.')
        FileMove(Target, FileTypeDef[Type])


def MoveByName(TargetDir):
    for File in os.listdir(TargetDir):
        for FileType in FileTypeDef:
            if File.endswith(FileType):
                print(File + " Found.")
                OutputText = 'Specific ' + FileType + ' not found. Moving file named ' + File + ' to default folder.'
                MoveDestination = FileTypeDef[FileType]
                for Keyword in KeywordDef:
                    if fnmatch.fnmatch(File, f'*{Keyword}*'):
                        OutputText = Keyword + ' Found named ' + File
                        MoveDestination = KeywordDef[Keyword]
                for ToDel in DeleteDef:
                    if fnmatch.fnmatch(File, '*' + ToDel + '*'):
                        OutputText = ''
                        FileDelete(File, ToDel)
                        MoveDestination = 'cancel'
                print(OutputText)
                FileMove(File, MoveDestination)


WatchedFolderDef = 'D:/Downloads'
WatchedFolder = ''


def StartFunction():
    global WatchedFolder
    WatchedFolder = input("Press Enter to continue with default\nType cd to enter new directory")
    print()  # Blank line for Spacing
    if WatchedFolder == 'cd':
        WatchedFolder = filedialog.askdirectory(initialdir="C:/", title="Select Directory")
        if WatchedFolder == '':
            print('No Directory Selected\nSwitching to Default Directory.\n')
            WatchedFolder = WatchedFolderDef
    else:
        WatchedFolder = WatchedFolderDef
    return WatchedFolder


MoveByName(StartFunction())
print(f'Finished File check of {WatchedFolder}.')

input("Press Enter to Exit")
sys.exit()
