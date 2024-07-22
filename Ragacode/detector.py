
from qrdet import QRDetector
import cv2
import numpy as np
import time
import resize2
import read


stop = False

cap = cv2.VideoCapture(0)
x = 0
print("ready")
while True:
    x = x + 1
    # Read the frame from the webcam
    ret, frame = cap.read()
    if not ret: break
    image = frame
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & ord('q'): stop = True

    detector = QRDetector(model_size='s')
    detections = detector.detect(image=image, is_bgr=True)

    with open("detections.txt", 'w') as f:
        f.writelines(str(detections))
    # print(detections)

    # Draw the detections
    for detection in detections:
        # ctl, cbl, ctr, cbl.astype(int)
        # polygon_xy = detection['polygon_xy']
        quad_xy = detection['quad_xy']
        confidence = detection['confidence']

        # polygon_points = np.array(polygon_xy, dtype=np.int32).reshape((-1, 1, 2))
        quad_points = np.array(quad_xy, dtype=np.int32).reshape((-1, 1, 2))

        # Draw the polygon
        # For Testing Only
        # cv2.polylines(image, [quad_points], isClosed=True, color=(0, 255, 0), thickness=2)

        # x1, y1 = quad_xy[0]
        # cv2.putText(frame, f'{confidence:.2f}', (x1, y1 - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=1, color=(0, 255, 0), thickness=2)
        
        # Crop the region of interest (ROI) based on polygon points
        ptl, ptr, pbr, pbl= quad_xy
        print(ptl, ptr, pbr, pbl)

        cropped_image = frame[int(ptl[1]):int(pbr[1]), int(ptl[0]):int(pbr[0])]
        # cropped_image = frame[ptl[1]:pbr[1], ptl[0]:pbr[0]]

        height, width, _ = cropped_image.shape
        height, width = 2880, 2880 #1440,1440
        dst_pts = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
        crop_area = np.array([ptl, ptr, pbr, pbl], dtype=np.float32)

        # polygon_points = np.array(polygon_xy, dtype=np.float32).reshape((4, 2))
        transform_matrix = cv2.getPerspectiveTransform(crop_area, dst_pts)

        # Apply the perspective transform to the ROI
        warped_image = cv2.warpPerspective(image, transform_matrix, (width, height))

        resize2.main()
        read.main()
    
        # Display the cropped image
        # cv2.imshow("Cropped Image", cropped_image)
        # cv2.imshow("Warped Image", warped_image)
        
        # cv2.imwrite("Cropped Image.jpeg", cropped_image)
        cv2.imwrite("Warped Image.jpeg", warped_image)
        # cv2.imwrite(filename='qreader_test_image_detections.jpeg', img=image)
        cv2.imshow("image",image)