#resume function
import tkinter as tk
from tkinter import filedialog

def gatherHistoricalTime(movieWatching):
    strDivider = ', Elapsed Time: '

    # Using readlines()
    file_path = 'movie_history.txt'

    try:
        # Try to open the file for reading
        with open(file_path, 'r', encoding="utf-8") as file1:
            Lines = file1.readlines()
    except FileNotFoundError:
        # If the file is not found, create it
        print(f"File '{file_path}' not found. Creating the file.")
        open(file_path, 'w', encoding="utf-8").close()
        # Now, open the file for reading
        with open(file_path, 'r', encoding="utf-8") as file1:
            Lines = file1.readlines()

    count = 0
    found_occurrences = 0
    # Strips the newline character
    for line in reversed(Lines):
        lineSplitted = line.replace('Filename: ', '').strip().split(strDivider)
        movieWatched = lineSplitted[0]
        if movieWatched == movieWatching:
            found_occurrences += 1
            if found_occurrences == 1:
                timeStamp = lineSplitted[1] #the elapsed time of a movie that has been previously watched
                break
    else:
        timeStamp = '00:00:00' #If the movie haven't been played before, the resume button resumes from this timestamp
    file1.close()
    return timeStamp
