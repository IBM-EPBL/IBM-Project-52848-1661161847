import cv2        
import threading   
import playsound  
import smtplib     

fire_cascade = cv2.CascadeClassifier('train/fire_detection.xml') 

vid = cv2.VideoCapture(0) 
runOnce = False 
Font = cv2.FONT_HERSHEY_SIMPLEX

def play_alarm_sound_function():
    playsound.playsound('music/fire_Alarm.mp3',True) 
    print("Fire alarm end") 

def send_mail_function(): 

    recipientmail = "1916168l@saec.ac.in" 
    recipientmail = recipientmail.lower() 
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("Happyvishvamm@gmail.com", 'zchgwcublcrobkqu') 
        server.sendmail('1916168l@saec.ac.in', recipientmail, "WildFire forest ") 
        print("Alert mail sent sucesfully to {}".format(recipientmail))
        server.close() 
        
    except Exception as e:
        print(e) 
		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) 

    
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
	cv2.putText(frame,"Fire",(x,w),Font,2,(0,0,225),2,cv2.LINE_AA)

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread

        if runOnce == False:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start() # To call Email thread
            runOnce = True
        if runOnce == True:
            print("Mail is already sent once")
            runOnce = True

    cv2.imshow('Forest', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release
cv2.destroyAllWindows    
