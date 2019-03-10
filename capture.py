import cv2,time,pandas
from datetime import datetime

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0)

while True:
    check,frame=video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    #time.sleep(3)
    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]     #image,threshold limit,color for greater than 30,threshold method ,[1] for thresh_binary which tells it its frame
    thresh_frame=cv2.dilate(thresh_frame ,None, iterations=2)     #dilate-for smoothning   if have an array and want process to b sofisticated then pass it here we dont have any so none   iteration-tells how many times u have to go through
                                                                    #image   greater the no greater the smoothning
    (_,cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     #_, for cv2 not in cv3    retriving or drawing external contors or objects that we are finding      approximation method that open cv is applying for
                                                                                                        #contors

    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,x+h),(0,255,0),3)

    status_list.append(status)
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("gray_frame",gray)
    cv2.imshow("Delta_frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color frame",frame)
    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())

        break
print(status_list)
print(times)
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv("Times.csv")


video.release()
cv2.destroyAllWindows()
