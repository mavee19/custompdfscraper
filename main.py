import time
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.parse
import requests
import os
from fake_useragent import UserAgent


# Function to handle the "Select Folder" button click event
def select_folder():
    # Open a file dialog to select the downloads folder
    folder_path = filedialog.askdirectory()
    return folder_path


def get_folder_path(url):
    # Specify the absolute path to save the file in the current directory
    split_url = url.split('/')
    folder_name = '-'.join(split_url[2:])
    current_time_ms = int(time.time() * 1000)
    folder_name_with_time = f"{folder_name}_{current_time_ms}"
    folder_path = os.path.join(downloads_folder, folder_name_with_time)
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def scrape_pdfs_from_url():
    # Get the current working directory
    current_directory = os.getcwd()
    # Construct the path to the chromedriver file
    chromedriver_path = os.path.join(current_directory, "chromedriver")
    # Create ChromeOptions object and set headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1280")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    ua = UserAgent()
    userAgent = ua.random
    # Create a Service object with the chromedriver path
    service = Service(chromedriver_path)
    # Create a webdriver instance using the Service object
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
    url = entry.get()
    driver.get(url)
    folder_path = get_folder_path(url)
    # Find all the <a> tags with 'onclick' attribute containing 'download'
    links = driver.find_elements(By.XPATH, '//a[contains(@onclick, "download")]')
    links_url = [link.get_attribute('href') for link in links]
    # print(links_url)
    for link in links_url:
        pdf_link = link
        # print(pdf_link)
        # Navigate to the PDF link and find the embedded PDF object
        driver.get(pdf_link)
        driver.implicitly_wait(10)
        embedded_pdf = driver.find_element(By.XPATH, '//object[contains(@data, ".pdf")]')
        # Extract the source URL of the embedded PDF
        embedded_pdf_url = embedded_pdf.get_attribute('data')
        # Extract the filename from the URL and sanitize it
        parsed_url = urllib.parse.urlparse(embedded_pdf_url)
        filename = os.path.basename(parsed_url.path)
        print(filename)

        # Download the embedded PDF file
        response = requests.get(embedded_pdf_url)
        file_path = os.path.join(folder_path, filename)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            # Wait for the file to finish downloading
            print(f"Finished downloading: {filename}")
        else:
            print(f"Failed to download: {filename}")

    driver.quit()


# Create the GUI window
window = tk.Tk()
window.wait_visibility()
window.title("Custom PDF Scraper")
window.geometry("550x100")  # Set the width and height of the window


downloads_folder = select_folder()

# Create a label and button for the downloads folder
label_folder = tk.Label(window, text="Downloads Folder:")
label_folder.grid(row=0, column=0, padx=5, pady=5, sticky="w")
label_folder_path = tk.Label(window, text=downloads_folder)
label_folder_path.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Create a label, entry, and button for the URL
label_url = tk.Label(window, text="Insert URL:")
label_url.grid(row=1, column=0, padx=5, pady=5, sticky="w")

entry = tk.Entry(window, width=50)
entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

button_scrape = tk.Button(window, text="Scrape PDF", command=scrape_pdfs_from_url)
button_scrape.grid(row=1, column=2, padx=5, pady=5)

# Run the GUI event loop
window.mainloop()
