import cv2
import pickle
import cvzone
import numpy as np
import os
import pandas as pd
from pandas import DataFrame

path="carParking1/P2.png"
os.makedirs('output1',exist_ok=True)
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 49, 22
def checkParkingSpace(imPro):
    spaceCounter=0
    available_slots=[]
    occupied_slots=[]
    available_count=0
    occupied_count=0
    img_spots=img.copy()
    img_labels=img.copy()


    for i,pos in enumerate(posList):
        x,y = pos
        imgCrop=imPro[y:y+height,x:x+width]
        count =cv2.countNonZero(imgCrop)
        #cvzone.putTextRect(img,str(count),(x,y+height),scale=1,thickness=1,offset=1,colorR=(0,0,255))
        #cv2.putText(img,f'Slot{i+1}',(x+5,(y+height//2)),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,255,255),
                   # 1,cv2.LINE_AA)
        if count<260:
            color =(0,255,0)
            thickness=2
            spaceCounter+=1
            available_count+=1
            label=f'A{available_count}'
            available_slots.append(i+1)

        else:
            color = (0,0,255)
            thickness=1
            occupied_count+=1
            label=f'O{occupied_count}'
            occupied_slots.append(i+1)
        cv2.rectangle(img_spots,pos, (pos[0] + width, pos[1] + height),color, thickness)
        spot=str(i+1)
        (text_w,text_h),_=cv2.getTextSize(spot, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        text_x=x+(width-text_w)//2
        text_y=y+(height+text_h)//2
        cv2.putText(img_spots,spot,(text_x,text_y),cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,color,1,cv2.LINE_AA)
        cv2.putText(img, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1, cv2.LINE_AA)
        cv2.rectangle(img_labels, pos, (pos[0] + width, pos[1] + height), color, thickness)
        (text_w, text_h), _ = cv2.getTextSize(spot, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        text_x = x + (width - text_w) // 2
        text_y = y + (height + text_h) // 2
        cv2.putText(img_labels, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1, cv2.LINE_AA)
        cv2.putText(img, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1, cv2.LINE_AA)
    cvzone.putTextRect(img_labels,f'Total slots:{len(posList)}|'
                           f'Available:{spaceCounter}|'
                       f'occupied:{len(posList)-spaceCounter}', (700, 700),
                       scale=2,thickness=2,offset=5,colorR=(0,255,0))
    cvzone.putTextRect(img_labels, f'A:Available,O:Occupied', (729, 729),
                       scale=2, thickness=2, offset=5, colorR=(0, 255, 0))
    cvzone.putTextRect(img_spots, f'Total slots:{len(posList)}|'
                                   f'Available:{spaceCounter}|'
                                   f'occupied:{len(posList) - spaceCounter}', (700, 700),
                       scale=2, thickness=2, offset=5, colorR=(0, 255, 0))
    summary= {
    'Total Number of Slots':[len(posList)],
    'Occupied Slots': [",".join(map(str, occupied_slots))],
     'Available Slots':[",".join(map(str,available_slots))],
    }
    df = pd.DataFrame(summary)
    df.to_excel('output1/parking_Slot_Details.xlsx',index=False,engine='openpyxl')

    summary ={
        'Total Number of Slots':[len(posList)],
        'Occupied Slots':[len(posList)-spaceCounter],
        'Available Slots':[spaceCounter]
    }
    df = pd.DataFrame(summary)
    df.to_excel('output1/Parking_Summary.xlsx',index=False,engine='openpyxl')
    return img_spots, img_labels

while True:
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5), 1)
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV,27,18)
    imgMedian = cv2.medianBlur(imgThreshold, 3)
    kernel=np.ones((3,3),np.uint8)
    imgdilate = cv2.dilate(imgMedian,kernel,iterations=1)
    img_spots,img_labels=checkParkingSpace(imgdilate)
    cv2.imshow("Parking Spots ordered",img_spots)
    cv2.imshow("Parking Status with Labels",img_labels)
    cv2.waitKey(0)