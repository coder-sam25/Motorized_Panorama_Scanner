import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
frames = []
capture_limit = 8  # Increased for better 180 coverage
interval = 4      # 5s is too long; 2s keeps you moving steadily
last_capture = time.time()
last_frame_captured = None

def resize_frame(frame, width=800):
    h, w = frame.shape[:2]
    ratio = width / w
    return cv2.resize(frame, (width, int(h * ratio)))

print(f"Goal: Capture {capture_limit} images. Match the 'ghost' image for perfect overlap!")

while len(frames) < capture_limit:
    ret, frame = cap.read()
    if not ret: break

    display_frame = frame.copy()
    
    # --- GHOSTING OVERLAY ---
    # Shows the previous capture semi-transparently to help you line up the overlap
    if last_frame_captured is not None:
        display_frame = cv2.addWeighted(frame, 0.6, last_frame_captured, 0.4, 0)

    # UI Overlay
    cv2.putText(display_frame, f"Captured: {len(frames)}/{capture_limit}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Webcam (Align with Ghost)", display_frame)
    
    current_time = time.time()
    if current_time - last_capture >= interval:
        frame_small = resize_frame(frame, width=800)
        frames.append(frame_small)
        last_frame_captured = frame.copy() # Store full size for ghosting
        last_capture = current_time
        print(f" Captured {len(frames)}")

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

if len(frames) < 2:
    print("Not enough images.")
    exit()

print(" Stitching in SCANS mode...")
# Use SCANS mode for linear/horizontal rotation
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
stitcher.setPanoConfidenceThresh(0.6) # Be more forgiving of slight mismatches

status, panorama = stitcher.stitch(frames)

if status != cv2.Stitcher_OK:
    print(f"Stitching failed (Status {status}). Try rotating more slowly or use more light.")
else:
    if status == cv2.Stitcher_OK:
        # 1. Create a mask of the panorama (255 where there is image, 0 where it's black)
        stitched = cv2.copyMakeBorder(panorama, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

        # 2. Find the largest contour (the whole panorama)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        c = max(cnts, key=cv2.contourArea)

        # 3. Create a mask for the rectangle search
        mask = np.zeros(thresh.shape, dtype="uint8")
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        # 4. Iteratively erode the mask until it fits inside the panorama
        minRect = mask.copy()
        sub = mask.copy()  

        while cv2.countNonZero(sub) > 0:
            minRect = cv2.erode(minRect, None)
            sub = cv2.subtract(minRect, thresh)

        # 5. Extract the final clean rectangle
        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        final_panorama = stitched[y:y + h, x:x + w]

        cv2.imshow("Clean 180 Panorama", final_panorama)
        cv2.imwrite("panoramic_scan.jpg", final_panorama)
        print(" Success! Clean crop saved.")

cv2.destroyAllWindows()