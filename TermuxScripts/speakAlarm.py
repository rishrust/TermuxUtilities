from datetime import datetime;
from time import sleep
import os
debug = False 


def sleep_till_correct_time(minutes):
    NEAR_TIME = 3
    QUICK_SLEEP= 30
    if(minutes < 30):
        if 30-minutes>=NEAR_TIME:
            if(debug):
                print("going to sleep fo ", 30-minutes)
            sleep((30-minutes)*60)
        else:
            if(debug):
                print("chome time is near")
                sleep(QUICK_SLEEP)
    else:
        if 60-minutes>=NEAR_TIME:
            if(debug):
                print("going to sleep fo ", 60-minutes)
            sleep((60-minutes)*60)
        else:
            if(debug):
                print("chome time is near")
                sleep(QUICK_SLEEP)






def termux_speak(message):
    command = "termux-tts-speak "+ message
    os.system(command)


def termux_play_chime(hour,minutes):
    file_path = ""
    if(hour >= 17):
        file_path+= "evening_chime.mp3"
    else:
        file_path += "day_chime.mp3"

    command = f"play  {file_path}"
    os.system(command)
    sleep(2)






CUSTOM_MESSAGE = {
    "8:0": "Good Morning! Start your day with a great breakfast.",
    "13:30": "Good Afternoon! Time to recharge with a delicious lunch.",
    "16:0": "Good Evening! A light snack sounds perfect right now.",
    "19:30": "Dinner time! Relax and enjoy your meal.",
    "23:30": "Time to wrap up the day and get some rest."
}

while 1: 
    current_time = str(datetime.now()).split()
    current_time = current_time[1].split(':')

    hour = int(current_time[0])
    minutes = int(current_time[1])
    sec = current_time[2]



    if(debug):
        hour = 23
        minutes = 30

    
    if(debug):
        print("current time is ", current_time)
    
    
    
    
    # bajajo y nhi
    if(hour>=0 and hour < 8 ):
        if(debug):
            print("It is meidnight")
        sleep_till_correct_time(minutes)
    elif minutes == 30 or minutes == 0:
        termux_play_chime(hour,minutes)
        message = ""
        if(hour==12):
            message=  "It is "+ str(hour)+" " +str(minutes) + " PM"

        elif(hour>12):
            message=  "It is "+ str(hour-12)+ " "+str(minutes) + " PM"

        else:
            message=  "It is "+ str(hour)+ " "+ str(minutes) + " A M"
        
        if(debug):
            print(message)
        termux_speak(message)
        
        # check for cutom message
        if str(hour)+':'+str(minutes) in CUSTOM_MESSAGE:
            termux_speak(CUSTOM_MESSAGE[str(hour)+':'+str(minutes)])
        if(debug):
            print("Going to sleep for 30 minutes")
        sleep(1800)


    else:
        sleep_till_correct_time(minutes)

