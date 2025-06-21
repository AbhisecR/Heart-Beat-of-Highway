import cv2
import mediapipe as mp
from deepface import DeepFace
from blockchain import log_emotion_to_blockchain
from v2x import broadcast_emotion_alert

# ========== EMOTION DETECTION SETUP ==========
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)
    emotion = "No face detected"

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x = int(bboxC.xmin * w)
            y = int(bboxC.ymin * h)
            width = int(bboxC.width * w)
            height = int(bboxC.height * h)

            pad = 10
            x1 = max(x - pad, 0)
            y1 = max(y - pad, 0)
            x2 = min(x + width + pad, w)
            y2 = min(y + height + pad, h)
            face_img = frame[y1:y2, x1:x2]

            try:
                analysis = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
                emotion = analysis[0]['dominant_emotion']

                # 🔐 Log emotion securely to blockchain
                log_emotion_to_blockchain(emotion)
                broadcast_emotion_alert(emotion)

            except:
                emotion = "Emotion error"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'Emotion: {emotion}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            break  # Analyze only first face for now

    cv2.imshow("Emotion Detection (MediaPipe + DeepFace + Blockchain)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
