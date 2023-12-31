import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# Extract Text From Image testing.....

def extra01(image_path):
    # Load the image from path
    img = cv2.imread(image_path)

    # Convert the image to gray scale 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours: 
        x, y, w, h = cv2.boundingRect(cnt)
      
        # Drawing a rectangle on copied image 
        rect = cv2.rectangle(img.copy(), (x, y), (x+w,y+h), (0 ,255 ,0), 5) 

    return pytesseract.image_to_string(rect)

def extra02(image_path):
    im = Image.open(image_path) # the second one 
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('temp2.jpg')
    text = pytesseract.image_to_string(Image.open('temp2.jpg'))
    return text