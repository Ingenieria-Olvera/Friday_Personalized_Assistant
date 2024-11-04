import cv2
import numpy as np
import sys
import time

#timing time in rectangle
inside_rect_f = False
inside_rect_h = False
inside_rect_p = False
inside_rect_q = False
start_time = 0
required_time_in_rect = 2
required_time_in_rect_to_quit = 10

# Set the video source to 0 (default camera) or use an argument
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

source = cv2.VideoCapture(s)

win_name = 'Hand Tracking Interface'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)


while cv2.waitKey(1) != 27:  # Escape key to exit
    has_frame, frame = source.read()
    if not has_frame:
        break

    # Convert the frame to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a range for skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)  # Adjust these values
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)



    # ALL RECTANGLES FOR THIS THING------------------------------------------------------------------

    #FRIDAY RECTANGLE
    top_left_F = (70, 70)
    bottom_right_F = (170, 120)
    color_F = (0, 0, 255)  # RED
    thickness = 2        # Thickness of the border
    cv2.rectangle(frame, top_left_F, bottom_right_F, color_F, thickness)


    # HELP RECTANGLE
    top_left_H = (50, 300)
    bottom_right_H = (100, 350)
    color_H = (0, 255, 0)
    cv2.rectangle(frame, top_left_H, bottom_right_H, color_H, thickness)


    #PROJECTS RECTANGLE
    top_left_P = (450, 70)
    bottom_right_P = (550, 120)
    color_P = (255, 0, 0)  # BLUE
    cv2.rectangle(frame, top_left_P, bottom_right_P, color_P, thickness)

    #QUIT RECTANGLE
    top_left_Q = (530, 300)
    bottom_right_Q = (580, 350)
    
    color_Q = (78, 54, 41)  # BROWN
    cv2.rectangle(frame, top_left_Q, bottom_right_Q, color_Q, thickness)
    #cv2.putText(frame, "Who is hungry?", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    #---------------------------------------------------------------------------------------------------------------------

    # INSIDE RECT CODE-------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------------------


    # Create a mask that filters out everything except the skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply some blur to the mask to reduce noise
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # If any contours are found, proceed
    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)

        #FRIDAY BELOOWWW-----------------------------------
        # Draw a bounding box around the largest contour (your hand)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if (x < bottom_right_F[0] and x + w > top_left_F[0] and y < bottom_right_F[1] and y + h > top_left_F[1]):
            if not inside_rect_f:
                inside_rect_f = True
                start_time = time.time()
            elapsed_time = time.time() - start_time
            if elapsed_time >= required_time_in_rect:
                cv2.putText(frame, "Action Triggered: Friday!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        else:
            inside_rect = False

        # HELP BELOWWW-----------------------------------------
        
        if (x < bottom_right_H[0] and x + w > top_left_H[0] and y < bottom_right_H[1] and y + h > top_left_H[1]):
            if not inside_rect_h:
                inside_rect_h = True
                start_time = time.time()
            elapsed_time = time.time() - start_time
            if elapsed_time >= required_time_in_rect:
                cv2.putText(frame, "Action Triggered: HELP!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        else:
            inside_rect = False

        # PROJECT BELOOWWW---------------------------

        if (x < bottom_right_P[0] and x + w > top_left_P[0] and y < bottom_right_P[1] and y + h > top_left_P[1]):
            if not inside_rect_p:
                inside_rect_p = True
                start_time = time.time()
            elapsed_time = time.time() - start_time
            if elapsed_time >= required_time_in_rect:
                cv2.putText(frame, "Action Triggered: PROJECTS!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        else:
            inside_rect = False

        '''

        #QUIT CODE, ITS A LITTLE BUGGY RN IT WORKS JUST A LITTLE BUGGY SO WE WONT INCLUDE IT
    
        if (x < bottom_right_Q[0] and x + w > top_left_Q[0] and y < bottom_right_Q[1] and y + h > top_left_Q[1]):
            if not inside_rect_q:
                inside_rect_q = True
                start_time = time.time()
            elapsed_time = time.time() - start_time
            if elapsed_time >= required_time_in_rect_to_quit:
                cv2.putText(frame, "Action Triggered: QUITTING!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                source.release()
                cv2.destroyAllWindows()
        else:
            inside_rect = False
        '''

    # Show the original frame with the hand-tracking rectangle
    cv2.imshow(win_name, frame)

# Release resources
source.release()
cv2.destroyAllWindows()
