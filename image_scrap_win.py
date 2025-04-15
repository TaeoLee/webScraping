import os
import time
import datetime
import re
import subprocess
import pytesseract
import cv2
import numpy as np
from PIL import Image

# --- Settings ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Change this to your Tesseract-OCR installation path

# URL to monitor
url = "https://kr.investing.com/indices/us-spx-500-futures?cid=1175153"
base_folder = "C:\\Users\\g1238\\stock_predict\\code\\screenshots" # Change this to your desired folder
output_file = "all_stock_prices.txt"

os.makedirs(base_folder, exist_ok=True)

print("Starting stock price OCR monitoring using webscreenshot...")

try:
  while True:
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Run webscreenshot
    subprocess.run([
      "webscreenshot",
      "-r", "chrome",
      "--renderer-binary", "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
      "-o", base_folder,
      url
    ])
            
    screenshot_name = "https_kr.investing.com_443_indices_us-spx-500-futures_cid_1175153.png"
    screenshot_path = os.path.join(base_folder, screenshot_name)

    # crop screenshot and save
    image = Image.open(screenshot_path)
    crop_area = (30, 700, 250, 830)
    cropped_image = image.crop(crop_area)
    image_path = os.path.join(base_folder, f"{timestamp}.png")
    cropped_image.save(image_path)
    
    os.remove(screenshot_path)
                
    # Check if screenshot exists
    if not os.path.exists(image_path):
      print(f"[{timestamp}] Screenshot not found: {image_path}")
      break
                
    print(f"[{timestamp}] Screenshot: {image_path}")

    # OCR
    img_cv = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(img_cv, 150, 255, cv2.THRESH_BINARY)
    extracted_text = pytesseract.image_to_string(binary, config='--psm 6')
    
    print(extracted_text)
    # Extract price
    match = re.search(r'\d{1},\d{3}\.\d+', extracted_text)
    stock_price = match.group(0) if match else "N/A"

    # Save to file
    with open(output_file, "a", encoding="utf-8") as f:
      f.write(f"{timestamp}: {stock_price}\n") 

    print(f"[{timestamp}] Stock Price (OCR): {stock_price}")

    #time.sleep(10)
    break
except KeyboardInterrupt:
  print("Monitoring stopped by user.")
