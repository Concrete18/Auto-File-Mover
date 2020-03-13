import os
import sys
import shutil
import fnmatch

WatchedFolderDef = 'D:/Downloads'

KeywordDef = {
    'Wallpaper': 'D:/Downloads/Wallpapers',
}

FileTypeDef = {
    '.docx': 'D:/Downloads/Documents',
    '.mp4': 'D:/Downloads/Video',
    '.png': 'D:/Downloads/Images',
    '.jpg': 'D:/Downloads/Images',
    '.txt': 'D:/Downloads/Documents',
    '.exe': 'D:/Downloads/Installers',
    '.wav': 'D:/Downloads/Audio Files',
}

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
                    if fnmatch.fnmatch(File, '*' + Keyword + '*'):
                        OutputText = Keyword + ' Found named ' + File
                        MoveDestination = KeywordDef[Keyword]
                for ToDel in DeleteDef:
                    if fnmatch.fnmatch(File, '*' + ToDel + '*'):
                        OutputText = ''
                        FileDelete(File, ToDel)
                        MoveDestination = 'cancel'
                print(OutputText)
                FileMove(File, MoveDestination)


WatchedFolderTemp = input("Press Enter to continue with default\nType cd to enter new directory") or WatchedFolderDef
print()  # Blank line for Spacing

MoveByName(WatchedFolderTemp)
print('Finished File check of ' + WatchedFolderTemp + '.')

input("Press Enter to Exit")
sys.exit()
