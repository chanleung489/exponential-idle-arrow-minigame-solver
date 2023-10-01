import pyautogui, mss.tools, mouseinfo, mouse, pytesseract, cv2
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
PNG_PATH = "png.png"
TXT_PATH = "text.txt"

class variableCurrency:
    def __init__(self, /, x1, y1, x2, y2, image, path, value) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.coords = [x1, y1, x2, y2]
        self.width = x2 - x1
        self.height = y2 - y1
        self.image = image
        self.path = path
        self.value = value
        
    def screenshot(self):
        # store_on_a()
        with mss.mss() as sct:
            monitor = {"top": self.y1, "left": self.x1, "width": self.width, "height": self.height}
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=self.path+PNG_PATH)

    def getValue(self):
        self.screenshot()
        image = Image.open(self.path+PNG_PATH)
        norm_img = np.zeros((image.size[0], image.size[1]))
        image = np.array(image)
        image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
        image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
        image = cv2.GaussianBlur(image, (1, 1), 0)
        # cv2.imshow('image',image)
        # cv2.waitKey(0)
        text = pytesseract.image_to_string(image)
        # print(str(list(text)))
        isValid = text != "" and [i for i in text if not i.isdigit()] == [".", "e", "p", "\n"]
        if isValid: 
            try:
                self.value = float(text[:-2])
            except:
                raise Exception(f"invalid {text[:-1]}")
            print(str(self.value))
            with open(self.path+TXT_PATH, "w") as file:
                file.write(str(self.value))
        # else:
        #     print("invalid"+str(list(text)))
        


currentP = variableCurrency(1744, 347, 1844, 380, image=0, path="getpos/currentP/", value=0)
upgrades = []
for i in range(5):
    upgrades.append(variableCurrency(1812, 441+i*67, 1902, 470+i*67, image=0, path=f"getpos/upgrades/{i}/", value=0))

while 1:
    # currentP.getValue()
    upgrades[0].getValue()
    

# storePos = []
# def store_on_a():
#     storePos.append(pyautogui.position())
#     print(*storePos)

# mouseinfo.mouseInfo()
# while 1:
    # print(pyautogui.position())

# pyautogui.displayMousePosition()
# upgrade1.getValue()

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
