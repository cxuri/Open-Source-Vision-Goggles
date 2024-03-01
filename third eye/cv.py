import cv2

def detect():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    eye_cascade_left = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lefteye_2splits.xml')
    eye_cascade_right = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')

    video_capture = cv2.VideoCapture(0) 

    while video_capture.isOpened(): 
        # Captures video_capture frame by frame 
        ret, frame = video_capture.read()  
        
        # To capture image in monochrome                     
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        # Number of faces detected
        num_faces = len(faces)
        
        for i, (x, y, w, h) in enumerate(faces, 1): 
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, 'Face {}'.format(i), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            roi_gray = gray[y:y + h, x:x + w] 
            roi_color = frame[y:y + h, x:x + w] 
        
            # Detect smiles
            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=10) 
            for (sx, sy, sw, sh) in smiles: 
                cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2) 

            # Detect eyes
            eyes_left = eye_cascade_left.detectMultiScale(roi_gray)
            for (elx, ely, elw, elh) in eyes_left:
                cv2.rectangle(roi_color, (elx, ely), (elx + elw, ely + elh), (0, 255, 0), 2)

            eyes_right = eye_cascade_right.detectMultiScale(roi_gray)
            for (erx, ery, erw, erh) in eyes_right:
                cv2.rectangle(roi_color, (erx, ery), (erx + erw, ery + erh), (0, 255, 0), 2)

        # Display the result on camera feed                      
        cv2.imshow('Video', frame)  
    
        # The control breaks once q key is pressed                         
        if cv2.waitKey(1) & 0xFF == ord('q'):                
            break
    
    # Release the capture once all the processing is done. 
    video_capture.release()                                  
    cv2.destroyAllWindows()

