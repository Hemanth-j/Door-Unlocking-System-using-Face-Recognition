from imutils import paths
import face_recognition
import pickle
import cv2
import os
import firebase_admin
from firebase_admin import credentials,db

cred = credentials.Certificate("C:\\Users\\HEMANTH\\Downloads\\face.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://face-recognition-244ed-default-rtdb.firebaseio.com/"})
store=db.reference("/")
image_path=list(paths.list_images("C:\\Users\\HEMANTH\\Downloads\\face recongnition\\cropped1"))
knownEncodings=[]
knownnames=[]
for (i,image_path) in enumerate(image_path):
    name=image_path.split(os.path.sep)[-2]
    image=cv2.imread(image_path)
    rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    boxes=face_recognition.face_locations(rgb,model="hog")
    encodings=face_recognition.face_encodings(rgb,boxes)
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownnames.append(name)
data={"encodings":knownEncodings,"names":knownnames}
f=open("face_enc","wb")
f.write(pickle.dumps(data))
f.close()

import time
cascPath="C:\\Users\\HEMANTH\\Downloads\\haarcascade_frontalface_default.xml"
faceCascade=cv2.CascadeClassifier(cascPath)
data=pickle.loads(open("face_enc","rb").read())
print("streaming started")
video_capture=cv2.VideoCapture(0)
count=1
while True:
    ret,frame=video_capture.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(60,60),flags=cv2.CASCADE_SCALE_IMAGE)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    encodings=face_recognition.face_encodings(rgb)
    names=[]
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"],encoding)
        name="Unknown"
        if True in matches:
            matchedIdxs=[i for (i,b) in enumerate(matches) if b]
            counts={}
            for i in matchedIdxs:
                name=data["names"][i]
                counts[name]=counts.get(name,0)+1
            name=max(counts,key=counts.get)
        names.append(name)
        for ((x,y,w,h),name) in zip(faces,names):
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,name,(x,y),cv2.FONT_HERSHEY_SIMPLEX,
              0.75, (0,255,0),2)

    cv2.imshow("frame",frame)

    if (name=="Unknown"):
        store.update({"person":"Unknown"})
    else:
        store.update({"person"+str(count): str(name)})
    count+=1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
video_capture.release()
cv2.destroyAllWindows()