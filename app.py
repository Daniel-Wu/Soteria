import time
import edgeiq
import cv2
"""
Use object detection to detect human faces in the frame in realtime.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""


def main():
    #Load in our machine learning models!
    detector_config = {"engine": edgeiq.Engine.DNN}

    #Get the face detector:
    facial_detector = edgeiq.ObjectDetection(
            "alwaysai/res10_300x300_ssd_iter_140000")
    facial_detector.load(**detector_config)

    print("Face Engine: {}".format(facial_detector.engine))
    print("Face Accelerator: {}\n".format(facial_detector.accelerator))
    print("Face Model:\n{}\n".format(facial_detector.model_id))

    #Get the gender detector
    gender_detector = edgeiq.Classification("alwaysai/gendernet")
    gender_detector.load(**detector_config)
    print("Gender Engine: {}".format(gender_detector.engine))
    print("Gender Accelerator: {}\n".format(gender_detector.accelerator))
    print("Gender Model:\n{}\n".format(gender_detector.model_id))
    print("Gender Labels:\n{}\n".format(gender_detector.labels))

    #Get the age detector
    age_detector = edgeiq.Classification("alwaysai/agenet")
    age_detector.load(**detector_config)
    print("Age Engine: {}".format(age_detector.engine))
    print("Age Accelerator: {}\n".format(age_detector.accelerator))
    print("Age Model:\n{}\n".format(age_detector.model_id))
    print("Age Labels:\n{}\n".format(age_detector.labels))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as webcam, \
                edgeiq.Streamer() as streamer:
            # Allow webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = webcam.read()
                # detect human faces
                face_results = facial_detector.detect_objects(
                        frame, confidence_level=.5)

                #Blur detected faces
                if len(face_results.predictions) > 0:
                    for pred in face_results.predictions:
                        start_y = int(0.9*pred.box.start_y)
                        end_y = int(1.1*pred.box.end_y)
                        start_x = int(0.9*pred.box.start_x)
                        end_x = int(1.1*pred.box.end_x)
                        ROI = frame[start_y:end_y, start_x:end_x]
                        blur = cv2.GaussianBlur(ROI, (51,51), 0) 
                        frame[start_y:end_y, start_x:end_x] = blur

                #Detect gender and age
                gender_results = gender_detector.classify_image(
                        frame, confidence_level=.9)
                age_results = age_detector.classify_image(frame)

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

                streamer.send_data(frame, text)

                fps.update()

                if streamer.check_exit():
                    break

    finally:
        # stop fps counter and display information
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()