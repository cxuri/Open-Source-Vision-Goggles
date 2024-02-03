import cv2

# URL of the stream
stream_url = 'http://192.168.1.7:81/stream'

# Open the stream
cap = cv2.VideoCapture(stream_url)

# Check if the stream is opened successfully
if not cap.isOpened():
    print("Error: Could not open stream")
    exit()

# Loop to read frames from the stream
while True:
    # Read a frame from the stream
    ret, frame = cap.read()

    # Check if frame is successfully read
    if not ret:
        print("Error: Could not read frame")
        break

    # Display the frame
    cv2.imshow('Frame', frame)

    # Check for key press, if 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the stream and destroy any OpenCV windows
cap.release()
cv2.destroyAllWindows()