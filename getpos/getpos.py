import pyautogui, mss.tools, mouseinfo, mouse, pytesseract, cv2
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class variableCurrency:
    def __init__(self, /, x1, y1, x2, y2, image, imagePath, value) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.coords = [x1, y1, x2, y2]
        self.width = x2 - x1
        self.height = y2 - y1
        self.image = image
        self.imagePath = imagePath
        self.value = value
        
    def screenshot(self):
        # store_on_a()
        with mss.mss() as sct:
            monitor = {"top": self.y1, "left": self.x1, "width": self.width, "height": self.height}
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=self.imagePath)

    def getValue(self):
        self.screenshot()
        image = Image.open(self.imagePath)
        image = np.array(image)
        # norm_img = np.zeros((image.size[0], image.size[1]))
        # image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
        # image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
        # image = cv2.GaussianBlur(image, (1, 1), 0)
        text = pytesseract.image_to_string(image)
        if text != "":
            print(text)
            with open("getpos/pVal.txt", "w") as pValText:
                pValText.write(text)
        


currentP = variableCurrency(1744, 347, 1844, 380, image=0, imagePath="getpos/currentP.png", value=0)
upgrade1 = variableCurrency(1812, 441, 1906, 466, image=0, imagePath="getpos/upgrade1.png", value=0)

# storePos = []
# def store_on_a():
#     storePos.append(pyautogui.position())
#     print(*storePos)

# mouseinfo.mouseInfo()
# while 1:
    # print(pyautogui.position())

# pyautogui.displayMousePosition()
upgrade1.screenshot()

# while 1:
#     screenshot(pPos)
#     image = Image.open("test.png")
#     image = np.array(image)
#     # norm_img = np.zeros((image.size[0], image.size[1]))
#     # image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
#     # image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
#     # image = cv2.GaussianBlur(image, (1, 1), 0)
#     text = pytesseract.image_to_string(image)
#     if text != "":
#         print(text)
#         with open("getpos/pVal.txt", "w") as pValText:
#             pValText.write(text)


# 1815,436 upgrade 1 y+60
# 1901,458
