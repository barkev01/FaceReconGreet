from time import time
import face_recognition as fr
import numpy as np
import cv2
import os
import Person
import PersonManager
from gtts import gTTS
from playsound import playsound
import time

video_capture = cv2.VideoCapture(0)
pm = PersonManager.PersonManager()
known_persons = []
known_persons_name = []
greet = False

def Text_to_speech(name_to_speak):
    speech = gTTS("Bonjour " + name_to_speak, lang="fr")
    speech.save('./sound/'+name_to_speak+'/'+'Bonjour.mp3')
    playsound('./sound/'+name_to_speak+'/'+'Bonjour.mp3')


for person in os.listdir('./img/'):
    p = Person.Person(person)
    pm.addPerson(p)
    for root_dir, cur_dir, image in os.walk('./img/'+person):
        p.setList(image)

for pers in pm.getList():
    for img in pers.get_list():
        image = fr.load_image_file('./img/'+pers.get_name()+'/'+img)
        if(len(fr.face_encodings(image))==1):
            known_persons.append((fr.face_encodings(image))[0])
            known_persons_name.append(pers.get_name())

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


while True:
    ret, frame = video_capture.read()

    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = fr.face_locations(rgb_small_frame)
        face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

        face_names = []

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(known_persons, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = fr.face_distance(known_persons, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_persons_name[best_match_index]
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    t = int(time.strftime('%S',time.localtime()))
    if( t%5 == 0 ):
        for names in face_names:
                
            Text_to_speech(names)

    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()