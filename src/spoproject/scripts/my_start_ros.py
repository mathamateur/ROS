
bashCommand1 = "python listener.py"
bashCommand2 = "python talker.py"

from subprocess import *

'''
process1 = Popen(bashCommand1.split(),stdin=PIPE, stdout=PIPE)
output, error = process1.communicate(None)

process2 = Popen(bashCommand2.split(),stdin=PIPE, stdout=PIPE)
output, error = process2.communicate(input())
'''

def run(cmd, stdout, stderr):
    return Popen(cmd, stdout=stdout, stderr=stderr, shell=False)
                 #preexec_fn=os.setsid)
    

def start_process(cmd):
    return run(cmd, PIPE, PIPE)


master = start_process(['/opt/ros/noetic/bin/roscore'])

listener_node = start_process(['python', 'listener.py'])

talker_node = start_process(['python', 'talker.py'])

talker_node.communicate()
