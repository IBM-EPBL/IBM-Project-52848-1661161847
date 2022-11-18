import cv2        
import threading   
import playsound  
from twilio.rest import Client
  

fire_cascade = cv2.CascadeClassifier('fire_detection.xml') 

vid = cv2.VideoCapture(0) 
runOnce = False 
Font = cv2.FONT_HERSHEY_SIMPLEX

def play_alarm_sound_function():
    playsound.playsound('fire_Alarm.mp3',True) 
    print("Fire alarm end") 

def send_Twilio_function(): 
    
    SID = 'AC153cd036f84d1a7a72baf185e662b651'

    Auth_Token = '***************************'

    cl = Client(SID, Auth_Token)

    cl.messages.create(body="Forest Fire Go To Saved Places", from_= '+13605838875',to='+917550155332')

    
		
while(True):
    Alarm_Status = False
    ret, Forest = vid.read() 
    gray = cv2.cvtColor(Forest, cv2.COLOR_BGR2GRAY) 
    fire = fire_cascade.detectMultiScale(Forest, 1.2, 5) 

    
    for (x,y,w,h) in fire:
        cv2.rectangle(Forest,(x-20,y-20),(x+w+20,y+h+20),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = Forest[y:y+h, x:x+w]
	cv2.putText(Forest,"Fire",(x,w),Font,2,(0,0,225),2,cv2.LINE_AA)

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread

        if runOnce == False:
            print("Twilio send initiated")
            threading.Thread(target=send_Twilio_function).start() # To call Twilio thread
            runOnce = True
        if runOnce == True:
            print("Twilio is already sent once")
            runOnce = True

    cv2.imshow('Forest', Forest)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release
cv2.destroyAllWindows    
