from flask import Flask,render_template,Response
import cv2
import mediapipe as mp

app=Flask(__name__)
cap=cv2.VideoCapture(0)

def generate_frames():
            
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)


    FACEMESH_LIPS = frozenset([(61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
                               (17, 314), (314, 405), (405, 321), (321, 375),
                               (375, 291), (61, 185), (185, 40), (40, 39), (39, 37),
                               (37, 0), (0, 267),
                               (267, 269), (269, 270), (270, 409), (409, 291),
                               (78, 95), (95, 88), (88, 178), (178, 87), (87, 14),
                               (14, 317), (317, 402), (402, 318), (318, 324),
                               (324, 308), (78, 191), (191, 80), (80, 81), (81, 82),
                               (82, 13), (13, 312), (312, 311), (311, 310),
                               (310, 415), (415, 308)])

    FACEMESH_LEFT_EYE = frozenset([(263, 249), (249, 390), (390, 373), (373, 374),
                                   (374, 380), (380, 381), (381, 382), (382, 362),
                                   (263, 466), (466, 388), (388, 387), (387, 386),
                                   (386, 385), (385, 384), (384, 398), (398, 362)])

    FACEMESH_LEFT_IRIS = frozenset([(474, 475), (475, 476), (476, 477),
                                     (477, 474)])

    FACEMESH_LEFT_EYEBROW = frozenset([(276, 283), (283, 282), (282, 295),
                                       (295, 285), (300, 293), (293, 334),
                                       (334, 296), (296, 336)])

    FACEMESH_RIGHT_EYE = frozenset([(33, 7), (7, 163), (163, 144), (144, 145),
                                    (145, 153), (153, 154), (154, 155), (155, 133),
                                    (33, 246), (246, 161), (161, 160), (160, 159),
                                    (159, 158), (158, 157), (157, 173), (173, 133)])

    FACEMESH_RIGHT_EYEBROW = frozenset([(46, 53), (53, 52), (52, 65), (65, 55),
                                        (70, 63), (63, 105), (105, 66), (66, 107)])

    FACEMESH_RIGHT_IRIS = frozenset([(469, 470), (470, 471), (471, 472),
                                     (472, 469)])

    FACEMESH_FACE_OVAL = frozenset([(10, 338), (338, 297), (297, 332), (332, 284),
                                    (284, 251), (251, 389), (389, 356), (356, 454),
                                    (454, 323), (323, 361), (361, 288), (288, 397),
                                    (397, 365), (365, 379), (379, 378), (378, 400),
                                    (400, 377), (377, 152), (152, 148), (148, 176),
                                    (176, 149), (149, 150), (150, 136), (136, 172),
                                    (172, 58), (58, 132), (132, 93), (93, 234),
                                    (234, 127), (127, 162), (162, 21), (21, 54),
                                    (54, 103), (103, 67), (67, 109), (109, 10)])

    lips = frozenset([(61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
                               (17, 314), (314, 405), (405, 321), (321, 375),
                               (375, 291), (61, 185), (185, 40), (40, 39), (39, 37),
                               (37, 0), (0, 267),
                               (267, 269), (269, 270), (270, 409), (409, 291),
                               (78, 95), (95, 88), (88, 178), (178, 87), (87, 14),
                               (14, 317), (317, 402), (402, 318), (318, 324),
                               (324, 308), (78, 191), (191, 80), (80, 81), (81, 82),
                               (82, 13), (13, 312), (312, 311), (311, 310),
                               (310, 415), (415, 308)])

    contours = frozenset().union(*[
        FACEMESH_LIPS, FACEMESH_LEFT_EYE, FACEMESH_LEFT_EYEBROW, FACEMESH_RIGHT_EYE,
        FACEMESH_RIGHT_EYEBROW, FACEMESH_FACE_OVAL
    ])



    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            mp_drawing.draw_landmarks(image, results.face_landmarks, lips, 
                                mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=0),
                                mp_drawing.DrawingSpec(color=(80,256,121), thickness=3, circle_radius=0)
                                )
            
            ret,buffer=cv2.imencode('.jpg',image)
            frame=buffer.tobytes()

            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
