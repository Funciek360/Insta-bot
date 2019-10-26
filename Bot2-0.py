# GUI BOT REFERENCES

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import time
import os
import urllib.request
import zipfile
import shutil
import threading

# WEB BOT REFERENCES
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, \
    StaleElementReferenceException
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from urllib.error import URLError
from urllib.request import urlopen
import requests
import os
from random import randint
import platform
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import subprocess
import webbrowser
from Naked.toolshed.shell import execute_js, muterun_js
from screeninfo import get_monitors

mouse = MouseController()
keyboard = KeyboardController()
MONITORS = get_monitors()
MONITORS_SIZES = []
for monitor in MONITORS:
    width, height = monitor.width, monitor.height
    if not [width, height] in MONITORS_SIZES:
        MONITORS_SIZES.append([width, height])
## DOWNLOAD GEKODRIVER IF NOT INSTALLED
system = platform.system()
print('SYSTEM: ', system.lower())
CWD = os.getcwd()
win_zip_directory = os.getcwd() + '/gekodriver.zip'
win_unzip_directory = os.getcwd() + '/gekodriver'



# check the system name and downloads the correct gekodriver ( for now it works only for windows )
if 'windows' in system.lower() :
    if not os.path.exists('geckodriver.exe'):
        url = f'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-win64.zip'
        urllib.request.urlretrieve(url, win_zip_directory)

        with zipfile.ZipFile(win_zip_directory, 'r') as zip_ref:
            zip_ref.extractall(win_unzip_directory)
        zip_ref.close()

        os.remove(win_zip_directory)
        shutil.move(win_unzip_directory + '/geckodriver.exe', CWD + '/geckodriver.exe')
        shutil.rmtree(win_unzip_directory)
    EXE_PATH = f'{CWD}/geckodriver.exe'

elif 'darwin' in system.lower():
    if not os.path.exists('geckodriver'):
        pass
    EXE_PATH = f'{CWD}/geckodriver'

elif 'linux' in system.lower():
    if not os.path.exists('geckodriver'):
        pass
    EXE_PATH = f'{CWD}/geckodriver'

def send(word):
    if word == '<ENTER>':
        keyboard.press(Key.enter)
    else:
        for letter in word:
            if letter == ' ':
                keyboard.press(Key.space)
                keyboard.release(Key.space)
            else:
                keyboard.press(letter)
                keyboard.release(letter)
'''
  ____   ____ _______    _____ _    _ _____ 
 |  _ \ / __ \__   __|  / ____| |  | |_   _|
 | |_) | |  | | | |    | |  __| |  | | | |  
 |  _ <| |  | | | |    | | |_ | |  | | | |  
 | |_) | |__| | | |    | |__| | |__| |_| |_ 
 |____/ \____/  |_|     \_____|\____/|_____|

'''

settings_block = 'Settings_'
all_settings = 'username', 'password', 'pages', 'auto_comment', 'auto_like', \
               'auto_follow', 'auto_unfollow', 'run_in_background', 'delay_time'

# check if all the data files of a user exists
def check_files(profile):
    files = [
        CWD + "/Datas/_Acomment_" + profile + ".txt",
        CWD + "/Datas/_Aunfollow_list_" + profile + ".txt",
        CWD + "/Datas/_profile_visited_" + profile + ".txt",
        CWD + "/Datas/Stats_" + profile + ".txt",
        CWD + "/Datas/to_visit_" + profile + ".txt",
    ]
    today_date = str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_mon) + "/" + str(
        time.localtime().tm_year)

    for file in files:
        if not os.path.exists(file):
            with open(file, "w") as file_:
                if file == CWD + "/Datas/Stats_" + profile + ".txt":
                    file_.write(
                        "Date:" + today_date + "\nfollowers_number:0:interactions:0:unfollow:0:comments:0:likes:0:follow:0 \n")
        if file == CWD + "/Datas/Stats_" + profile + ".txt":
            with open(file, "a") as file_:
                with open(file, "r") as file_read:
                    lines = file_read.read()
                if not "Date:" + today_date in lines:
                    file_.write(
                        "Date:" + today_date + "\nfollowers_number:0:interactions:0:unfollow:0:comments:0:likes:0:follow:0 \n")


# remove all the data files of a user
def remove_files(profile):
    files = [
        CWD + "/Datas/_Acomment_" + profile + ".txt",
        CWD + "/Datas/_Aunfollow_list_" + profile + ".txt",
        CWD + "/Datas/_profile_visited_" + profile + ".txt",
        CWD + "/Datas/Stats_" + profile + ".txt",
        CWD + "/Datas/to_visit_" + profile + ".txt",
    ]

    for file in files:

        if os.path.exists(file):
            os.remove(file)

# check if a word is in a file
def word_in_file(file_path, word):
    with open(file_path, 'r') as file:
        return word in file.read()

# read a data field in a file by a given datas separator and the block title
# SETTINGS_MARCO -- > Block Title
# username: hey: pass: hey: age: 12: --> datas
# SETTINGS_GIULIO -- > Block Title
# username: hey1: pass: hey1: age: 22: --> datas
def read_in_block(file_path, Block_title, datas_separator, *args):
    returned_dict = dict()
    for arg in args:
        returned_dict[arg] = []

    with open(file_path, 'r') as file:
        text = file.readlines()

    for index in range(len(text)):
        line = text[index]
        line = line.strip()
        if line.lower().startswith(Block_title.lower()):
            next_no_null_line_counter = 1
            if index + next_no_null_line_counter >= len(text):
                raise ValueError("No data funnded")
            while text[index + next_no_null_line_counter].strip() == "":
                next_no_null_line_counter += 1

            datas_line = text[index + next_no_null_line_counter]
            datas_line = datas_line.strip()
            datas_line = datas_line.split(datas_separator)

            for i in range(len(datas_line)):
                data = datas_line[i]
                data = data.strip()
                if data in (args):
                    returned_dict[data].append(datas_line[i + 1])

    return returned_dict

# rewrite some datas inside a block by a given block title and datas separator
def write_in_block(file_path, Block_title, datas_separator, **kwargs):
    with open(file_path, 'r') as file:
        text = file.readlines()

    returned_dict = dict()
    for key, value in kwargs.items():
        returned_dict[key] = []

    for index in range(len(text)):
        line = text[index]
        line = line.strip()
        next_no_null_line_counter = 0
        if line.lower().startswith(Block_title.lower()):
            next_no_null_line_counter = 1
            if index + next_no_null_line_counter >= len(text):
                raise ValueError("No data funnded")
            while text[index + next_no_null_line_counter].strip() == "":
                next_no_null_line_counter += 1

            datas_line = text[index + next_no_null_line_counter]
            datas_line = datas_line.strip()
            datas_line = datas_line.split(datas_separator)

            for i in range(len(datas_line)):
                data = datas_line[i]

                if data in (returned_dict):
                    to_edit = datas_line[i + 1]
                    if "+=" in kwargs[data]:
                        previous_num = int(datas_line[i + 1])
                        new_num = previous_num + int(kwargs[data][2:])
                        datas_line[i + 1] = str(new_num)
                    else:
                        datas_line[i + 1] = kwargs[data]

            datas_line = datas_separator.join(datas_line)
            text[index + next_no_null_line_counter] = datas_line + "\n"
    with open(file_path, 'w') as file:
        for line in text:
            file.write(line)

# remove a data block by a given block title
def remove_block(file_path, Block_title):
    with open(file_path, 'r') as file:
        text = file.readlines()

    for index in range(len(text)):
        if index > len(text) - 1:
            break
        line = text[index]
        line = line.strip()
        next_no_null_line_counter = 0
        if line.lower().startswith(Block_title.lower()):
            next_no_null_line_counter = 1
            while text[index + next_no_null_line_counter].strip() == "":
                next_no_null_line_counter += 1

            text.remove(text[index])
            text.remove(text[index + next_no_null_line_counter - (1)])

    with open(file_path, 'w') as file:
        for line in text:
            file.write(line)

# BOT GUI
class Window:

    def __init__(self):

        self.settings_file = CWD + "/Datas/Settings.txt"

        # Gui settings
        self.root = tk.Tk()
        self.root.title("Instagram Tab")
        self.custom_font = ("Nirmala UI", 12)
        self.custom_font_10 = ("Nirmala UI", 9)
        style = ttk.Style()
        style.configure('my.TMenubutton', font=self.custom_font)
        # self.master.iconbitmap(default=cwd + "/assets/icona.ico")
        self.resolution = [int(elem) for elem in read_in_block(SETTINGS_FILE, 'MonitorResolution', ':', 'm_r')['m_r'][0].strip().split('x')]
        self.appBarPos = read_in_block(SETTINGS_FILE, 'ApplicationBar', ':', 'position')['position'][0]
        w = 730  # width for the Tk root
        h = 405  # height for the Tk root
        if self.resolution == [0, 0]:
            x = (self.root.winfo_screenwidth() / 2) - (w / 2)
            y = (self.root.winfo_screenheight() / 2) - (h / 2)
        else:
            x = (MONITOR_WIDTH / 2) - (w / 2)
            y = (MONITOR_HEIGHT / 2) - (h / 2)



        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.configure(bg="black")

        # Datas variables to save
        self.login_username = tk.StringVar()
        self.login_password = tk.StringVar()
        self.instagram_pages = tk.StringVar()
        self.instagram_page = tk.StringVar()
        self.delay_time = tk.StringVar()
        self.delay_time.set('120')
        self.auto_comment = tk.IntVar()
        self.auto_like = tk.IntVar()
        self.auto_follow = tk.IntVar()
        self.auto_unfollow = tk.IntVar()
        self.run_in_background = tk.IntVar()

        # Gui frames
        self.options_frame = tk.Canvas(self.root, width=220, height=395, bg="white", highlightthickness=0)
        self.stats_frame = tk.Canvas(self.root, width=495, height=395, bg="white", highlightthickness=0)
        self.new_profile_frame = tk.Canvas(self.root, width=495, height=395, bg="white", highlightthickness=0)
        self.comment_frame = tk.Canvas(self.root, width=495, height=395, bg="white", highlightthickness=0)
        self.profiles_frame = tk.Canvas(self.root, width=495, height=395, bg="white", highlightthickness=0)

        # emoji settings for the comment section
        self.emoji_dict = {}
        self.user_bot_dict = {}

        self.emoji_num_name = dict()
        self.emoji_name_num = dict()
        counter = 0
        for key in self.emoji_dict:
            self.emoji_num_name[counter] = key
            self.emoji_name_num[key] = counter
            counter += 1
        self.edit_profile_ = False

        # functions to run at the gui start
        self.create_new_profile_frame()
        self.create_comment_frame()
        self.create_profiles_frame()
        self.create_stable_frame()
        self.create_stats_frame()
        self.place_profiles_frame()
        self.place_stable_frame()

    def create_stable_frame(self):
        self.current_username = tk.StringVar()
        self.last_username = ""
        y = 10
        user_name = tk.Label(self.options_frame, text="Current user: ", fg="black", bg="white", font=self.custom_font)
        user_name.place(y=y, x=10)
        self.root.update()
        username = read_in_block(SETTINGS_FILE, "Last login", ":", "username")
        las_login_username = username['username'][0]
        self.current_username.set(las_login_username)
        if las_login_username not in usernames and las_login_username != 'None':
            # SETTINGS EDITING
            write_in_block(SETTINGS_FILE, "Last login", ":", username='None')
            self.current_username.set('None')
        self.last_username = self.current_username.get()
        username_options = ttk.OptionMenu(self.options_frame, self.current_username, self.current_username.get(), style='my.TMenubutton')
        username_options.place(y=y + 30, x=10)
        self.username_options = username_options
        self.update_username_optionmenu()
        self.root.update()
        profiles_button = tk.Button(self.options_frame, text="Profiles", bg="white", font=self.custom_font, command=self.place_profiles_frame)
        profiles_button.place(y=y + 75, x=10)
        self.root.update()
        stats_button = tk.Button(self.options_frame, text="stats", bg="white", font=self.custom_font, command=self.place_stats_frame)
        stats_button.place(y=profiles_button.winfo_height() + 90 + y, x=10)
        self.root.update()

        self.change_resolution_button = tk.Button(self.options_frame, text="Monitor Resolution", bg="green", font=self.custom_font, command=self.get_monitor_resolution)
        self.change_resolution_button.place(y=stats_button.winfo_height() + 135 + y, x=10)
        if self.resolution == [0, 0]:
            self.change_resolution_button.config(bg='red', fg='white')
            self.get_monitor_resolution()
        if len(MONITORS_SIZES) < 2:
            self.change_resolution_button.config(state='disable')

        self.change_appBarPos_button = tk.Button(self.options_frame, text="AppBar Position", bg="green", font=self.custom_font, command=self.get_app_bar_pos)
        self.change_appBarPos_button.place(y=stats_button.winfo_height() + 185 + y, x=10)
        if self.appBarPos == '':
            self.change_appBarPos_button.config(bg='red', fg='white')
            self.get_app_bar_pos()

    def get_app_bar_pos(self):
        # Creating master Tkinter window
        popup = tk.Toplevel(self.root)
        popup.wm_title("TaskBar position")
        w = 350  # width for the Tk root
        h = 270  # height for the Tk root
        if self.resolution == [0, 0]:
            x = (self.root.winfo_screenwidth() / 2) - (w / 2)
            y = (self.root.winfo_screenheight() / 2) - (h / 2)
        else:
            x = (MONITOR_WIDTH / 2) - (w / 2)
            y = (MONITOR_HEIGHT / 2) - (h / 2)

        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popup.resizable(False, False)

        canvas = tk.Canvas(popup, width=250, height=250)
        canvas.place(x=0, y=0)

        label_1 = tk.Label(popup, text='for the correct functioning of the bot,\nindicate the position of the application bar')
        canvas.create_window(175, 35, window=label_1)

        monitors_frame = tk.Canvas(popup, width=210, height=100, bg='white')
        canvas.create_window(175, 120, window=monitors_frame)

        # Tkinter string variable
        # able to store any string value
        v = tk.StringVar()

        values = {
            'LEFT': 'LEFT',
            'RIGHT': 'RIGHT',
            'TOP': 'TOP',
            'BOTTOM': 'BOTTOM',
        }

        # Loop is used to create multiple Radiobuttons
        # rather than creating each button seperately
        x = 15
        y = 10
        for (text, value) in values.items():
            radio_button = tk.Radiobutton(monitors_frame, font=self.custom_font_10,text=f'{value}', variable=v, value=value, bg='white', bd=0, highlightthickness=0)
            monitors_frame.create_window(x, y, window=radio_button, anchor=tk.NW)
            y+=30

        scrollbar = tk.Scrollbar(monitors_frame, command=monitors_frame.yview)
        scrollbar.place(x=0, y=0, relheight=1)
        monitors_frame.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 10, 0, y))

        label_2 = tk.Label(popup, text="Remember to execute the app on the main monitor\nfor run correctly the bot", fg='red')
        canvas.create_window(175, 210, window=label_2)
        button = tk.Button(popup, text="Submit", command=lambda: self.submit_appBar_pos(v.get(), popup))
        canvas.create_window(175, 250, window=button)
        self.change_appBarPos_button.config(bg='green', fg='black')

    def submit_appBar_pos(self, position, popup):
        write_in_block(SETTINGS_FILE, "ApplicationBar", ":", position=position)
        popup.destroy()

    def get_monitor_resolution(self):

        if len(MONITORS_SIZES) > 1:
            # Creating master Tkinter window
            popup = tk.Toplevel(self.root)
            popup.wm_title("Monitor resolution")
            w = 350  # width for the Tk root
            h = 270  # height for the Tk root
            if self.resolution == [0, 0]:
                x = (self.root.winfo_screenwidth() / 2) - (w / 2)
                y = (self.root.winfo_screenheight() / 2) - (h / 2)
            else:
                x = (MONITOR_WIDTH / 2) - (w / 2)
                y = (MONITOR_HEIGHT / 2) - (h / 2)

            popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
            popup.resizable(False, False)

            canvas = tk.Canvas(popup, width=250, height=250)
            canvas.place(x=0, y=0)

            label_1 = tk.Label(popup, text='There are more monitors.\n   Which one is the main monitor?  ')
            canvas.create_window(175, 35, window=label_1)

            monitors_frame = tk.Canvas(popup, width=210, height=100, bg='white')
            canvas.create_window(175, 120, window=monitors_frame)

            # Tkinter string variable
            # able to store any string value
            v = tk.StringVar()

            values = dict()
            for i in range(len(MONITORS_SIZES)):
                values[f'Monitor {i}'] = MONITORS_SIZES[i]

            # Loop is used to create multiple Radiobuttons
            # rather than creating each button seperately
            x = 15
            y = 10
            for (text, value) in values.items():
                radio_button = tk.Radiobutton(monitors_frame, text=f'{text}: {value}', variable=v, value=value, bg='white', bd=0, highlightthickness=0)
                monitors_frame.create_window(x, y, window=radio_button, anchor=tk.NW)
                y+=30

            scrollbar = tk.Scrollbar(monitors_frame, command=monitors_frame.yview)
            scrollbar.place(x=0, y=0, relheight=1)
            monitors_frame.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 10, 0, y))

            label_2 = tk.Label(popup, text="Remember to execute the app on the main monitor\nfor run correctly the bot", fg='red')
            canvas.create_window(175, 210, window=label_2)
            button = tk.Button(popup, text="Submit", command=lambda: self.submit_monitor_resolution(v.get().strip('[]').replace(' ', 'x'), popup))
            canvas.create_window(175, 250, window=button)
        else:
            write_in_block(SETTINGS_FILE, "MonitorResolution", ":", m_r=str(MONITORS_SIZES[0][0]) + 'x' + str(MONITORS_SIZES[0][1]))
        self.change_resolution_button.config(bg='green', fg='black')

    def submit_monitor_resolution(self, resolution, popup):
        write_in_block(SETTINGS_FILE, "MonitorResolution", ":", m_r=resolution)
        MONITOR_WIDTH, MONITOR_HEIGHT = [int(elem) for elem in resolution.split('x')]
        print(f'MONITOR WIDTH: {MONITOR_WIDTH}, MONITOR_HEIGHT: {MONITOR_HEIGHT}')
        popup.destroy()


    def place_stable_frame(self):
        self.options_frame.place(x=5, y=5, anchor=tk.NW)

    def create_stats_frame(self):
        # get current date and edits the stats file of the user
        today_date = str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_mon) + "/" + \
                     str(time.localtime().tm_year)
        if self.current_username.get() != 'None':
            infos = read_in_block(CWD + "/Datas/Stats_" + self.current_username.get() + ".txt", 'Date:' + today_date, ':',
                                  'followers_number', 'interactions', 'unfollow', 'comments', 'likes', 'follow', )

            profile_visited_today = infos['interactions']
            profile_followed_today = infos['follow']
            profile_unfollowed_today = infos['unfollow']
            likes_left_today = infos['likes']
            comments_left_today = infos['comments']
        else:
            profile_visited_today = 'None'
            profile_followed_today = 'None'
            profile_unfollowed_today = 'None'
            likes_left_today = 'None'
            comments_left_today = 'None'

        # stats frame graphics
        instagram_stats = tk.LabelFrame(self.stats_frame, text="Instagram Stats", bg="white", width=460, height=382, font=self.custom_font_10)
        self.stats_frame.create_window(10, 10, window=instagram_stats, anchor=tk.NW)
        date_label = tk.Label(instagram_stats, text="Today Date: ", bg="white", font=self.custom_font)
        date_label.place(x=10, y=10)
        self.root.update()
        date = tk.Label(instagram_stats, text=today_date, bg="white", fg="green", font=self.custom_font)
        date.place(x=date_label.winfo_x() + date_label.winfo_width() + 10, y=10)
        profile_visited_label = tk.Label(instagram_stats, text="Profile visited: ", bg="white", font=self.custom_font)
        profile_visited_label.place(x=10, y=40)
        self.root.update()
        profile_visited = tk.Label(instagram_stats, text=profile_visited_today, bg="white", fg="green", font=self.custom_font)
        profile_visited.place(x=profile_visited_label.winfo_x() + profile_visited_label.winfo_width() + 10, y=40)
        profile_followed_label = tk.Label(instagram_stats, text="Profile followed: ", bg="white", font=self.custom_font)
        profile_followed_label.place(x=10, y=70)
        self.root.update()
        profile_followed = tk.Label(instagram_stats, text=profile_followed_today, bg="white", fg="green", font=self.custom_font)
        profile_followed.place(x=profile_followed_label.winfo_x() + profile_followed_label.winfo_width() + 10, y=70)
        profile_unfollowed_label = tk.Label(instagram_stats, text="Profile unfollowed: ", bg="white", font=self.custom_font)
        profile_unfollowed_label.place(x=10, y=100)
        self.root.update()
        profile_unfollowed = tk.Label(instagram_stats, text=profile_unfollowed_today, bg="white", fg="green", font=self.custom_font)
        profile_unfollowed.place(x=profile_unfollowed_label.winfo_x() + profile_unfollowed_label.winfo_width() + 10, y=100)
        likes_left_label = tk.Label(instagram_stats, text="Likes left: ", bg="white", font=self.custom_font)
        likes_left_label.place(x=10, y=130)
        self.root.update()
        likes_left = tk.Label(instagram_stats, text=likes_left_today, bg="white", fg="green", font=self.custom_font)
        likes_left.place(x=likes_left_label.winfo_x() + likes_left_label.winfo_width() + 10, y=130)
        comments_left_label = tk.Label(instagram_stats, text="Comments left: ", bg="white", font=self.custom_font)
        comments_left_label.place(x=10, y=160)
        self.root.update()
        comments_left = tk.Label(instagram_stats, text=comments_left_today, bg="white", fg="green", font=self.custom_font)
        comments_left.place(x=comments_left_label.winfo_x() + comments_left_label.winfo_width() + 10, y=160)
        stats_list = tk.Button(instagram_stats, text="Stats History", state="disable", bg="white", font=self.custom_font, command=self.create_stats_list)
        stats_list.place(x=10, y=250)
        followers_count_list = tk.Button(instagram_stats, text="Followers History",  state="disable", bg="white", font=self.custom_font, command=self.create_followers_list)
        followers_count_list.place(x=10, y=300)
        refresh_button = tk.Button(instagram_stats, text="Refresh", bg="white", font=self.custom_font, command=self.create_stats_frame)
        refresh_button.place(x=300, y=200)
        scrollbar = tk.Scrollbar(self.stats_frame, command=self.stats_frame.yview)
        self.stats_frame.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 600))
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)

    def place_stats_frame(self):
        self.new_profile_frame.place_forget()
        self.comment_frame.place_forget()
        self.profiles_frame.place_forget()
        self.stats_frame.place(x=230, y=5)

    def create_stats_list(self):
        pass

    def create_followers_list(self):
        pass

    def create_profiles_frame(self):
        profiles_page = tk.LabelFrame(self.profiles_frame, text="Profiles", bg="white", width=460, height=382, font=self.custom_font_10)
        self.profiles_page = profiles_page
        self.profiles_frame.create_window(10, 10, window=profiles_page, anchor=tk.NW)

        infos = read_in_block(SETTINGS_FILE, settings_block, ':', 'username', 'password')
        usernames = infos['username']
        passwords = infos['password']

        x = 20
        y = 10
        # get all the users from the settings file and list them in the home page
        for i, username in enumerate(usernames):
            password = passwords[i]
            if len(username) <= 12:
                label_text = username
            else:
                label_text = username[:10] + '..'
            username_label = tk.Label(profiles_page, text=label_text, font=self.custom_font)
            username_label.place(x=x, y=y)
            edit_username = tk.Button(profiles_page, text='Edit', font=self.custom_font_10, command=lambda username_=username: self.edit_profile(username_))
            edit_username.place(x=x + 130, y=y - 5)
            remove_username = tk.Button(profiles_page, text='Remove', font=self.custom_font_10, command=lambda username_=username: self.remove_profile(username_))
            remove_username.place(x=x + 200, y=y - 5)
            run_bot = tk.Button(profiles_page, text='Run', font=self.custom_font_10, command=lambda username_=username, pswd=password: self.run_bot(username_, pswd))
            run_bot.place(x=x + 300, y=y - 5)
            stop_bot = tk.Button(profiles_page, text='Stop', font=self.custom_font_10, command=lambda username_=username: self.stop_bot(username_))
            stop_bot.place(x=x + 370, y=y - 5)
            y += 50

        add_profile = tk.Button(profiles_page, text='Add profile', font=self.custom_font, command=self.place_and_clear_new_profile_frame)
        add_profile.place(x=x, y=y)
        scrollbar = tk.Scrollbar(self.profiles_frame, command=self.profiles_frame.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        self.profiles_frame.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y + 80))
        if y > 320:
            profiles_page.configure(height=y + 60)

    # run instagram bot
    def run_bot(self, user, pswd):
        try:
            threading.Thread(target=self.bot, args=[user, pswd]).start()
        except Exception:
            pass

    # start instagram bot
    def bot(self, user, pswd):
        bot = InstagramBot(user, pswd)
        self.user_bot_dict[user] = bot
        bot.setup()
        bot.run()

    # stop instagram bot
    def stop_bot(self, user):
        bot = self.user_bot_dict[user]
        bot.stop()

    # remove all the files of a user and remove the user from the settings file
    def remove_profile(self, profile):
        if messagebox.askyesno('Attenction',
                               'Are you sure to delete this profile? ({0}).\nThis will cause the loss of all the relative stats and dsatas'.format(profile)):
            remove_block(SETTINGS_FILE, 'Settings_' + profile)
            remove_files(profile)
            self.update_username_optionmenu()
        for widget in self.profiles_frame.winfo_children():
            widget.destroy()
        # update the profiles frame
        self.create_profiles_frame()

    # chenge the last session user in the settings file
    def change_last_session_username(self, username):
        self.current_username.set(username)
        if username != self.last_username:
            # SETTINGS EDITING
            write_in_block(SETTINGS_FILE, "Last login", ":", username=username)
            self.last_username = username

        self.create_stats_frame()

    def update_username_optionmenu(self):
        username = 'None'
        infos = read_in_block(SETTINGS_FILE, settings_block, ":", "username")
        usernames = infos['username']
        self.username_options['menu'].delete(0, 'end')
        for username in usernames:
            self.username_options['menu'].add_command(label=username, command=lambda
                username_=username: self.change_last_session_username(username_))

        if self.current_username.get() not in usernames:
            self.current_username.set('None')

    # open the user settings page with the current user datas filled
    def edit_profile(self, profile):

        infos = read_in_block(SETTINGS_FILE, settings_block + profile, ':', *all_settings)
        self.edit_username = infos['username'][0]
        self.display_comment_button()
        self.place_and_clear_new_profile_frame()

        self.pages_list.config(state='normal')
        self.login_username.set(infos['username'][0])
        self.login_password.set(infos['password'][0])
        self.instagram_pages.set(infos['pages'][0])
        self.delay_time.set(infos['delay_time'][0])
        self.auto_comment.set(int(infos['auto_comment'][0]))
        self.auto_like.set(int(infos['auto_like'][0]))
        self.auto_follow.set(int(infos['auto_follow'][0]))
        self.auto_unfollow.set(int(infos['auto_unfollow'][0]))
        self.run_in_background.set(int(infos['run_in_background'][0]))


        self.pages_list.delete(1.0, tk.END)
        self.pages_list.insert(tk.INSERT, '- ' + self.instagram_pages.get().replace(' ', '').replace(',', '\n- '))
        self.pages_list.config(state='disabled')

        self.edit_profile_ = True
        self.display_comment_button()
        self.instagram_datas.config(text=f'Instagram Datas [Edit: {self.edit_username}]')

    def place_profiles_frame(self):
        self.new_profile_frame.place_forget()
        self.comment_frame.place_forget()
        self.stats_frame.place_forget()
        self.profiles_frame.place(x=230, y=5)

    # create the page where the user can save and edit his preferences
    def create_new_profile_frame(self):

        instagram_datas = tk.LabelFrame(self.new_profile_frame, text="Instagram Datas", bg="white", width=460, height=505, font=self.custom_font_10)
        self.instagram_datas = instagram_datas
        self.new_profile_frame.create_window(10, 10, window=instagram_datas, anchor=tk.NW)
        instagram_login_name_label = tk.Label(instagram_datas, text="Ig. Login username : ", font=self.custom_font, bg="white")
        instagram_login_name_label.place(x=10, y=0)
        instagram_login_password_label = tk.Label(instagram_datas, text="Ig. Login password : ", bg="white", font=self.custom_font)
        instagram_login_password_label.place(x=10, y=40)
        instagram_pages = tk.Label(instagram_datas, text="Pages to interact with : ", bg="white", font=self.custom_font)
        instagram_pages.place(x=10, y=75)
        self.root.update()
        instagram_login_name_entry = tk.Entry(instagram_datas, textvariable=self.login_username, bg="white", font=self.custom_font)
        instagram_login_name_entry.place(x=instagram_login_name_label.winfo_width() + 40, y=5)
        instagram_login_password_entry = tk.Entry(instagram_datas, textvariable=self.login_password, bg="white", show="*", font=self.custom_font, highlightbackground="red",
                                                  highlightthickness=0, )
        instagram_login_password_entry.place(x=instagram_login_password_label.winfo_width() + 40, y=40)
        search_page = tk.Entry(instagram_datas, bg="white", textvariable=self.instagram_page, font=self.custom_font, width=15)
        search_page.place(x=250, y=110)
        search_page.bind("<KeyRelease>", lambda event: self.search_page())
        add_page_button = tk.Button(self.instagram_datas, text="Add", bg="white", font=self.custom_font_10, command=self.add_page)
        add_page_button.place(x=250, y=140)
        remove_page_button = tk.Button(self.instagram_datas, text="Remove", bg="white", font=self.custom_font_10, command=self.remove_page)
        remove_page_button.place(x=320, y=140)
        self.pages_list = ScrolledText(instagram_datas, bg="white", font=self.custom_font, width=20, height=6)
        self.pages_list.place(x=10, y=110)
        instagram_interactions = tk.LabelFrame(instagram_datas, text="Bot Ig. interactions", bg="white", font=self.custom_font_10)
        self.instagram_interactions = instagram_interactions
        instagram_interactions.place(x=10, y=250)
        put_like = tk.Checkbutton(instagram_interactions, text="Auto like", bg="white", variable=self.auto_like, font=self.custom_font)
        put_like.place(x=0, y=0)
        self.root.update()
        put_comment = tk.Checkbutton(instagram_interactions, text="Auto comment", bg="white", variable=self.auto_comment, font=self.custom_font, command=self.display_comment_button)
        put_comment.place(x=put_like.winfo_width() + 10, y=0)
        self.put_comment_checkbox = put_comment
        self.write_comment_button = tk.Button(self.instagram_datas, text="Write comment", bg="white", font=self.custom_font_10, command=self.place_comment_frame)
        self.root.update()
        put_follow = tk.Checkbutton(instagram_interactions, text="Auto follow", bg="white", variable=self.auto_follow, font=self.custom_font, command=self.follow_option)
        put_follow.place(x=0, y=put_like.winfo_height())
        self.root.update()
        put_unfollow = tk.Checkbutton(instagram_interactions, text="Auto unfollow", bg="white", variable=self.auto_unfollow, font=self.custom_font)
        put_unfollow.place(x=put_follow.winfo_width() + 10, y=put_like.winfo_height())
        self.root.update()
        instagram_interactions.configure(width=put_unfollow.winfo_x() + put_unfollow.winfo_width() + 10, height=put_unfollow.winfo_y() + put_unfollow.winfo_height() + 5)
        self.root.update()
        delay_time_1 = tk.Label(instagram_datas, text="Delay time(seconds) between ", bg="white", font=self.custom_font)
        delay_time_1.place(x=10, y=instagram_interactions.winfo_y() + instagram_interactions.winfo_height() + 5)
        self.root.update()
        delay_time_2 = tk.Label(instagram_datas, text="two interaction cycles : ", bg="white", font=self.custom_font)
        delay_time_2.place(x=10, y=delay_time_1.winfo_y() + 5)
        self.root.update()
        delay_time_entry = tk.Entry(instagram_datas, textvariable=self.delay_time, bg="white", font=self.custom_font, width=5)
        delay_time_entry.place(x=delay_time_2.winfo_width() + 100, y=instagram_interactions.winfo_y() + instagram_interactions.winfo_height() + 15)
        bot_options = tk.LabelFrame(instagram_datas, text="Bot options", bg="white", font=self.custom_font_10)
        bot_options.place(x=10, y=delay_time_1.winfo_y() + 50)
        self.root.update()
        Run_in_background = tk.Checkbutton(bot_options, text="Run in background", bg="white", variable=self.run_in_background, font=self.custom_font)
        Run_in_background.place(x=0, y=0)
        self.root.update()
        bot_options.configure(width=Run_in_background.winfo_x() + Run_in_background.winfo_width() + 5, height=Run_in_background.winfo_y() + Run_in_background.winfo_height() + 5)
        self.root.update()
        scrollbar = tk.Scrollbar(self.new_profile_frame, command=self.new_profile_frame.yview)
        self.new_profile_frame.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 520))
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        sumbit = tk.Button(instagram_datas, text="Sumbit", font=self.custom_font, command=self.sumbit_settings)
        sumbit.place(x=250, y=instagram_interactions.winfo_y() + instagram_interactions.winfo_height() + 90)
        clear = tk.Button(instagram_datas, text="Clear", font=self.custom_font, command=self.clear_new_profile_frame)
        clear.place(x=350, y=instagram_interactions.winfo_y() + instagram_interactions.winfo_height() + 90)

    # add a name in the user 'pages' data field
    def add_page(self):
        username = None
        if self.edit_profile_:
            username = self.edit_username
        else:
            username = self.login_username.get()

        if username is not None:
            new_page = self.instagram_page.get()
            pages = self.instagram_pages.get().replace(' ', '').split(',')
            if not new_page in pages and new_page not in ['', ' ']:
                total_pages = self.instagram_pages.get()
                new_total_pages = total_pages + new_page if total_pages in ['', ' '] else total_pages + ',' + new_page
                self.instagram_pages.set(new_total_pages)
                # SETTINGS EDITING
                write_in_block(self.settings_file, settings_block + username, ":",
                               pages=self.instagram_pages.get())

            self.instagram_page.set("")
            self.pages_list.config(state='normal')
            self.pages_list.delete(1.0, tk.END)
            self.pages_list.insert(tk.INSERT, '- ' + self.instagram_pages.get().replace(' ', '').replace(',', '\n- '))
            self.pages_list.config(state='disabled')

    # remove a name in the user 'pages' data field
    def remove_page(self):
        username = None
        if self.edit_profile_:
            username = self.edit_username
        else:
            username = self.login_username.get()

        if username is not None:
            old_page = self.instagram_page.get()
            pages = self.instagram_pages.get().replace(' ', '').split(',')
            if old_page in pages:
                pages.remove(old_page)
                self.instagram_pages.set(','.join(pages))
                # SETTINGS EDITING
                write_in_block(self.settings_file, settings_block + username, ":",
                               pages=self.instagram_pages.get())

            self.instagram_page.set("")
            self.pages_list.config(state='normal')
            self.pages_list.delete(1.0, tk.END)
            self.pages_list.insert(tk.INSERT, '- ' + self.instagram_pages.get().replace(',', '\n- '))
            self.pages_list.config(state='disabled')

    # clear the datas inside the user settings gui page
    def clear_new_profile_frame(self):
        self.login_username.set("")
        self.login_password.set("")
        self.auto_comment.set(0)
        self.auto_like.set(0)
        self.auto_follow.set(0)
        self.auto_unfollow.set(0)

        self.instagram_page.set("")

    def place_new_profile_frame(self):
        self.instagram_pages.set("")
        self.stats_frame.place_forget()
        self.comment_frame.place_forget()
        self.profiles_frame.place_forget()
        self.new_profile_frame.yview_moveto(0)
        self.instagram_datas.config(text=f'Instagram Datas [Creating new profile]')
        self.new_profile_frame.place(x=230, y=5)

    def search_page(self):
        to_search_page = self.instagram_page.get()
        pages = self.instagram_pages.get().replace(' ', '').split(',')
        founded = ''
        for page in pages:
            if page.startswith(to_search_page):
                founded += '- ' + page + '\n'

        self.pages_list.config(state='normal')
        self.pages_list.delete(1.0, tk.END)
        self.pages_list.insert(1.0, founded)
        self.pages_list.config(state='disabled')

    def place_and_clear_new_profile_frame(self):
        self.clear_new_profile_frame()
        self.pages_list.config(state='normal')
        self.pages_list.delete(1.0, tk.END)
        self.pages_list.config(state='disable')
        self.edit_profile_ = False
        self.place_new_profile_frame()

    # place the button for open the gui comment page
    def display_comment_button(self):
        if self.auto_comment.get():
            self.write_comment_button.place(
                x=self.instagram_interactions.winfo_x() + self.instagram_interactions.winfo_width() + 10,
                y=self.instagram_interactions.winfo_y())
        else:
            self.write_comment_button.place_forget()

    def create_comment_frame(self):
        # comment page graphics
        comment_page = tk.LabelFrame(self.comment_frame, text="Ig. comment", bg="white", width=460, height=382, font=self.custom_font_10)
        self.comment_page = comment_page
        self.comment_frame.create_window(10, 10, window=comment_page, anchor=tk.NW)
        self.emoji_frame = tk.Canvas(comment_page, width=443, height=160, bg="white")
        self.emoji_frame.place(x=5, y=190)
        self.emoji_frame.bind("<MouseWheel>", lambda event, item=self.emoji_frame: self._on_mousewheel(event, item))
        comment_label = tk.Label(comment_page, text="Write your ig. comment: ", font=self.custom_font, bg="white")
        comment_label.place(x=10, y=10)
        self.comment_text = ScrolledText(comment_page, bg="white", font=self.custom_font, width=46, height=3)
        self.comment_text.place(x=10, y=50)
        self.root.update()
        sumbit_comment = tk.Button(comment_page, text="Sumbit comment", command=self.sumbit_comment, font=self.custom_font_10)
        self.root.update()
        sumbit_comment.place(x=435 - sumbit_comment.winfo_reqwidth(), y=self.comment_text.winfo_height() + 60, anchor=tk.NW)
        search_emoji_label = tk.Label(comment_page, text="Search emoji(emoji name): ", font=self.custom_font, bg="white")
        search_emoji_label.place(x=10, y=self.comment_text.winfo_height() + 55)
        self.root.update()
        self.search_emoji = tk.Text(comment_page, bg="white", font=self.custom_font, width=10, height=1)
        self.search_emoji.place(x=10, y=self.comment_text.winfo_height() + 85)
        self.search_emoji.bind("<KeyRelease>", lambda event: self.search_emojy())
        scrollbar_emoji = tk.Scrollbar(self.emoji_frame, command=self.emoji_frame.yview)
        self.emoji_frame.configure(yscrollcommand=scrollbar_emoji.set, scrollregion=(0, 0, 0, 400))
        scrollbar_emoji.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        self.display_emojy()
        scrollbar = tk.Scrollbar(self.comment_frame, command=self.comment_frame.yview)
        self.comment_frame.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 400))
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)

    def search_emojy(self):
        emoji_to_search = self.search_emoji.get(1.0, tk.END)
        emoji_to_search = emoji_to_search.strip().upper()
        emojis = self.emoji_frame.find_withtag("emoji")
        for elem in emojis:
            self.emoji_frame.delete(elem)
        self.emoji_name_list = list(self.emoji_dict.keys())
        self.emoji_name_list.sort()
        if emoji_to_search == "" or emoji_to_search == " ":
            self.display_emojy()
        else:
            x = 10
            y = 10
            for emoji_name in self.emoji_name_list:
                if emoji_to_search in emoji_name:
                    emoji_code = self.emoji_dict[emoji_name]
                    code_ = self.emoji_name_num[emoji_name]
                    emoji_button = self.emoji_frame.create_text(x, y, text=emoji_code, font=self.custom_font,
                                                                tag="emoji")
                    self.emoji_frame.tag_bind(emoji_button, "<Button-1>",
                                              lambda event, code=emoji_code: self.add_emoji(code))

                    if x <= 370:
                        x += 30
                    else:
                        x = 10
                        y += 30
            self.emoji_frame.configure(scrollregion=(0, 0, 300, y + 60))

    def display_emojy(self):
        emojis = self.emoji_frame.find_withtag("emoji")
        for elem in emojis:
            self.emoji_frame.delete(elem)

        x = 10
        y = 10

        for emoji_name in self.emoji_dict:
            emoji_code = self.emoji_dict[emoji_name]
            code_ = self.emoji_name_num[emoji_name]
            emoji_button = self.emoji_frame.create_text(x, y, text=emoji_code, font=self.custom_font, tag="emoji")
            self.emoji_frame.tag_bind(emoji_button, "<Button-1>", lambda event, code=emoji_code: self.add_emoji(code))

            if x <= 370:
                x += 30
            else:
                x = 10
                y += 30

        self.emoji_frame.configure(scrollregion=(0, 0, 0, y + 60))

    def add_emoji(self, emojy):
        self.comment_text.insert(tk.INSERT, emojy)

    def sumbit_comment(self):
        text = self.comment_text.get(1.0, tk.END)
        text = text.encode('utf-16', 'surrogatepass').decode('utf-16')
        user = 'None'
        if self.login_username.get() == '':
            user = self.current_username.get()
        else:
            user = self.login_username.get()

        with open(CWD + "/Datas/_Acomment_" + user + ".txt", 'w', encoding='utf-8') as file:
            file.write(text)

        self.comment_text.delete(1.0, tk.END)
        self.place_new_profile_frame()

    def place_comment_frame(self):
        self.stats_frame.place_forget()
        self.new_profile_frame.place_forget()
        self.profiles_frame.place_forget()
        self.comment_frame.place(x=230, y=5)

    def follow_option(self):
        pass

    def sumbit_settings(self):
        # write the user settings inside the file
        username = self.login_username.get()
        password = self.login_password.get()
        pages = self.instagram_pages.get()
        auto_cm = self.auto_comment.get()
        auto_lk = self.auto_like.get()
        auto_flw = self.auto_follow.get()
        auto_unflw = self.auto_unfollow.get()
        background = self.run_in_background.get()
        delay_time = self.delay_time.get()

        if username.strip() == '' or password.strip() == '':
            messagebox.askokcancel('Attenction', 'You must fille the username and password field before continue')
            return

        if not delay_time.strip().isdigit():
            messagebox.askokcancel('Attenction', 'Delay time must contains only numbers')
            return

        if not os.path.exists(self.settings_file):
            open(self.settings_file, "w").close()
        # if the user is editing his profile instead creating new one it updates the settings already existing
        if self.edit_profile_:
            remove_block(SETTINGS_FILE, 'Settings_' + self.edit_username)

            # SETTINGS EDITING
            with open(self.settings_file, 'a') as file:
                file.write("\nSettings_" + username +
                           "\nusername: :password::pages: :auto_comment: :auto_like: "
                           ":auto_follow: :auto_unfollow: :run_in_background: :delay_time: :")
            # SETTINGS EDITING
            write_in_block(self.settings_file, settings_block + username, ":",
                           username=username, password=password, pages=pages,
                           auto_comment=str(auto_cm), auto_like=str(auto_lk), auto_follow=str(auto_flw),
                           auto_unfollow=str(auto_unflw),
                           run_in_background=str(background), delay_time=str(delay_time))

            old_files = [
                CWD + "/Datas/_Acomment_" + self.edit_username + ".txt",
                CWD + "/Datas/_Aunfollow_list_" + self.edit_username + ".txt",
                CWD + "/Datas/_profile_visited_" + self.edit_username + ".txt",
                CWD + "/Datas/Stats_" + self.edit_username + ".txt",
                CWD + "/Datas/to_visit_" + self.edit_username + ".txt",
            ]

            new_files = [
                CWD + "/Datas/_Acomment_" + username + ".txt",
                CWD + "/Datas/_Aunfollow_list_" + username + ".txt",
                CWD + "/Datas/_profile_visited_" + username + ".txt",
                CWD + "/Datas/Stats_" + username + ".txt",
                CWD + "/Datas/to_visit_" + username + ".txt",
            ]
            for i in range(len(old_files)):
                os.rename(old_files[i], new_files[i])

            self.edit_profile_ = False
        # if the program can't fine the user block inside the settings file it creates a new block for write the datas
        elif not word_in_file(self.settings_file, "Settings_" + username):
            with open(self.settings_file, 'a') as file:
                file.write("\nSettings_" + username +
                           "\nusername: :password::pages::auto_comment: :auto_like: "
                           ":auto_follow: :auto_unfollow: :run_in_background: :delay_time: :")
            # SETTINGS EDITING
            write_in_block(self.settings_file, settings_block + username, ":",
                           username=username, password=password, pages=pages,
                           auto_comment=str(auto_cm), auto_like=str(auto_lk), auto_follow=str(auto_flw),
                           auto_unfollow=str(auto_unflw),
                           run_in_background=str(background), delay_time=str(delay_time))

            check_files(username)


        else:
            messagebox.askokcancel('Attenction',
                                   "This username yet exists, click the Edit button for modify it's settings")

        # reset the variables
        self.login_username.set("")
        self.login_password.set("")
        self.auto_comment.set(0)
        self.auto_like.set(0)
        self.auto_follow.set(0)
        self.auto_unfollow.set(0)
        self.run_in_background.set(0)
        self.instagram_page.set("")
        self.delay_time.set("120")
        self.update_username_optionmenu()
        self.create_profiles_frame()
        self.place_profiles_frame()
        self.display_comment_button()

    def _on_mousewheel(self, event, object):
        delta_ = int(event.delta)
        num = -10 * (delta_ // 120)
        object.yview_scroll(num, tk.UNITS)

    def start_loop(self):
        self.root.mainloop()


'''
  ____   ____ _______  __          ________ ____  
 |  _ \ / __ \__   __| \ \        / /  ____|  _ \ 
 | |_) | |  | | | |     \ \  /\  / /| |__  | |_) |
 |  _ <| |  | | | |      \ \/  \/ / |  __| |  _ < 
 | |_) | |__| | | |       \  /\  /  | |____| |_) |
 |____/ \____/  |_|        \/  \/   |______|____/ 

'''

# WEB BOT CONSTANTS
FROM_FILE = "from file"
RANDOM = "random"
UP_DOWN = "up_down"
DOWN_UP = "down_up"
PATH_ACCESS_BUTTON = "//button[@type='submit']"
NAME_USERNAME_BAR = "username"
NAME_PASSWORD_BAR = "password"
SAVE_LOGIN_DATAS_POPUP_CSS_SELECTOR = ".GAMXX"
DOWNLOAD_INSTAGRAM_POPUP_CSS_SELECTOR = "._3m3RQ._7XMpj"
FIRST_HOME_POPUP_CSS_SELECTOR = ".aOOlW.HoLwm"
PROFILE_POSTS_CSS_SELECTOR = ".eLAPa"
POST_COMMENTS_CSS_SELECTOR = ".C4VMK"
HASHTAGS_PATH = "//a[contains(@href, '/explore/tags')]"
FOLLOWERS_TABLE_XPATH = "//a[contains(@href, '/followers')]"
FOLLOWING_TABLE_XPATH = "//a[contains(@href, '/following')]"
TABLE_IMAGE_BLOCK_PROFILE_DISPLAY_CSS_SELECTOR = ".coreSpriteApproveLarge.ghWe6"
FOLLOWERS_TABLE_TITLE_XPATH = FOLLOWING_TABLE_TITLE_XPATH = "//h1[@class='m82CD']"
SHOW_ALL_FOLLOWERS_BUTTON_CSS_SELECTOR = ".sqdOP.yWX7d.ZIAjV"
PROFILE_NAMES_IN_FOLLOWERS_TABLE_CSS_SELECTOR = PROFILE_NAMES_IN_FOLLOWING_TABLE_CSS_SELECTOR = ".FPmhX.notranslate._0imsa"
POST_TITLE_FOTO_OR_VIDEO_XPATH = "//a[@class='FPmhX notranslate nJAzx']"
BUTTONS_UNDER_POST_XPATH = "//button[@class='dCJp8 afkep']"
LIKE_BUTTON_RELATIVE_XPATH = ".//span[@class='glyphsSpriteHeart__outline__24__grey_9 u-__7']"  # RELATIVE TO THE BUTTONS_UNDER_POST
COMMENT_BUTTON_RELATIVE_XPATH = ".//span[@class='glyphsSpriteComment__outline__24__grey_9 u-__7']"  # RELATIVE TO THE BUTTONS_UNDER_POST
COMMENT_TEXTARE_XPATH = "//textarea[@class='Ypffh']"
NEXT_POST_CSS_SELECTOR = ".HBoOv.coreSpriteRightPaginationArrow"
UNFOLLOW_BUTTON_CSS_SELECTOR_1 = "._5f5mN.-fzfL._6VtSN.yZn4P"
UNFOLLOW_BUTTON_CSS_SELECTOR_2 = ".ffKix.sqdOP.L3NKy._4pI4F._8A5w5"
CONFIRM_UNFOLLOW_CSS_SELECTOR = ".aOOlW.-Cab_"
FOLLOW_BUTTON_CSS_SELECTOR_1 = "._5f5mN.jIbKX._6VtSN.yZn4P"
FOLLOW_BUTTON_CSS_SELECTOR_2 = ".ffKix.sqdOP.L3NKy._4pI4F"
FOLLOW_BUTTON_PRIVATE_PROFILE_CSS_SELECTOR = ".BY3EC.sqdOP.L3NKy"
JS_ADD_TEXT_TO_INPUT = """
  var elm = arguments[0], txt = arguments[1];
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
  """

REMOVED_PAGE_XPATH = "//body[@class=' p-error dialog-404']"
PRIVATE_PAGE_XPATH = "//h2[@class='rkEop']"
PROFILE_NO_POSTS_XPATH = "//div[@class='FuWoR -wdIA      A2kdl']"
PROFILE_NO_POSTS_SELECTOR = '.FuWoR.-wdIA.A2kdl'
TABLE_CSS_SELECTOR = ".isgrP"
TABELLA_PER_VEDERE_ALTEZZA_ELEMETNO_CSS_SELECTOR = ".PZuss"

# check if internet is working
def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except Exception as err:
        print(err)
        return False

# check if internet is working
def check_internet_status():
    while not internet_on():
        print("NO INTERNET")
        time.sleep(5)

# remove a word from a file
def remove_word_from_file(file_path, word):
    word = word.strip()
    with open(file_path, "r") as file_read:
        lines = file_read.readlines()
    for index in range(len(lines)):
        line = lines[index]
        line = line.strip()
        lines[index] = line
    while "" in lines:
        lines.remove("")
    while " " in lines:
        lines.remove(" ")
    with open(file_path, "w") as file_write:
        lines.remove(word)
        for line in lines:
            file_write.write(line + "\n")


# append a word in a file
def write_in_file(file_path, word):
    with open(file_path, "a") as file:
        file.write(word)


# take the first word in a file
def take_first_in_list(file_path, line=0):
    with open(file_path, "r") as file_read:
        lines = file_read.readlines()
        if line == len(lines):
            return "end", line
        current_line = lines[line].strip()
        while current_line == "":
            if current_line != "":
                break
            line += 1
            if line == len(lines):
                return "end", line
            current_line = lines[line].strip()

        return current_line, line




# WEB INSTAGRAM BOT
class InstagramBot:
    def __init__(self, username, password, headless=True):

        # Bot options
        self._headless = headless
        options_ = firefoxOptions()
        test_broswer = webdriver.Firefox(executable_path=EXE_PATH)
        test_broswer.maximize_window()
        self.broswer_height = test_broswer.execute_script('return window.innerHeight;')
        self.broswer_width = test_broswer.execute_script('return window.innerWidth;')
        test_broswer.quit()

        if headless:
            options_.add_argument('--headless')
            options_.add_argument('--disable-gpu')
            options_.add_argument(f"--width={self.broswer_width}")
            options_.add_argument(f"--height={self.broswer_height}")
        self.real_broswer = webbrowser.get('firefox')

        self.real_broswer.open('http://www.instagram.com/accounts/login')
        self.broswer = webdriver.Firefox(options=options_, executable_path=EXE_PATH)
        if not headless:
            self.broswer.maximize_window()
        self.broswer.set_page_load_timeout(30)
        self._username = username
        self._password = password
        self._instagram_link = "https://www.instagram.com/"
        self._stats_file = CWD + "/Datas/Stats_" + username + ".txt"
        self._today_date = str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_mon) + "/" + str(
            time.localtime().tm_year)
        self._failed_unfollow_count = 0

        self.x_surplus = MONITOR_WIDTH - self.broswer_width
        self.y_surplus = MONITOR_HEIGHT - self.broswer_height

        print(f'BROSWER_WIDTH: {self.broswer_width}, BROSWER_HEITGHT: {self.broswer_height}, X_SURPLUS: {self.x_surplus}, Y_SURPLUS: {self.y_surplus}')

        # files to edit during the bot runs
        self.COMMENT_FILE = CWD + "/Datas/_Acomment_" + username + ".txt"
        self.UNFOLLOW_LIST_FILE = CWD + "/Datas/_Aunfollow_list_" + username + ".txt"
        self.PROFILE_VISITED_FILE = CWD + "/Datas/_profile_visited_" + username + ".txt"
        self.STATS_FILE = CWD + "/Datas/Stats_" + username + ".txt"
        self.TO_VISIT_FILE = CWD + "/Datas/to_visit_" + username + ".txt"

    def click(self, elem, x=0, y=0):
        time.sleep(2)
        x_ = elem.location['x']
        y_ = elem.location['y']
        pos = (0, 0)
        if APP_BAR_POSITION == 'LEFT':
            pos = (x_ + self.x_surplus + 10 + x, y_ + self.y_surplus + 10 + y)
        elif APP_BAR_POSITION == 'RIGHT':
            pos = (x_ + self.x_surplus + 10 - x, y_ + self.y_surplus + 10 + y)
        elif APP_BAR_POSITION == 'TOP':
            pos = (x_ + self.x_surplus + 10 + x, y_ + self.y_surplus + 10 + y)
        elif APP_BAR_POSITION == 'BOTTOM':
            pos = (x_ + self.x_surplus + 10 + x, y_ + self.y_surplus + 10 - y)
        mouse.position = pos
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(0.5)

    def setup(self):
        self.login()  # opend instagram and do the login
        print('logged')
        self.real_broswer.open(self._instagram_link)
        self.remove_initial_popup()  # remove ig intial popup windows
        print('removing popus')
        self._session_start_following_count = self.user_following_num(self._username)  # check how many users u are following at the start

    def stop(self):
        self.broswer.quit()  # quit the bot

    # run the bot
    def run(self):
        with open(self.COMMENT_FILE, "r", encoding="utf-8") as file:
            comment = file.read().strip()

        infos = read_in_block(SETTINGS_FILE, settings_block, ":", "pages")
        pages = infos['pages'][0]
        pages = pages.replace(' ', '').split(',')
        page = pages[randint(0, len(pages) - 1)]
        print(page)
        hashtag_followers = self.collect_followers_hashtags(page, 60)  # collect profiles from one of the pages that the user gave
        print('ended')
        hashtags = hashtag_followers['hashtags']
        followers = hashtag_followers['followers']

        # get all the usernames inside the to_visit file
        with open(self.TO_VISIT_FILE, 'a') as file:
            with open(self.TO_VISIT_FILE, 'r') as file_read:
                usernames = file_read.readlines()

                for index in range(len(usernames)):
                    username = usernames[index]
                    usernames[index] = username.strip()
            # get all the usernames inside the profile_visited file
            with open(self.PROFILE_VISITED_FILE, 'r') as file_read:
                visited_usernames = file_read.readlines()

                for index in range(len(visited_usernames)):
                    username = visited_usernames[index]
                    visited_usernames[index] = username.strip()
            if followers is not None:
                for profile in followers:
                    # if the profile is not in the profile_visited file the bot write it inside the to_visit file
                    if profile not in usernames and profile not in visited_usernames:
                        file.write(profile + "\n")

        with open(self.TO_VISIT_FILE, 'r') as file_read:
            usernames = file_read.readlines()

        infos = read_in_block(SETTINGS_FILE, settings_block + self._username, ':', *all_settings)

        bool_dict = {0: False, 1: True}

        # for each profile in the to_visit file the bot visit him and left some interactions
        for i, profile in enumerate(usernames):
            print('USER NUMBER: ', i)
            self.complete_bot(profile, posts_num=3, left_how_many_comments=1,
                              put_like=bool_dict[int(infos['auto_like'][0])],
                              put_comment=bool_dict[int(infos['auto_comment'][0])], comment=comment,
                              unfollow=bool_dict[int(infos['auto_unfollow'][0])],
                              follow=bool_dict[int(infos['auto_follow'][0])],
                              follow_private=False,
                              follow_no_post=False, total_time=int(infos['delay_time'][0]))

        self.run()

    # do the instagram login
    def login(self):
        check_internet_status()
        self.broswer.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(self.broswer, 10).until(lambda d: d.find_element_by_xpath(PATH_ACCESS_BUTTON).is_displayed())

        username_input = self.broswer.find_element_by_name(NAME_USERNAME_BAR)
        username_input.send_keys(self._username)
        self.click(username_input)
        send(self._username)

        password_input = self.broswer.find_element_by_name(NAME_PASSWORD_BAR)
        password_input.send_keys(self._password)
        self.click(password_input)
        send(self._password)

        WebDriverWait(self.broswer, 5).until(lambda d: d.find_element_by_xpath(PATH_ACCESS_BUTTON).is_displayed())
        WebDriverWait(self.broswer, 5).until(EC.element_to_be_clickable((By.XPATH, PATH_ACCESS_BUTTON)))

        access_button = self.broswer.find_element_by_xpath(PATH_ACCESS_BUTTON)
        self.click(access_button)
        access_button.click()


        time.sleep(3)
        try:
            elem = self.broswer.find_element_by_xpath(PATH_ACCESS_BUTTON)
            elem.click()
            self.click(elem)
        except (NoSuchElementException, WebDriverException):
            return

    # update the date
    def update_today_date(self):
        self._today_date = str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_mon) + "/" + str(
            time.localtime().tm_year)

    # remove the initial instagram popup windows
    def remove_initial_popup(self):
        check_internet_status()
        try:
            WebDriverWait(self.broswer, 5).until(
                lambda d: d.find_element_by_css_selector(SAVE_LOGIN_DATAS_POPUP_CSS_SELECTOR).is_displayed())
            save_login_datas = self.broswer.find_element_by_css_selector(SAVE_LOGIN_DATAS_POPUP_CSS_SELECTOR)
            self.click(save_login_datas)
            save_login_datas.click()

        except (NoSuchElementException, TimeoutException):
            pass

        try:
            WebDriverWait(self.broswer, 5).until(
                lambda d: d.find_element_by_css_selector(DOWNLOAD_INSTAGRAM_POPUP_CSS_SELECTOR).is_displayed())
            save_login_datas = self.broswer.find_element_by_css_selector(DOWNLOAD_INSTAGRAM_POPUP_CSS_SELECTOR)
            self.click(save_login_datas)
            save_login_datas.click()

        except (NoSuchElementException, TimeoutException):
            pass

        try:
            WebDriverWait(self.broswer, 5).until(
                lambda d: d.find_element_by_css_selector(FIRST_HOME_POPUP_CSS_SELECTOR).is_displayed())
            attivazione_notifiche = self.broswer.find_element_by_css_selector(FIRST_HOME_POPUP_CSS_SELECTOR)
            self.click(attivazione_notifiche)
            attivazione_notifiche.click()

        except (NoSuchElementException, TimeoutException):
            pass

    # find the posts elements inside the profile page
    def find_posts(self):
        try:
            WebDriverWait(self.broswer, 5).until(
                lambda d: d.find_element_by_css_selector(PROFILE_POSTS_CSS_SELECTOR).is_displayed())
            posts = self.broswer.find_elements_by_css_selector(PROFILE_POSTS_CSS_SELECTOR)
        except Exception:
            return None
        return posts

    # find the hashtags inside the post caption
    def find_hashtags(self):
        try:
            WebDriverWait(self.broswer, 10).until(
                lambda d: d.find_element_by_css_selector(POST_COMMENTS_CSS_SELECTOR).is_displayed())
            hashtags = self.broswer.find_elements_by_xpath(HASHTAGS_PATH)
        except Exception:
            return None
        for i in range(len(hashtags)):
            elem = hashtags[i]
            hashtags[i] = elem.text
        return hashtags

    # find the like button when the post element is opened
    def find_like_button(self):
        try:
            WebDriverWait(self.broswer, 10).until(
                lambda d: d.find_element_by_xpath(POST_TITLE_FOTO_OR_VIDEO_XPATH).is_displayed())
            button_to_like = None
            buttons_under_post = self.broswer.find_elements_by_xpath(BUTTONS_UNDER_POST_XPATH)
            for button in buttons_under_post:
                try:
                    button_to_like = button.find_element_by_css_selector(
                        ".glyphsSpriteHeart__outline__24__grey_9.u-__7")
                except NoSuchElementException:
                    continue
                else:
                    break
            # button_yet_liked = self.broswer.find_element_by_css_selector(".glyphsSpriteHeart__filled__24__red_5.u-__7")
        except Exception:
            raise NoSuchElementException("Cannot found any like button")
        return button_to_like

    # find the comment button when the post element is opened
    def find_comment_button(self):
        try:
            comment_button = None
            buttons_under_post = self.broswer.find_elements_by_xpath(BUTTONS_UNDER_POST_XPATH)
            for button in buttons_under_post:
                try:
                    comment_button = button.find_element_by_xpath(COMMENT_BUTTON_RELATIVE_XPATH)
                except NoSuchElementException:
                    continue
                else:
                    break

        except Exception:
            raise NoSuchElementException("Cannot found any comment button")
        return comment_button

    # find the followers frame of a profile for collect the profiles
    def find_followers_frame(self):
        try:
            WebDriverWait(self.broswer, 10).until(
                lambda d: d.find_element_by_xpath(FOLLOWERS_TABLE_XPATH).is_displayed())
            followers_table = self.broswer.find_element_by_xpath(FOLLOWERS_TABLE_XPATH)
        except NoSuchElementException:
            raise NoSuchElementException("can't find followers table")
        else:
            return followers_table

    # find the following frame of your profile for collect the profiles
    def find_following_frame(self):
        try:
            WebDriverWait(self.broswer, 10).until(
                lambda d: d.find_element_by_xpath(FOLLOWING_TABLE_XPATH).is_displayed())
            following_table = self.broswer.find_element_by_xpath(FOLLOWING_TABLE_XPATH)
        except NoSuchElementException:
            raise NoSuchElementException("can't find followers table")
        else:
            return following_table

    # open the following fram and collect all the profiles
    def find_user_followers(self, profile, time_for_collect):
        try:
            self.visit_user_page(profile)
            time.sleep(1)
            followers_table = self.find_followers_frame()
            # followers_table.click()
            self.click(followers_table)

            followers_elements = self.collect_followers(time_for_collect, time_for_collect=15)
            if followers_elements is None:
                return None
            print("I have found {0} profiles".format(len(followers_elements)))
            profiles = []
            for link_elem in followers_elements:
                profiles.append(link_elem.text)
            return profiles
        except (TimeoutException, NoSuchElementException):
            print("error in function 'find_user_followers'")
            return

    def is_inexistent_profile(self, profile):
        try:
            print('checking if inexistent')
            self.visit_user_page(profile)
            WebDriverWait(self.broswer, 1).until(lambda d: d.find_element_by_xpath(REMOVED_PAGE_XPATH).is_displayed())
            romed_page = self.broswer.find_element_by_xpath(REMOVED_PAGE_XPATH)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # check if a profile is private
    def is_private_profile(self, profile):
        try:
            print('checking if is private')
            self.visit_user_page(profile)
            WebDriverWait(self.broswer, 1).until(lambda d: d.find_element_by_xpath(PRIVATE_PAGE_XPATH).is_displayed())
            romed_page = self.broswer.find_element_by_xpath(PRIVATE_PAGE_XPATH)
            return True
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
            return False

    # check if a profile has no posts
    def is_no_post_profile(self, profile):
        try:
            print('checking if is no post')
            self.visit_user_page(profile)
            WebDriverWait(self.broswer, 1).until(
                lambda d: d.find_element_by_css_selector(PROFILE_NO_POSTS_SELECTOR).is_displayed())
            romed_page = self.broswer.find_element_by_css_selector(PROFILE_NO_POSTS_SELECTOR)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # check if a profile is already followed
    def profile_is_followed(self, profile):
        try:
            self.visit_user_page(profile)
            type_ = 1
            try:
                WebDriverWait(self.broswer, 2).until(
                    lambda d: d.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_1).is_displayed())
            except (StaleElementReferenceException, TimeoutException):
                type_ = 2
                WebDriverWait(self.broswer, 2).until(
                    lambda d: d.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_2).is_displayed())
                pass
            time.sleep(1)
            if type_ == 1:
                unfollow_button = self.broswer.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_1)
            elif type_ == 2:
                unfollow_button = self.broswer.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_2)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # check if a profile is not followed
    def profile_is_not_followed(self, profile):
        try:
            self.visit_user_page(profile)

            type_ = 1
            try:
                WebDriverWait(self.broswer, 2).until(
                    lambda d: d.find_element_by_css_selector(FOLLOW_BUTTON_CSS_SELECTOR_1).is_displayed())
            except (StaleElementReferenceException, TimeoutException):
                type_ = 2
                WebDriverWait(self.broswer, 2).until(
                    lambda d: d.find_element_by_css_selector(FOLLOW_BUTTON_CSS_SELECTOR_2).is_displayed())
                pass
            time.sleep(1)
            if type_ == 1:
                follow_button = self.broswer.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_1)
            elif type_ == 2:
                follow_button = self.broswer.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_2)

            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # find the comment bar, write and send the comment
    def write_comment(self, comment):
        try:
            WebDriverWait(self.broswer, 10).until(
                lambda d: d.find_element_by_xpath(COMMENT_TEXTARE_XPATH).is_displayed())
            comment_input_bar = self.broswer.find_element_by_xpath(COMMENT_TEXTARE_XPATH)
        except Exception:
            return
        else:
            comment_input_bar.click()
            self.broswer.execute_script(JS_ADD_TEXT_TO_INPUT, comment_input_bar, comment)
            comment_input_bar.click()
            comment_input_bar.send_keys(" ", Keys.ENTER)
            time.sleep(2)

    # scroll the followers/following table frame
    def scroll_table(self, scroll_time):
        WebDriverWait(self.broswer, 5).until(
            lambda d: d.find_element_by_xpath(FOLLOWERS_TABLE_TITLE_XPATH).is_displayed())
        try:
            WebDriverWait(self.broswer, 5).until(
                lambda d: d.find_element_by_css_selector(PROFILE_NAMES_IN_FOLLOWERS_TABLE_CSS_SELECTOR).is_displayed())
        except TimeoutException:
            return None
        tabella_scroll = self.broswer.find_element_by_css_selector(TABLE_CSS_SELECTOR)
        tabella_height = self.broswer.find_element_by_css_selector(TABELLA_PER_VEDERE_ALTEZZA_ELEMETNO_CSS_SELECTOR)
        time_start = time.time()
        scroll_dimension = 100
        scroll_number = 0
        previous_height = ""
        while time.time() - time_start < scroll_time:
            new_height = tabella_height.size["height"]
            if scroll_number % 15 == 0:
                if new_height == previous_height:
                    print(new_height, previous_height, scroll_dimension)
                    return
                else:
                    previous_height = new_height
            self.broswer.execute_script("arguments[0].scrollTo(0, {0});".format(scroll_dimension), tabella_scroll)
            scroll_dimension += 200
            time.sleep(0.1)
            scroll_number += 1

    # open the followers fram of a profile and collect the profiles
    def collect_followers(self, user, time_for_collect):
        self.visit_user_page(user)
        time.sleep(1)
        followers_table = self.find_followers_frame()
        followers_table.click()
        time.sleep(1)
        self.scroll_table(time_for_collect)
        profiles_element = self.collect_following()
        if profiles_element is None:
            return None
        print("I have found {0} profiles".format(len(profiles_element)))
        profiles = []
        for link_elem in profiles_element:
            profiles.append(link_elem.text)
        return profiles

    # check if there are some profiles in the table (returns None if not)
    def collect_following(self):
        WebDriverWait(self.broswer, 5).until(
            lambda d: d.find_element_by_xpath(FOLLOWING_TABLE_TITLE_XPATH).is_displayed())
        try:
            WebDriverWait(self.broswer, 5).until(
                lambda d: d.find_element_by_css_selector(PROFILE_NAMES_IN_FOLLOWING_TABLE_CSS_SELECTOR).is_displayed())
        except (TimeoutException, StaleElementReferenceException):
            return None
        profiles_in_table = self.broswer.find_elements_by_css_selector(PROFILE_NAMES_IN_FOLLOWING_TABLE_CSS_SELECTOR)
        return profiles_in_table

    # go to a profile url
    def visit_user_page(self, user, force=False):
        user = user.strip()
        print(self.broswer.current_url)
        print(self._instagram_link + user + "/")
        print(force)
        if self.broswer.current_url not in [self._instagram_link + user + "/", self._instagram_link + user] or force:
            print('visiting' + user)
            self.broswer.get(self._instagram_link + user)
            time.sleep(1)
            keyboard.press(Key.ctrl)
            keyboard.press('w')
            keyboard.release(Key.ctrl)
            keyboard.release('w')
            time.sleep(1)
            self.real_broswer.open(self._instagram_link + user, new=0)


    # get the user followers count
    def user_followers_num(self, user):
        check_internet_status()
        url = self._instagram_link + user
        r = requests.get(url).text
        followers_start = '"edge_followed_by":{"count":'
        followers_end = '},"followed_by_viewer"'
        return int(r[r.find(followers_start) + len(followers_start):r.rfind(followers_end)])

    # get the user following count
    def user_following_num(self, user):
        check_internet_status()
        url = self._instagram_link + user
        r = requests.get(url).text
        followed_start = '"edge_follow":{"count":'
        followed_end = '},"follows_viewer"'
        return int(r[r.find(followed_start) + len(followed_start):r.rfind(followed_end)])

    #  unfollow a profile
    def unfollow_profile(self, profile):
        try:
            time.sleep(1)
            self.visit_user_page(profile)
            type_ = 1
            try:
                WebDriverWait(self.broswer, 5).until(
                    lambda d: d.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_1).is_displayed())
            except (StaleElementReferenceException, TimeoutException):
                type_ = 2
                WebDriverWait(self.broswer, 5).until(
                    lambda d: d.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_2).is_displayed())
                pass
            time.sleep(1)
            if type_ == 1:
                unfollow_button = self.broswer.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_1)
            elif type_ == 2:
                unfollow_button = self.broswer.find_element_by_css_selector(UNFOLLOW_BUTTON_CSS_SELECTOR_2)
            self.click(unfollow_button)
            unfollow_button.click()
            WebDriverWait(self.broswer, 10).until(
                lambda d: d.find_element_by_css_selector(CONFIRM_UNFOLLOW_CSS_SELECTOR).is_displayed())
            time.sleep(1)
            confirm_unfollow_button = self.broswer.find_element_by_css_selector(CONFIRM_UNFOLLOW_CSS_SELECTOR)
            self.click(confirm_unfollow_button, y=40)
            # confirm_unfollow_button.click()
            # STATS EDITING
            write_in_block(self._stats_file, "Date:" + self._today_date, ":", unfollow="+=1")
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    #  follow a profile
    def follow_profile(self, profile):
        try:

            self.visit_user_page(profile)
            type_ = 1
            try:
                WebDriverWait(self.broswer, 5).until(
                    lambda d: d.find_element_by_css_selector(FOLLOW_BUTTON_CSS_SELECTOR_1).is_displayed())
            except (StaleElementReferenceException, TimeoutException):
                type_ = 2
                try:
                    WebDriverWait(self.broswer, 2).until(
                        lambda d: d.find_element_by_css_selector(FOLLOW_BUTTON_CSS_SELECTOR_2).is_displayed())
                except (StaleElementReferenceException, TimeoutException):
                    type_ = 3
                    WebDriverWait(self.broswer, 2).until(lambda d: d.find_element_by_css_selector(
                        FOLLOW_BUTTON_PRIVATE_PROFILE_CSS_SELECTOR).is_displayed())

            time.sleep(1)
            if type_ == 1:
                follow_button = self.broswer.find_element_by_css_selector(FOLLOW_BUTTON_CSS_SELECTOR_1)
            elif type_ == 2:
                follow_button = self.broswer.find_element_by_css_selector(FOLLOW_BUTTON_CSS_SELECTOR_2)
            elif type_ == 3:
                follow_button = self.broswer.find_element_by_css_selector(FOLLOW_BUTTON_PRIVATE_PROFILE_CSS_SELECTOR)
            self.click(follow_button)
            # follow_button.click()
            # STATS EDITING
            write_in_block(self._stats_file, "Date:" + self._today_date, ":", follow="+=1")
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    #  colloct the profiles that I follow
    def my_following_list(self, time_for_collect):

        self.visit_user_page(self._username)
        time.sleep(1)
        following_table = self.find_following_frame()
        following_table.click()
        time.sleep(1)
        self.scroll_table(time_for_collect)
        profiles_element = self.collect_following()
        if profiles_element is None:
            return None
        print("I have found {0} profiles".format(len(profiles_element)))
        profiles = []
        for link_elem in profiles_element:
            profiles.append(link_elem.text)
        return profiles

    # click the next post arrow
    def next_post(self):
        next_post_ = self.broswer.find_element_by_css_selector(NEXT_POST_CSS_SELECTOR)
        return next_post_
    # interact with a profile by putting likes/comments on posts
    def interact_with_profile(self, profile, posts_num=1, put_comment=False, put_like=False, left_how_many_comments=0,
                              comment=""):

        try:
            self.visit_user_page(profile)
            if not put_comment and not put_like:
                return True
            posts = self.find_posts()
            post = posts[0]
            self.click(post)
            post.click()
            for index in range(posts_num):
                if index > len(posts) - 1:
                    return True

                time.sleep(1)
                button_to_like = self.find_like_button()
                if put_like:
                    if button_to_like is not None:
                        try:
                            self.click(button_to_like, y=40)
                            # button_to_like.click()
                            # STATS EDITING
                            write_in_block(self._stats_file, "Date:" + self._today_date, ":", likes="+=1")
                        except WebDriverException as err:
                            print(str(err))
                if put_comment:
                    if index < left_how_many_comments:
                        comment_button = self.find_comment_button()
                        if comment_button is not None and button_to_like is not None:
                            try:
                                self.click(comment_button, y=40)
                                comment_button.click()
                            except WebDriverException as err:
                                print(str(err))
                            send(comment)
                            send('<ENTER>')
                            # self.write_comment(comment)
                            # STATS EDITING
                            write_in_block(self._stats_file, "Date:" + self._today_date, ":", comments="+=1")
                try:
                    next_post_ = self.next_post()
                    self.click(next_post_, y=40)
                    next_post_.click()
                except NoSuchElementException:
                    return True
        except (NoSuchElementException, TimeoutException):
            return False
        else:
            return True

    # collect the followers of a profile and the hashtags of its posts
    def collect_followers_hashtags(self, profile, time_):
        hashtags_followers = {'hashtags': [], 'followers': []}
        print('COLLECTING PROFILES')
        try:
            self.visit_user_page(profile)
            if self.is_private_profile(profile):
                return hashtags_followers
            elif self.is_no_post_profile(profile):
                followers = self.collect_followers(profile, time_)
                if followers is None:
                    followers = []
                hashtags_followers['followers'] = followers
                return hashtags_followers
            else:
                followers = self.collect_followers(profile, time_)
                hashtags_followers['followers'] = followers
                self.visit_user_page(profile)
                posts = self.find_posts()
                post = posts[0]
                post.click()
                for index in range(3):
                    time.sleep(1)
                    hashtags = self.find_hashtags()
                    if hashtags is not None:
                        for hashtag in hashtags:
                            if hashtag not in hashtags_followers['hashtags']:
                                hashtags_followers['hashtags'].append(hashtag)
                    try:
                        next_post_ = self.next_post()
                        next_post_.click()
                    except NoSuchElementException:
                        return hashtags_followers
        except (NoSuchElementException, TimeoutException):
            return hashtags_followers
        else:
            return hashtags_followers

    def complete_bot(self, profile, posts_num=1, left_how_many_comments=1, put_like=False,
                     put_comment=False, comment="", unfollow=False, follow=False,
                     follow_private=False, follow_no_post=False, total_time=60):

        check_internet_status()

        time.sleep(5)
        t1 = time.time()
        print("\n" + profile)

        if self.is_private_profile(profile):
            if follow_private:
                self.follow_profile(profile)
                write_in_file(self.UNFOLLOW_LIST_FILE, profile)

                write_in_file(self.PROFILE_VISITED_FILE, profile)
                print("private profile")
            else:
                remove_word_from_file(self.TO_VISIT_FILE, profile)
                return
        elif self.is_no_post_profile(profile):
            if follow_no_post:
                self.follow_profile(profile)
                write_in_file(self.UNFOLLOW_LIST_FILE, profile)
                remove_word_from_file(self.TO_VISIT_FILE, profile)
                write_in_file(self.PROFILE_VISITED_FILE, profile)
                print("no post profile")
            else:
                remove_word_from_file(self.TO_VISIT_FILE, profile)
                return
        elif self.is_inexistent_profile(profile):
            print("not existing page")
            remove_word_from_file(self.TO_VISIT_FILE, profile)

        elif follow:
            print("interactions")
            worked_interactions = self.interact_with_profile(profile, posts_num=posts_num, put_like=put_like,
                                                             put_comment=put_comment,
                                                             left_how_many_comments=left_how_many_comments,
                                                             comment=comment)
            print("following")
            if worked_interactions:
                worked_follow = self.follow_profile(profile)
                if worked_follow:
                    write_in_file(self.UNFOLLOW_LIST_FILE, profile)
                    remove_word_from_file(self.TO_VISIT_FILE, profile)
                    write_in_file(self.PROFILE_VISITED_FILE, profile)

        if unfollow:
            with open(self.UNFOLLOW_LIST_FILE, 'r') as file_read:
                profiles = file_read.readlines()
            # SE CI SONO PIU' DI 100 PROFILE NELLA UNFOLLOW LIST INZIA A UNFOLLOWARE
            if len(profiles) >= 100:
                check_internet_status()
                print('COLLECTING PROFILE TO UNFOLLOW')
                following_list = self.my_following_list(20)
                if following_list is None:
                    print("No following list found")
                    return

                current_following = self.user_following_num(self._username)
                print("current following: ", current_following, ", at start: ", self._session_start_following_count)
                people_to_unfollow_count = current_following - self._session_start_following_count
                print("unfollow count: ", people_to_unfollow_count)

                for _ in range(people_to_unfollow_count):
                    profile_to_unfollow, line = take_first_in_list(self.UNFOLLOW_LIST_FILE)
                    while not (profile_to_unfollow in following_list):
                        if profile_to_unfollow == "end":
                            raise Exception("non ho trovato chi unfolloware")
                        profile_to_unfollow, line = take_first_in_list(self.UNFOLLOW_LIST_FILE, line=line + 1)
                    worked = self.unfollow_profile(profile_to_unfollow)
                    print("unfollowing " + profile_to_unfollow)
                    if worked:
                        remove_word_from_file(self.UNFOLLOW_LIST_FILE, profile_to_unfollow)
                    line = 0

        self.update_today_date()
        time_end = time.time() - t1

        if total_time <= time_end:
            pass
        elif time_end < total_time:
            time.sleep(total_time - time_end)

        print("time: ", time.time() - t1)
        print("failed_unfollow_count: ", self._failed_unfollow_count)

    def unfollow_process(self, unfollow_type=RANDOM, sense=DOWN_UP, times=None,
                         following_target=None, file=None, edit_file=False, sleep_time=60):
        """
        :param unfollow_type:  RAMNDOM it will unfollow in order the people from ur following list,
                               FROM_FILE it will unfollow only the people on the file

        :param sense:  UP_DOWN it will read the following list from up to down
                       DOWN_UP it will read the following list from down to up

        :param times:   param if the unfollow_typ is RANDOM, it specify how many profiles to unfollow
                        (you can use or times or following target, if you specify both the param times will be used)

        :param following_target: param if the unfollow_typ is RANDOM, it specify at the end of the process how many people you want still to follow
                                 if you at the start follow 500 profiles and your target is 400 the bot will unfollow 100 profiles

        :param file:  param if the unfollow_typ is FROM_FILE, the file path

        :param edit_file:  param if the unfollow_typ is FROM_FILE, it specify if you want that the bot when unfollow a profile on the list have to remove it or no

        :param sleep_time:  the dalay from one unfollow and the next

        :return: None

        usage examples

        .unfollow_process(FROM_FILE, sense=DOWN_UP, file=UNFOLLOW_LIST_FILE, sleep_time=30)
        .unfollow_process(RANDOM, sense=DOWN_UP, times=200, sleep_time=30)
        .unfollow_process(RANDOM, sense=UP_DOWN, following_target=200, sleep_time=30)

        """
        file_copy = ""
        try:
            check_internet_status()
            following_list = self.my_following_list(30)
            if following_list is None:
                raise ValueError("Not found following list")
            if unfollow_type == RANDOM:
                if sense == UP_DOWN:
                    sense = (0, len(following_list), 1)
                elif sense == DOWN_UP:
                    sense = (len(following_list) - 1, -1, -1)

                if times is not None:
                    current_following = self.user_following_num(self._username)
                    if times > current_following:
                        times = current_following
                    counter = 0
                    for index in range(*sense):
                        check_internet_status()
                        start_time = time.time()
                        if counter < times:
                            pass
                        else:
                            return
                        profile = following_list[index]
                        worked = self.unfollow_profile(profile)
                        print(index, profile, worked)
                        counter += 1
                        end_time = time.time()
                        process_time = end_time - start_time
                        if process_time >= sleep_time:
                            pass
                        else:
                            time.sleep(sleep_time - process_time)

                elif following_target is not None:
                    current_following = self.user_following_num(self._username)
                    if following_target > current_following:
                        return
                    else:
                        people_to_unfollow_count = current_following - following_target
                        print("to unfollow {0} profiles".format(people_to_unfollow_count))
                        counter = 0
                        for index in range(*sense):
                            check_internet_status()
                            start_time = time.time()
                            if counter < people_to_unfollow_count:
                                pass
                            else:
                                return
                            profile = following_list[index]
                            worked = self.unfollow_profile(profile)
                            print(index, profile, worked)
                            counter += 1
                            end_time = time.time()
                            process_time = end_time - start_time
                            if process_time >= sleep_time:
                                pass
                            else:
                                time.sleep(sleep_time - process_time)

            if unfollow_type == FROM_FILE:

                if file is None:
                    raise NoSuchElementException("File from where read the profiles not specified")
                if not isinstance(edit_file, bool):
                    return ValueError("@param edit_file should be Boolean")
                if not edit_file:
                    file_copy = CWD + "/Datas/file_unfollow_copy.txt"

                    with open(file_copy, "w") as file_copy_:
                        with open(file, "r") as file_read:
                            lines = file_read.readlines()
                        for line in lines:
                            file_copy_.write(line)

                    with open(file_copy, "r") as file:
                        times = len(file.readlines())

                else:
                    file_copy = file
                    with open(file_copy, "r") as file:
                        times = len(file.readlines())

                current_following = self.user_following_num(self._username)
                if times > current_following:
                    times = current_following

                for index in range(times):
                    check_internet_status()
                    start_time = time.time()
                    try:
                        profile_to_unfollow, line = take_first_in_list(file_copy)
                        while not (profile_to_unfollow in following_list):
                            profile_to_unfollow, line = take_first_in_list(self.UNFOLLOW_LIST_FILE, line=line + 1)
                    except IndexError:
                        return

                    worked = self.unfollow_profile(profile_to_unfollow)
                    print(index, profile_to_unfollow, worked)
                    if worked:
                        remove_word_from_file(file_copy, profile_to_unfollow)

                    end_time = time.time()
                    process_time = end_time - start_time
                    if process_time >= sleep_time:
                        pass
                    else:
                        time.sleep(sleep_time - process_time)
        except WebDriverException as e:
            print(str(e))
            print("seomething went wrong, maybe the broswer has been closed")
        finally:
            try:
                if not edit_file:
                    if file_copy != "":
                        os.remove(file_copy)
            except Exception:
                pass

    def follow_process(self, follow_type=FROM_FILE,
                       sleep_time=60, edit_file=False, file=None, follow_private=False, follow_no_post=False):

        file_copy = ""
        try:
            if follow_type == FROM_FILE:

                if file is None:
                    raise NoSuchElementException("File from where read the profiles not specified")
                if not isinstance(edit_file, bool):
                    return ValueError("@param edit_file should be Boolean")
                if not edit_file:

                    file_copy = CWD + "/Datas/file_follow_copy.txt"
                    with open(file_copy, "w") as file_copy_:
                        with open(file, "r") as file_read:
                            lines = file_read.readlines()
                        for line in lines:
                            file_copy_.write(line)

                    with open(file_copy, "r") as file:
                        times = len(file.readlines())

                else:
                    file_copy = file
                    with open(file_copy, "r") as file:
                        times = len(file.readlines())

                for index in range(times):
                    check_internet_status()
                    start_time = time.time()
                    try:
                        profile_to_follow, line = take_first_in_list(file_copy)
                    except IndexError:
                        return
                    if self.profile_is_followed(profile_to_follow):
                        remove_word_from_file(file_copy, profile_to_follow)
                        print(profile_to_follow, index, "yet followed")
                        continue

                    if self.is_inexistent_profile(profile_to_follow):
                        remove_word_from_file(file_copy, profile_to_follow)
                        print(profile_to_follow, index, "inexistent")
                        continue

                    if self.is_private_profile(profile_to_follow):
                        if follow_private:
                            pass
                        else:
                            remove_word_from_file(file_copy, profile_to_follow)
                            continue
                        print("private profile")

                    if self.is_no_post_profile(profile_to_follow):
                        if follow_no_post:
                            pass
                        else:
                            remove_word_from_file(file_copy, profile_to_follow)
                            continue
                        print("no post profile")

                    worked = self.follow_profile(profile_to_follow)
                    print(profile_to_follow, index, worked)
                    if worked:
                        remove_word_from_file(file_copy, profile_to_follow)
                    end_time = time.time()
                    process_time = end_time - start_time
                    if process_time >= sleep_time:
                        pass
                    else:
                        time.sleep(sleep_time - process_time)
        except WebDriverException as e:
            print("seomething went wrong, maybe the broswer has been closed")
            print(str(e))
        finally:
            try:
                if not edit_file:
                    if file_copy != "":
                        os.remove(file_copy)
            except Exception:
                pass


if __name__ == '__main__':
    today_date = str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_mon) + "/" + str(
        time.localtime().tm_year)
    SETTINGS_FILE = CWD + "/Datas/Settings.txt"
    DATAS_FOLDER = CWD + "/Datas"


    if not os.path.exists(DATAS_FOLDER):
        os.mkdir(DATAS_FOLDER)

    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w') as file:
            file.write("Last login\ndate:" + today_date + ":username:" + "None" + "\nMonitorResolution\nm_r:0x0\nApplicationBar\nposition:")
    else:
        with open(SETTINGS_FILE, 'r') as file:
            lines = file.readlines()
            while '\n' in lines:
                lines.remove('\n')
            with open(SETTINGS_FILE, 'w') as file_w:
                for line in lines:
                    file_w.write(line)
    MONITOR_WIDTH, MONITOR_HEIGHT = [int(elem) for elem in read_in_block(SETTINGS_FILE, 'MonitorResolution', ':', 'm_r')['m_r'][0].strip().split('x')]
    APP_BAR_POSITION = read_in_block(SETTINGS_FILE, 'ApplicationBar', ':', 'position')['position'][0]
    print(f'MONITOR WIDTH: {MONITOR_WIDTH}, MONITOR_HEIGHT: {MONITOR_HEIGHT}')
    infos = read_in_block(SETTINGS_FILE, settings_block, ":", "username")
    usernames = infos['username']

    for username in usernames:
        check_files(username)

    gui = Window()
    gui.start_loop()
