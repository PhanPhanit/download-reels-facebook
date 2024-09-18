import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
from bs4 import BeautifulSoup

def remove_dup_array(arrays) -> list:
    new_array = []
    for array in arrays:
        if array not in new_array:
            new_array.append(array)

    return new_array



array = ["1", "13", "2", "1", "10", "13", "2", "14", "13", "1"]

def check_name_download(folder_path) -> str:
    # Define video file extensions
    video_extensions = ('*.mp4', '*.mkv', '*.avi', '*.mov', '*.flv', '*.wmv', '*.webm')
    # Get list of all video files
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(folder_path, ext)))

    # Extract filenames with extensions
    video_name = [os.path.basename(video) for video in video_files]
    pattern = re.compile(r'^\d+_')
    video_name_return = ""
    for name in video_name:
        filename = os.path.basename(name)
        if not pattern.match(filename):
            video_name_return = name
            break
    
    return video_name_return

title = check_name_download("C:\\Users\\Phan Phanit\\Downloads\\ESUIT Video Downloader for Facebook")

name, ext = os.path.splitext(title)

# print(name)
# print(ext)

my_text = "Hello World"
modified_text = my_text[:-2]  # Removes the last two characters
print(modified_text)