import sys
import os
import time
import re
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse  # Import argparse for command-line arguments

# Paths
libdir = "/opt/kvb-abfahrt/lib"
picdir = "/opt/kvb-abfahrt/pic"
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_OLED import OLED_1in5
from PIL import Image, ImageDraw, ImageFont

# Set up command-line arguments
parser = argparse.ArgumentParser(description="KVB Departure Display Script")
parser.add_argument('--log', action='store_true', help="Enable logging output")
args = parser.parse_args()

# Configure logging
if args.log:
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARNING)

# Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')

# Path to ChromeDriver
service = Service('/usr/bin/chromedriver')  # Update with the actual path

def extract_actual_time(departure_time):
    # Extract the part of the string before any parenthesis or newline
    match = re.search(r'\d{2}:\d{2}', departure_time)
    if match:
        actual_time = match.group(0)
    else:
        actual_time = departure_time
    return actual_time.strip()

def fetch_departures():
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(service=service, options=options)
        url = 'https://www.vrs.de/am/s/0e7c23ccc3387904e928c8a853965e55'
        driver.get(url)
        time.sleep(5)  # Adjust wait time based on page load speed

        # Find departure data
        table = driver.find_element(By.ID, 'stopEvents-1')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        departures = []
        for row in rows[1:]:  # Skip the header row
            cols = row.find_elements(By.TAG_NAME, 'td')
            departure_time = cols[0].text.strip()
            minutes_to_departure = cols[1].text.strip()
            line = cols[2].text.strip()
            direction = cols[3].text.strip()

            departure_time = extract_actual_time(departure_time)

            if '18' in line:
                departure = {
                    'departure_time': departure_time,
                    'minutes_to_departure': minutes_to_departure,
                    'line': line,
                    'direction': direction
                }
                departures.append(departure)
                # Debugging output
                logging.info(f"Fetched departure: {departure}")

        driver.quit()
        return departures
    except Exception as e:
        logging.error("Error fetching data: %s", e)
        return []

def display_departure(disp, font, departure):
    image = Image.new('L', (disp.width, disp.height), 0)
    draw = ImageDraw.Draw(image)

    # Display each entry
    current_time = datetime.now().strftime('%H:%M:%S')
    draw.text((0, 0), f"{current_time}", font=font, fill=127)
    draw.text((0, 18), f"Abfahrt:", font=font, fill=127)
    draw.text((0, 18*2), f"{departure['departure_time']}", font=font, fill=127)
    draw.text((0, 18*3), f"in:", font=font, fill=127)
    draw.text((0, 18*4), f"{departure['minutes_to_departure']}", font=font, fill=127)
    draw.text((0, 18*5), f"Richtung:", font=font, fill=127)
    draw.text((0, 18*6), f"{departure['direction']}", font=font, fill=127)

    disp.ShowImage(disp.getbuffer(image))

def main():
    disp = OLED_1in5.OLED_1in5()
    disp.Init()
    disp.clear()
    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    departures = fetch_departures()
    departure_index = 0

    while True:
        if departures:
            display_departure(disp, font, departures[departure_index])
            departure_index = (departure_index + 1) % len(departures)
            time.sleep(5)  # Display each entry for 5 seconds

        if departure_index == 0:
            departures = fetch_departures()
            if not departures:
                logging.info("No departures found or error occurred.")
                time.sleep(60)  # Wait before trying again

if __name__ == '__main__':
    main()
