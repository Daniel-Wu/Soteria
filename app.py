from flask import Flask, render_template, Response

app = Flask(__name__)

import cv2
import numpy as np
import time
import edgeiq
"""
Use ML to blur and record demographics of faces in real time.
"""

def describe_model(detector, name =""):
    print(name, "Engine: {}".format(detector.engine))
    print(name, "Accelerator: {}\n".format(detector.accelerator))
    print(name, "Model:\n{}\n".format(detector.model_id))

def blur_detections(frame, predictions):
    #Blur detected faces
    max_y, max_x, _ = frame.shape

    if len(predictions) > 0:
        for pred in predictions:
            start_y = int(0.9*pred.box.start_y)
            end_y = min(int(1.1*pred.box.end_y), max_y)
            start_x = int(0.9*pred.box.start_x)
            end_x = min(int(1.1*pred.box.end_x), max_x)
            try:
                ROI = frame[start_y:end_y, start_x:end_x]
                blur = cv2.GaussianBlur(ROI, (51,51), 0) 
                frame[start_y:end_y, start_x:end_x] = blur
            except:
                return frame

    return frame

def imwrite(img, text, org, thickness=1):
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), thickness=thickness)
    return img


def gen():
    #Load in our machine learning models!
    detector_config = {"engine":edgeiq.Engine.DNN_OPENVINO, "accelerator":edgeiq.Accelerator.MYRIAD}

    #Get the face detector:
    facial_detector = edgeiq.ObjectDetection(
            "alwaysai/res10_300x300_ssd_iter_140000")
    facial_detector.load(**detector_config)
    describe_model(facial_detector, "Face")

    #Get the gender detector
    gender_detector = edgeiq.Classification("alwaysai/gendernet")
    gender_detector.load(**detector_config)
    describe_model(gender_detector, "Gender")

    #Get the age detector
    age_detector = edgeiq.Classification("alwaysai/agenet")
    age_detector.load(**detector_config)
    describe_model(age_detector, "Age")
    
    texts = ["No patient detected!"]

    with edgeiq.WebcamVideoStream(cam=0) as webcam:
        # loop detection
        while True:
            frame = webcam.read()
            # detect human faces
            face_results = facial_detector.detect_objects(
                    frame, confidence_level=.5)


            if len(face_results.predictions) > 0:
                face = frame[face_results.predictions[0].box.start_y:face_results.predictions[0].box.end_y, 
                face_results.predictions[0].box.start_x:face_results.predictions[0].box.end_x]

                #Detect gender and age
                gender_results = gender_detector.classify_image(
                        face, confidence_level=.9)
                age_results = age_detector.classify_image(face)

                frame = blur_detections(frame, face_results.predictions)

                # Find the index of highest confidence
                if len(gender_results.predictions) > 0 and len(age_results.predictions) > 0:
                    top_prediction1 = gender_results.predictions[0]
                    top_prediction2 = age_results.predictions[0]
                    texts = []
                    texts.append("Gender Classification:")
                    texts.append("{}, {:.1f}%".format(
                            top_prediction1.label,
                            top_prediction1.confidence * 100))
                    texts.append("Age Classification:")
                    texts.append("{}, {:.1f}%".format(
                            top_prediction2.label,
                            top_prediction2.confidence * 100))
            else:
                texts = ["No patient detected!"]

            #HACK: Add a panel to the right side of the image
            label_panel = np.zeros((frame.shape[0], frame.shape[1]//2, frame.shape[2])) + 255
            org_coords = [(frame.shape[0]//15, i*frame.shape[1]//10) for i in range(1,5)]
            for i, text in enumerate(texts):
                label_panel = imwrite(label_panel, text, org_coords[i], thickness = 1 + ((i%2) == 0))

            frame = np.concatenate((frame, label_panel), axis = 1)

            #Encode and deploy
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            #yield frame
            yield (b'\r\n--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5005, debug=False)