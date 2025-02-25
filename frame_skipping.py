import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the exported NCNN model
ncnn_model = YOLO("yolo11n_ncnn_model")

# Calculating frame
frame_count = 0

frame_skip = 5

names = ncnn_model.names


results = list()

# Run inference
while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

    # Run frame skipping by forwording the frame during skipping
    if frame_count % frame_skip == 0:
        # Run YOLO11 inference on the frame
        results = ncnn_model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        frame_count = 0

    for i in range(len(results[0].boxes)):
        start_point = (int(results[0].boxes.xyxy[i][0]),int(results[0].boxes.xyxy[i][1]))
        end_point = (int(results[0].boxes.xyxy[i][2]),int(results[0].boxes.xyxy[i][3]))
        color = (255,0,0)
        frame = cv2.rectangle(frame,start_point,end_point,color,1)
        org = (start_point[0],start_point[1]-10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_color = (0,0,255)

        frame = cv2.putText(frame, names[int(results[0].boxes.cls[i])], org, font, 1, font_color, 1)

    frame_count += 1

    # Display the resulting frame
    cv2.imshow("Camera", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources and close windows
picam2.stop()
cv2.destroyAllWindows()
print("Process ended")