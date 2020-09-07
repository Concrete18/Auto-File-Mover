# Auto Folder Cleaner

This script searches a watched directory in order to move files based on their filetypes and keywords. It works by using For Loops to go through files in the watched directory. It checks for matches in a file type and keyword Dictionaries.

## Features

* Fully Configurable preferences(Example Below).
* Auto move files based on keywords or filetypes.
* Ask to delete files based on a delete file type list.
* AutoStart Capable but also has File Dialog to choose any folder for execution.
* Threading for completing multiple transfers at a time.

## Future Plans

* Progress Bar (Once I figure out how to)
* sdd

## Preferences Example

```Python
WatchedFolderDef = 'D:/Downloads'

# Checks for keywords in file names.
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
# No means it reverts to moving to FileTypeDef.
DeleteDef = {'.exe', '.test'}
```
