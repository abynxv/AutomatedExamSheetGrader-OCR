import cv2
import numpy as np
from PIL import Image

def correct_orientation(image):
    return image

def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use edge detection instead of simple thresholding
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Use HoughLines to detect lines and determine skew angle
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
    
    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90
            if -45 <= angle <= 45:  # Filter for reasonable text angles
                angles.append(angle)
        
        if angles:
            # Use median angle to avoid outliers
            angle = np.median(angles)
        else:
            angle = 0
    else:
        angle = 0
    
    # Apply rotation
    if abs(angle) > 0.1:  # Only rotate if angle is significant
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), 
                               flags=cv2.INTER_CUBIC, 
                               borderMode=cv2.BORDER_REPLICATE)
        return rotated
    
    return image

def enhance_image(image):
    # Convert to LAB color space for better enhancement
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    
    # Apply CLAHE to the L channel only
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_channel = clahe.apply(l_channel)
    
    # Merge channels back
    enhanced_lab = cv2.merge([l_channel, a_channel, b_channel])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # Optional: Apply slight sharpening
    kernel = np.array([[-1,-1,-1], 
                      [-1, 9,-1], 
                      [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    # Blend original and sharpened (70% enhanced, 30% sharpened)
    result = cv2.addWeighted(enhanced, 0.7, sharpened, 0.3, 0)
    
    return result
