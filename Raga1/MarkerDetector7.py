import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw

cap = cv2.VideoCapture(0)
x = 0
while True:
    x = x + 1
    # Read the frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        break
    
    image = frame
    image2 = frame
    cv2.imwrite("frame.png",frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    image = Image.open('frame.png').convert('RGB')
    draw = ImageDraw.Draw(image)
    cv2.imshow("frame",frame)
    #cv2.moveWindow('img',30,40)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # if x >33:
    #     break
    
    for barcode in decode(image):
        rect = barcode.rect
        draw.rectangle(
            (
                (rect.left, rect.top),
                (rect.left + rect.width, rect.top + rect.height)
            ),
            outline='#0080ff'
        )
        draw.polygon(barcode.polygon, outline='#e945ff')
        #print(rect);print(barcode)
        print(barcode[0],barcode[1],barcode[2],barcode[3],barcode[4],barcode[5])
        pt_A,pt_B,pt_C,pt_D = barcode[3]
        print(pt_A,pt_B,pt_C,pt_D)

        # Used L2 norm. You can use L1 also.
        width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
        width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
        maxWidth = max(int(width_AD), int(width_BC))
        
        height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
        height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
        maxHeight = max(int(height_AB), int(height_CD))

        input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
        output_pts = np.float32([[0, 0],
                            [0, maxHeight - 1],
                            [maxWidth - 1, maxHeight - 1],
                            [maxWidth - 1, 0]])

        # Compute the perspective transform M
        M = cv2.getPerspectiveTransform(input_pts,output_pts)
        out = cv2.warpPerspective(image2,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)
        
        
        image.save('bounding_box_and_polygon.png')

        cv2.imshow("warpedQR",out)
        cv2.imwrite('warpedQR.png',out)

    

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
