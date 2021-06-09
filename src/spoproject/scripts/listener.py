#!/usr/bin/env python

import sys
import os
from pydub import AudioSegment
from pydub.playback import play

import rospy
from std_msgs.msg import String

print(os.getcwd())

list_audio = []

def play_chord(n):
    global list_audio
    folder = '/home/radioon/catkin_ws/src/spoproject/scripts/mp3_chords'
    chords = os.listdir(folder)
    file = folder + "/" + chords[n]
    s = AudioSegment.from_mp3(file)
    list_audio.append(s)
    play(s)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + ' OH, I heard %s', data.data)
    n = int(data.data)
    play_chord(n)

def listener():

    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
    sum(list_audio).export('result.mp3', format='mp3')
