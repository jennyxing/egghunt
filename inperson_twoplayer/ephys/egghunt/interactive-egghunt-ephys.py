#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.1.2),
    on February 03, 2023, at 11:00
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

import psychopy
psychopy.useVersion('2022.1.2')


from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

agent1_score = 0
agent2_score = 0
import pandas as pd, numpy as np

coord_df = pd.read_csv('C:\\Users\\Kevin\\Desktop\\EGGHUNT\\egghunttask\\coord_key.csv')

def convert_coords(in_x, in_y, revert=False, agent='computer'):
    # input true coords (e.g., [.15, 0])
    # output possible moves and grid coords
    if agent == 'computer':
        
        if revert:
            out_x = coord_df[coord_df['x']==in_x][coord_df['y']==in_y]['true_x'].iloc[0]
            out_y = coord_df[coord_df['y']==in_y][coord_df['x']==in_x]['true_y'].iloc[0]
            possiblemoves = list(coord_df[coord_df['y']==in_y][coord_df['x']==in_x]['possiblemovescomp'].iloc[0].split(";"))
        else:
            out_x = coord_df[coord_df['true_x']==in_x][coord_df['true_y']==in_y]['x'].iloc[0]
            out_y = coord_df[coord_df['true_y']==in_y][coord_df['true_x']==in_x]['y'].iloc[0]
            possiblemoves = list(coord_df[coord_df['true_y']==in_y][coord_df['true_x']==in_x]['possiblemovescomp'].iloc[0].split(";"))
        
    elif agent == 'player1':
        if revert:
            out_x = coord_df[coord_df['x']==in_x][coord_df['y']==in_y]['true_x'].iloc[0]
            out_y = coord_df[coord_df['y']==in_y][coord_df['x']==in_x]['true_y'].iloc[0]
            possiblemoves = list(coord_df[coord_df['y']==in_y][coord_df['x']==in_x]['possiblemoves1'].iloc[0].split(";"))
        else:
            out_x = coord_df[coord_df['true_x']==in_x][coord_df['true_y']==in_y]['x'].iloc[0]
            out_y = coord_df[coord_df['true_y']==in_y][coord_df['true_x']==in_x]['y'].iloc[0]
            possiblemoves = list(coord_df[coord_df['true_y']==in_y][coord_df['true_x']==in_x]['possiblemoves1'].iloc[0].split(";"))
    
    elif agent == 'player2':
        if revert:
            out_x = coord_df[coord_df['x']==in_x][coord_df['y']==in_y]['true_x'].iloc[0]
            out_y = coord_df[coord_df['y']==in_y][coord_df['x']==in_x]['true_y'].iloc[0]
            possiblemoves = list(coord_df[coord_df['y']==in_y][coord_df['x']==in_x]['possiblemoves2'].iloc[0].split(";"))
        else:
            out_x = coord_df[coord_df['true_x']==in_x][coord_df['true_y']==in_y]['x'].iloc[0]
            out_y = coord_df[coord_df['true_y']==in_y][coord_df['true_x']==in_x]['y'].iloc[0]
            possiblemoves = list(coord_df[coord_df['true_y']==in_y][coord_df['true_x']==in_x]['possiblemoves2'].iloc[0].split(";"))
        
    return out_x, out_y, possiblemoves

def convert_moves(next_move, revert=False):
    # converts string (e.g., 'left') to position (e.g., -.15)
    if revert:
        if next_move == 'left' or next_move == 'num_4' or next_move == 'h':
            x_shift = -1
            y_shift = 0
        elif next_move == 'right' or next_move == 'num_6' or next_move == 'k':
            x_shift = 1
            y_shift = 0
        elif next_move == 'up' or next_move == 'num_8' or next_move == 'u':
            y_shift = 1
            x_shift = 0
        elif next_move == 'down' or next_move == 'num_2' or next_move == 'n':
            y_shift = -1
            x_shift = 0
        elif next_move == 'space' or next_move == 'num_5' or next_move == 'j':
            y_shift = 0
            x_shift = 0

    else:
        if next_move == 'left' or next_move == 'num_4' or next_move == 'h':
            x_shift = -.15
            y_shift = 0
        elif next_move == 'right' or next_move == 'num_6' or next_move == 'k':
            x_shift = .15
            y_shift = 0
        elif next_move == 'up' or next_move == 'num_8' or next_move == 'u':
            y_shift = .15
            x_shift = 0
        elif next_move == 'down' or next_move == 'num_2' or next_move == 'n':
            y_shift = -.15
            x_shift = 0
        elif next_move == 'space' or next_move == 'num_5' or next_move == 'j':
            y_shift = 0
            x_shift = 0
    
    return x_shift, y_shift

def get_adjacent_tiles(stag_x, stag_y):
    # input stag coords, output list of adjacent coords
    grid_x, grid_y, possiblemoves = convert_coords(stag_x, stag_y)

    adjacent_spaces = []
    for move in possiblemoves:
        x_shift, y_shift = convert_moves(move)
        adjacent_spaces += [[stag_x+x_shift, stag_y+y_shift]]
    
    return adjacent_spaces
def maximize_chick_distance(agent0_pos, agent1_pos, agent2_pos, possiblemoves, use_nsteps=True):
    max_distance = 0
    best_move = None
    
    move_dict = {'left': (-.15, 0), 
                 'right': (.15, 0), 
                 'up': (0, .15), 
                 'down': (0, -.15), 
                 'space': (0, 0)}
    
    new_possible_moves = []
    for move in possiblemoves: 
        if use_nsteps: # Manhattan distance to move according to number of steps
            distance1 = abs(agent0_pos[0] + move_dict[move][0] - agent1_pos[0]) + abs(agent0_pos[1] + move_dict[move][1] - agent1_pos[1]) 
            distance2 = abs(agent0_pos[0] + move_dict[move][0] - agent2_pos[0]) + abs(agent0_pos[1] + move_dict[move][1] - agent2_pos[1])
            distance = np.round(distance1 + distance2, 4)

        else: #Euclidean distance
            distance1 = ((agent0_pos[0] + move_dict[move][0] - agent1_pos[0]) ** 2 + (agent0_pos[1] + move_dict[move][1] - agent1_pos[1]) ** 2) ** 0.5 
            distance2 = ((agent0_pos[0] + move_dict[move][0] - agent2_pos[0]) ** 2 + (agent0_pos[1] + move_dict[move][1] - agent2_pos[1]) ** 2) ** 0.5
            distance = np.round(distance1 + distance2, 4)

        print(move, distance1, distance2, distance)

        # if move maximizes distance, then store
        # moves to maximize distance if the move does not place chicken next to agent
        # if multiple moves are equal in distance, then chooses randomly among them
        
        if max_distance == 0:
            first_move_in_list, first_dist_in_list = move, distance

        if distance1 > .15 and distance2 > .15:
            if distance >= max_distance:
                if distance == max_distance or max_distance == 0:
                    # how to choose if all dists are equal:
                    if move == 'space':
                        if distance1 < .15 or distance2 < .15:
                            continue
                        else:
                            new_possible_moves.append(move)

                    else: 
                        if max_distance == 0:
                            max_distance = distance
                            best_move = move
                        else:
                            new_possible_moves.append(move)
                else:
                    max_distance = distance
                    best_move = move

    if first_dist_in_list == max_distance:
        new_possible_moves.append(first_move_in_list)

    if len(new_possible_moves) > 0:
        best_move = np.random.choice(new_possible_moves)
    
    if best_move is None:
        best_move = 'space'
        
    print(new_possible_moves)
    print(best_move)
            
    return best_move


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.1.2'
expName = 'egghunt'  # from the Builder filename that created this script
expInfo = {'player1': '', 'player1av': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 'player2': '', 'player2av': [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/sub1-%s_sub2-%s_task-%s_%s' % (expInfo['player1'], expInfo['player2'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Kevin\\Desktop\\EGGHUNT\\egghunttask\\interactive-egghunt-ephys.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# Setup ioHub
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# Initialize components for Routine "start_exp"
start_expClock = core.Clock()
# --- Initialize components for "GridWorld" ---
b_0_2 = visual.Rect(
    win=win, name='b_0_2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(0, .3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_0_1 = visual.Rect(
    win=win, name='b_0_1',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(0, .15), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_3_0 = visual.Rect(
    win=win, name='b_3_0',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.45, 0), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_2_2 = visual.Rect(
    win=win, name='b_2_2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.3, .3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_1_2 = visual.Rect(
    win=win, name='b_1_2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.15, .3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_2_1 = visual.Rect(
    win=win, name='b_2_1',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.3, .15), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_2_neg1 = visual.Rect(
    win=win, name='b_2_neg1',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.3, -.15), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_2_neg2 = visual.Rect(
    win=win, name='b_2_neg2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.3, -.3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_2_0 = visual.Rect(
    win=win, name='b_2_0',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.3, 0), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_1_neg2 = visual.Rect(
    win=win, name='b_1_neg2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.15, -.3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_1_0 = visual.Rect(
    win=win, name='b_1_0',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(.15, 0), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_0_0 = visual.Rect(
    win=win, name='b_0_0',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(0, 0), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg1_0 = visual.Rect(
    win=win, name='b_neg1_0',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.15, 0), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg1_2 = visual.Rect(
    win=win, name='b_neg1_2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.15, .3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg1_neg2 = visual.Rect(
    win=win, name='b_neg1_neg2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.15, -.3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg2_0 = visual.Rect(
    win=win, name='b_neg2_0',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.3, 0), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg2_1 = visual.Rect(
    win=win, name='b_neg2_1',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.3, .15), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg2_neg1 = visual.Rect(
    win=win, name='b_neg2_neg1',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.3, -.15), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg2_neg2 = visual.Rect(
    win=win, name='b_neg2_neg2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.3, -.3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg2_2 = visual.Rect(
    win=win, name='b_neg2_2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.3, .3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_neg3_0 = visual.Rect(
    win=win, name='b_neg3_0',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(-.45, 0), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_0_neg1 = visual.Rect(
    win=win, name='b_0_neg1',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(0, -.15), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)
b_0_neg2 = visual.Rect(
    win=win, name='b_0_neg2',
    width=(0.15, 0.15)[0], height=(0.15, 0.15)[1],
    ori=0.0, pos=(0, -.3), anchor='center', autoDraw=True,
    lineWidth=5.0,     colorSpace='rgb',  lineColor='black', fillColor='white',
    opacity=None, depth=-2.0, interpolate=True)

egg_left = visual.ImageStim(
    win=win,
    name='egg_left', 
    image='stimuli/egg.png', mask=None, anchor='center',
    ori=0.0, pos=(-.45, 0), size=(0.06, 0.06), #autoDraw=True,
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False, depth=-3.0)
egg_left.setAutoDraw(True)

egg_right = visual.ImageStim(
    win=win,
    name='egg_right', 
    image='stimuli/egg.png', mask=None, anchor='center',
    ori=0.0, pos=(.45, 0), size=(0.06, 0.06), #autoDraw=True,
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False, depth=-3.0)
egg_right.setAutoDraw(True)

#rabbit_left = visual.Rect(
#    win=win, name='rabbit_left',
#    width=(0.05, 0.05)[0], height=(0.05, 0.05)[1],
#    ori=0.0, pos=(-.45, 0), anchor='center', autoDraw=True,
#    lineWidth=1.0,     colorSpace='rgb',  lineColor='blue', fillColor='yellow',
#    opacity=None, depth=-3.0, interpolate=True)
#rabbit_right = visual.Rect(
#    win=win, name='rabbit_right',
#    width=(0.05, 0.05)[0], height=(0.05, 0.05)[1],
#    ori=0.0, pos=(.45, 0), anchor='center', autoDraw=True,
#    lineWidth=1.0,     colorSpace='rgb',  lineColor='blue', fillColor='yellow',
#    opacity=None, depth=-3.0, interpolate=True)
avatar1_no = expInfo['player1av']
agent1_imgs = {'stay':f'stimuli/avatars/avatar-{avatar1_no}_down.png',
               'up':f'stimuli/avatars/avatar-{avatar1_no}_up.png',
               'down':f'stimuli/avatars/avatar-{avatar1_no}_down.png',
               'left':f'stimuli/avatars/avatar-{avatar1_no}_left.png',
               'right':f'stimuli/avatars/avatar-{avatar1_no}_right.png'}
avatar2_no = expInfo['player2av']
agent2_imgs = {'stay':f'stimuli/avatars/avatar-{avatar2_no}_down.png',
               'up':f'stimuli/avatars/avatar-{avatar2_no}_up.png',
               'down':f'stimuli/avatars/avatar-{avatar2_no}_down.png',
               'left':f'stimuli/avatars/avatar-{avatar2_no}_left.png',
               'right':f'stimuli/avatars/avatar-{avatar2_no}_right.png'}

agent1 = visual.ImageStim(
    win=win,
    name='agent1', 
    image=agent1_imgs['down'], mask=None, anchor='center',
    ori=0.0, pos=[-.3,-.3], size=(0.1, 0.1), #autoDraw=True,
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False, depth=-10.0)

agent2 = visual.ImageStim(
    win=win,
    name='agent2', 
    image=agent2_imgs['down'], mask=None, anchor='center',
    ori=0.0, pos=[.3,.3], size=(0.1, 0.1), #autoDraw=True,
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False, depth=-10.0)


#agent_stims = ['stimuli/player-pink.png', 'stimuli/player-yellow.png','stimuli/player-pink.png', 'stimuli/player-yellow.png']
#agents_imgs = list(np.random.permutation(agent_stim))

#agent1 = visual.ShapeStim(
#    win=win, name='agent1',
#    size=(0.1, 0.1), vertices='circle',
#    ori=0.0, pos=agent1_pos, anchor='center', autoDraw=True,
#    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='red',
#    opacity=None, depth=-5.0, interpolate=True)
#agent2 = visual.ShapeStim(
#    win=win, name='agent2',
#    size=(0.1, 0.1), vertices='circle',
#    ori=0.0, pos=agent2_pos, anchor='center', autoDraw=True,
#    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='blue',
#    opacity=None, depth=-5.0, interpolate=True)

#
nchicks = 1 #int(expInfo['nchicks'])

chick1_pos = [0., 0.]
chick2_pos = [0., 0.]
chick3_pos = [0., 0.]

#chick_stim = ['stimuli/chick-green.png', 'stimuli/chick-blue.png', 'stimuli/chick-red.png']
#chick1_img, chick2_img, chick3_img = np.random.permutation(chick_stim)
chick1_imgs = {'stay':f'stimuli/chicken_down.png',
               'up':f'stimuli/chicken_up.png',
               'down':f'stimuli/chicken_down.png',
               'left':f'stimuli/chicken_left.png',
               'right':f'stimuli/chicken_right.png'}

chick1 = visual.ImageStim(
    win=win,
    name='chick1', 
    image=chick1_imgs['down'], mask=None, anchor='center',
    ori=0.0, pos=chick1_pos, size=(0.09, 0.09), #autoDraw=True,
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False, depth=-2.0)
chick1.setAutoDraw(True)

#if nchicks >= 2:
#    chick2 = visual.ImageStim(
#    win=win,
#    name='chick2', 
#    image=chick2_img, mask=None, anchor='center',
#    ori=0.0, pos=chick2_pos, size=(0.1, 0.1), #autoDraw=True,
#    color=[1,1,1], colorSpace='rgb', opacity=None,
#    flipHoriz=False, flipVert=False,
#    texRes=128.0, interpolate=False, depth=-2.0)
#    chick2.setAutoDraw(True)
#
#if nchicks >= 3:
#    chick3 = visual.ImageStim(
#    win=win,
#    name='chick3', 
#    image=chick3_img, mask=None, anchor='center',
#    ori=0.0, pos=chick3_pos, size=(0.1, 0.1), #autoDraw=True,
#    color=[1,1,1], colorSpace='rgb', opacity=None,
#    flipHoriz=False, flipVert=False,
#    texRes=128.0, interpolate=False, depth=-2.0)
#    chick3.setAutoDraw(True)
#
#stag = visual.Rect(
#    win=win, name='stag',
#    width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
#    ori=0.0, pos=stag1_pos, anchor='center', autoDraw=True,
#    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='yellow',
#    opacity=None, depth=-2.0, interpolate=True)
#if (expInfo['interact'] == 'y') or (expInfo['interact'] == 'yes') or (expInfo['interact'] == '1'):
#    interaction_bool = 1
#    nointeraction_bool = 0
#    print('interacting...')
    
interaction_bool = 1
nointeraction_bool = 0
print('interacting...')
#if int(expInfo['player2']) == 3987:
#    interaction_bool = 0
#    nointeraction_bool = 1
#    print('NOT interacting...')
#else:
#    interaction_bool = 1
#    nointeraction_bool = 0
#    print('interacting...')
win.mouseVisible = False
diode_square_white = visual.Rect(
    win=win, name='diode_square_white',units='norm', 
    width=(.45,.45)[0], height=(.45,.45)[1],
    ori=0.0, pos=(-1,-1), anchor='bottom-center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='white',
    opacity=None, depth=-5.0, interpolate=True)

# Initialize components for Routine "start_1"
start_1Clock = core.Clock()
start_instr_1 = visual.TextStim(win=win, name='start_instr_1',
    text='~EGG HUNT~\n\nIn this game, you and another player will aim to collect as many eggs as you can to earn points!\n\nOn each round, both of you will start with 150 points. 10 points will be subtracted for every turn taken. For example, 50 points will be subtracted from your score if you take 5 turns to end the round. The round will end once you or the other player collects an egg (worth 100 points each) or both of you cooperate to catch the chicken (worth 400 points total, or 200 points to each player). Keep in mind that rounds can end if players take too long to collect eggs or catch the chicken. You can collect an egg by moving to a space with an egg. You can catch the chicken if you and the other player move to spaces that are next to the chicken. On your turn, you will stay in the same position if you press the corresponding key or if you do not select a move in 6 seconds.\n\nThese points will be tallied at the end of the study and converted to real money for each of the players. Have fun!',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
instr_resp_1 = keyboard.Keyboard()
start_egg = visual.ImageStim(
    win=win,
    name='start_egg', 
    image='stimuli/egg.png', mask=None, anchor='center',
    ori=0.0, pos=(-0.175, 0.325), size=(0.075, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
start_chicken = visual.ImageStim(
    win=win,
    name='start_chicken', 
    image='stimuli/chicken_down.png', mask=None, anchor='center',
    ori=0.0, pos=(0.175, 0.325), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)

# Initialize components for Routine "get_ready"
get_readyClock = core.Clock()
start_exp_key = keyboard.Keyboard()
get_ready_disp = visual.TextStim(win=win, name='get_ready_disp',
    text='Get ready...',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "p1_confirm"
p1_confirmClock = core.Clock()
p1_ready = visual.TextStim(win=win, name='p1_ready',
    text='PLAYER 1\nAre you ready to begin the next round?',
    font='Open Sans',
    pos=(0, .15), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
diode_p1_ready = visual.Rect(
    win=win, name='diode_p1_ready',units='norm', 
    width=(.45,.45)[0], height=(.45,.45)[1],
    ori=0.0, pos=(-1,-1), anchor='bottom-center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)
player1_ready_display = visual.ImageStim(
    win=win,
    name='player1_ready_display', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
p1_ready_resp = keyboard.Keyboard()
movement_key_text1 = visual.TextStim(win=win, name='movement_key_text1',
    text='Press any movement key to continue',
    font='Open Sans',
    pos=(0, -.15), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
display_pct_txt = visual.TextStim(win=win, name='display_pct_txt',
    text='',
    font='Open Sans',
    pos=(.5, -.4), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);

# Initialize components for Routine "p2_confirm"
p2_confirmClock = core.Clock()
p2_ready = visual.TextStim(win=win, name='p2_ready',
    text='PLAYER 2\nAre you ready to begin the next round?',
    font='Open Sans',
    pos=(0, .15), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
diode_p2_ready = visual.Rect(
    win=win, name='diode_p2_ready',units='norm', 
    width=(.45,.45)[0], height=(.45,.45)[1],
    ori=0.0, pos=(-1,-1), anchor='bottom-center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)
player2_ready_display = visual.ImageStim(
    win=win,
    name='player2_ready_display', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
p2_ready_resp = keyboard.Keyboard()
movement_key_text2 = visual.TextStim(win=win, name='movement_key_text2',
    text='Press any movement key to continue',
    font='Open Sans',
    pos=(0, -.15), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
display_pct_txt_2 = visual.TextStim(win=win, name='display_pct_txt_2',
    text='',
    font='Open Sans',
    pos=(.5, -.4), height=0.02, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);

# Initialize components for Routine "start_round"
start_roundClock = core.Clock()
agent1_indicator_text = visual.TextStim(win=win, 
    name='agent1_indicator_text',
    text='\n\n\n\n\n\n\nPLAYER 1',
    font='Open Sans',
    pos=[0,0], 
    height=0.0145, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-20.0);
agent2_indicator_text = visual.TextStim(win=win, 
    name='agent2_indicator_text',
    text='\n\n\n\n\n\n\nPLAYER 2',
    font='Open Sans',
    pos=[0,0], 
    height=0.0145, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-20.0);
agent1_indicator_text.bold = True
agent2_indicator_text.bold = True

agent1_indicator_text.setAutoDraw(False)
agent2_indicator_text.setAutoDraw(False)
start_round_txt = visual.TextStim(win=win, name='start_round_txt',
    text='',
    font='Open Sans',
    pos=(0, .15), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
diode_square_round_start = visual.Rect(
    win=win, name='diode_square_round_start',units='norm', 
    width=(.45,.45)[0], height=(.45,.45)[1],
    ori=0.0, pos=(-1,-1), anchor='bottom-center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='black',
    opacity=None, depth=-5.0, interpolate=True)
start_round_player_display = visual.ImageStim(
    win=win,
    name='start_round_player_display', 
    image='sin', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)

# Initialize components for Routine "move_chick1"
move_chick1Clock = core.Clock()
if nchicks > 1:
    chick1_instr_txt = 'CHICKEN 1 TURN'
else:
    chick1_instr_txt = 'CHICKEN TURN'

instr_chick = visual.TextStim(win=win, name='instr_chick',
    text=chick1_instr_txt,
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "move_agent1"
move_agent1Clock = core.Clock()
resp_agent1 = keyboard.Keyboard()
instr_agent1 = visual.TextStim(win=win, name='instr_agent1',
    text='PLAYER 1 TURN',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "move_agent2"
move_agent2Clock = core.Clock()
resp_agent2 = keyboard.Keyboard()
instr_agent2 = visual.TextStim(win=win, name='instr_agent2',
    text='PLAYER 2 TURN',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "move_agent2"
move_agent2Clock = core.Clock()
resp_agent2 = keyboard.Keyboard()
instr_agent2 = visual.TextStim(win=win, name='instr_agent2',
    text='PLAYER 2 TURN',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "move_agent1"
move_agent1Clock = core.Clock()
resp_agent1 = keyboard.Keyboard()
instr_agent1 = visual.TextStim(win=win, name='instr_agent1',
    text='PLAYER 1 TURN',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "end_turns"
end_turnsClock = core.Clock()

# Initialize components for Routine "end_round"
end_roundClock = core.Clock()
end_text = visual.TextStim(win=win, name='end_text',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
diode_square = visual.Rect(
    win=win, name='diode_square',units='norm', 
    width=(.45,.45)[0], height=(.45,.45)[1],
    ori=0.0, pos=(-1,-1), anchor='bottom-center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='black',
    opacity=None, depth=-3.0, interpolate=True)

# Initialize components for Routine "end_game"
end_gameClock = core.Clock()
thanks = visual.TextStim(win=win, name='thanks',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
end_resp = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "start_exp"-------
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
start_expComponents = []
for thisComponent in start_expComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
start_expClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "start_exp"-------
while continueRoutine:
    # get current time
    t = start_expClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=start_expClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in start_expComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "start_exp"-------
for thisComponent in start_expComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "start_exp" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "start_1"-------
continueRoutine = True
# update component parameters for each repeat
instr_resp_1.keys = []
instr_resp_1.rt = []
_instr_resp_1_allKeys = []
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

AgentsComponents = [chick1] #agent1, agent2, 
if nchicks >= 2:
    AgentsComponents += [chick2]

if nchicks >= 3:
    AgentsComponents += [chick3]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# keep track of which components have finished
start_1Components = [start_instr_1, instr_resp_1, start_egg, start_chicken]
for thisComponent in start_1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
start_1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "start_1"-------
while continueRoutine:
    # get current time
    t = start_1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=start_1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *start_instr_1* updates
    if start_instr_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_instr_1.frameNStart = frameN  # exact frame index
        start_instr_1.tStart = t  # local t and not account for scr refresh
        start_instr_1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_instr_1, 'tStartRefresh')  # time at next scr refresh
        start_instr_1.setAutoDraw(True)
    
    # *instr_resp_1* updates
    waitOnFlip = False
    if instr_resp_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instr_resp_1.frameNStart = frameN  # exact frame index
        instr_resp_1.tStart = t  # local t and not account for scr refresh
        instr_resp_1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instr_resp_1, 'tStartRefresh')  # time at next scr refresh
        instr_resp_1.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(instr_resp_1.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(instr_resp_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if instr_resp_1.status == STARTED and not waitOnFlip:
        theseKeys = instr_resp_1.getKeys(keyList=None, waitRelease=False)
        _instr_resp_1_allKeys.extend(theseKeys)
        if len(_instr_resp_1_allKeys):
            instr_resp_1.keys = _instr_resp_1_allKeys[-1].name  # just the last key pressed
            instr_resp_1.rt = _instr_resp_1_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *start_egg* updates
    if start_egg.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_egg.frameNStart = frameN  # exact frame index
        start_egg.tStart = t  # local t and not account for scr refresh
        start_egg.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_egg, 'tStartRefresh')  # time at next scr refresh
        start_egg.setAutoDraw(True)
    
    # *start_chicken* updates
    if start_chicken.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_chicken.frameNStart = frameN  # exact frame index
        start_chicken.tStart = t  # local t and not account for scr refresh
        start_chicken.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_chicken, 'tStartRefresh')  # time at next scr refresh
        start_chicken.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in start_1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "start_1"-------
for thisComponent in start_1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('start_instr_1.started', start_instr_1.tStartRefresh)
thisExp.addData('start_instr_1.stopped', start_instr_1.tStopRefresh)
# check responses
if instr_resp_1.keys in ['', [], None]:  # No response was made
    instr_resp_1.keys = None
thisExp.addData('instr_resp_1.keys',instr_resp_1.keys)
if instr_resp_1.keys != None:  # we had a response
    thisExp.addData('instr_resp_1.rt', instr_resp_1.rt)
thisExp.addData('instr_resp_1.started', instr_resp_1.tStartRefresh)
thisExp.addData('instr_resp_1.stopped', instr_resp_1.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('start_egg.started', start_egg.tStartRefresh)
thisExp.addData('start_egg.stopped', start_egg.tStopRefresh)
thisExp.addData('start_chicken.started', start_chicken.tStartRefresh)
thisExp.addData('start_chicken.stopped', start_chicken.tStopRefresh)
# the Routine "start_1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "get_ready"-------
continueRoutine = True
# update component parameters for each repeat
start_exp_key.keys = []
start_exp_key.rt = []
_start_exp_key_allKeys = []
RoundCount = -1
# keep track of which components have finished
get_readyComponents = [start_exp_key, get_ready_disp]
for thisComponent in get_readyComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
get_readyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "get_ready"-------
while continueRoutine:
    # get current time
    t = get_readyClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=get_readyClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *start_exp_key* updates
    waitOnFlip = False
    if start_exp_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_exp_key.frameNStart = frameN  # exact frame index
        start_exp_key.tStart = t  # local t and not account for scr refresh
        start_exp_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_exp_key, 'tStartRefresh')  # time at next scr refresh
        start_exp_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(start_exp_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(start_exp_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if start_exp_key.status == STARTED and not waitOnFlip:
        theseKeys = start_exp_key.getKeys(keyList=['equal'], waitRelease=False)
        _start_exp_key_allKeys.extend(theseKeys)
        if len(_start_exp_key_allKeys):
            start_exp_key.keys = _start_exp_key_allKeys[-1].name  # just the last key pressed
            start_exp_key.rt = _start_exp_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *get_ready_disp* updates
    if get_ready_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        get_ready_disp.frameNStart = frameN  # exact frame index
        get_ready_disp.tStart = t  # local t and not account for scr refresh
        get_ready_disp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(get_ready_disp, 'tStartRefresh')  # time at next scr refresh
        get_ready_disp.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in get_readyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "get_ready"-------
for thisComponent in get_readyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if start_exp_key.keys in ['', [], None]:  # No response was made
    start_exp_key.keys = None
thisExp.addData('start_exp_key.keys',start_exp_key.keys)
if start_exp_key.keys != None:  # we had a response
    thisExp.addData('start_exp_key.rt', start_exp_key.rt)
thisExp.addData('start_exp_key.started', start_exp_key.tStartRefresh)
thisExp.addData('start_exp_key.stopped', start_exp_key.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('get_ready_disp.started', get_ready_disp.tStartRefresh)
thisExp.addData('get_ready_disp.stopped', get_ready_disp.tStopRefresh)
trigger_time = globalClock.getTime()
thisExp.addData('trigger_onset', trigger_time)
# the Routine "get_ready" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
rounds = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('rounds.xlsx'),
    seed=None, name='rounds')
thisExp.addLoop(rounds)  # add the loop to the experiment
thisRound = rounds.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisRound.rgb)
if thisRound != None:
    for paramName in thisRound:
        exec('{} = thisRound[paramName]'.format(paramName))

for thisRound in rounds:
    currentLoop = rounds
    # abbreviate parameter names if possible (e.g. rgb = thisRound.rgb)
    if thisRound != None:
        for paramName in thisRound:
            exec('{} = thisRound[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "p1_confirm"-------
    continueRoutine = True
    # update component parameters for each repeat
    player1_ready_display.setImage(agent1_imgs['stay'])
    p1_ready_resp.keys = []
    p1_ready_resp.rt = []
    _p1_ready_resp_allKeys = []
    RoundCount += 1
    display_percent_complete = f'{np.round(RoundCount*100/32,1)}% complete'
    display_pct_txt.setText(display_percent_complete)
    # keep track of which components have finished
    p1_confirmComponents = [p1_ready, diode_p1_ready, player1_ready_display, p1_ready_resp, movement_key_text1, display_pct_txt]
    for thisComponent in p1_confirmComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    p1_confirmClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "p1_confirm"-------
    while continueRoutine:
        # get current time
        t = p1_confirmClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=p1_confirmClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *p1_ready* updates
        if p1_ready.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            p1_ready.frameNStart = frameN  # exact frame index
            p1_ready.tStart = t  # local t and not account for scr refresh
            p1_ready.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p1_ready, 'tStartRefresh')  # time at next scr refresh
            p1_ready.setAutoDraw(True)
        
        # *diode_p1_ready* updates
        if diode_p1_ready.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            diode_p1_ready.frameNStart = frameN  # exact frame index
            diode_p1_ready.tStart = t  # local t and not account for scr refresh
            diode_p1_ready.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(diode_p1_ready, 'tStartRefresh')  # time at next scr refresh
            diode_p1_ready.setAutoDraw(True)
        
        # *player1_ready_display* updates
        if player1_ready_display.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            player1_ready_display.frameNStart = frameN  # exact frame index
            player1_ready_display.tStart = t  # local t and not account for scr refresh
            player1_ready_display.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(player1_ready_display, 'tStartRefresh')  # time at next scr refresh
            player1_ready_display.setAutoDraw(True)
        
        # *p1_ready_resp* updates
        waitOnFlip = False
        if p1_ready_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            p1_ready_resp.frameNStart = frameN  # exact frame index
            p1_ready_resp.tStart = t  # local t and not account for scr refresh
            p1_ready_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p1_ready_resp, 'tStartRefresh')  # time at next scr refresh
            p1_ready_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(p1_ready_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(p1_ready_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if p1_ready_resp.status == STARTED and not waitOnFlip:
            theseKeys = p1_ready_resp.getKeys(keyList=['u','h','k','j','n'], waitRelease=False)
            _p1_ready_resp_allKeys.extend(theseKeys)
            if len(_p1_ready_resp_allKeys):
                p1_ready_resp.keys = _p1_ready_resp_allKeys[-1].name  # just the last key pressed
                p1_ready_resp.rt = _p1_ready_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *movement_key_text1* updates
        if movement_key_text1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movement_key_text1.frameNStart = frameN  # exact frame index
            movement_key_text1.tStart = t  # local t and not account for scr refresh
            movement_key_text1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movement_key_text1, 'tStartRefresh')  # time at next scr refresh
            movement_key_text1.setAutoDraw(True)
        
        # *display_pct_txt* updates
        if display_pct_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            display_pct_txt.frameNStart = frameN  # exact frame index
            display_pct_txt.tStart = t  # local t and not account for scr refresh
            display_pct_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(display_pct_txt, 'tStartRefresh')  # time at next scr refresh
            display_pct_txt.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in p1_confirmComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "p1_confirm"-------
    for thisComponent in p1_confirmComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    rounds.addData('p1_ready.started', p1_ready.tStartRefresh)
    rounds.addData('p1_ready.stopped', p1_ready.tStopRefresh)
    rounds.addData('diode_p1_ready.started', diode_p1_ready.tStartRefresh)
    rounds.addData('diode_p1_ready.stopped', diode_p1_ready.tStopRefresh)
    rounds.addData('player1_ready_display.started', player1_ready_display.tStartRefresh)
    rounds.addData('player1_ready_display.stopped', player1_ready_display.tStopRefresh)
    # check responses
    if p1_ready_resp.keys in ['', [], None]:  # No response was made
        p1_ready_resp.keys = None
    rounds.addData('p1_ready_resp.keys',p1_ready_resp.keys)
    if p1_ready_resp.keys != None:  # we had a response
        rounds.addData('p1_ready_resp.rt', p1_ready_resp.rt)
    rounds.addData('p1_ready_resp.started', p1_ready_resp.tStartRefresh)
    rounds.addData('p1_ready_resp.stopped', p1_ready_resp.tStopRefresh)
    rounds.addData('movement_key_text1.started', movement_key_text1.tStartRefresh)
    rounds.addData('movement_key_text1.stopped', movement_key_text1.tStopRefresh)
    rounds.addData('display_pct_txt.started', display_pct_txt.tStartRefresh)
    rounds.addData('display_pct_txt.stopped', display_pct_txt.tStopRefresh)
    # the Routine "p1_confirm" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "p2_confirm"-------
    continueRoutine = True
    # update component parameters for each repeat
    player2_ready_display.setImage(agent2_imgs['stay'])
    p2_ready_resp.keys = []
    p2_ready_resp.rt = []
    _p2_ready_resp_allKeys = []
    display_pct_txt_2.setText(display_percent_complete)
    # keep track of which components have finished
    p2_confirmComponents = [p2_ready, diode_p2_ready, player2_ready_display, p2_ready_resp, movement_key_text2, display_pct_txt_2]
    for thisComponent in p2_confirmComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    p2_confirmClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "p2_confirm"-------
    while continueRoutine:
        # get current time
        t = p2_confirmClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=p2_confirmClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *p2_ready* updates
        if p2_ready.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            p2_ready.frameNStart = frameN  # exact frame index
            p2_ready.tStart = t  # local t and not account for scr refresh
            p2_ready.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p2_ready, 'tStartRefresh')  # time at next scr refresh
            p2_ready.setAutoDraw(True)
        
        # *diode_p2_ready* updates
        if diode_p2_ready.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            diode_p2_ready.frameNStart = frameN  # exact frame index
            diode_p2_ready.tStart = t  # local t and not account for scr refresh
            diode_p2_ready.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(diode_p2_ready, 'tStartRefresh')  # time at next scr refresh
            diode_p2_ready.setAutoDraw(True)
        
        # *player2_ready_display* updates
        if player2_ready_display.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            player2_ready_display.frameNStart = frameN  # exact frame index
            player2_ready_display.tStart = t  # local t and not account for scr refresh
            player2_ready_display.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(player2_ready_display, 'tStartRefresh')  # time at next scr refresh
            player2_ready_display.setAutoDraw(True)
        
        # *p2_ready_resp* updates
        waitOnFlip = False
        if p2_ready_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            p2_ready_resp.frameNStart = frameN  # exact frame index
            p2_ready_resp.tStart = t  # local t and not account for scr refresh
            p2_ready_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p2_ready_resp, 'tStartRefresh')  # time at next scr refresh
            p2_ready_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(p2_ready_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(p2_ready_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if p2_ready_resp.status == STARTED and not waitOnFlip:
            theseKeys = p2_ready_resp.getKeys(keyList=['num_5','num_8','num_4','num_6','num_2'], waitRelease=False)
            _p2_ready_resp_allKeys.extend(theseKeys)
            if len(_p2_ready_resp_allKeys):
                p2_ready_resp.keys = _p2_ready_resp_allKeys[-1].name  # just the last key pressed
                p2_ready_resp.rt = _p2_ready_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *movement_key_text2* updates
        if movement_key_text2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movement_key_text2.frameNStart = frameN  # exact frame index
            movement_key_text2.tStart = t  # local t and not account for scr refresh
            movement_key_text2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movement_key_text2, 'tStartRefresh')  # time at next scr refresh
            movement_key_text2.setAutoDraw(True)
        
        # *display_pct_txt_2* updates
        if display_pct_txt_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            display_pct_txt_2.frameNStart = frameN  # exact frame index
            display_pct_txt_2.tStart = t  # local t and not account for scr refresh
            display_pct_txt_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(display_pct_txt_2, 'tStartRefresh')  # time at next scr refresh
            display_pct_txt_2.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in p2_confirmComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "p2_confirm"-------
    for thisComponent in p2_confirmComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    rounds.addData('p2_ready.started', p2_ready.tStartRefresh)
    rounds.addData('p2_ready.stopped', p2_ready.tStopRefresh)
    rounds.addData('diode_p2_ready.started', diode_p2_ready.tStartRefresh)
    rounds.addData('diode_p2_ready.stopped', diode_p2_ready.tStopRefresh)
    rounds.addData('player2_ready_display.started', player2_ready_display.tStartRefresh)
    rounds.addData('player2_ready_display.stopped', player2_ready_display.tStopRefresh)
    # check responses
    if p2_ready_resp.keys in ['', [], None]:  # No response was made
        p2_ready_resp.keys = None
    rounds.addData('p2_ready_resp.keys',p2_ready_resp.keys)
    if p2_ready_resp.keys != None:  # we had a response
        rounds.addData('p2_ready_resp.rt', p2_ready_resp.rt)
    rounds.addData('p2_ready_resp.started', p2_ready_resp.tStartRefresh)
    rounds.addData('p2_ready_resp.stopped', p2_ready_resp.tStopRefresh)
    rounds.addData('movement_key_text2.started', movement_key_text2.tStartRefresh)
    rounds.addData('movement_key_text2.stopped', movement_key_text2.tStopRefresh)
    rounds.addData('display_pct_txt_2.started', display_pct_txt_2.tStartRefresh)
    rounds.addData('display_pct_txt_2.stopped', display_pct_txt_2.tStopRefresh)
    # the Routine "p2_confirm" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "start_round"-------
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # check who goes first
    if firstplayer == 'player1':
        player1_turn = 1
        player2_turn = 0
        PLAYER_START_TEXT = '\nPLAYER 1 GOES FIRST'
        PLAYER_START_IMG = agent1_imgs['down']
    elif firstplayer == 'player2':
        player1_turn = 0
        player2_turn = 1
        PLAYER_START_TEXT = '\nPLAYER 2 GOES FIRST'
        PLAYER_START_IMG = agent2_imgs['down']
    
    
    # store timing:
    start_round_time = globalClock.getTime() - trigger_time
    thisExp.addData('round_start_onset', start_round_time)
    start_round_txt.setText(PLAYER_START_TEXT)
    start_round_player_display.setImage(PLAYER_START_IMG)
    # keep track of which components have finished
    start_roundComponents = [start_round_txt, diode_square_round_start, start_round_player_display]
    for thisComponent in start_roundComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    start_roundClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "start_round"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = start_roundClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=start_roundClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *start_round_txt* updates
        if start_round_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_round_txt.frameNStart = frameN  # exact frame index
            start_round_txt.tStart = t  # local t and not account for scr refresh
            start_round_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_round_txt, 'tStartRefresh')  # time at next scr refresh
            start_round_txt.setAutoDraw(True)
        if start_round_txt.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > start_round_txt.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                start_round_txt.tStop = t  # not accounting for scr refresh
                start_round_txt.frameNStop = frameN  # exact frame index
                win.timeOnFlip(start_round_txt, 'tStopRefresh')  # time at next scr refresh
                start_round_txt.setAutoDraw(False)
        
        # *diode_square_round_start* updates
        if diode_square_round_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            diode_square_round_start.frameNStart = frameN  # exact frame index
            diode_square_round_start.tStart = t  # local t and not account for scr refresh
            diode_square_round_start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(diode_square_round_start, 'tStartRefresh')  # time at next scr refresh
            diode_square_round_start.setAutoDraw(True)
        if diode_square_round_start.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > diode_square_round_start.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                diode_square_round_start.tStop = t  # not accounting for scr refresh
                diode_square_round_start.frameNStop = frameN  # exact frame index
                win.timeOnFlip(diode_square_round_start, 'tStopRefresh')  # time at next scr refresh
                diode_square_round_start.setAutoDraw(False)
        
        # *start_round_player_display* updates
        if start_round_player_display.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_round_player_display.frameNStart = frameN  # exact frame index
            start_round_player_display.tStart = t  # local t and not account for scr refresh
            start_round_player_display.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_round_player_display, 'tStartRefresh')  # time at next scr refresh
            start_round_player_display.setAutoDraw(True)
        if start_round_player_display.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > start_round_player_display.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                start_round_player_display.tStop = t  # not accounting for scr refresh
                start_round_player_display.frameNStop = frameN  # exact frame index
                win.timeOnFlip(start_round_player_display, 'tStopRefresh')  # time at next scr refresh
                start_round_player_display.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in start_roundComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "start_round"-------
    for thisComponent in start_roundComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    agent1_pos = [agent1_startx, agent1_starty]
    agent2_pos = [agent2_startx, agent2_starty]
    chick1_pos = [chick_startx, chick_starty]
    #random_side = np.random.permutation([-.3, .3])
    #chick1_pos = [0., np.random.choice([-.3,-.15,0,.15,.3])]
    ##agent2_pos = [random_side[1], np.random.choice([-.3,-.15,.15,.3])]
    #if easy_defect == 'player1': 
    #    p_sides = np.random.permutation([-1,1])
    #    agent1_pos = [random_side[0], p_sides[0]*.15]
    #    agent2_pos = [random_side[1], p_sides[1]*.3]
    #    # make it easier for p1 to get egg, 
    #    # place opposite side of chicken, closer to egg
    ##    if chick1_pos[1] != 0:
    ##        agent1_pos = [random_side[0], np.sign(chick1_pos[1])*-1*.15]
    ##        agent2_pos = [random_side[1], np.sign(chick1_pos[1])*.3]
    ##    else:
    ##        p_sides = np.random.permutation([-1,1])
    ##        agent1_pos = [random_side[0], p_sides[0]*.15]
    ##        agent2_pos = [random_side[1], p_sides[1]*.3]
    #        
    #elif easy_defect == 'player2':
    #    p_sides = np.random.permutation([-1,1])
    #    agent1_pos = [random_side[0], p_sides[0]*.3]
    #    agent2_pos = [random_side[1], p_sides[1]*.15]
    #    # make it easier for p2 to get egg, 
    #    # place opposite side of chicken, closer to egg
    ##    if chick1_pos[1] != 0:
    ##        agent2_pos = [random_side[1], np.sign(chick1_pos[1])*-1*.15]
    ##        agent1_pos = [random_side[0], np.sign(chick1_pos[1])*.3]
    ##    else:
    ##        p_sides = np.random.permutation([-1,1])
    ##        agent2_pos = [random_side[0], p_sides[1]*.15]
    ##        agent1_pos = [random_side[1], p_sides[0]*.3]
    #
    #elif easy_defect == 'both':
    #    # make it harder for both to get egg, 
    #    # place opposite side of chicken, closer to egg
    #    p_sides = np.random.permutation([-1,1])
    #    agent2_pos = [random_side[0], p_sides[1]*.15]
    #    agent1_pos = [random_side[1], p_sides[0]*.15]
    #    
    #elif easy_defect == 'none':
    #    # make it harder for both to get egg, 
    #    # place same side of chicken, further to egg
    #    p_sides = np.random.permutation([-1,1])
    #    agent2_pos = [random_side[0], p_sides[1]*.3]
    #    agent1_pos = [random_side[1], p_sides[0]*.3]
    
    agent1.setPos(agent1_pos, log=True)
    #agent1_indicator_text.setPos(agent1_pos, log=True)
    startx, starty, startposmoves = convert_coords(agent1_pos[0], agent1_pos[1])
    thisExp.addData('agent1_startx', startx)
    thisExp.addData('agent1_starty', starty)
    
    agent2.setPos(agent2_pos, log=True)
    #agent2_indicator_text.setPos(agent2_pos, log=True)
    startx, starty, startposmoves = convert_coords(agent2_pos[0], agent2_pos[1])
    thisExp.addData('agent2_startx', startx)
    thisExp.addData('agent2_starty', starty)
    
    chick1.setPos(chick1_pos, log=True)
    startx, starty, startposmoves = convert_coords(chick1_pos[0], chick1_pos[1])
    thisExp.addData('chick1_startx', startx)
    thisExp.addData('chick1_starty', starty)
    
    if nchicks >= 2:
        chick2_pos = [-.15, np.random.choice([-.3,0,.3])]
        chick2.setPos(chick2_pos, log=True)
    
    if nchicks >= 3:
        chick3_pos = [.15, np.random.choice([-.3,0,.3])]
        chick3.setPos(chick3_pos, log=True)
    
    TrialCount = 0
    TurnBonus25 = 175
    endLoop = 0
    trial_text = visual.TextStim(win=win, name='trial_text',
        text='',
        font='Open Sans',
        pos=(.55, .35), height=0.04, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    agent1_indicator_text.setPos(agent1_pos)
    agent1_indicator_text.setAutoDraw(True)
    agent2_indicator_text.setPos(agent2_pos)
    agent2_indicator_text.setAutoDraw(True)
    rounds.addData('start_round_txt.started', start_round_txt.tStartRefresh)
    rounds.addData('start_round_txt.stopped', start_round_txt.tStopRefresh)
    GridWorldComponents = [diode_square_white, b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]
    
    for thisComponent in GridWorldComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(True)
    
    AgentsComponents = [agent1, agent2, chick1]
    if nchicks >= 2:
        AgentsComponents += [chick2]
    
    if nchicks >= 3:
        AgentsComponents += [chick3]
        
    for thisComponent in AgentsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(True)
    rounds.addData('diode_square_round_start.started', diode_square_round_start.tStartRefresh)
    rounds.addData('diode_square_round_start.stopped', diode_square_round_start.tStopRefresh)
    rounds.addData('start_round_player_display.started', start_round_player_display.tStartRefresh)
    rounds.addData('start_round_player_display.stopped', start_round_player_display.tStopRefresh)
    round_start_time = globalClock.getTime()
    thisExp.addData('round_start_onset', round_start_time)
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=ntrials, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "move_chick1"-------
        continueRoutine = True
        # update component parameters for each repeat
        instr_chick.bold = True
        
        TrialCount += 1
        current_time_bonus = (16 - TrialCount) * 10 # minus 10 pts
        
        #TurnBonus25 = TurnBonus25 - 25
        #current_time_bonus = TurnBonus25 # minus 25 pts
        #trial_num_text = f'turn bonus:\n{current_time_bonus} points' # out of {trials.nReps} trials'
        trial_num_text = f'' # out of {trials.nReps} trials'
        
        trial_text.setText(trial_num_text)
        trial_text.setAutoDraw(True)
        chick_jitter = np.random.uniform(2,3)
        thisExp.addData('chick_jitter', chick_jitter)
        chick_timer = core.Clock()
        
        # get grid coords and moves
        out_x, out_y, possiblemoves = convert_coords(chick1_pos[0], chick1_pos[1], agent='computer')
        
        # NEED TO EDIT THIS
        if (chick1_pos[0]== agent2_pos[0] and chick1_pos[1] == agent2_pos[1]) or (chick1_pos[0]== agent1_pos[0] and chick1_pos[1] == agent1_pos[1]):
            possiblemoves.remove('space')
            
        flag = True
        while flag:
            #this_chick1_move = np.random.choice(possiblemoves)
            this_chick1_move = maximize_chick_distance(chick1_pos, agent1_pos, agent2_pos, possiblemoves)
            x_shift, y_shift = convert_moves(this_chick1_move)
            
            if nchicks >= 2:
                if ([chick1_pos[0]+x_shift, chick1_pos[1]+y_shift] == agent2_pos) or ([chick1_pos[0]+x_shift, chick1_pos[1]+y_shift] == chick2_pos) or ([chick1_pos[0]+x_shift, chick1_pos[1]+y_shift] == agent1_pos):
                    flag = True
                    possiblemoves.remove(this_chick1_move)
                elif (abs(chick1_pos[0]+x_shift) > .35):
                    flag = True
                    possiblemoves.remove(this_chick1_move)
                else:
                    flag = False
            elif nchicks == 1:
                if ([chick1_pos[0]+x_shift, chick1_pos[1]+y_shift] == agent2_pos) or ([chick1_pos[0]+x_shift, chick1_pos[1]+y_shift] == agent1_pos):
                    flag = True
                    possiblemoves.remove('space')
                    possiblemoves.remove(this_chick1_move)
                elif (abs(chick1_pos[0]+x_shift) > .35):
                    flag = True
                    possiblemoves.remove(this_chick1_move)
                else:
                    flag = False
        
            
        
        # keep track of which components have finished
        move_chick1Components = [instr_chick]
        for thisComponent in move_chick1Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        move_chick1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "move_chick1"-------
        while continueRoutine:
            # get current time
            t = move_chick1Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=move_chick1Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if chick_timer.getTime()>chick_jitter:
                if this_chick1_move != 'space':
                    chick1.image = chick1_imgs[this_chick1_move]
                else:
                    chick1.image = chick1_imgs['stay']
            
                chick1_pos = [chick1_pos[0]+x_shift, chick1_pos[1]+y_shift]
                chick1.setPos(chick1_pos, log=True)
                thisExp.addData(f'chick1_action', this_chick1_move)
            
                # store timing:
                chick_move_onset_time = globalClock.getTime() - trigger_time
                thisExp.addData('chick_move_onset', chick_move_onset_time)
                
                chick_move_since_round_start = globalClock.getTime() - round_start_time
                thisExp.addData('chick_move_onset_from_round_start', chick_move_since_round_start)
            
                #print('chick1', out_x, out_y, possiblemoves, this_chick1_move)
                win.flip()
                core.wait(1)
            
                chick1.image = chick1_imgs['down']
                win.flip()
                continueRoutine = False
            
            # *instr_chick* updates
            if instr_chick.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instr_chick.frameNStart = frameN  # exact frame index
                instr_chick.tStart = t  # local t and not account for scr refresh
                instr_chick.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instr_chick, 'tStartRefresh')  # time at next scr refresh
                instr_chick.setAutoDraw(True)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in move_chick1Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "move_chick1"-------
        for thisComponent in move_chick1Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('instr_chick.started', instr_chick.tStartRefresh)
        trials.addData('instr_chick.stopped', instr_chick.tStopRefresh)
        # the Routine "move_chick1" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        player1_first = data.TrialHandler(nReps=player1_turn, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='player1_first')
        thisExp.addLoop(player1_first)  # add the loop to the experiment
        thisPlayer1_first = player1_first.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisPlayer1_first.rgb)
        if thisPlayer1_first != None:
            for paramName in thisPlayer1_first:
                exec('{} = thisPlayer1_first[paramName]'.format(paramName))
        
        for thisPlayer1_first in player1_first:
            currentLoop = player1_first
            # abbreviate parameter names if possible (e.g. rgb = thisPlayer1_first.rgb)
            if thisPlayer1_first != None:
                for paramName in thisPlayer1_first:
                    exec('{} = thisPlayer1_first[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "move_agent1"-------
            continueRoutine = True
            routineTimer.add(6.000000)
            # update component parameters for each repeat
            resp_agent1.keys = []
            resp_agent1.rt = []
            _resp_agent1_allKeys = []
            agent1_jitter = np.random.uniform(1,1.5)
            thisExp.addData('agent1_jitter', agent1_jitter)
            
            instr_agent1.bold = True
            agent1_indicator_text.color = "red"
            
            # get grid coords and moves
            out_x, out_y, possiblemoves = convert_coords(agent1_pos[0], agent1_pos[1], agent='player1')
            
            # remove possible move if adjacent to another agent
            for this_move in possiblemoves:
                x_shift, y_shift = convert_moves(this_move)
                if [agent1_pos[0]+x_shift, agent1_pos[1]+y_shift] == chick1_pos:
                    possiblemoves.remove(this_move)
                if [agent1_pos[0]+x_shift, agent1_pos[1]+y_shift] == agent2_pos:
                    possiblemoves.remove(this_move)
            
            this_agent1_move = ''
            # keep track of which components have finished
            move_agent1Components = [resp_agent1, instr_agent1]
            for thisComponent in move_agent1Components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            move_agent1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "move_agent1"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = move_agent1Clock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=move_agent1Clock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *resp_agent1* updates
                waitOnFlip = False
                if resp_agent1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    resp_agent1.frameNStart = frameN  # exact frame index
                    resp_agent1.tStart = t  # local t and not account for scr refresh
                    resp_agent1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(resp_agent1, 'tStartRefresh')  # time at next scr refresh
                    resp_agent1.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(resp_agent1.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(resp_agent1.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if resp_agent1.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > resp_agent1.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        resp_agent1.tStop = t  # not accounting for scr refresh
                        resp_agent1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(resp_agent1, 'tStopRefresh')  # time at next scr refresh
                        resp_agent1.status = FINISHED
                if resp_agent1.status == STARTED and not waitOnFlip:
                    theseKeys = resp_agent1.getKeys(keyList=None, waitRelease=False)
                    _resp_agent1_allKeys.extend(theseKeys)
                    if len(_resp_agent1_allKeys):
                        resp_agent1.keys = _resp_agent1_allKeys[-1].name  # just the last key pressed
                        resp_agent1.rt = _resp_agent1_allKeys[-1].rt
                
                # *instr_agent1* updates
                if instr_agent1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    instr_agent1.frameNStart = frameN  # exact frame index
                    instr_agent1.tStart = t  # local t and not account for scr refresh
                    instr_agent1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(instr_agent1, 'tStartRefresh')  # time at next scr refresh
                    instr_agent1.setAutoDraw(True)
                if instr_agent1.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > instr_agent1.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        instr_agent1.tStop = t  # not accounting for scr refresh
                        instr_agent1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(instr_agent1, 'tStopRefresh')  # time at next scr refresh
                        instr_agent1.setAutoDraw(False)
                current_agent1_keyresp = resp_agent1.getKeys(clear=True)
                if current_agent1_keyresp:
                     if resp_agent1.keys in possiblemoves:
                        if resp_agent1.keys == 'h':
                            this_agent1_move = 'left'
                            agent1_pos = [agent1_pos[0]-.15, agent1_pos[1]]
                            agent1.image = agent1_imgs['left']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        elif resp_agent1.keys == 'k':
                            this_agent1_move = 'right'
                            agent1_pos = [agent1_pos[0]+.15, agent1_pos[1]]
                            agent1.image = agent1_imgs['right']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        elif resp_agent1.keys == 'u':
                            this_agent1_move = 'up'
                            agent1_pos = [agent1_pos[0], agent1_pos[1]+.15]
                            agent1.image = agent1_imgs['up']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        elif resp_agent1.keys == 'n':
                            this_agent1_move = 'down'
                            agent1_pos = [agent1_pos[0], agent1_pos[1]-.15]
                            agent1.image = agent1_imgs['down']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        else:
                            this_agent1_move = 'null'
                            agent1.image = agent1_imgs['down']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                            
                        agent1.setPos(agent1_pos, log=True)
                        agent1_indicator_text.setPos(agent1_pos, log=True)
                        
                        if agent1_pos[0] > .3:
                            egg_right.setAutoDraw(False)
                        if agent1_pos[0] < -.3:
                            egg_left.setAutoDraw(False)
                        win.flip()
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in move_agent1Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "move_agent1"-------
            for thisComponent in move_agent1Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            player1_first.addData('instr_agent1.started', instr_agent1.tStartRefresh)
            player1_first.addData('instr_agent1.stopped', instr_agent1.tStopRefresh)
            #print('agent1', out_x, out_y, possiblemoves, resp_agent1.keys, agent1_pos)
            
            if this_agent1_move in ['up','down','left','right']:
                thisExp.addData(f'agent1_action', this_agent1_move)
            else:
                thisExp.addData(f'agent1_action', 'null')
            
            core.wait(agent1_jitter)
            agent1.image = agent1_imgs['down']
            win.flip()
            
            agent1_indicator_text.color = "black"
            
            # ------Prepare to start Routine "move_agent2"-------
            continueRoutine = True
            routineTimer.add(6.000000)
            # update component parameters for each repeat
            resp_agent2.keys = []
            resp_agent2.rt = []
            _resp_agent2_allKeys = []
            agent2_jitter = np.random.uniform(1,1.5)
            thisExp.addData('agent2_jitter', agent2_jitter)
            
            instr_agent2.bold = True
            agent2_indicator_text.color = "red"
            
            # get grid coords and moves
            out_x, out_y, possiblemoves = convert_coords(agent2_pos[0], agent2_pos[1], agent='player2')
            
            # remove possible move if adjacent to another agent
            for this_move in possiblemoves:
                x_shift, y_shift = convert_moves(this_move)
                if [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift] == chick1_pos:
                    possiblemoves.remove(this_move)
                if [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift] == agent1_pos:
                    possiblemoves.remove(this_move)
                    
            this_agent2_move = ''
            
            # keep track of which components have finished
            move_agent2Components = [resp_agent2, instr_agent2]
            for thisComponent in move_agent2Components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            move_agent2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "move_agent2"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = move_agent2Clock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=move_agent2Clock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *resp_agent2* updates
                waitOnFlip = False
                if resp_agent2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    resp_agent2.frameNStart = frameN  # exact frame index
                    resp_agent2.tStart = t  # local t and not account for scr refresh
                    resp_agent2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(resp_agent2, 'tStartRefresh')  # time at next scr refresh
                    resp_agent2.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(resp_agent2.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(resp_agent2.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if resp_agent2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > resp_agent2.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        resp_agent2.tStop = t  # not accounting for scr refresh
                        resp_agent2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(resp_agent2, 'tStopRefresh')  # time at next scr refresh
                        resp_agent2.status = FINISHED
                if resp_agent2.status == STARTED and not waitOnFlip:
                    theseKeys = resp_agent2.getKeys(keyList=None, waitRelease=False)
                    _resp_agent2_allKeys.extend(theseKeys)
                    if len(_resp_agent2_allKeys):
                        resp_agent2.keys = _resp_agent2_allKeys[-1].name  # just the last key pressed
                        resp_agent2.rt = _resp_agent2_allKeys[-1].rt
                
                # *instr_agent2* updates
                if instr_agent2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    instr_agent2.frameNStart = frameN  # exact frame index
                    instr_agent2.tStart = t  # local t and not account for scr refresh
                    instr_agent2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(instr_agent2, 'tStartRefresh')  # time at next scr refresh
                    instr_agent2.setAutoDraw(True)
                if instr_agent2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > instr_agent2.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        instr_agent2.tStop = t  # not accounting for scr refresh
                        instr_agent2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(instr_agent2, 'tStopRefresh')  # time at next scr refresh
                        instr_agent2.setAutoDraw(False)
                #if resp_agent2.keys:
                current_agent2_keyresp = resp_agent2.getKeys(clear=True)
                if current_agent2_keyresp:
                    if resp_agent2.keys in possiblemoves:
                        if resp_agent2.keys == 'num_4':
                            this_agent2_move = 'left'
                            agent2_pos = [agent2_pos[0]-.15, agent2_pos[1]]
                            agent2.image = agent2_imgs['left']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        elif resp_agent2.keys == 'num_6':
                            this_agent2_move = 'right'
                            agent2_pos = [agent2_pos[0]+.15, agent2_pos[1]]
                            agent2.image = agent2_imgs['right']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        elif resp_agent2.keys == 'num_8':
                            this_agent2_move = 'up'
                            agent2_pos = [agent2_pos[0], agent2_pos[1]+.15]
                            agent2.image = agent2_imgs['up']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        elif resp_agent2.keys == 'num_2':
                            this_agent2_move = 'down'
                            agent2_pos = [agent2_pos[0], agent2_pos[1]-.15]
                            agent2.image = agent2_imgs['down']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        else:
                            this_agent2_move = 'null'
                            agent2.image = agent2_imgs['down']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                            
                        agent2.setPos(agent2_pos, log=True)
                        agent2_indicator_text.setPos(agent2_pos, log=True)
                        
                        if agent2_pos[0] > .3:
                            egg_right.setAutoDraw(False)
                        if agent2_pos[0] < -.3:
                            egg_left.setAutoDraw(False)
                        win.flip()
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in move_agent2Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "move_agent2"-------
            for thisComponent in move_agent2Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            player1_first.addData('instr_agent2.started', instr_agent2.tStartRefresh)
            player1_first.addData('instr_agent2.stopped', instr_agent2.tStopRefresh)
            #print('agent2', out_x, out_y, possiblemoves, resp_agent2.keys, agent2_pos)
            
            if this_agent2_move in ['up','down','left','right']:
                thisExp.addData(f'agent2_action', this_agent2_move)
            else:
                thisExp.addData(f'agent2_action', 'null')
            
            core.wait(agent2_jitter)
            agent2.image = agent2_imgs['down']
            win.flip()
            agent2_indicator_text.color = "black"
        # completed player1_turn repeats of 'player1_first'
        
        
        # set up handler to look after randomisation of conditions etc
        player2_first = data.TrialHandler(nReps=player2_turn, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='player2_first')
        thisExp.addLoop(player2_first)  # add the loop to the experiment
        thisPlayer2_first = player2_first.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisPlayer2_first.rgb)
        if thisPlayer2_first != None:
            for paramName in thisPlayer2_first:
                exec('{} = thisPlayer2_first[paramName]'.format(paramName))
        
        for thisPlayer2_first in player2_first:
            currentLoop = player2_first
            # abbreviate parameter names if possible (e.g. rgb = thisPlayer2_first.rgb)
            if thisPlayer2_first != None:
                for paramName in thisPlayer2_first:
                    exec('{} = thisPlayer2_first[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "move_agent2"-------
            continueRoutine = True
            routineTimer.add(6.000000)
            # update component parameters for each repeat
            resp_agent2.keys = []
            resp_agent2.rt = []
            _resp_agent2_allKeys = []
            agent2_jitter = np.random.uniform(1,1.5)
            thisExp.addData('agent2_jitter', agent2_jitter)
            
            instr_agent2.bold = True
            agent2_indicator_text.color = "red"
            
            # get grid coords and moves
            out_x, out_y, possiblemoves = convert_coords(agent2_pos[0], agent2_pos[1], agent='player2')
            
            # remove possible move if adjacent to another agent
            for this_move in possiblemoves:
                x_shift, y_shift = convert_moves(this_move)
                if [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift] == chick1_pos:
                    possiblemoves.remove(this_move)
                if [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift] == agent1_pos:
                    possiblemoves.remove(this_move)
                    
            this_agent2_move = ''
            
            # keep track of which components have finished
            move_agent2Components = [resp_agent2, instr_agent2]
            for thisComponent in move_agent2Components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            move_agent2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "move_agent2"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = move_agent2Clock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=move_agent2Clock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *resp_agent2* updates
                waitOnFlip = False
                if resp_agent2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    resp_agent2.frameNStart = frameN  # exact frame index
                    resp_agent2.tStart = t  # local t and not account for scr refresh
                    resp_agent2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(resp_agent2, 'tStartRefresh')  # time at next scr refresh
                    resp_agent2.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(resp_agent2.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(resp_agent2.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if resp_agent2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > resp_agent2.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        resp_agent2.tStop = t  # not accounting for scr refresh
                        resp_agent2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(resp_agent2, 'tStopRefresh')  # time at next scr refresh
                        resp_agent2.status = FINISHED
                if resp_agent2.status == STARTED and not waitOnFlip:
                    theseKeys = resp_agent2.getKeys(keyList=None, waitRelease=False)
                    _resp_agent2_allKeys.extend(theseKeys)
                    if len(_resp_agent2_allKeys):
                        resp_agent2.keys = _resp_agent2_allKeys[-1].name  # just the last key pressed
                        resp_agent2.rt = _resp_agent2_allKeys[-1].rt
                
                # *instr_agent2* updates
                if instr_agent2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    instr_agent2.frameNStart = frameN  # exact frame index
                    instr_agent2.tStart = t  # local t and not account for scr refresh
                    instr_agent2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(instr_agent2, 'tStartRefresh')  # time at next scr refresh
                    instr_agent2.setAutoDraw(True)
                if instr_agent2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > instr_agent2.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        instr_agent2.tStop = t  # not accounting for scr refresh
                        instr_agent2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(instr_agent2, 'tStopRefresh')  # time at next scr refresh
                        instr_agent2.setAutoDraw(False)
                #if resp_agent2.keys:
                current_agent2_keyresp = resp_agent2.getKeys(clear=True)
                if current_agent2_keyresp:
                    if resp_agent2.keys in possiblemoves:
                        if resp_agent2.keys == 'num_4':
                            this_agent2_move = 'left'
                            agent2_pos = [agent2_pos[0]-.15, agent2_pos[1]]
                            agent2.image = agent2_imgs['left']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        elif resp_agent2.keys == 'num_6':
                            this_agent2_move = 'right'
                            agent2_pos = [agent2_pos[0]+.15, agent2_pos[1]]
                            agent2.image = agent2_imgs['right']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        elif resp_agent2.keys == 'num_8':
                            this_agent2_move = 'up'
                            agent2_pos = [agent2_pos[0], agent2_pos[1]+.15]
                            agent2.image = agent2_imgs['up']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        elif resp_agent2.keys == 'num_2':
                            this_agent2_move = 'down'
                            agent2_pos = [agent2_pos[0], agent2_pos[1]-.15]
                            agent2.image = agent2_imgs['down']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                        else:
                            this_agent2_move = 'null'
                            agent2.image = agent2_imgs['down']
                            
                            # store timing:
                            agent2_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent2_move_onset', agent2_move_onset_time)
                
                            agent2_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent2_move_onset_from_round_start', agent2_move_since_round_start)
                
                            win.flip()
                            
                        agent2.setPos(agent2_pos, log=True)
                        agent2_indicator_text.setPos(agent2_pos, log=True)
                        
                        if agent2_pos[0] > .3:
                            egg_right.setAutoDraw(False)
                        if agent2_pos[0] < -.3:
                            egg_left.setAutoDraw(False)
                        win.flip()
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in move_agent2Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "move_agent2"-------
            for thisComponent in move_agent2Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            player2_first.addData('instr_agent2.started', instr_agent2.tStartRefresh)
            player2_first.addData('instr_agent2.stopped', instr_agent2.tStopRefresh)
            #print('agent2', out_x, out_y, possiblemoves, resp_agent2.keys, agent2_pos)
            
            if this_agent2_move in ['up','down','left','right']:
                thisExp.addData(f'agent2_action', this_agent2_move)
            else:
                thisExp.addData(f'agent2_action', 'null')
            
            core.wait(agent2_jitter)
            agent2.image = agent2_imgs['down']
            win.flip()
            agent2_indicator_text.color = "black"
            
            # ------Prepare to start Routine "move_agent1"-------
            continueRoutine = True
            routineTimer.add(6.000000)
            # update component parameters for each repeat
            resp_agent1.keys = []
            resp_agent1.rt = []
            _resp_agent1_allKeys = []
            agent1_jitter = np.random.uniform(1,1.5)
            thisExp.addData('agent1_jitter', agent1_jitter)
            
            instr_agent1.bold = True
            agent1_indicator_text.color = "red"
            
            # get grid coords and moves
            out_x, out_y, possiblemoves = convert_coords(agent1_pos[0], agent1_pos[1], agent='player1')
            
            # remove possible move if adjacent to another agent
            for this_move in possiblemoves:
                x_shift, y_shift = convert_moves(this_move)
                if [agent1_pos[0]+x_shift, agent1_pos[1]+y_shift] == chick1_pos:
                    possiblemoves.remove(this_move)
                if [agent1_pos[0]+x_shift, agent1_pos[1]+y_shift] == agent2_pos:
                    possiblemoves.remove(this_move)
            
            this_agent1_move = ''
            # keep track of which components have finished
            move_agent1Components = [resp_agent1, instr_agent1]
            for thisComponent in move_agent1Components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            move_agent1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "move_agent1"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = move_agent1Clock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=move_agent1Clock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *resp_agent1* updates
                waitOnFlip = False
                if resp_agent1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    resp_agent1.frameNStart = frameN  # exact frame index
                    resp_agent1.tStart = t  # local t and not account for scr refresh
                    resp_agent1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(resp_agent1, 'tStartRefresh')  # time at next scr refresh
                    resp_agent1.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(resp_agent1.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(resp_agent1.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if resp_agent1.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > resp_agent1.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        resp_agent1.tStop = t  # not accounting for scr refresh
                        resp_agent1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(resp_agent1, 'tStopRefresh')  # time at next scr refresh
                        resp_agent1.status = FINISHED
                if resp_agent1.status == STARTED and not waitOnFlip:
                    theseKeys = resp_agent1.getKeys(keyList=None, waitRelease=False)
                    _resp_agent1_allKeys.extend(theseKeys)
                    if len(_resp_agent1_allKeys):
                        resp_agent1.keys = _resp_agent1_allKeys[-1].name  # just the last key pressed
                        resp_agent1.rt = _resp_agent1_allKeys[-1].rt
                
                # *instr_agent1* updates
                if instr_agent1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    instr_agent1.frameNStart = frameN  # exact frame index
                    instr_agent1.tStart = t  # local t and not account for scr refresh
                    instr_agent1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(instr_agent1, 'tStartRefresh')  # time at next scr refresh
                    instr_agent1.setAutoDraw(True)
                if instr_agent1.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > instr_agent1.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        instr_agent1.tStop = t  # not accounting for scr refresh
                        instr_agent1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(instr_agent1, 'tStopRefresh')  # time at next scr refresh
                        instr_agent1.setAutoDraw(False)
                current_agent1_keyresp = resp_agent1.getKeys(clear=True)
                if current_agent1_keyresp:
                     if resp_agent1.keys in possiblemoves:
                        if resp_agent1.keys == 'h':
                            this_agent1_move = 'left'
                            agent1_pos = [agent1_pos[0]-.15, agent1_pos[1]]
                            agent1.image = agent1_imgs['left']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        elif resp_agent1.keys == 'k':
                            this_agent1_move = 'right'
                            agent1_pos = [agent1_pos[0]+.15, agent1_pos[1]]
                            agent1.image = agent1_imgs['right']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        elif resp_agent1.keys == 'u':
                            this_agent1_move = 'up'
                            agent1_pos = [agent1_pos[0], agent1_pos[1]+.15]
                            agent1.image = agent1_imgs['up']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        elif resp_agent1.keys == 'n':
                            this_agent1_move = 'down'
                            agent1_pos = [agent1_pos[0], agent1_pos[1]-.15]
                            agent1.image = agent1_imgs['down']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                        else:
                            this_agent1_move = 'null'
                            agent1.image = agent1_imgs['down']
                            
                            # store timing:
                            agent1_move_onset_time = globalClock.getTime() - trigger_time
                            thisExp.addData('agent1_move_onset', agent1_move_onset_time)
                            
                            agent1_move_since_round_start = globalClock.getTime() - round_start_time
                            thisExp.addData('agent1_move_onset_from_round_start', agent1_move_since_round_start)
                
                            win.flip()
                            
                        agent1.setPos(agent1_pos, log=True)
                        agent1_indicator_text.setPos(agent1_pos, log=True)
                        
                        if agent1_pos[0] > .3:
                            egg_right.setAutoDraw(False)
                        if agent1_pos[0] < -.3:
                            egg_left.setAutoDraw(False)
                        win.flip()
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in move_agent1Components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "move_agent1"-------
            for thisComponent in move_agent1Components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            player2_first.addData('instr_agent1.started', instr_agent1.tStartRefresh)
            player2_first.addData('instr_agent1.stopped', instr_agent1.tStopRefresh)
            #print('agent1', out_x, out_y, possiblemoves, resp_agent1.keys, agent1_pos)
            
            if this_agent1_move in ['up','down','left','right']:
                thisExp.addData(f'agent1_action', this_agent1_move)
            else:
                thisExp.addData(f'agent1_action', 'null')
            
            core.wait(agent1_jitter)
            agent1.image = agent1_imgs['down']
            win.flip()
            
            agent1_indicator_text.color = "black"
        # completed player2_turn repeats of 'player2_first'
        
        
        # ------Prepare to start Routine "end_turns"-------
        continueRoutine = True
        # update component parameters for each repeat
        cur_agents = [agent1, agent2, chick1]
        
        for this_agent in cur_agents:
            this_x, this_y, this_moves = convert_coords(round(this_agent.pos[0],2), round(this_agent.pos[1],2))
            thisExp.addData(f'{this_agent.name}_x', this_x)
            thisExp.addData(f'{this_agent.name}_y', this_y)
        # keep track of which components have finished
        end_turnsComponents = []
        for thisComponent in end_turnsComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        end_turnsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "end_turns"-------
        while continueRoutine:
            # get current time
            t = end_turnsClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=end_turnsClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in end_turnsComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "end_turns"-------
        for thisComponent in end_turnsComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        agent1_pts = 0 + current_time_bonus
        agent2_pts = 0 + current_time_bonus
        
        if (abs(agent2_pos[0]) > .35) and (abs(agent1_pos[0]) > .35):
            agent1_pts = 100 + current_time_bonus
            agent2_pts = 100 + current_time_bonus
            trials.nReps = 0
            trials.Finished = True
            endLoop = 1
            thisExp.addData('outcome', 'both defect')
            print('ending agent 1+2')
        elif (abs(agent1_pos[0]) > .35):
            agent1_pts = 100 + current_time_bonus
            agent2_pts = 0 + current_time_bonus
            trials.nReps = 0
            trials.Finished = True
            endLoop = 1
            thisExp.addData('outcome', 'agent1 defect')
            print('ending agent 1')
        elif (abs(agent2_pos[0]) > .35):
            agent1_pts = 0 + current_time_bonus
            agent2_pts = 100 + current_time_bonus
            trials.nReps = 0
            trials.Finished = True
            endLoop = 1
            thisExp.addData('outcome', 'agent2 defect')
            print('ending agent 2')
        else:
            thisExp.addData('outcome', 'none')
            
        if endLoop != 1:
            # compute chick 1 coords
            adjacent_spaces1 = get_adjacent_tiles(chick1_pos[0], chick1_pos[1])
            print(adjacent_spaces1)
            
            agent1_hunt1 = False
            if agent1_pos in adjacent_spaces1:
                agent1_hunt1 = True
                print('agent 1 hunt 1')
                
            agent2_hunt1 = False
            if agent2_pos in adjacent_spaces1:
                agent2_hunt1 = True
                print('agent 2 hunt 2')
            
            if nchicks == 1:
                if agent1_hunt1 and agent2_hunt1:
                    agent1_pts = 200 + current_time_bonus
                    agent2_pts = 200 + current_time_bonus
                    trials.nReps = 0
                    trials.Finished = True
                    endLoop = 1
                    thisExp.addData('outcome', 'cooperate')
                    print('ending agent 1+2')
        
            if nchicks >= 2:
                adjacent_spaces2 = get_adjacent_tiles(chick2_pos[0], chick2_pos[1])
                print(adjacent_spaces2)
                
                agent1_hunt2 = False
                if agent1_pos in adjacent_spaces2:
                    agent1_hunt2 = True
                    print('agent 1 hunt 2')
                    
                agent2_hunt2 = False
                if agent2_pos in adjacent_spaces2:
                    agent2_hunt2 = True
                    print('agent 2 hunt 2')
                
                if agent1_hunt1 and agent2_hunt1:
                    agent1_pts = 500 + current_time_bonus
                    agent2_pts = 200 + current_time_bonus
                    trials.nReps = 0
                    trials.Finished = True
                    endLoop = 1
                    print('ending agent 1+2')
                    
                if agent1_hunt2 and agent2_hunt2:
                    agent1_pts = 200 + current_time_bonus
                    agent2_pts = 500 + current_time_bonus
                    trials.nReps = 0
                    trials.Finished = True
                    endLoop = 1
                    print('ending agent 1+2')
        
        thisExp.addData('agent1_pts', agent1_pts)
        thisExp.addData('agent2_pts', agent2_pts)
        
        # the Routine "end_turns" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed ntrials repeats of 'trials'
    
    
    # ------Prepare to start Routine "end_round"-------
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('total_trials', TrialCount)
    agent1_score += agent1_pts
    agent2_score += agent2_pts
    
    thisExp.addData('agent1_score', agent1_score)
    thisExp.addData('agent2_score', agent2_score)
    # store timing:
    end_round_time = globalClock.getTime() - trigger_time
    thisExp.addData('round_end_onset', end_round_time)
    
    ITI_dur = np.random.uniform(2,3)
    thisExp.addData('ITI', ITI_dur)
    
    trial_text.setAutoDraw(False)
    GridWorldComponents = [diode_square_white, b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]
    
    for thisComponent in GridWorldComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
            
    AgentsComponents = [agent1, agent2, agent1_indicator_text, agent2_indicator_text, chick1]
    if nchicks >= 2:
        AgentsComponents += [chick2]
    
    if nchicks >= 3:
        AgentsComponents += [chick3]
        
    for thisComponent in AgentsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    if agent1_pts > 0:
        agent1_complete_text = f'PLAYER 1:\n+{agent1_pts} points\n\n'
    elif agent1_pts <= 0:
        agent1_complete_text = f'PLAYER 1:\n{agent1_pts} points\n\n'
    
    if agent2_pts > 0 :
        agent2_complete_text = f'PLAYER 2:\n+{agent2_pts} points'
    elif agent1_pts <= 0:
        agent2_complete_text = f'PLAYER 2:\n{agent2_pts} points'
    
    round_complete_text = f'ROUND COMPLETED\n\n' + agent1_complete_text + agent2_complete_text
    end_text.setText(round_complete_text)
    # keep track of which components have finished
    end_roundComponents = [end_text, diode_square]
    for thisComponent in end_roundComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    end_roundClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "end_round"-------
    while continueRoutine:
        # get current time
        t = end_roundClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=end_roundClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *end_text* updates
        if end_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            end_text.frameNStart = frameN  # exact frame index
            end_text.tStart = t  # local t and not account for scr refresh
            end_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end_text, 'tStartRefresh')  # time at next scr refresh
            end_text.setAutoDraw(True)
        if end_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > end_text.tStartRefresh + ITI_dur-frameTolerance:
                # keep track of stop time/frame for later
                end_text.tStop = t  # not accounting for scr refresh
                end_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(end_text, 'tStopRefresh')  # time at next scr refresh
                end_text.setAutoDraw(False)
        
        # *diode_square* updates
        if diode_square.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            diode_square.frameNStart = frameN  # exact frame index
            diode_square.tStart = t  # local t and not account for scr refresh
            diode_square.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(diode_square, 'tStartRefresh')  # time at next scr refresh
            diode_square.setAutoDraw(True)
        if diode_square.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > diode_square.tStartRefresh + ITI_dur-frameTolerance:
                # keep track of stop time/frame for later
                diode_square.tStop = t  # not accounting for scr refresh
                diode_square.frameNStop = frameN  # exact frame index
                win.timeOnFlip(diode_square, 'tStopRefresh')  # time at next scr refresh
                diode_square.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in end_roundComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "end_round"-------
    for thisComponent in end_roundComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    rounds.addData('end_text.started', end_text.tStartRefresh)
    rounds.addData('end_text.stopped', end_text.tStopRefresh)
    rounds.addData('diode_square.started', diode_square.tStartRefresh)
    rounds.addData('diode_square.stopped', diode_square.tStopRefresh)
    # the Routine "end_round" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 1.0 repeats of 'rounds'


# ------Prepare to start Routine "end_game"-------
continueRoutine = True
# update component parameters for each repeat
GridWorldComponents = [diode_square_white, b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

AgentsComponents = [agent1, agent2, agent1_indicator_text, agent2_indicator_text, chick1]
if nchicks >= 2:
    AgentsComponents += [chick2]

if nchicks >= 3:
    AgentsComponents += [chick3]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
        
end_text = f'Thanks for playing!\n\nPlayer 1 earned {agent1_score} points.\nPlayer 2 earned {agent2_score} points.\n\nPress any key to exit'


thanks.setText(end_text)
end_resp.keys = []
end_resp.rt = []
_end_resp_allKeys = []
# keep track of which components have finished
end_gameComponents = [thanks, end_resp]
for thisComponent in end_gameComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
end_gameClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end_game"-------
while continueRoutine:
    # get current time
    t = end_gameClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=end_gameClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *thanks* updates
    if thanks.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        thanks.frameNStart = frameN  # exact frame index
        thanks.tStart = t  # local t and not account for scr refresh
        thanks.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(thanks, 'tStartRefresh')  # time at next scr refresh
        thanks.setAutoDraw(True)
    
    # *end_resp* updates
    waitOnFlip = False
    if end_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_resp.frameNStart = frameN  # exact frame index
        end_resp.tStart = t  # local t and not account for scr refresh
        end_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_resp, 'tStartRefresh')  # time at next scr refresh
        end_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(end_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(end_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if end_resp.status == STARTED and not waitOnFlip:
        theseKeys = end_resp.getKeys(keyList=None, waitRelease=False)
        _end_resp_allKeys.extend(theseKeys)
        if len(_end_resp_allKeys):
            end_resp.keys = _end_resp_allKeys[-1].name  # just the last key pressed
            end_resp.rt = _end_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in end_gameComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end_game"-------
for thisComponent in end_gameComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('thanks.started', thanks.tStartRefresh)
thisExp.addData('thanks.stopped', thanks.tStopRefresh)
# check responses
if end_resp.keys in ['', [], None]:  # No response was made
    end_resp.keys = None
thisExp.addData('end_resp.keys',end_resp.keys)
if end_resp.keys != None:  # we had a response
    thisExp.addData('end_resp.rt', end_resp.rt)
thisExp.addData('end_resp.started', end_resp.tStartRefresh)
thisExp.addData('end_resp.stopped', end_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "end_game" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# --- Ending "GridWorld" ---
GridWorldComponents = [diode_square_white, egg_left, egg_right, b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# --- Ending "Agents" ---
AgentsComponents = [agent1, agent2, chick1]
if nchicks >= 2:
    AgentsComponents += [chick2]
    
if nchicks >= 3:
    AgentsComponents += [chick3]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
win.mouseVisible = True

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
