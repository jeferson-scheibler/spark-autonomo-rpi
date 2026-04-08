import mediapipe as mp
import cv2

model_path = None

try:
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions, RunningMode
    from mediapipe.framework.formats import landmark_pb2
    NOVA_API = True
except Exception:
    NOVA_API = False

mp_draw = mp.solutions.drawing_utils
mp_hands_style = mp.solutions.drawing_styles
mp_hands_module = mp.solutions.hands

hands = mp_hands_module.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

def dedos_levantados(landmarks):
    dedos = []
    if landmarks[4].x < landmarks[3].x:
        dedos.append(1)
    else:
        dedos.append(0)
    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if landmarks[tip].y < landmarks[pip].y:
            dedos.append(1)
        else:
            dedos.append(0)
    return dedos

def identificar_gesto(landmarks):
    dedos = dedos_levantados(landmarks)
    total = sum(dedos)

    if total == 5:
        return "PARAR"
    if total == 0:
        return "AVANCAR"
    if dedos == [1, 0, 0, 0, 0]:
        return "RE"
    if dedos == [0, 1, 0, 0, 0]:
        return "VELOCIDADE+"

    return None

def processar_gestos(frame):
    resultado_gesto = None
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands_module.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                mp_draw.DrawingSpec(color=(255, 255, 0), thickness=2)
            )

            gesto = identificar_gesto(hand_landmarks.landmark)

            if gesto:
                resultado_gesto = gesto
                cv2.putText(
                    frame,
                    f"Gesto: {gesto}",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 255),
                    2
                )

    return frame, resultado_gesto
