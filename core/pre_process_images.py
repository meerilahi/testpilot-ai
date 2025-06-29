import cv2
from PIL import Image
import numpy as np
from typing import List, Dict

def extract_writing_area(image, debug=False, name=None):
    image_np = np.array(image)
    img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    orig = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 1: Preprocessing
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Step 2: Morphological closing to join broken lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Step 3: Contour detection
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    height, width = img.shape[:2]
    candidates = []

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            area = cv2.contourArea(approx)
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / h

            if 0.5 < aspect_ratio < 1.5 and area > 0.3 * width * height:
                candidates.append((area, approx))

    if debug:
        debug_img = orig.copy()
        for _, approx in candidates:
            cv2.drawContours(debug_img, [approx], -1, (0, 255, 0), 2)   
        for cnt in contours:
            cv2.drawContours(debug_img, [cnt], -1, (255, 0, 0), 1)
        cv2.imwrite(f"debug_detected_boxes_{name}.png", debug_img)

    if not candidates:
        # Fallback: crop image from all sides with custom margins
        top_margin = 350
        bottom_margin = 350
        left_margin = 200
        right_margin = 200
        cropped_fallback = orig[top_margin:height - bottom_margin, left_margin:width - right_margin]
        cropped_fallback_rgb = cv2.cvtColor(cropped_fallback, cv2.COLOR_BGR2RGB)
        if debug:
            cv2.imwrite(f"extracted_fallback_{name}.png", cropped_fallback_rgb)
        pil_image = Image.fromarray(cropped_fallback_rgb)
        return pil_image
        
    # Step 4: Choose the largest candidate
    best_box = sorted(candidates, key=lambda x: x[0], reverse=True)[0][1]
    pts = best_box.reshape(4, 2)
    rect = order_points(pts)

    # Step 5: Perspective transform
    (tl, tr, br, bl) = rect
    target_width = int(max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl)))
    target_height = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))

    dst = np.array([
        [0, 0],
        [target_width, 0],
        [target_width, target_height],
        [0, target_height]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(orig, M, (target_width, target_height))
    margin = 25  
    h, w = warped.shape[:2]
    cropped_tightly = warped[margin:h-margin, margin:w-margin]
    cropped_tightly_rgb = cv2.cvtColor(cropped_tightly, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cropped_tightly_rgb)
    return pil_image

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]    # top-left
    rect[2] = pts[np.argmax(s)]    # bottom-right
    rect[1] = pts[np.argmin(diff)] # top-right
    rect[3] = pts[np.argmax(diff)] # bottom-left

    return rect

def pre_process_images(images_dic : Dict[int,List[Image.Image]]):
    processed_images = {}
    for question_number, images in images_dic.items():
        processed_images[question_number] = [extract_writing_area(image, name=f"{question_number}_{index}") for index, image in  enumerate(images)]
    return processed_images