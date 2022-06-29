import pyfirmata
from time import sleep
import firebase_admin
from firebase_admin import credentials,db
cred=credentials.Certificate("C:\\Users\\HEMANTH\\Downloads\\face.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://face-recognition-244ed-default-rtdb.firebaseio.com/"})
store=db.reference("/")
port = "COM6"
board=pyfirmata.Arduino(port)
it=pyfirmata.util.Iterator(board)
it.start()
buz=board.get_pin("d:13:o")
count=100
while True:

    data=store.child("person"+str(count)).get()
    print("person"+str(count))
    print(data)
    if(data=="Unknown is entering"):
            buz.write(1)
            sleep(3)
            buz.write(0)
            count=count+1

    else:
            buz.write(0)
            sleep(2)
            buz.write(1)
            sleep(2)
            count += 1