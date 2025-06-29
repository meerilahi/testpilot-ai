from PIL import Image
def extract_student_id(image: Image.Image) -> int:
    # image = np.array(image)
    # cropped_image = image[525:805, 105:300]
    # cv2.imwrite('temp_data/cropped_image.jpg', cropped_image)
    # image = cv2.imread('temp_data/cropped_image.jpg')
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5,5), 0)
    # thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
    # filled_bubbles = []
    # for c in cnts:
    #     x, y, w, h = cv2.boundingRect(c)
    #     aspect_ratio = w / float(h)
    #     area = cv2.contourArea(c)
    #     if 0.8 <= aspect_ratio <= 1.2 and 225 <= area <= 400:
    #         roi = thresh[y:y+h, x:x+w]
    #         total_pixels = w * h
    #         filled_pixels = cv2.countNonZero(roi)
    #         fill_ratio = filled_pixels / float(total_pixels)
    #         if fill_ratio > 0.5:
    #             filled_bubbles.append((x, y, w, h))
    #             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # print(filled_bubbles)
    # def get_number(x,y, w,h):
    #     x_center = x+w//2
    #     y_center = y+h//2
    #     x_map = { (5,38) : 1, (38,65) : 2, (65,97) : 3, (97,125) : 4, (125,157) : 5, (157,190) : 6}
    #     y_map = { (5,35) : 1, (35,60) : 2, (60,85) : 3, (85,115) : 4, (115,139) : 5, (139,165) : 6, (165,190) : 7, (190,215) : 8, (215,243) : 9, (243,270) : 0 }
    #     col = -1
    #     for key in x_map.keys():
    #         if x_center >= key[0] and x_center < key[1]:
    #             col = x_map[key]
    #     digit = -1
    #     for key in y_map.keys():
    #         if y_center >= key[0] and y_center < key[1]:
    #             digit = y_map[key]
    #     return digit,col
    # numbers = []
    # for bubble in filled_bubbles:
    #     number = get_number(bubble[0],bubble[1],bubble[2],bubble[3])
    #     numbers.append(number)
    # sorted_data = sorted(numbers, key=lambda x: x[1])
    # roll_number = ""
    # for item in sorted_data:
    #     roll_number += str(item[0])
    # return int(roll_number)

    return 123456  # Placeholder for the actual student ID extraction logic

# pil_image = Image.open('temp_data/title.jpg')
# student_id = extract_student_id(pil_image)
# print(f"Extracted Student ID: {student_id}")
