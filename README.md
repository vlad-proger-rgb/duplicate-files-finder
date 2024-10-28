# Duplicate Files Finder

File manager with storage optimizer and duplicate files finder based on file content

## Description

This program can find duplicate files based on their **content**, but not simply by name/date/size/etc. Pressing buttons is accompanied by sounds.

## Usage

1. Open the program
2. Select the folder to analyze
3. Select the type to search (Music, Videos, Photos, Log files)
4. Select the type extension, (e.g. for music one of ".mp3", ".wav", ".flac")
5. Click "Find duplicates"
6. During the process the program will freeze the interface (unfortunately)
7. When completed, on the Main panel you will see a list of duplicate files

## Details

### Main panel

Found duplicates are grouped. Each group is a list of files, which have the same content. On top of group you can see its size and number of files.
Each file element has the following buttons:

* Open in player
* Open in explorer
* Delete (all deleted files will be moved to the trash)
* Size
* Name

In case of log files, on top there will be "Delete log files" button. Sometimes, file deletion fails due to usage by another program.

### Top panel

Top panel shows the number of found duplicates and space to be freed up.

### Left panel

* Entry box for folder path
* Combo box for extension to search
* Select folder button
* File type buttons: Music, Videos, Photos, Log files
* Execute search button
* Change the font size of file names/sizes
