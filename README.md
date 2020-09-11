# Auto Folder Cleaner

This script searches a watched directory in order to move files based on their filetypes and keywords.
It works by using For Loops to go through files in the watched directory.
It checks for matches in a file type and keyword Dictionaries.

## Features

* Fully Configurable preferences(Example Below).
* Json based config file with PC name detection for choosing the config to use.
* Auto move files based on keywords or filetypes.
* Ask to delete files based on a delete file type list.
* AutoStart Capable but also has File Dialog to choose any folder for execution.
* Threading for completing multiple transfers at a time.

## Future Plans

* Progress Bar (Once I figure out how to)
* Incorporate [send2trash](https://github.com/arsenetar/send2trash) in delete check.

## Preferences Example

```json
{
    "settings":
        {
            "watched_folder": "C:/Downloads",
            "autostart": 0
        },
    "dictionaries":
        {
            "file_type_groups":
                {
                    "audio": [".mp3", ".wav", ".flac"],
                    "image": [".jpg", ".png", ".gif", "tiff", "tif"],
                    "video": [".mp4", ".wave", ".mkv", ".mpeg", "mpeg4", ".avi", ".mpeg4", ".avi", ".wmv"],
                    "text": [".txt", ".doc", ".docx", ".pdf", ".odt"],
                    "spreadsheet": [".xls", ".xlsx", ".xlsm", ".ods"],
                    "compressed": [".deb", ".pkg", ".rar", ".rpm", ".tar", ".gz", ".z", ".zip"],
                    "executable": [".exe", ".bat", ".apk", ".bin", ".com", ".jar", ".msi", ".wsf"],
                    "presentation": [".key", ".odp", ".pps", ".ppt", ".pptx"],
                    "programming": [".c", ".class", ".cpp", ".cs", ".h", ".java", ".php", ".py", ".sh", ".swift", ".vb"]
                },
            "file_group_dest":
                {
                    "audio":"C:/Downloads/Audio Files",
                    "image":"C:/Downloads/Images",
                    "video":"C:/Downloads/Videos",
                    "text":"C:/Downloads/Documents",
                    "spreadsheet":"C:/Downloads/Spreadsheets",
                    "compressed":"C:/Downloads/Compressed Files",
                    "executable":"C:/Downloads/Executable",
                    "presentation":"C:/Downloads/Presentations",
                    "programming":"C:/Downloads/Programming"
                },
            "keywords_dest":
                {
                    "Wallpaper": ["images", "D:/Google Drive/Photos/Wallpapers"]
                },
            "special_case_dest":
                {
                    ".mkv":"C:/Downloads/HD Videos"
                },
            "delete_def":
                [
                    ".exe", ".test", ".zip", ".rar", ".7z"
                ]
        }
}
```
