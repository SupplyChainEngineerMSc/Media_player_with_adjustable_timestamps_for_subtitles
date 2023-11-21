import vlc
import tkinter as tk
from read_timestamp import gatherHistoricalTime
from tkinter import filedialog
import time
import shutil
import os
import sys  # Import sys module for exiting the script
from datetime import datetime

class VLCPlayer:
    def __init__(self, video_path, subtitle_path):
        self.instance = vlc.Instance("--no-xlib")
        self.media_player = self.instance.media_player_new()

        self.video_path = video_path
        self.subtitle_path = subtitle_path

        self.create_player()

    def create_player(self):
        # Create a media instance for video
        video_media = self.instance.media_new(self.video_path)
        # Create a media instance for subtitle
        subtitle_media = self.instance.media_new(self.subtitle_path)
        subtitle_media.add_option(":start-time=0")
        # Creating options for subtitles
        options = f'sub-file={self.subtitle_path}'
        media = self.instance.media_new(self.video_path, options)
        # Set the media to the media player
        self.media_player.set_media(media)


    def start_player(self):
        self.media_player.play()

    def stop_player(self):
        return self.media_player.get_time()  # Capture current playback time

    def set_time(self, new_time):
        self.media_player.set_time(new_time)

    def adjust_subtitles(self, offset):
        current_time = self.stop_player()

        with open(self.subtitle_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(self.subtitle_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if '-->' in line:
                    start, end = line.split('-->')
                    start_time = self.parse_time(start.strip()) + offset
                    end_time = self.parse_time(end.strip()) + offset

                    adjusted_line = f"{self.format_time(start_time)} --> {self.format_time(end_time)}\n"
                    file.write(adjusted_line)
                else:
                    file.write(line)

        self.create_player()
        self.start_player()

        self.set_time(current_time)  # Set the time to the captured value

    def resume_from_stop(self):
        self.stop_player()
        new_time = gatherHistoricalTime(self.video_path)
        print("new_time er: ", new_time)

        def time_str_to_seconds(time_str):
            # Parse the time string into a datetime object
            time_object = datetime.strptime(time_str, '%H:%M:%S')

            # Calculate the total number of seconds
            total_seconds = time_object.hour * 3600 + time_object.minute * 60 + time_object.second

            return total_seconds

        new_time_seconds = time_str_to_seconds(new_time)

        self.set_time(new_time_seconds*1000)
        print("new time is: ", new_time_seconds*1000)
        self.start_player()

    def jump_forward(self):
        current_time = self.stop_player()
        new_time = current_time + 15000  # 15 seconds in milliseconds
        self.set_time(new_time)
        self.start_player()

    def jump_backward(self):
        current_time = self.stop_player()
        new_time = max(0, current_time - 15000)  # 15 seconds in milliseconds, ensure not negative
        self.set_time(new_time)
        self.start_player()

    def parse_time(self, time_str):
        h, m, s = map(float, time_str.replace(",", ".").split(":"))
        return int((h * 3600 + m * 60 + s) * 1000)

    def format_time(self, time_ms):
        s, ms = divmod(time_ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(ms):03d}"

    def on_close(self, event=None):
        elapsed_time = self.media_player.get_time() / 1000  # Convert milliseconds to seconds
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        # Append filename and elapsed time to the text file
        movie_history_path = r"movie_history.txt"
        with open(movie_history_path, 'a', encoding='utf-8') as history_file:
            history_file.write(f"Filename: {self.video_path}, Elapsed Time: {formatted_time}\n")
        print(f"Elapsed Time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}")
        self.stop_player()
        root.destroy()
        sys.exit()  # Terminate the script



# Paths to the video file and subtitle file (SRT format)
def select_input_file(titlex):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title=titlex)
    return file_path


# Path to the video file
video_path = select_input_file("Select video file")

# Path to the subtitle file (SRT format)
subtitle_path_regular = select_input_file("Select subtitle file")
subtitle_path = r"{}".format(subtitle_path_regular).replace('/', '\\')


def copy_and_rename_file(file_path):
    # Split the file path into directory and filename
    directory, filename = os.path.split(file_path)

    # Split the filename into name and extension
    name, extension = os.path.splitext(filename)

    # Generate the new filename with "_copied" added before the extension
    new_filename = f"{name}_copied{extension}"

    # Create the full path for the new file
    new_file_path = os.path.join(directory, new_filename)

    try:
        # Check if the file with "_copied" already exists
        if not os.path.exists(new_file_path):
            # Copy the file to the new path
            shutil.copy(file_path, new_file_path)
            print(f"File copied successfully to {new_file_path}")
        else:
            print(f"File with '_copied' already exists in the directory.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function to copy and rename the file
copy_and_rename_file(subtitle_path)

player = VLCPlayer(video_path, subtitle_path)

def resume_button(event):
    player.resume_from_stop()

def on_up_arrow(event):
    player.adjust_subtitles(250)


def on_down_arrow(event):
    player.adjust_subtitles(-250)


def on_right_arrow(event):
    player.jump_forward()


def on_left_arrow(event):
    player.jump_backward()


root = tk.Tk()
root.title("VLC Player")


# Function to toggle fullscreen
def toggle_fullscreen(event):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))


# Bind double-click event to toggle_fullscreen function
root.bind("<Double-Button-1>", toggle_fullscreen)

# Create a Tkinter label for displaying the elapsed time
time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 12), bg="black", fg="white")
time_label.place(x=10, y=10)  # Adjust position as needed

# Set the window handle for the VLC player
wnd_id = root.winfo_id()
player.media_player.set_hwnd(wnd_id)

player.start_player()

root.bind("<Up>", on_up_arrow)
root.bind("<Down>", on_down_arrow)
root.bind("<Right>", on_right_arrow)
root.bind("<Left>", on_left_arrow)


root.bind("<r>", resume_button)

# Function to toggle fullscreen on "f" key
def fullscreen_on_f(event):
    toggle_fullscreen(event)


# Bind fullscreen_on_f function to the "f" key
root.bind("<f>", fullscreen_on_f)


# Function to toggle play/pause on space or "p" key
def toggle_play_pause(event):
    if player.media_player.is_playing():
        player.media_player.pause()
    else:
        player.media_player.play()


# Bind toggle_play_pause function to spacebar and "p" key
root.bind("<space>", toggle_play_pause)
root.bind("p", toggle_play_pause)


def on_close(event):
    player.on_close()


root.protocol("WM_DELETE_WINDOW", player.on_close)

root.mainloop()
