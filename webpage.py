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
            ROI = frame[start_y:end_y, start_x:end_x]
            blur = cv2.GaussianBlur(ROI, (51,51), 0) 
            frame[start_y:end_y, start_x:end_x] = blur
    return frame

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

    with edgeiq.WebcamVideoStream(cam=0) as webcam:
        # Allow webcam to warm up
        time.sleep(2.0)

        # loop detection
        while True:
            frame = webcam.read()
            # detect human faces
            face_results = facial_detector.detect_objects(
                    frame, confidence_level=.5)

            #Detect gender and age
            gender_results = gender_detector.classify_image(
                    frame, confidence_level=.9)
            age_results = age_detector.classify_image(frame)

            frame = blur_detections(frame, face_results.predictions)

            # Find the index of highest confidence
            if len(gender_results.predictions) > 0 and len(age_results.predictions) > 0:
                top_prediction1 = gender_results.predictions[0]
                top_prediction2 = age_results.predictions[0]
                text1 = "Classification: {}, {:.2f}%".format(
                        top_prediction1.label,
                        top_prediction1.confidence * 100)
                text2 = "Classification: {}, {:.2f}%".format(
                        top_prediction2.label,
                        top_prediction2.confidence * 100)
            else:
                text1 = "Can not classify this image, confidence under " \
                        "90 percent for Gender Identification"
                text2 = None

            # Generate text to display on streamer
            text = ["Gender Model: {}".format(gender_detector.model_id)]
            text.append("Age Model: {}".format(age_detector.model_id))
            text.append("Face Model: {}".format(facial_detector.model_id))
            text.append(
                    "Inference time: {:1.3f} s".format(gender_results.duration + 
                    age_results.duration + face_results.duration))
            text.append("Faces:")

            for prediction in face_results.predictions:
                text.append("{}: {:2.2f}%".format(
                    prediction.label, prediction.confidence * 100))

            text.append(text1)
            if text2 != None:
                text.append(text2)

            #Encode and deploy
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            #yield frame
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def video_feed():
    return Response(gen(),
                    #mimetype='image/jpeg')#
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)