import pyautogui
import time
import random

IPHONE_WIDTH = 265
BOARD_BUFFER = 50
IPHONE_HEIGHT = 220
BUFFER_FROM_TOP = 350
CELL_SIZE = 55
WIGGLE = BOARD_BUFFER // 2

class WordHunter:
    def __init__(self, solutions):
        self.solutions = solutions
        self.screen_width, self.screen_height = pyautogui.size()

    def move_mouse_to_path(self, delay=0, timeout=85):
        """
        Move the mouse to each coordinate in the path.
        
        :param delay: Time to wait between moving to each coordinate (in seconds).
        """
  
        self.init_game()
        start_time = time.time()
        for pair in self.solutions:
            if time.time() - start_time > timeout:
                break
            path = pair[1]
            # Move to the first coordinate and click mouse down
            coords = [self.convert_coord_to_pixel(coord) for coord in path]
            pyautogui.moveTo(coords[0][0] + random.randint(-2,2), coords[0][1] + random.randint(-2,2), duration=delay)
            for coord in coords:
                pyautogui.dragTo(coord[0], coord[1], button='left', mouseDownUp=False, duration=delay)
        

    def init_game(self):
        top_left_x = self.screen_width - IPHONE_WIDTH
        top_left_y = BUFFER_FROM_TOP
        pyautogui.moveTo(top_left_x, top_left_y)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        pyautogui.mouseDown()

    def convert_coord_to_pixel(self, coordinate):
        """
        Convert a board coordinate (row, col) to pixel coordinates on the screen.
        
        :param coordinate: Tuple (row, col) representing the board coordinate.
        :return: Tuple (x, y) representing the pixel coordinates.
        """
        row, col = coordinate
        top_left_x = self.screen_width - IPHONE_WIDTH
        top_left_y = BUFFER_FROM_TOP

        x = top_left_x + (col * CELL_SIZE) + (CELL_SIZE / 2)
        y = top_left_y + (row * CELL_SIZE) + (CELL_SIZE / 2)

        return int(x), int(y)
