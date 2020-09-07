# Auto Folder Cleaner

This script searches a watched directory in order to move files based on their filetypes and keywords. It works by using For Loops to go through files in the watched directory. It checks for matches in a file type and keyword Dictionaries.

## Features

* Fully Configurable preferences(Example Below).
* Json based config file with PC name detection for choosing the config to use.
* Auto move files based on keywords or filetypes.
* Ask to delete files based on a delete file type list.
* AutoStart Capable but also has File Dialog to choose any folder for execution.
* Threading for completing multiple transfers at a time.

## Future Plans

* Progress Bar (Once I figure out how to)

## Preferences Example

```json
{
    "config": {
        "watched folder": [
            "C:/Downloads"
        ],
        "autostart": [
            0
        ],
        "keyword folder destinations": {
            "Wallpaper": "C:/Downloads/Wallpapers"
        },
        "file type definitions": {
            "image": [".jpg", ".png", ".gif"],
            "video": [".mp4", ".wave"],
            "text": [".txt", ".docx", ".doc", ".pdf"]
        },
        "file type folder destinations": {
            ".docx": "C:/Downloads/Documents",
            ".mp4": "C:/Downloads/Video",
            ".png": "C:/Downloads/Images",
            ".jpg": "C:/Downloads/Images",
            ".gif": "C:/Downloads/Images",
            ".txt": "C:/Downloads/Documents",
            ".exe": "C:/Downloads/Installers",
            ".wav": "C:/Downloads/Audio Files",
            ".zip": "C:/Downloads/Compressed Files",
            ".rar": "C:/Downloads/Compressed Files",
            ".7z": "C:/Downloads/Compressed Files"
        },
        "delete check list": [
        ".exe",
        ".test",
        ".zip",
        ".rar",
        ".7z"
        ]
    }
}
```
