import pyautogui
import cv2
import numpy as np
import pytesseract
import os
from concurrent.futures import ThreadPoolExecutor
import time
IPHONE_WIDTH = 265
BOARD_BUFFER = 50
IPHONE_HEIGHT = 220
BUFFER_FROM_TOP = 350
SAVE_PATH = "/Users/colinzhu/Documents/Projects/wordhunt/board/"
BOARD_PATH = "/Users/colinzhu/Documents/Projects/wordhunt/"
IMAGE_NAME = "/board.png"

class BoardCV:
    def __init__(self):
        self.board = []
        self.screen_width, self.screen_height = pyautogui.size()
        self.region = (self.screen_width - IPHONE_WIDTH, BUFFER_FROM_TOP, IPHONE_WIDTH - BOARD_BUFFER, IPHONE_HEIGHT)
        self.templates = self.load_templates("/Users/colinzhu/Documents/Projects/wordhunt/board")

    def capture_board(self):
        # Step 1: Capture the screenshot
        screenshot = pyautogui.screenshot(region=self.region)

        # Convert the screenshot to a NumPy array
        screenshot_np = np.array(screenshot)

        # Convert the color space from RGB to BGR
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        self.image = screenshot_cv

    def load_image(self):
        self.image = cv2.imread(BOARD_PATH + IMAGE_NAME)
        if self.image is None:
            raise FileNotFoundError(f"Image not found at path: {BOARD_PATH + IMAGE_NAME}")

    def divide_image(self):
        height, width, _ = self.image.shape
        self.cell_height = height // 4
        self.cell_width = width // 4

    def process_letter(self, square):
        gray = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Crop image by the first contour 
        x, y, w, h = cv2.boundingRect(contours[0])
        cropped_image = thresholded[y:y+h, x:x+w]

        # Further crop the image by 3 pixels on all sides
        crop_margin = 4
        cropped_image = cropped_image[crop_margin:-crop_margin, crop_margin:-crop_margin]


        letter = self.check_against_database(cropped_image)
        if letter:
           return letter.strip()
        letter = pytesseract.image_to_string(cropped_image, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        if letter:
            filename = f"{SAVE_PATH}{letter}.png"
            cv2.imwrite(filename, cropped_image)
        return letter.strip()


    def load_templates(self, directory):
        templates = {}
        for filename in os.listdir(directory):
            if filename.endswith('.png'):
                template = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)
                templates[filename] = template
        return templates

    def match_template(self, image, template, filename):
        if image.shape[0] > template.shape[0] or image.shape[1] > template.shape[1]:
            resized_image = cv2.resize(image, (template.shape[1], template.shape[0]))
            res = cv2.matchTemplate(template, resized_image, cv2.TM_CCOEFF_NORMED)
        else:
            res = cv2.matchTemplate(template, image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            return filename
        return None

    def check_against_database(self, image):
        for filename, template in self.templates.items():
            if image.shape[0] > template.shape[0] or image.shape[1] > template.shape[1]:
                resized_image = cv2.resize(image, (template.shape[1], template.shape[0]))
                res = cv2.matchTemplate(template, resized_image, cv2.TM_CCOEFF_NORMED)
            else:
                res = cv2.matchTemplate(template, image, cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(res >= threshold)
            if len(loc[0]) > 0:
                return filename.strip('.png')
        print("No match found")
        return None

    def process_board(self):
        self.divide_image()

        for row in range(4):
            board_row = []
            for col in range(4):
                x_start = col * self.cell_width
                y_start = row * self.cell_height
                square = self.image[y_start:y_start + self.cell_height, x_start:x_start + self.cell_width]
         
                letter = self.process_letter(square)
                board_row.append(letter)
            self.board.append(board_row)
    
    def get_board(self):
        return self.board