import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
import os
import glob
from bs4 import BeautifulSoup
import random

def remove_dup_array(arrays) -> list:
    new_array = []
    for array in arrays:
        if array not in new_array:
            new_array.append(array)

    return new_array

def find_element_wait(driver, selenium_by, selector, time=10):
    try:
        element = WebDriverWait(driver, time).until(EC.presence_of_element_located((selenium_by, selector)))
        return element
    except TimeoutException:
        return None

def rename_video(video_path, new_video_path):
    try:
        os.rename(video_path, new_video_path)
    except FileNotFoundError:
        print("Error: The specified video file was not found.")
    except PermissionError:
        print("Error: You do not have the necessary permissions to rename this file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def wait_until_download_complete(download_dir):
    while True:
        current_files = set(os.listdir(download_dir))
        download_complete = False
        for file in current_files:
            if file.endswith('.crdownload'):
                download_complete = False
                break
            else:
                download_complete = True
        
        if download_complete:
            break
        
        time.sleep(2)

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

def main():
    save_folder_path = "C:\\Users\\Phan Phanit\\Downloads\\ESUIT Video Downloader for Facebook"
    user_data = "C:\\Users\\Phan Phanit\\AppData\\Local\\Google\\Chrome\\User Data"
    profile_dir = "Profile 16"
    # Get text html from txt file
    html_text = ""
    with open('html_data.txt', 'r', encoding='utf-8') as file:
        # Read the content of the file
        html_text = file.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_text, 'html.parser')
    a_tags = soup.find_all('a', {'aria-label': 'Reel tile preview'})
    facebook_reels_urls = []
    for tag in a_tags:
        href = tag.get('href')
        array_text = href.split("?")
        reels_url = array_text[0]
        full_reels_url = f"https://www.facebook.com{reels_url}"
        facebook_reels_urls.append(full_reels_url)
    # Remove Duplicate Link
    facebook_reels_urls = remove_dup_array(facebook_reels_urls)
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={user_data}")
    options.add_argument(f"profile-directory={profile_dir}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    time.sleep(5)
    video_count = len(facebook_reels_urls)
    video_inc = 1
    for reels_url in facebook_reels_urls:
        try:
            driver.get(reels_url)
            time.sleep(5)
            # Click Button Download
            button_download = find_element_wait(driver, By.CSS_SELECTOR, 'div.download-videos-for-facebook-like-button > button > span')
            button_download.click()
            time.sleep(5)
            wait_until_download_complete(save_folder_path)
            video_old_name = check_name_download(save_folder_path)
            video_old_name_path = f"{save_folder_path}/{video_old_name}"
            # Create Video New Name
            title, extension = os.path.splitext(video_old_name)
            new_title = ""
            if title.endswith(".hd"):
                new_title = title[:-3]
            new_title = new_title[:200]
            video_new_name_path = f"{save_folder_path}/{video_inc}_{new_title}{extension}"
            rename_video(video_old_name_path, video_new_name_path)
            random_number = random.randint(5, 15)
            time.sleep(random_number)
            print(f"{video_count}/{video_inc} - {new_title}")
            video_inc += 1
        except Exception as e:
            print(f"Download Error : {e}")

    driver.quit()

if __name__ == "__main__":
    main()