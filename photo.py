import cv2
import pytesseract

# Set the path to the installed Tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change to your path

def preprocess_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blurring and thresholding to reveal the characters on the license plate
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Return the preprocessed image
    return thresh

def extract_plate_number(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Use Tesseract OCR to extract text
    result = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 6')
    
    # Return the result
    return result.strip()

# Set the path to your image
image_path = 'image.jpeg'

# Extract the plate number
plate_number = extract_plate_number(image_path)

# Print the extracted plate number
print("Extracted Plate Number:", plate_number)

# Display the original and preprocessed images (optional)
original_image = cv2.imread(image_path)
cv2.imshow('Original Image', original_image)
cv2.imshow('Preprocessed Image', preprocess_image(image_path))
cv2.waitKey(0)
cv2.destroyAllWindows()
