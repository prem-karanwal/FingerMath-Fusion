import cv2
import time
import handTrackingModule as htm
import random

wcam, hcam = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0
detector = htm.handDetector(detectionCon=1)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 1280, 720) 

def generate_random_equation():
    operators = ['+', '-', '*']
    num1 = random.randint(0, 5)
    num2 = random.randint(0, 5)
    num3 = random.randint(0, 5)

    operator1 = random.choice(operators)
    operator2 = random.choice(operators)


    equation = f"{num1} {operator1} {num2} {operator2} {num3}"
    result = eval(equation)


    while result < 0 or result > 5 :
        # Ensure the result is within the desired range
        num1 = random.randint(0, 5)
        num2 = random.randint(0, 5)
        num3 = random.randint(0, 5)
        operator1 = random.choice(operators)
        operator2 = random.choice(operators)

        equation = f"{num1} {operator1} {num2} {operator2} {num3}"
        result = eval(equation)

    return equation, result

equation, result = generate_random_equation()

frame_counter = 0
i=0
delay_duration = 30

h=0
corr=0
incorr=0
while True:
    success,img=cap.read()
    img = detector.findHands(img, draw=True )
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)
    tipId=[4,8,12,16,20]
    frame_counter += 1
    i+=1
    if(i<=50):
            cv2.putText(img, "Let's Play A Game ", (120, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 0, 0),2)
        
    elif (i>50 and i<=150):
            cv2.putText(img, "Solve this equation and Use Your Fingers ", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255),1)
            cv2.putText(img, "to show the correct answer ", (50, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255),1)

    
    

    if frame_counter >= delay_duration and i>150:
        frame_counter = 0
        if(len(lmList)!=0 and h<10):
            fingers=[]
            # thumb
            if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):
                    fingers.append(1)
            else :
                    fingers.append(0)
            #4 fingers
            for id in range(1,len(tipId)):
                
                if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):
                    fingers.append(1)
                
                else :
                    fingers.append(0)

            # Detect fingers as you did before

            total_fingers = fingers.count(1)
            cv2.rectangle(img, (20, 255), (100, 350), (0, 255, 0), cv2.FILLED)

            cv2.putText(img, str(total_fingers), (35, 335), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 10)
            
            
            # Check User's Answer
            print(total_fingers, result)
            if total_fingers == result:
                feedback = "Correct!"
                h+=1
                if(h<=10):
                     
                     corr+=1
                     equation, result = generate_random_equation()
                
                     
            else:
                feedback = "Incorrect."
                h+=1
                if(h<=10):
                     incorr+=1
                     equation, result = generate_random_equation()
            print(corr, incorr)
            
                 
    if(h==10):
        cv2.putText(img, f"You Got: {corr} correct and {incorr} incorrect", (130, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9,
                        (255, 255, 255), 1)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

    if(h<10 and i>150):
          cv2.putText(img, f"Equation: {equation}", (120, 130), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 0, 255),1)


    cv2.imshow("image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
