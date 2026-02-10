#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.1.2),
    on March 18, 2023, at 09:30
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

try:
    coord_df = pd.read_csv('C:\\Users\\Kevin\\Desktop\\EGGHUNT\\egghunttask\\coord_key.csv')
except:
    coord_df = pd.read_csv('coord_key.csv')

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


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.1.2'
expName = 'practice-egghunt'  # from the Builder filename that created this script
expInfo = {'patient id': '', 'player': [1,2], 'playerav': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/sub%s-%s_task-%s_%s' % (expInfo['player'], expInfo['patient id'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Shawn\\Documents\\GitHub\\Task_egghunt\\inperson_twoplayer\\ephys\\practice\\practice-egghunt-ephys.py',
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
    size=[1536, 864], fullscr=True, screen=0, 
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

egg_right = visual.ImageStim(
    win=win,
    name='egg_right', 
    image='stimuli/egg.png', mask=None, anchor='center',
    ori=0.0, pos=(.45, 0), size=(0.06, 0.06), #autoDraw=True,
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False, depth=-3.0)

GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]
for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

avatar1_no = expInfo['playerav']
agent1_imgs = {'stay':f'stimuli/avatars/avatar-{avatar1_no}_down.png',
               'up':f'stimuli/avatars/avatar-{avatar1_no}_up.png',
               'down':f'stimuli/avatars/avatar-{avatar1_no}_down.png',
               'left':f'stimuli/avatars/avatar-{avatar1_no}_left.png',
               'right':f'stimuli/avatars/avatar-{avatar1_no}_right.png'}
avatar2_no = 17
agent2_imgs = {'stay':f'stimuli/avatars/avatar-{avatar2_no}_down.png',
               'up':f'stimuli/avatars/avatar-{avatar2_no}_up.png',
               'down':f'stimuli/avatars/avatar-{avatar2_no}_down.png',
               'left':f'stimuli/avatars/avatar-{avatar2_no}_left.png',
               'right':f'stimuli/avatars/avatar-{avatar2_no}_right.png'}

PLAYER_START_IMG = agent1_imgs['down']

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
if expInfo['player'] == '1':
    player_num = '1'
    comp_num = '2'
    
    up_key = 'u'
    right_key = 'k'
    left_key = 'h'
    down_key = 'n'
    stay_key = 'j'
    moving_key_instr_txt = {'up':'Use \'u\' to move up',
                        'left':'Use \'h\' to move left',
                        'stay':'Use \'j\' to stay in place',
                        'right':'Use \'k\' to move right',
                        'down':'Use \'n\' to move down'}

elif expInfo['player'] == '2':
    player_num = '2'
    comp_num = '1'
    
    up_key = 'num_8'
    right_key = 'num_6'
    left_key = 'num_4'
    down_key = 'num_2'
    stay_key = 'num_5'
    moving_key_instr_txt = {'up':'Use \'8\' to move up',
                        'left':'Use \'4\' to move left',
                        'stay':'Use \'5\' to stay in place',
                        'right':'Use \'6\' to move right',
                        'down':'Use \'2\' to move down'}

PLAYER_TURN_TXT = f'PLAYER {player_num} TURN'
COMP_TURN_TXT = f'PLAYER {comp_num} TURN'

# Initialize components for Routine "overview"
overviewClock = core.Clock()
start_egg_1 = visual.ImageStim(
    win=win,
    name='start_egg_1', 
    image='stimuli/egg.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.15), size=(0.075, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

start_chicken_2 = visual.ImageStim(
    win=win,
    name='start_chicken_2', 
    image='stimuli/chicken_down.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -.15), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)

instr_back_txt = visual.TextStim(win=win, name='back_forth',
    text='',
    font='Arial',
    pos=(0, -.4), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

instr_back_txt.text = '\nPress RIGHT ARROW to continue.'
instr_back_txt.autoDraw = True
win.flip()
instr_keyboard = keyboard.Keyboard()

# Initialize components for Routine "movement_keys"
movement_keysClock = core.Clock()
text_3 = visual.TextStim(win=win, name='text_3',
    text='',
    font='Open Sans',
    pos=(0, -.45), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_10 = keyboard.Keyboard()
text_up = visual.TextStim(win=win, name='text_up',
    text='',
    font='Open Sans',
    pos=(0, .15), height=0.03, wrapWidth=0.2, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
text_down = visual.TextStim(win=win, name='text_down',
    text='',
    font='Open Sans',
    pos=(0, -.15), height=0.03, wrapWidth=0.2, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
text_stay = visual.TextStim(win=win, name='text_stay',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.03, wrapWidth=0.2, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
text_right = visual.TextStim(win=win, name='text_right',
    text='',
    font='Open Sans',
    pos=(.3, 0), height=0.03, wrapWidth=0.2, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
text_left = visual.TextStim(win=win, name='text_left',
    text='',
    font='Open Sans',
    pos=(-.3, 0), height=0.03, wrapWidth=0.2, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);
movement_instr_txt = visual.TextStim(win=win, name='movement_instr_txt',
    text='You will move around on the screen using the following keys. Please find these on your keyboard now.',
    font='Open Sans',
    pos=(0, .3), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-7.0);

# Initialize components for Routine "egg_self_start"
egg_self_startClock = core.Clock()
start_round_txt = visual.TextStim(win=win, name='start_round_txt',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
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
    ori=0.0, pos=(0, -.1), size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)
start_egg_self_txt = f'You are PLAYER {player_num}.\nTo begin this tutorial, let\'s try to collect an egg for 100 points. On the next screen, follow the instructions in red to collect one of the two eggs by moving to its location with your avatar.\n\n\n\n\n\nPress RIGHT ARROW to continue.'
key_resp_4 = keyboard.Keyboard()

# Initialize components for Routine "agent1_egg_self"
agent1_egg_selfClock = core.Clock()
resp_agent1 = keyboard.Keyboard()
instr_agent1 = visual.TextStim(win=win, name='instr_agent1',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
count1 = 0
instr_display_egg_self = visual.TextStim(win=win, name='instr_display_egg_self',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "comp_egg_self"
comp_egg_selfClock = core.Clock()
instr_computer = visual.TextStim(win=win, name='instr_computer',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
count1_comp = 0
instr_comp_turn_egg_self = visual.TextStim(win=win, name='instr_comp_turn_egg_self',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "egg_self_end"
egg_self_endClock = core.Clock()
end_txt_egg_self = visual.TextStim(win=win, name='end_txt_egg_self',
    text="Notice how you got to the egg before the other player. This earned you 100 points, but the other player did not receive any additional points. You both started with 150 points, but took 3 turns (so you lost 30 points). In total, you received 220 points, but the other player only received 120 points.\n\nOn other rounds, the other player may collect an egg before you. Let's see an example of how that could play out.\n\nPress RIGHT ARROW to continue.",
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_3 = keyboard.Keyboard()
if expInfo['player'] == '1':
    agent1_pts = 100+(150-30)
    agent2_pts = 150-30
elif expInfo['player'] == '2':
    agent1_pts = 150-30
    agent2_pts = 100+(150-30)
        
        
agent1_complete_text = f'PLAYER 1:\n+{agent1_pts} points\n\n'
agent2_complete_text = f'PLAYER 2:\n+{agent2_pts} points'

round_complete_text = f'ROUND COMPLETED\n\n' + agent1_complete_text + agent2_complete_text

end_text_2 = visual.TextStim(win=win, name='end_text_2',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-7.0);

# Initialize components for Routine "agent1_egg_other"
agent1_egg_otherClock = core.Clock()
resp_agent1_2 = keyboard.Keyboard()
instr_agent1_2 = visual.TextStim(win=win, name='instr_agent1_2',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
count2 = 0
instr_display_egg_self_2 = visual.TextStim(win=win, name='instr_display_egg_self_2',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "comp_egg_other"
comp_egg_otherClock = core.Clock()
instr_computer_2 = visual.TextStim(win=win, name='instr_computer_2',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
count2_comp = 0
instr_comp_turn_egg_other = visual.TextStim(win=win, name='instr_comp_turn_egg_other',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "egg_other_end"
egg_other_endClock = core.Clock()
end_txt_egg_self_2 = visual.TextStim(win=win, name='end_txt_egg_self_2',
    text="This time, the other player got to the egg before you. This earned them 100 points, but you did not receive any additional points. You both started with 150 points, but took 2 turns (so you lost 20 points). In total, the other player received 230 points, but you only received 130 points.\n\nOn some rounds, you may both be able to collect one of the eggs. Let's see an example of how that could play out.\n\nPress RIGHT ARROW to continue.",
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_5 = keyboard.Keyboard()
end_text_3 = visual.TextStim(win=win, name='end_text_3',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);

if expInfo['player'] == '1':
    agent1_pts2 = (150-20)
    agent2_pts2 = 100+(150-20)
elif expInfo['player'] == '2':
    agent1_pts2 = 100+(150-20)
    agent2_pts2 = (150-20)
agent1_complete_text2 = f'PLAYER 1:\n+{agent1_pts2} points\n\n'
agent2_complete_text2 = f'PLAYER 2:\n+{agent2_pts2} points'
round_complete_text2 = f'ROUND COMPLETED\n\n' + agent1_complete_text2 + agent2_complete_text2


# Initialize components for Routine "comp_egg_both"
comp_egg_bothClock = core.Clock()
instr_computer_3 = visual.TextStim(win=win, name='instr_computer_3',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
instr_comp_turn_egg_both = visual.TextStim(win=win, name='instr_comp_turn_egg_both',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "agent1_egg_both"
agent1_egg_bothClock = core.Clock()
resp_agent1_3 = keyboard.Keyboard()
instr_agent1_3 = visual.TextStim(win=win, name='instr_agent1_3',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
instr_display_egg_self_3 = visual.TextStim(win=win, name='instr_display_egg_self_3',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "egg_both_end"
egg_both_endClock = core.Clock()
end_txt_egg_self_4 = visual.TextStim(win=win, name='end_txt_egg_self_4',
    text='This time, both you and the other player collected an egg, which means that you both earned 100 points. You both started with 150 points, but took 1 turn (so you lost 10 points). In total, you both received 240 points.\n\nRemember that either one of you will be able to collect an egg or both of you depending on how you play the game.\n\nPress RIGHT ARROW to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_7 = keyboard.Keyboard()
end_text_4 = visual.TextStim(win=win, name='end_text_4',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
   
agent1_pts3 = 100+(150-10)
agent2_pts3 = 100+(150-10)
agent1_complete_text3 = f'PLAYER 1:\n+{agent1_pts3} points\n\n'
agent2_complete_text3 = f'PLAYER 2:\n+{agent2_pts3} points'
round_complete_text3 = f'ROUND COMPLETED\n\n' + agent1_complete_text3 + agent2_complete_text3


# Initialize components for Routine "catch_chick_start"
catch_chick_startClock = core.Clock()
end_txt_catch_chick = visual.TextStim(win=win, name='end_txt_catch_chick',
    text="You can also earn points if you catch the chicken. However, the chicken will often move away from players. You and the other player must work together to catch it! You can do this by moving to two spaces that are right next to the chicken.\n\nIf you catch a chicken, you will both collect the eggs that it lays and split the amount between the two of you. This is DOUBLE the amount of points from collecting an egg, but it is much more difficult. Let's see an example of how this might play out.\n\nPress RIGHT ARROW to continue.",
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_6 = keyboard.Keyboard()

# Initialize components for Routine "move_chick1"
move_chick1Clock = core.Clock()
chick1_instr_txt = 'CHICKEN TURN'
count1_chick = 0
instr_chick = visual.TextStim(win=win, name='instr_chick',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
instr_chick_turn_catch_chick = visual.TextStim(win=win, name='instr_chick_turn_catch_chick',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "agent_catch_chick"
agent_catch_chickClock = core.Clock()
resp_agent1_4 = keyboard.Keyboard()
instr_agent1_4 = visual.TextStim(win=win, name='instr_agent1_4',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
count4 = 0
instr_display_egg_self_4 = visual.TextStim(win=win, name='instr_display_egg_self_4',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "comp_catch_chick"
comp_catch_chickClock = core.Clock()
instr_computer_4 = visual.TextStim(win=win, name='instr_computer_4',
    text='',
    font='Open Sans',
    pos=(0, .45), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
count4_comp = 0
instr_comp_turn_egg_self_2 = visual.TextStim(win=win, name='instr_comp_turn_egg_self_2',
    text='',
    font='Open Sans',
    pos=(0, -.425), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "catch_chick_end"
catch_chick_endClock = core.Clock()
end_txt_egg_self_5 = visual.TextStim(win=win, name='end_txt_egg_self_5',
    text='You and the other player caught a chicken, which means that you each earned 200 points (400 total). You both started with 150 points, but took 3 turns (so you lost 30 points). In total, you both received 320 points.\n\nRemember you need to cooperate with the other player in order to catch the chicken because it will always try to escape the players. Be careful though because you lose 10 points for every turn you take.\n\nPress RIGHT ARROW to continue.',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_8 = keyboard.Keyboard()
end_text_5 = visual.TextStim(win=win, name='end_text_5',
    text='',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
agent1_pts4 = 200+(150-30)
agent2_pts4 = 200+(150-30)
agent1_complete_text4 = f'PLAYER 1:\n+{agent1_pts4} points\n\n'
agent2_complete_text4 = f'PLAYER 2:\n+{agent2_pts4} points'
round_complete_text4 = f'ROUND COMPLETED\n\n' + agent1_complete_text4 + agent2_complete_text4


# Initialize components for Routine "end_tutorial"
end_tutorialClock = core.Clock()
text_2 = visual.TextStim(win=win, name='text_2',
    text='You will next play multiple rounds of the game with another person.\n\nIn the real game, each player also only has 6 seconds to select a move during your turn. If you do not choose a move after 6 seconds, you will stay in the same space.\n\nThanks and please let the researcher know if you have any questions. Have fun!',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp_9 = keyboard.Keyboard()

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
AgentsComponents = [chick1, agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "start_exp" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "overview"-------
continueRoutine = True
# update component parameters for each repeat
instr_strs = {}
instr_strs[0] = f'In this game, you will collect as many eggs as you can to earn points! Points will be tallied and converted to real money at the end of the study.'
instr_strs[1] = f'You will be paired with another player. This player is also trying to earn points. You will take turns moving around the screen.'
instr_strs[2] = f'In this game, eggs are worth 100 points. You can collect an egg by moving to a tile with an egg.'
instr_strs[3] = f'You can also catch a chicken if you and the other player move to tile that are next to the chicken. Catching a chicken is worth 400 points, which is then split between the players (200 points each).'
instr_strs[4] = 'On each round, both of you will start with 150 points. 10 points will be subtracted for every turn taken. For example, 50 points will be subtracted from your score if you take 5 turns to end the round. Each round will end when you or the other player collects an egg or both of you catch the chicken together. Keep in mind that some rounds can end before you collect eggs or catch a chicken.'
instr_disp_txt = visual.TextStim(win=win, name='instructions',
    text='',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
instr_disp_txt.text = instr_strs[0]
instr_disp_txt.autoDraw = True

curr_instr = 0
instr_keyboard.keys = []
instr_keyboard.rt = []
_instr_keyboard_allKeys = []
# keep track of which components have finished
overviewComponents = [instr_keyboard]
for thisComponent in overviewComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
overviewClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "overview"-------
while continueRoutine:
    # get current time
    t = overviewClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=overviewClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    instr_keys = event.getKeys()
    
    if curr_instr == 0:
        instr_back_txt.text = '\nPress RIGHT ARROW to continue.'
    
        if 'right' in instr_keys or 'k' in instr_keys:
            instr_keyboard.clearEvents()
            curr_instr += 1
            instr_disp_txt.text = instr_strs[curr_instr]
            instr_back_txt.autoDraw = True
            win.flip()
    elif curr_instr == 4:
        instr_back_txt.text = 'Press LEFT ARROW to go back.\nPress RIGHT ARROW to continue.'
        if 'right' in instr_keys or 'k' in instr_keys:
            instr_keyboard.clearEvents()
            continueRoutine = False
        elif 'left' in instr_keys or 'h' in instr_keys:
            instr_keyboard.clearEvents()
            curr_instr -= 1
            instr_disp_txt.text = instr_strs[curr_instr]
            
            # if prev instr == 0, then remove left arrow as option
            if curr_instr == 0:
                instr_back_txt.autoDraw = False
            else:
                instr_back_txt.autoDraw = True
                
            win.flip()
    else:
        
        if curr_instr == 2:
            start_egg_1.setAutoDraw(True)
        elif curr_instr == 3:
            start_chicken_2.setAutoDraw(True)
        instr_back_txt.text = 'Press LEFT ARROW to go back.\nPress RIGHT ARROW to continue.'
        if 'right' in instr_keys or 'k' in instr_keys:
            instr_keyboard.clearEvents()
            curr_instr += 1
            instr_disp_txt.text = instr_strs[curr_instr]
            instr_back_txt.autoDraw = True
            win.flip()
            start_egg_1.setAutoDraw(False)
            start_chicken_2.setAutoDraw(False)
        elif 'left' in instr_keys or 'h' in instr_keys:
            instr_keyboard.clearEvents()
            curr_instr -= 1
            instr_disp_txt.text = instr_strs[curr_instr]
            
            start_egg_1.setAutoDraw(False)
            start_chicken_2.setAutoDraw(False)
            # if prev instr == 0, then remove left arrow as option
            if curr_instr == 0:
                instr_back_txt.text = '\nPress RIGHT ARROW to continue.'
            else:
                instr_back_txt.text = 'Press LEFT ARROW to go back.\nPress RIGHT ARROW to continue.'
                
            win.flip()
    
    # *instr_keyboard* updates
    waitOnFlip = False
    if instr_keyboard.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instr_keyboard.frameNStart = frameN  # exact frame index
        instr_keyboard.tStart = t  # local t and not account for scr refresh
        instr_keyboard.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instr_keyboard, 'tStartRefresh')  # time at next scr refresh
        instr_keyboard.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(instr_keyboard.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(instr_keyboard.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if instr_keyboard.status == STARTED and not waitOnFlip:
        theseKeys = instr_keyboard.getKeys(keyList=['left','right'], waitRelease=False)
        _instr_keyboard_allKeys.extend(theseKeys)
        if len(_instr_keyboard_allKeys):
            instr_keyboard.keys = _instr_keyboard_allKeys[-1].name  # just the last key pressed
            instr_keyboard.rt = _instr_keyboard_allKeys[-1].rt
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in overviewComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "overview"-------
for thisComponent in overviewComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
instr_back_txt.autoDraw = False
instr_disp_txt.autoDraw = False


start_chicken_2.setAutoDraw(False)
# check responses
if instr_keyboard.keys in ['', [], None]:  # No response was made
    instr_keyboard.keys = None
thisExp.addData('instr_keyboard.keys',instr_keyboard.keys)
if instr_keyboard.keys != None:  # we had a response
    thisExp.addData('instr_keyboard.rt', instr_keyboard.rt)
thisExp.addData('instr_keyboard.started', instr_keyboard.tStartRefresh)
thisExp.addData('instr_keyboard.stopped', instr_keyboard.tStopRefresh)
thisExp.nextEntry()
# the Routine "overview" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "movement_keys"-------
continueRoutine = True
# update component parameters for each repeat
text_3.setText('Press RIGHT ARROW to continue.')
key_resp_10.keys = []
key_resp_10.rt = []
_key_resp_10_allKeys = []
text_up.setText(moving_key_instr_txt['up'])
text_down.setText(moving_key_instr_txt['down'])
text_stay.setText(moving_key_instr_txt['stay'])
text_right.setText(moving_key_instr_txt['right'])
text_left.setText(moving_key_instr_txt['left'])
# keep track of which components have finished
movement_keysComponents = [text_3, key_resp_10, text_up, text_down, text_stay, text_right, text_left, movement_instr_txt]
for thisComponent in movement_keysComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
movement_keysClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "movement_keys"-------
while continueRoutine:
    # get current time
    t = movement_keysClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=movement_keysClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_3* updates
    if text_3.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
        # keep track of start time/frame for later
        text_3.frameNStart = frameN  # exact frame index
        text_3.tStart = t  # local t and not account for scr refresh
        text_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
        text_3.setAutoDraw(True)
    
    # *key_resp_10* updates
    waitOnFlip = False
    if key_resp_10.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
        # keep track of start time/frame for later
        key_resp_10.frameNStart = frameN  # exact frame index
        key_resp_10.tStart = t  # local t and not account for scr refresh
        key_resp_10.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_10, 'tStartRefresh')  # time at next scr refresh
        key_resp_10.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_10.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_10.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_10.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_10.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_10_allKeys.extend(theseKeys)
        if len(_key_resp_10_allKeys):
            key_resp_10.keys = _key_resp_10_allKeys[-1].name  # just the last key pressed
            key_resp_10.rt = _key_resp_10_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *text_up* updates
    if text_up.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_up.frameNStart = frameN  # exact frame index
        text_up.tStart = t  # local t and not account for scr refresh
        text_up.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_up, 'tStartRefresh')  # time at next scr refresh
        text_up.setAutoDraw(True)
    
    # *text_down* updates
    if text_down.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_down.frameNStart = frameN  # exact frame index
        text_down.tStart = t  # local t and not account for scr refresh
        text_down.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_down, 'tStartRefresh')  # time at next scr refresh
        text_down.setAutoDraw(True)
    
    # *text_stay* updates
    if text_stay.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_stay.frameNStart = frameN  # exact frame index
        text_stay.tStart = t  # local t and not account for scr refresh
        text_stay.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_stay, 'tStartRefresh')  # time at next scr refresh
        text_stay.setAutoDraw(True)
    
    # *text_right* updates
    if text_right.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_right.frameNStart = frameN  # exact frame index
        text_right.tStart = t  # local t and not account for scr refresh
        text_right.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_right, 'tStartRefresh')  # time at next scr refresh
        text_right.setAutoDraw(True)
    
    # *text_left* updates
    if text_left.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_left.frameNStart = frameN  # exact frame index
        text_left.tStart = t  # local t and not account for scr refresh
        text_left.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_left, 'tStartRefresh')  # time at next scr refresh
        text_left.setAutoDraw(True)
    
    # *movement_instr_txt* updates
    if movement_instr_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        movement_instr_txt.frameNStart = frameN  # exact frame index
        movement_instr_txt.tStart = t  # local t and not account for scr refresh
        movement_instr_txt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(movement_instr_txt, 'tStartRefresh')  # time at next scr refresh
        movement_instr_txt.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in movement_keysComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "movement_keys"-------
for thisComponent in movement_keysComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text_3.started', text_3.tStartRefresh)
thisExp.addData('text_3.stopped', text_3.tStopRefresh)
# check responses
if key_resp_10.keys in ['', [], None]:  # No response was made
    key_resp_10.keys = None
thisExp.addData('key_resp_10.keys',key_resp_10.keys)
if key_resp_10.keys != None:  # we had a response
    thisExp.addData('key_resp_10.rt', key_resp_10.rt)
thisExp.addData('key_resp_10.started', key_resp_10.tStartRefresh)
thisExp.addData('key_resp_10.stopped', key_resp_10.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('text_up.started', text_up.tStartRefresh)
thisExp.addData('text_up.stopped', text_up.tStopRefresh)
thisExp.addData('text_down.started', text_down.tStartRefresh)
thisExp.addData('text_down.stopped', text_down.tStopRefresh)
thisExp.addData('text_stay.started', text_stay.tStartRefresh)
thisExp.addData('text_stay.stopped', text_stay.tStopRefresh)
thisExp.addData('text_right.started', text_right.tStartRefresh)
thisExp.addData('text_right.stopped', text_right.tStopRefresh)
thisExp.addData('text_left.started', text_left.tStartRefresh)
thisExp.addData('text_left.stopped', text_left.tStopRefresh)
thisExp.addData('movement_instr_txt.started', movement_instr_txt.tStartRefresh)
thisExp.addData('movement_instr_txt.stopped', movement_instr_txt.tStopRefresh)
# the Routine "movement_keys" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "egg_self_start"-------
continueRoutine = True
# update component parameters for each repeat
agent1_indicator_text = visual.TextStim(win=win, 
    name='agent1_indicator_text',
    text=f'\n\n\n\n\n\n\nPLAYER {player_num}',
    font='Open Sans',
    pos=[0,0], 
    height=0.0145, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-20.0);
agent2_indicator_text = visual.TextStim(win=win, 
    name='agent2_indicator_text',
    text=f'\n\n\n\n\n\n\nPLAYER {comp_num}',
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
start_round_txt.setText(start_egg_self_txt)
start_round_player_display.setImage(PLAYER_START_IMG)
key_resp_4.keys = []
key_resp_4.rt = []
_key_resp_4_allKeys = []
# keep track of which components have finished
egg_self_startComponents = [start_round_txt, diode_square_round_start, start_round_player_display, key_resp_4]
for thisComponent in egg_self_startComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
egg_self_startClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "egg_self_start"-------
while continueRoutine:
    # get current time
    t = egg_self_startClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=egg_self_startClock)
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
    
    # *diode_square_round_start* updates
    if diode_square_round_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        diode_square_round_start.frameNStart = frameN  # exact frame index
        diode_square_round_start.tStart = t  # local t and not account for scr refresh
        diode_square_round_start.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(diode_square_round_start, 'tStartRefresh')  # time at next scr refresh
        diode_square_round_start.setAutoDraw(True)
    
    # *start_round_player_display* updates
    if start_round_player_display.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_round_player_display.frameNStart = frameN  # exact frame index
        start_round_player_display.tStart = t  # local t and not account for scr refresh
        start_round_player_display.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_round_player_display, 'tStartRefresh')  # time at next scr refresh
        start_round_player_display.setAutoDraw(True)
    
    # *key_resp_4* updates
    waitOnFlip = False
    if key_resp_4.status == NOT_STARTED and tThisFlip >= 3-frameTolerance:
        # keep track of start time/frame for later
        key_resp_4.frameNStart = frameN  # exact frame index
        key_resp_4.tStart = t  # local t and not account for scr refresh
        key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
        key_resp_4.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_4.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_4.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_4_allKeys.extend(theseKeys)
        if len(_key_resp_4_allKeys):
            key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
            key_resp_4.rt = _key_resp_4_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in egg_self_startComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "egg_self_start"-------
for thisComponent in egg_self_startComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
agent1_pos = [-.3, -.3]
agent2_pos = [.15, .3]
chick1_pos = [0, 0]

chick1.setPos(chick1_pos, log=True)
agent1.setPos(agent1_pos, log=True)
agent2.setPos(agent2_pos, log=True)
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
thisExp.addData('start_round_txt.started', start_round_txt.tStartRefresh)
thisExp.addData('start_round_txt.stopped', start_round_txt.tStopRefresh)
GridWorldComponents = [diode_square_white, b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)

AgentsComponents = [agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)
thisExp.addData('diode_square_round_start.started', diode_square_round_start.tStartRefresh)
thisExp.addData('diode_square_round_start.stopped', diode_square_round_start.tStopRefresh)
thisExp.addData('start_round_player_display.started', start_round_player_display.tStartRefresh)
thisExp.addData('start_round_player_display.stopped', start_round_player_display.tStopRefresh)
# check responses
if key_resp_4.keys in ['', [], None]:  # No response was made
    key_resp_4.keys = None
thisExp.addData('key_resp_4.keys',key_resp_4.keys)
if key_resp_4.keys != None:  # we had a response
    thisExp.addData('key_resp_4.rt', key_resp_4.rt)
thisExp.addData('key_resp_4.started', key_resp_4.tStartRefresh)
thisExp.addData('key_resp_4.stopped', key_resp_4.tStopRefresh)
thisExp.nextEntry()
# the Routine "egg_self_start" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
egg_self_loop = data.TrialHandler(nReps=3.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='egg_self_loop')
thisExp.addLoop(egg_self_loop)  # add the loop to the experiment
thisEgg_self_loop = egg_self_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisEgg_self_loop.rgb)
if thisEgg_self_loop != None:
    for paramName in thisEgg_self_loop:
        exec('{} = thisEgg_self_loop[paramName]'.format(paramName))

for thisEgg_self_loop in egg_self_loop:
    currentLoop = egg_self_loop
    # abbreviate parameter names if possible (e.g. rgb = thisEgg_self_loop.rgb)
    if thisEgg_self_loop != None:
        for paramName in thisEgg_self_loop:
            exec('{} = thisEgg_self_loop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "agent1_egg_self"-------
    continueRoutine = True
    # update component parameters for each repeat
    resp_agent1.keys = []
    resp_agent1.rt = []
    _resp_agent1_allKeys = []
    instr_agent1.setText(PLAYER_TURN_TXT)
    agent1_jitter = np.random.uniform(1,1.5)
    thisExp.addData('agent1_jitter', agent1_jitter)
    
    instr_agent1.bold = True
    agent1_indicator_text.color = "red"
    
    # remove possible move if adjacent to another agent
    count1 += 1
    if count1 == 1:
        possiblemoves = [up_key]
        this_instr_txt = f'Your turn. Press the {up_key.replace("num_","")} key to move up'
    elif count1 == 2:
        possiblemoves = [up_key]
        this_instr_txt = f'Your turn. Press the {up_key.replace("num_","")} key to move up'
    elif count1 == 3:
        possiblemoves = [left_key]
        this_instr_txt = f'Your turn.\nPress the {left_key.replace("num_","")} key to move left and collect the egg'
        
    this_agent1_move = ''
    instr_display_egg_self.setText(this_instr_txt)
    # keep track of which components have finished
    agent1_egg_selfComponents = [resp_agent1, instr_agent1, instr_display_egg_self]
    for thisComponent in agent1_egg_selfComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    agent1_egg_selfClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "agent1_egg_self"-------
    while continueRoutine:
        # get current time
        t = agent1_egg_selfClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=agent1_egg_selfClock)
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
        current_agent1_keyresp = resp_agent1.getKeys(clear=True)
        if resp_agent1.keys == 'escape':
            core.quit()
        if current_agent1_keyresp:
             if resp_agent1.keys in possiblemoves:
                if resp_agent1.keys == 'h' or resp_agent1.keys == 'num_4':
                    this_agent1_move = 'left'
                    agent1_pos = [agent1_pos[0]-.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['left']
                    
                    win.flip()
                elif resp_agent1.keys == 'k' or resp_agent1.keys == 'num_6':
                    this_agent1_move = 'right'
                    agent1_pos = [agent1_pos[0]+.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['right']
                    
                    win.flip()
                elif resp_agent1.keys == 'u' or resp_agent1.keys == 'num_8':
                    this_agent1_move = 'up'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]+.15]
                    agent1.image = agent1_imgs['up']
                    
                    win.flip()
                elif resp_agent1.keys == 'n' or resp_agent1.keys == 'num_2':
                    this_agent1_move = 'down'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]-.15]
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                else:
                    this_agent1_move = 'null'
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                    
                agent1.setPos(agent1_pos, log=True)
                agent1_indicator_text.setPos(agent1_pos, log=True)
                
                if agent1_pos[0] > .3:
                    egg_right.setAutoDraw(False)
                if agent1_pos[0] < -.3:
                    egg_left.setAutoDraw(False)
                win.flip()
                continueRoutine = False
        
        # *instr_display_egg_self* updates
        if instr_display_egg_self.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_display_egg_self.frameNStart = frameN  # exact frame index
            instr_display_egg_self.tStart = t  # local t and not account for scr refresh
            instr_display_egg_self.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_display_egg_self, 'tStartRefresh')  # time at next scr refresh
            instr_display_egg_self.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in agent1_egg_selfComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "agent1_egg_self"-------
    for thisComponent in agent1_egg_selfComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    egg_self_loop.addData('instr_agent1.started', instr_agent1.tStartRefresh)
    egg_self_loop.addData('instr_agent1.stopped', instr_agent1.tStopRefresh)
    if this_agent1_move in ['up','down','left','right']:
        thisExp.addData(f'agent1_action', this_agent1_move)
    else:
        thisExp.addData(f'agent1_action', 'null')
    
    core.wait(agent1_jitter)
    agent1.image = agent1_imgs['down']
    win.flip()
    
    agent1_indicator_text.color = "black"
    egg_self_loop.addData('instr_display_egg_self.started', instr_display_egg_self.tStartRefresh)
    egg_self_loop.addData('instr_display_egg_self.stopped', instr_display_egg_self.tStopRefresh)
    # the Routine "agent1_egg_self" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "comp_egg_self"-------
    continueRoutine = True
    # update component parameters for each repeat
    instr_computer.setText(COMP_TURN_TXT)
    instr_computer.bold = True
    agent2_indicator_text.color = "red"
    timer1 = core.Clock()
    
    count1_comp += 1
    if count1_comp == 1:
        # right
        x_shift = .15
        y_shift = 0
        this_comp_move_1 = 'right'
        this_comp_instr_txt = 'It is the other player\'s turn now'
    elif count1_comp == 2:
        # down
        x_shift = 0
        y_shift = -.15
        this_comp_move_1 = 'down'
        this_comp_instr_txt = 'It is the other player\'s turn now'
    elif count1_comp == 3:
        # down
        x_shift = 0
        y_shift = -.15
        this_comp_move_1 = 'down'
        this_comp_instr_txt = 'It is the other player\'s turn now'
    
    instr_comp_turn_egg_self.setText(this_comp_instr_txt)
    # keep track of which components have finished
    comp_egg_selfComponents = [instr_computer, instr_comp_turn_egg_self]
    for thisComponent in comp_egg_selfComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    comp_egg_selfClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "comp_egg_self"-------
    while continueRoutine:
        # get current time
        t = comp_egg_selfClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=comp_egg_selfClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr_computer* updates
        if instr_computer.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_computer.frameNStart = frameN  # exact frame index
            instr_computer.tStart = t  # local t and not account for scr refresh
            instr_computer.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_computer, 'tStartRefresh')  # time at next scr refresh
            instr_computer.setAutoDraw(True)
        if timer1.getTime()>2:
            
            agent2.image = agent2_imgs[this_comp_move_1]
            agent2_pos = [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift]
            agent2.setPos(agent2_pos, log=True)
            agent2_indicator_text.setPos(agent2_pos, log=True)
        
            win.flip()
            core.wait(1)
        
            agent2.image = agent2_imgs['down']
            win.flip()
            continueRoutine = False
        
        # *instr_comp_turn_egg_self* updates
        if instr_comp_turn_egg_self.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_comp_turn_egg_self.frameNStart = frameN  # exact frame index
            instr_comp_turn_egg_self.tStart = t  # local t and not account for scr refresh
            instr_comp_turn_egg_self.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_comp_turn_egg_self, 'tStartRefresh')  # time at next scr refresh
            instr_comp_turn_egg_self.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in comp_egg_selfComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "comp_egg_self"-------
    for thisComponent in comp_egg_selfComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    egg_self_loop.addData('instr_computer.started', instr_computer.tStartRefresh)
    egg_self_loop.addData('instr_computer.stopped', instr_computer.tStopRefresh)
    
    agent2_indicator_text.color = "black"
    egg_self_loop.addData('instr_comp_turn_egg_self.started', instr_comp_turn_egg_self.tStartRefresh)
    egg_self_loop.addData('instr_comp_turn_egg_self.stopped', instr_comp_turn_egg_self.tStopRefresh)
    # the Routine "comp_egg_self" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 3.0 repeats of 'egg_self_loop'


# ------Prepare to start Routine "egg_self_end"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_3.keys = []
key_resp_3.rt = []
_key_resp_3_allKeys = []
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

AgentsComponents = [chick1, agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

agent1_indicator_text.setAutoDraw(False)
agent2_indicator_text.setAutoDraw(False)
end_text_2.setText(round_complete_text)
# keep track of which components have finished
egg_self_endComponents = [end_txt_egg_self, key_resp_3, end_text_2]
for thisComponent in egg_self_endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
egg_self_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "egg_self_end"-------
while continueRoutine:
    # get current time
    t = egg_self_endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=egg_self_endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_txt_egg_self* updates
    if end_txt_egg_self.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
        # keep track of start time/frame for later
        end_txt_egg_self.frameNStart = frameN  # exact frame index
        end_txt_egg_self.tStart = t  # local t and not account for scr refresh
        end_txt_egg_self.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_txt_egg_self, 'tStartRefresh')  # time at next scr refresh
        end_txt_egg_self.setAutoDraw(True)
    
    # *key_resp_3* updates
    waitOnFlip = False
    if key_resp_3.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
        # keep track of start time/frame for later
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.tStart = t  # local t and not account for scr refresh
        key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_3.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_3.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_3_allKeys.extend(theseKeys)
        if len(_key_resp_3_allKeys):
            key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
            key_resp_3.rt = _key_resp_3_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *end_text_2* updates
    if end_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_text_2.frameNStart = frameN  # exact frame index
        end_text_2.tStart = t  # local t and not account for scr refresh
        end_text_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_text_2, 'tStartRefresh')  # time at next scr refresh
        end_text_2.setAutoDraw(True)
    if end_text_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end_text_2.tStartRefresh + 2-frameTolerance:
            # keep track of stop time/frame for later
            end_text_2.tStop = t  # not accounting for scr refresh
            end_text_2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end_text_2, 'tStopRefresh')  # time at next scr refresh
            end_text_2.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in egg_self_endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "egg_self_end"-------
for thisComponent in egg_self_endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('end_txt_egg_self.started', end_txt_egg_self.tStartRefresh)
thisExp.addData('end_txt_egg_self.stopped', end_txt_egg_self.tStopRefresh)
# check responses
if key_resp_3.keys in ['', [], None]:  # No response was made
    key_resp_3.keys = None
thisExp.addData('key_resp_3.keys',key_resp_3.keys)
if key_resp_3.keys != None:  # we had a response
    thisExp.addData('key_resp_3.rt', key_resp_3.rt)
thisExp.addData('key_resp_3.started', key_resp_3.tStartRefresh)
thisExp.addData('key_resp_3.stopped', key_resp_3.tStopRefresh)
thisExp.nextEntry()
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)

AgentsComponents = [agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)
agent1_pos = [.15, -.3]
agent2_pos = [-.15, 0]
chick1_pos = [0, .3]

chick1.setPos(chick1_pos, log=True)
agent1.setPos(agent1_pos, log=True)
agent2.setPos(agent2_pos, log=True)
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
thisExp.addData('end_text_2.started', end_text_2.tStartRefresh)
thisExp.addData('end_text_2.stopped', end_text_2.tStopRefresh)
# the Routine "egg_self_end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
egg_other_loop = data.TrialHandler(nReps=2.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='egg_other_loop')
thisExp.addLoop(egg_other_loop)  # add the loop to the experiment
thisEgg_other_loop = egg_other_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisEgg_other_loop.rgb)
if thisEgg_other_loop != None:
    for paramName in thisEgg_other_loop:
        exec('{} = thisEgg_other_loop[paramName]'.format(paramName))

for thisEgg_other_loop in egg_other_loop:
    currentLoop = egg_other_loop
    # abbreviate parameter names if possible (e.g. rgb = thisEgg_other_loop.rgb)
    if thisEgg_other_loop != None:
        for paramName in thisEgg_other_loop:
            exec('{} = thisEgg_other_loop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "agent1_egg_other"-------
    continueRoutine = True
    # update component parameters for each repeat
    resp_agent1_2.keys = []
    resp_agent1_2.rt = []
    _resp_agent1_2_allKeys = []
    instr_agent1_2.setText(PLAYER_TURN_TXT)
    agent1_jitter = np.random.uniform(1,1.5)
    thisExp.addData('agent1_jitter', agent1_jitter)
    
    instr_agent1_2.bold = True
    agent1_indicator_text.color = "red"
    
    # remove possible move if adjacent to another agent
    count2 += 1
    if count2 == 1:
        possiblemoves = [right_key]
        this_instr_txt = f'Your turn. Press the {right_key.replace("num_","")} key to move right'
    elif count2 == 2:
        possiblemoves = [up_key]
        this_instr_txt = f'Your turn.\nPress the {up_key.replace("num_","")} key to move up'
    
    this_agent1_move = ''
    instr_display_egg_self_2.setText(this_instr_txt)
    # keep track of which components have finished
    agent1_egg_otherComponents = [resp_agent1_2, instr_agent1_2, instr_display_egg_self_2]
    for thisComponent in agent1_egg_otherComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    agent1_egg_otherClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "agent1_egg_other"-------
    while continueRoutine:
        # get current time
        t = agent1_egg_otherClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=agent1_egg_otherClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *resp_agent1_2* updates
        waitOnFlip = False
        if resp_agent1_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            resp_agent1_2.frameNStart = frameN  # exact frame index
            resp_agent1_2.tStart = t  # local t and not account for scr refresh
            resp_agent1_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(resp_agent1_2, 'tStartRefresh')  # time at next scr refresh
            resp_agent1_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(resp_agent1_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(resp_agent1_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if resp_agent1_2.status == STARTED and not waitOnFlip:
            theseKeys = resp_agent1_2.getKeys(keyList=None, waitRelease=False)
            _resp_agent1_2_allKeys.extend(theseKeys)
            if len(_resp_agent1_2_allKeys):
                resp_agent1_2.keys = _resp_agent1_2_allKeys[-1].name  # just the last key pressed
                resp_agent1_2.rt = _resp_agent1_2_allKeys[-1].rt
        
        # *instr_agent1_2* updates
        if instr_agent1_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_agent1_2.frameNStart = frameN  # exact frame index
            instr_agent1_2.tStart = t  # local t and not account for scr refresh
            instr_agent1_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_agent1_2, 'tStartRefresh')  # time at next scr refresh
            instr_agent1_2.setAutoDraw(True)
        current_agent1_keyresp = resp_agent1_2.getKeys(clear=True)
        if resp_agent1_2.keys == 'escape':
            core.quit()
        if current_agent1_keyresp:
             if resp_agent1_2.keys in possiblemoves:
                if resp_agent1_2.keys == 'h' or resp_agent1_2.keys == 'num_4':
                    this_agent1_move = 'left'
                    agent1_pos = [agent1_pos[0]-.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['left']
                    
                    win.flip()
                elif resp_agent1_2.keys == 'k' or resp_agent1_2.keys == 'num_6':
                    this_agent1_move = 'right'
                    agent1_pos = [agent1_pos[0]+.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['right']
                    
                    win.flip()
                elif resp_agent1_2.keys == 'u' or resp_agent1_2.keys == 'num_8':
                    this_agent1_move = 'up'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]+.15]
                    agent1.image = agent1_imgs['up']
                    
                    win.flip()
                elif resp_agent1_2.keys == 'n' or resp_agent1_2.keys == 'num_2':
                    this_agent1_move = 'down'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]-.15]
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                else:
                    this_agent1_move = 'null'
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                    
                agent1.setPos(agent1_pos, log=True)
                agent1_indicator_text.setPos(agent1_pos, log=True)
                
                if agent1_pos[0] > .3:
                    egg_right.setAutoDraw(False)
                if agent1_pos[0] < -.3:
                    egg_left.setAutoDraw(False)
                win.flip()
                continueRoutine = False
        
        # *instr_display_egg_self_2* updates
        if instr_display_egg_self_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_display_egg_self_2.frameNStart = frameN  # exact frame index
            instr_display_egg_self_2.tStart = t  # local t and not account for scr refresh
            instr_display_egg_self_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_display_egg_self_2, 'tStartRefresh')  # time at next scr refresh
            instr_display_egg_self_2.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in agent1_egg_otherComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "agent1_egg_other"-------
    for thisComponent in agent1_egg_otherComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    egg_other_loop.addData('instr_agent1_2.started', instr_agent1_2.tStartRefresh)
    egg_other_loop.addData('instr_agent1_2.stopped', instr_agent1_2.tStopRefresh)
    if this_agent1_move in ['up','down','left','right']:
        thisExp.addData(f'agent1_action', this_agent1_move)
    else:
        thisExp.addData(f'agent1_action', 'null')
    
    core.wait(agent1_jitter)
    agent1.image = agent1_imgs['down']
    win.flip()
    
    agent1_indicator_text.color = "black"
    egg_other_loop.addData('instr_display_egg_self_2.started', instr_display_egg_self_2.tStartRefresh)
    egg_other_loop.addData('instr_display_egg_self_2.stopped', instr_display_egg_self_2.tStopRefresh)
    # the Routine "agent1_egg_other" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "comp_egg_other"-------
    continueRoutine = True
    # update component parameters for each repeat
    instr_computer_2.setText(COMP_TURN_TXT)
    instr_computer_2.bold = True
    agent2_indicator_text.color = "red"
    timer2 = core.Clock()
    
    count2_comp += 1
    if count2_comp == 1:
        # left
        x_shift = -.15
        y_shift = 0
        this_comp_move_2 = 'left'
        this_comp_instr_txt = 'It is the other player\'s turn now'
    elif count2_comp == 2:
        # left
        x_shift = -.15
        y_shift = 0
        this_comp_move_2 = 'left'
        this_comp_instr_txt = 'It is the other player\'s turn now'
    
    
    instr_comp_turn_egg_other.setText(this_comp_instr_txt)
    # keep track of which components have finished
    comp_egg_otherComponents = [instr_computer_2, instr_comp_turn_egg_other]
    for thisComponent in comp_egg_otherComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    comp_egg_otherClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "comp_egg_other"-------
    while continueRoutine:
        # get current time
        t = comp_egg_otherClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=comp_egg_otherClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr_computer_2* updates
        if instr_computer_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_computer_2.frameNStart = frameN  # exact frame index
            instr_computer_2.tStart = t  # local t and not account for scr refresh
            instr_computer_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_computer_2, 'tStartRefresh')  # time at next scr refresh
            instr_computer_2.setAutoDraw(True)
        if timer2.getTime()>2:
            
            agent2.image = agent2_imgs[this_comp_move_2]
            agent2_pos = [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift]
            agent2.setPos(agent2_pos, log=True)
            agent2_indicator_text.setPos(agent2_pos, log=True)
        
            if agent2_pos[0] > .3:
                egg_right.setAutoDraw(False)
            if agent2_pos[0] < -.3:
                egg_left.setAutoDraw(False)
            win.flip()
            core.wait(1)
        
            agent2.image = agent2_imgs['down']
            win.flip()
            continueRoutine = False
        
        
        # *instr_comp_turn_egg_other* updates
        if instr_comp_turn_egg_other.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_comp_turn_egg_other.frameNStart = frameN  # exact frame index
            instr_comp_turn_egg_other.tStart = t  # local t and not account for scr refresh
            instr_comp_turn_egg_other.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_comp_turn_egg_other, 'tStartRefresh')  # time at next scr refresh
            instr_comp_turn_egg_other.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in comp_egg_otherComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "comp_egg_other"-------
    for thisComponent in comp_egg_otherComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    egg_other_loop.addData('instr_computer_2.started', instr_computer_2.tStartRefresh)
    egg_other_loop.addData('instr_computer_2.stopped', instr_computer_2.tStopRefresh)
    
    agent2_indicator_text.color = "black"
    egg_other_loop.addData('instr_comp_turn_egg_other.started', instr_comp_turn_egg_other.tStartRefresh)
    egg_other_loop.addData('instr_comp_turn_egg_other.stopped', instr_comp_turn_egg_other.tStopRefresh)
    # the Routine "comp_egg_other" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 2.0 repeats of 'egg_other_loop'


# ------Prepare to start Routine "egg_other_end"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_5.keys = []
key_resp_5.rt = []
_key_resp_5_allKeys = []
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

AgentsComponents = [chick1, agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
agent1_indicator_text.setAutoDraw(False)
agent2_indicator_text.setAutoDraw(False)
end_text_3.setText(round_complete_text2)
# keep track of which components have finished
egg_other_endComponents = [end_txt_egg_self_2, key_resp_5, end_text_3]
for thisComponent in egg_other_endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
egg_other_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "egg_other_end"-------
while continueRoutine:
    # get current time
    t = egg_other_endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=egg_other_endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_txt_egg_self_2* updates
    if end_txt_egg_self_2.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
        # keep track of start time/frame for later
        end_txt_egg_self_2.frameNStart = frameN  # exact frame index
        end_txt_egg_self_2.tStart = t  # local t and not account for scr refresh
        end_txt_egg_self_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_txt_egg_self_2, 'tStartRefresh')  # time at next scr refresh
        end_txt_egg_self_2.setAutoDraw(True)
    
    # *key_resp_5* updates
    waitOnFlip = False
    if key_resp_5.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
        # keep track of start time/frame for later
        key_resp_5.frameNStart = frameN  # exact frame index
        key_resp_5.tStart = t  # local t and not account for scr refresh
        key_resp_5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_5, 'tStartRefresh')  # time at next scr refresh
        key_resp_5.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_5.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_5.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_5_allKeys.extend(theseKeys)
        if len(_key_resp_5_allKeys):
            key_resp_5.keys = _key_resp_5_allKeys[-1].name  # just the last key pressed
            key_resp_5.rt = _key_resp_5_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *end_text_3* updates
    if end_text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_text_3.frameNStart = frameN  # exact frame index
        end_text_3.tStart = t  # local t and not account for scr refresh
        end_text_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_text_3, 'tStartRefresh')  # time at next scr refresh
        end_text_3.setAutoDraw(True)
    if end_text_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end_text_3.tStartRefresh + 2-frameTolerance:
            # keep track of stop time/frame for later
            end_text_3.tStop = t  # not accounting for scr refresh
            end_text_3.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end_text_3, 'tStopRefresh')  # time at next scr refresh
            end_text_3.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in egg_other_endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "egg_other_end"-------
for thisComponent in egg_other_endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('end_txt_egg_self_2.started', end_txt_egg_self_2.tStartRefresh)
thisExp.addData('end_txt_egg_self_2.stopped', end_txt_egg_self_2.tStopRefresh)
# check responses
if key_resp_5.keys in ['', [], None]:  # No response was made
    key_resp_5.keys = None
thisExp.addData('key_resp_5.keys',key_resp_5.keys)
if key_resp_5.keys != None:  # we had a response
    thisExp.addData('key_resp_5.rt', key_resp_5.rt)
thisExp.addData('key_resp_5.started', key_resp_5.tStartRefresh)
thisExp.addData('key_resp_5.stopped', key_resp_5.tStopRefresh)
thisExp.nextEntry()
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)

AgentsComponents = [agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)
agent1_pos = [-.3, 0]
agent2_pos = [.3, 0]
chick1_pos = [0, -.3]

chick1.setPos(chick1_pos, log=True)
agent1.setPos(agent1_pos, log=True)
agent2.setPos(agent2_pos, log=True)
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
thisExp.addData('end_text_3.started', end_text_3.tStartRefresh)
thisExp.addData('end_text_3.stopped', end_text_3.tStopRefresh)
# the Routine "egg_other_end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
egg_both_loop = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='egg_both_loop')
thisExp.addLoop(egg_both_loop)  # add the loop to the experiment
thisEgg_both_loop = egg_both_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisEgg_both_loop.rgb)
if thisEgg_both_loop != None:
    for paramName in thisEgg_both_loop:
        exec('{} = thisEgg_both_loop[paramName]'.format(paramName))

for thisEgg_both_loop in egg_both_loop:
    currentLoop = egg_both_loop
    # abbreviate parameter names if possible (e.g. rgb = thisEgg_both_loop.rgb)
    if thisEgg_both_loop != None:
        for paramName in thisEgg_both_loop:
            exec('{} = thisEgg_both_loop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "comp_egg_both"-------
    continueRoutine = True
    # update component parameters for each repeat
    instr_computer_3.setText(COMP_TURN_TXT)
    instr_computer_3.bold = True
    agent2_indicator_text.color = "red"
    timer3 = core.Clock()
    
    x_shift = .15
    y_shift = 0
    this_comp_move_3 = 'right'
    this_comp_instr_txt = 'It is the other player\'s turn'
    instr_comp_turn_egg_both.setText(this_comp_instr_txt)
    # keep track of which components have finished
    comp_egg_bothComponents = [instr_computer_3, instr_comp_turn_egg_both]
    for thisComponent in comp_egg_bothComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    comp_egg_bothClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "comp_egg_both"-------
    while continueRoutine:
        # get current time
        t = comp_egg_bothClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=comp_egg_bothClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr_computer_3* updates
        if instr_computer_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_computer_3.frameNStart = frameN  # exact frame index
            instr_computer_3.tStart = t  # local t and not account for scr refresh
            instr_computer_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_computer_3, 'tStartRefresh')  # time at next scr refresh
            instr_computer_3.setAutoDraw(True)
        if timer3.getTime()>2:
            
            agent2.image = agent2_imgs[this_comp_move_3]
            agent2_pos = [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift]
            agent2.setPos(agent2_pos, log=True)
            agent2_indicator_text.setPos(agent2_pos, log=True)
        
            if agent2_pos[0] > .3:
                egg_right.setAutoDraw(False)
            if agent2_pos[0] < -.3:
                egg_left.setAutoDraw(False)
            win.flip()
            core.wait(1)
        
            agent2.image = agent2_imgs['down']
            win.flip()
            continueRoutine = False
        
        # *instr_comp_turn_egg_both* updates
        if instr_comp_turn_egg_both.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_comp_turn_egg_both.frameNStart = frameN  # exact frame index
            instr_comp_turn_egg_both.tStart = t  # local t and not account for scr refresh
            instr_comp_turn_egg_both.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_comp_turn_egg_both, 'tStartRefresh')  # time at next scr refresh
            instr_comp_turn_egg_both.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in comp_egg_bothComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "comp_egg_both"-------
    for thisComponent in comp_egg_bothComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    egg_both_loop.addData('instr_computer_3.started', instr_computer_3.tStartRefresh)
    egg_both_loop.addData('instr_computer_3.stopped', instr_computer_3.tStopRefresh)
    
    agent2_indicator_text.color = "black"
    egg_both_loop.addData('instr_comp_turn_egg_both.started', instr_comp_turn_egg_both.tStartRefresh)
    egg_both_loop.addData('instr_comp_turn_egg_both.stopped', instr_comp_turn_egg_both.tStopRefresh)
    # the Routine "comp_egg_both" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "agent1_egg_both"-------
    continueRoutine = True
    # update component parameters for each repeat
    resp_agent1_3.keys = []
    resp_agent1_3.rt = []
    _resp_agent1_3_allKeys = []
    instr_agent1_3.setText(PLAYER_TURN_TXT)
    agent1_jitter = np.random.uniform(1,1.5)
    thisExp.addData('agent1_jitter', agent1_jitter)
    
    instr_agent1_3.bold = True
    agent1_indicator_text.color = "red"
    
    # remove possible move if adjacent to another agent
    possiblemoves = [left_key]
    this_instr_txt = f'Your turn. Both of you can collect an egg this time.\nPress the {left_key.replace("num_","")} key to move left to collect the egg'
    
    this_agent1_move = ''
    instr_display_egg_self_3.setText(this_instr_txt)
    # keep track of which components have finished
    agent1_egg_bothComponents = [resp_agent1_3, instr_agent1_3, instr_display_egg_self_3]
    for thisComponent in agent1_egg_bothComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    agent1_egg_bothClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "agent1_egg_both"-------
    while continueRoutine:
        # get current time
        t = agent1_egg_bothClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=agent1_egg_bothClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *resp_agent1_3* updates
        waitOnFlip = False
        if resp_agent1_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            resp_agent1_3.frameNStart = frameN  # exact frame index
            resp_agent1_3.tStart = t  # local t and not account for scr refresh
            resp_agent1_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(resp_agent1_3, 'tStartRefresh')  # time at next scr refresh
            resp_agent1_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(resp_agent1_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(resp_agent1_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if resp_agent1_3.status == STARTED and not waitOnFlip:
            theseKeys = resp_agent1_3.getKeys(keyList=None, waitRelease=False)
            _resp_agent1_3_allKeys.extend(theseKeys)
            if len(_resp_agent1_3_allKeys):
                resp_agent1_3.keys = _resp_agent1_3_allKeys[-1].name  # just the last key pressed
                resp_agent1_3.rt = _resp_agent1_3_allKeys[-1].rt
        
        # *instr_agent1_3* updates
        if instr_agent1_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_agent1_3.frameNStart = frameN  # exact frame index
            instr_agent1_3.tStart = t  # local t and not account for scr refresh
            instr_agent1_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_agent1_3, 'tStartRefresh')  # time at next scr refresh
            instr_agent1_3.setAutoDraw(True)
        current_agent1_keyresp = resp_agent1_3.getKeys(clear=True)
        if resp_agent1_3.keys == 'escape':
            core.quit()
        if current_agent1_keyresp:
             if resp_agent1_3.keys in possiblemoves:
                if resp_agent1_3.keys == 'h' or resp_agent1_3.keys == 'num_4':
                    this_agent1_move = 'left'
                    agent1_pos = [agent1_pos[0]-.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['left']
                    
                    win.flip()
                elif resp_agent1_3.keys == 'k' or resp_agent1_3.keys == 'num_6':
                    this_agent1_move = 'right'
                    agent1_pos = [agent1_pos[0]+.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['right']
                    
                    win.flip()
                elif resp_agent1_3.keys == 'u' or resp_agent1_3.keys == 'num_8':
                    this_agent1_move = 'up'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]+.15]
                    agent1.image = agent1_imgs['up']
                    
                    win.flip()
                elif resp_agent1_3.keys == 'n' or resp_agent1_3.keys == 'num_2':
                    this_agent1_move = 'down'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]-.15]
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                else:
                    this_agent1_move = 'null'
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                    
                agent1.setPos(agent1_pos, log=True)
                agent1_indicator_text.setPos(agent1_pos, log=True)
                
                if agent1_pos[0] > .3:
                    egg_right.setAutoDraw(False)
                if agent1_pos[0] < -.3:
                    egg_left.setAutoDraw(False)
                win.flip()
                continueRoutine = False
        
        # *instr_display_egg_self_3* updates
        if instr_display_egg_self_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_display_egg_self_3.frameNStart = frameN  # exact frame index
            instr_display_egg_self_3.tStart = t  # local t and not account for scr refresh
            instr_display_egg_self_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_display_egg_self_3, 'tStartRefresh')  # time at next scr refresh
            instr_display_egg_self_3.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in agent1_egg_bothComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "agent1_egg_both"-------
    for thisComponent in agent1_egg_bothComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    egg_both_loop.addData('instr_agent1_3.started', instr_agent1_3.tStartRefresh)
    egg_both_loop.addData('instr_agent1_3.stopped', instr_agent1_3.tStopRefresh)
    if this_agent1_move in ['up','down','left','right']:
        thisExp.addData(f'agent1_action', this_agent1_move)
    else:
        thisExp.addData(f'agent1_action', 'null')
    
    core.wait(agent1_jitter)
    agent1.image = agent1_imgs['down']
    win.flip()
    
    agent1_indicator_text.color = "black"
    egg_both_loop.addData('instr_display_egg_self_3.started', instr_display_egg_self_3.tStartRefresh)
    egg_both_loop.addData('instr_display_egg_self_3.stopped', instr_display_egg_self_3.tStopRefresh)
    # the Routine "agent1_egg_both" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 1.0 repeats of 'egg_both_loop'


# ------Prepare to start Routine "egg_both_end"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_7.keys = []
key_resp_7.rt = []
_key_resp_7_allKeys = []
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

AgentsComponents = [chick1, agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
end_text_4.setText(round_complete_text3)
agent1_indicator_text.setAutoDraw(False)
agent2_indicator_text.setAutoDraw(False)
# keep track of which components have finished
egg_both_endComponents = [end_txt_egg_self_4, key_resp_7, end_text_4]
for thisComponent in egg_both_endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
egg_both_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "egg_both_end"-------
while continueRoutine:
    # get current time
    t = egg_both_endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=egg_both_endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_txt_egg_self_4* updates
    if end_txt_egg_self_4.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
        # keep track of start time/frame for later
        end_txt_egg_self_4.frameNStart = frameN  # exact frame index
        end_txt_egg_self_4.tStart = t  # local t and not account for scr refresh
        end_txt_egg_self_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_txt_egg_self_4, 'tStartRefresh')  # time at next scr refresh
        end_txt_egg_self_4.setAutoDraw(True)
    
    # *key_resp_7* updates
    waitOnFlip = False
    if key_resp_7.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
        # keep track of start time/frame for later
        key_resp_7.frameNStart = frameN  # exact frame index
        key_resp_7.tStart = t  # local t and not account for scr refresh
        key_resp_7.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_7, 'tStartRefresh')  # time at next scr refresh
        key_resp_7.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_7.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_7.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_7.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_7.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_7_allKeys.extend(theseKeys)
        if len(_key_resp_7_allKeys):
            key_resp_7.keys = _key_resp_7_allKeys[-1].name  # just the last key pressed
            key_resp_7.rt = _key_resp_7_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *end_text_4* updates
    if end_text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_text_4.frameNStart = frameN  # exact frame index
        end_text_4.tStart = t  # local t and not account for scr refresh
        end_text_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_text_4, 'tStartRefresh')  # time at next scr refresh
        end_text_4.setAutoDraw(True)
    if end_text_4.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end_text_4.tStartRefresh + 2-frameTolerance:
            # keep track of stop time/frame for later
            end_text_4.tStop = t  # not accounting for scr refresh
            end_text_4.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end_text_4, 'tStopRefresh')  # time at next scr refresh
            end_text_4.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in egg_both_endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "egg_both_end"-------
for thisComponent in egg_both_endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('end_txt_egg_self_4.started', end_txt_egg_self_4.tStartRefresh)
thisExp.addData('end_txt_egg_self_4.stopped', end_txt_egg_self_4.tStopRefresh)
# check responses
if key_resp_7.keys in ['', [], None]:  # No response was made
    key_resp_7.keys = None
thisExp.addData('key_resp_7.keys',key_resp_7.keys)
if key_resp_7.keys != None:  # we had a response
    thisExp.addData('key_resp_7.rt', key_resp_7.rt)
thisExp.addData('key_resp_7.started', key_resp_7.tStartRefresh)
thisExp.addData('key_resp_7.stopped', key_resp_7.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('end_text_4.started', end_text_4.tStartRefresh)
thisExp.addData('end_text_4.stopped', end_text_4.tStopRefresh)
# the Routine "egg_both_end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "catch_chick_start"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_6.keys = []
key_resp_6.rt = []
_key_resp_6_allKeys = []
# keep track of which components have finished
catch_chick_startComponents = [end_txt_catch_chick, key_resp_6]
for thisComponent in catch_chick_startComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
catch_chick_startClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "catch_chick_start"-------
while continueRoutine:
    # get current time
    t = catch_chick_startClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=catch_chick_startClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_txt_catch_chick* updates
    if end_txt_catch_chick.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_txt_catch_chick.frameNStart = frameN  # exact frame index
        end_txt_catch_chick.tStart = t  # local t and not account for scr refresh
        end_txt_catch_chick.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_txt_catch_chick, 'tStartRefresh')  # time at next scr refresh
        end_txt_catch_chick.setAutoDraw(True)
    
    # *key_resp_6* updates
    waitOnFlip = False
    if key_resp_6.status == NOT_STARTED and tThisFlip >= 3-frameTolerance:
        # keep track of start time/frame for later
        key_resp_6.frameNStart = frameN  # exact frame index
        key_resp_6.tStart = t  # local t and not account for scr refresh
        key_resp_6.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_6, 'tStartRefresh')  # time at next scr refresh
        key_resp_6.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_6.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_6.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_6.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_6.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_6_allKeys.extend(theseKeys)
        if len(_key_resp_6_allKeys):
            key_resp_6.keys = _key_resp_6_allKeys[-1].name  # just the last key pressed
            key_resp_6.rt = _key_resp_6_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in catch_chick_startComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "catch_chick_start"-------
for thisComponent in catch_chick_startComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('end_txt_catch_chick.started', end_txt_catch_chick.tStartRefresh)
thisExp.addData('end_txt_catch_chick.stopped', end_txt_catch_chick.tStopRefresh)
# check responses
if key_resp_6.keys in ['', [], None]:  # No response was made
    key_resp_6.keys = None
thisExp.addData('key_resp_6.keys',key_resp_6.keys)
if key_resp_6.keys != None:  # we had a response
    thisExp.addData('key_resp_6.rt', key_resp_6.rt)
thisExp.addData('key_resp_6.started', key_resp_6.tStartRefresh)
thisExp.addData('key_resp_6.stopped', key_resp_6.tStopRefresh)
thisExp.nextEntry()
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)

AgentsComponents = [chick1, agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(True)
agent1_pos = [0,-.15]
agent2_pos = [-.3, .3]
chick1_pos = [-.3,0]

chick1.setPos(chick1_pos, log=True)
agent1.setPos(agent1_pos, log=True)
agent2.setPos(agent2_pos, log=True)
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
# the Routine "catch_chick_start" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
catch_chick_loop = data.TrialHandler(nReps=3.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='catch_chick_loop')
thisExp.addLoop(catch_chick_loop)  # add the loop to the experiment
thisCatch_chick_loop = catch_chick_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisCatch_chick_loop.rgb)
if thisCatch_chick_loop != None:
    for paramName in thisCatch_chick_loop:
        exec('{} = thisCatch_chick_loop[paramName]'.format(paramName))

for thisCatch_chick_loop in catch_chick_loop:
    currentLoop = catch_chick_loop
    # abbreviate parameter names if possible (e.g. rgb = thisCatch_chick_loop.rgb)
    if thisCatch_chick_loop != None:
        for paramName in thisCatch_chick_loop:
            exec('{} = thisCatch_chick_loop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "move_chick1"-------
    continueRoutine = True
    # update component parameters for each repeat
    instr_chick.bold = True
    instr_chick.bold = True
    chick_jitter = np.random.uniform(2,3)
    chick_timer = core.Clock()
    
    count1_chick += 1
    if count1_chick == 1:
        # down
        x_shift = 0
        y_shift = -.15
        this_chick_move_4 = 'down'
        this_chick_instr_txt = 'The chicken moves first'
    elif count1_chick == 2:
        # down
        x_shift = 0
        y_shift = -.15
        this_chick_move_4 = 'down'
        this_chick_instr_txt = 'It is the chicken\'s turn now'
    elif count1_chick == 3:
        # down
        x_shift = 0
        y_shift = 0
        this_chick_move_4 = 'stay'
        this_chick_instr_txt = 'It is the chicken\'s turn now'
    
    instr_chick.setText(chick1_instr_txt)
    instr_chick_turn_catch_chick.setText(this_chick_instr_txt)
    # keep track of which components have finished
    move_chick1Components = [instr_chick, instr_chick_turn_catch_chick]
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
            
            chick1.image = chick1_imgs[this_chick_move_4]
            chick1_pos = [chick1_pos[0]+x_shift, chick1_pos[1]+y_shift]
            chick1.setPos(chick1_pos, log=True)
        
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
        
        # *instr_chick_turn_catch_chick* updates
        if instr_chick_turn_catch_chick.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_chick_turn_catch_chick.frameNStart = frameN  # exact frame index
            instr_chick_turn_catch_chick.tStart = t  # local t and not account for scr refresh
            instr_chick_turn_catch_chick.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_chick_turn_catch_chick, 'tStartRefresh')  # time at next scr refresh
            instr_chick_turn_catch_chick.setAutoDraw(True)
        
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
    catch_chick_loop.addData('instr_chick.started', instr_chick.tStartRefresh)
    catch_chick_loop.addData('instr_chick.stopped', instr_chick.tStopRefresh)
    catch_chick_loop.addData('instr_chick_turn_catch_chick.started', instr_chick_turn_catch_chick.tStartRefresh)
    catch_chick_loop.addData('instr_chick_turn_catch_chick.stopped', instr_chick_turn_catch_chick.tStopRefresh)
    # the Routine "move_chick1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "agent_catch_chick"-------
    continueRoutine = True
    # update component parameters for each repeat
    resp_agent1_4.keys = []
    resp_agent1_4.rt = []
    _resp_agent1_4_allKeys = []
    instr_agent1_4.setText(PLAYER_TURN_TXT)
    agent1_jitter = np.random.uniform(1,1.5)
    thisExp.addData('agent1_jitter', agent1_jitter)
    
    instr_agent1_4.bold = True
    agent1_indicator_text.color = "red"
    
    # remove possible move if adjacent to another agent
    count4 += 1
    if count4 == 1:
        possiblemoves = [down_key]
        this_instr_txt = f'Your turn. Press the {down_key.replace("num_","")} key to move down'
    elif count4 == 2:
        possiblemoves = [left_key]
        this_instr_txt = f'Your turn. Press the {left_key.replace("num_","")} key to move left'
    elif count4 == 3:
        possiblemoves = [stay_key]
        this_instr_txt = f'You arrived to the chicken first. Press the {stay_key.replace("num_","")} key to stay in place to wait for the other player'
    
    this_agent1_move = ''
    instr_display_egg_self_4.setText(this_instr_txt)
    # keep track of which components have finished
    agent_catch_chickComponents = [resp_agent1_4, instr_agent1_4, instr_display_egg_self_4]
    for thisComponent in agent_catch_chickComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    agent_catch_chickClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "agent_catch_chick"-------
    while continueRoutine:
        # get current time
        t = agent_catch_chickClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=agent_catch_chickClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *resp_agent1_4* updates
        waitOnFlip = False
        if resp_agent1_4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            resp_agent1_4.frameNStart = frameN  # exact frame index
            resp_agent1_4.tStart = t  # local t and not account for scr refresh
            resp_agent1_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(resp_agent1_4, 'tStartRefresh')  # time at next scr refresh
            resp_agent1_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(resp_agent1_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(resp_agent1_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if resp_agent1_4.status == STARTED and not waitOnFlip:
            theseKeys = resp_agent1_4.getKeys(keyList=None, waitRelease=False)
            _resp_agent1_4_allKeys.extend(theseKeys)
            if len(_resp_agent1_4_allKeys):
                resp_agent1_4.keys = _resp_agent1_4_allKeys[-1].name  # just the last key pressed
                resp_agent1_4.rt = _resp_agent1_4_allKeys[-1].rt
        
        # *instr_agent1_4* updates
        if instr_agent1_4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_agent1_4.frameNStart = frameN  # exact frame index
            instr_agent1_4.tStart = t  # local t and not account for scr refresh
            instr_agent1_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_agent1_4, 'tStartRefresh')  # time at next scr refresh
            instr_agent1_4.setAutoDraw(True)
        current_agent1_keyresp = resp_agent1_4.getKeys(clear=True)
        if resp_agent1_4.keys == 'escape':
            core.quit()
        if current_agent1_keyresp:
             if resp_agent1_4.keys in possiblemoves:
                if resp_agent1_4.keys == 'h' or resp_agent1_4.keys == 'num_4':
                    this_agent1_move = 'left'
                    agent1_pos = [agent1_pos[0]-.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['left']
                    
                    win.flip()
                elif resp_agent1_4.keys == 'k' or resp_agent1_4.keys == 'num_6':
                    this_agent1_move = 'right'
                    agent1_pos = [agent1_pos[0]+.15, agent1_pos[1]]
                    agent1.image = agent1_imgs['right']
                    
                    win.flip()
                elif resp_agent1_4.keys == 'u' or resp_agent1_4.keys == 'num_8':
                    this_agent1_move = 'up'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]+.15]
                    agent1.image = agent1_imgs['up']
                    
                    win.flip()
                elif resp_agent1_4.keys == 'n' or resp_agent1_4.keys == 'num_2':
                    this_agent1_move = 'down'
                    agent1_pos = [agent1_pos[0], agent1_pos[1]-.15]
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                else:
                    this_agent1_move = 'null'
                    agent1.image = agent1_imgs['down']
                    
                    win.flip()
                    
                agent1.setPos(agent1_pos, log=True)
                agent1_indicator_text.setPos(agent1_pos, log=True)
                
                if agent1_pos[0] > .3:
                    egg_right.setAutoDraw(False)
                if agent1_pos[0] < -.3:
                    egg_left.setAutoDraw(False)
                win.flip()
                continueRoutine = False
        
        # *instr_display_egg_self_4* updates
        if instr_display_egg_self_4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_display_egg_self_4.frameNStart = frameN  # exact frame index
            instr_display_egg_self_4.tStart = t  # local t and not account for scr refresh
            instr_display_egg_self_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_display_egg_self_4, 'tStartRefresh')  # time at next scr refresh
            instr_display_egg_self_4.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in agent_catch_chickComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "agent_catch_chick"-------
    for thisComponent in agent_catch_chickComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    catch_chick_loop.addData('instr_agent1_4.started', instr_agent1_4.tStartRefresh)
    catch_chick_loop.addData('instr_agent1_4.stopped', instr_agent1_4.tStopRefresh)
    if this_agent1_move in ['up','down','left','right']:
        thisExp.addData(f'agent1_action', this_agent1_move)
    else:
        thisExp.addData(f'agent1_action', 'null')
    
    core.wait(agent1_jitter)
    agent1.image = agent1_imgs['down']
    win.flip()
    
    agent1_indicator_text.color = "black"
    catch_chick_loop.addData('instr_display_egg_self_4.started', instr_display_egg_self_4.tStartRefresh)
    catch_chick_loop.addData('instr_display_egg_self_4.stopped', instr_display_egg_self_4.tStopRefresh)
    # the Routine "agent_catch_chick" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "comp_catch_chick"-------
    continueRoutine = True
    # update component parameters for each repeat
    instr_computer_4.setText(COMP_TURN_TXT)
    instr_computer_4.bold = True
    agent2_indicator_text.color = "red"
    timer4 = core.Clock()
    
    count4_comp += 1
    if count4_comp == 1:
        # down
        x_shift = 0
        y_shift = -.15
        this_comp_move_4 = 'down'
        this_comp_instr_txt = 'It is the other player\'s turn now'
    elif count4_comp == 2:
        # down
        x_shift = 0
        y_shift = -.15
        this_comp_move_4 = 'down'
        this_comp_instr_txt = 'It is the other player\'s turn now, but they can\'t catch the chicken yet'
    elif count4_comp == 3:
        # down
        x_shift = 0
        y_shift = -.15
        this_comp_move_4 = 'down'
        this_comp_instr_txt = 'Now the other player can catch the chicken with you'
    
    instr_comp_turn_egg_self_2.setText(this_comp_instr_txt)
    # keep track of which components have finished
    comp_catch_chickComponents = [instr_computer_4, instr_comp_turn_egg_self_2]
    for thisComponent in comp_catch_chickComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    comp_catch_chickClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "comp_catch_chick"-------
    while continueRoutine:
        # get current time
        t = comp_catch_chickClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=comp_catch_chickClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instr_computer_4* updates
        if instr_computer_4.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_computer_4.frameNStart = frameN  # exact frame index
            instr_computer_4.tStart = t  # local t and not account for scr refresh
            instr_computer_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_computer_4, 'tStartRefresh')  # time at next scr refresh
            instr_computer_4.setAutoDraw(True)
        if timer4.getTime()>2:
            
            agent2.image = agent2_imgs[this_comp_move_4]
            agent2_pos = [agent2_pos[0]+x_shift, agent2_pos[1]+y_shift]
            agent2.setPos(agent2_pos, log=True)
            agent2_indicator_text.setPos(agent2_pos, log=True)
        
            win.flip()
            core.wait(1)
        
            agent2.image = agent2_imgs['down']
            win.flip()
            continueRoutine = False
            
        
        # *instr_comp_turn_egg_self_2* updates
        if instr_comp_turn_egg_self_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            instr_comp_turn_egg_self_2.frameNStart = frameN  # exact frame index
            instr_comp_turn_egg_self_2.tStart = t  # local t and not account for scr refresh
            instr_comp_turn_egg_self_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instr_comp_turn_egg_self_2, 'tStartRefresh')  # time at next scr refresh
            instr_comp_turn_egg_self_2.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in comp_catch_chickComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "comp_catch_chick"-------
    for thisComponent in comp_catch_chickComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    catch_chick_loop.addData('instr_computer_4.started', instr_computer_4.tStartRefresh)
    catch_chick_loop.addData('instr_computer_4.stopped', instr_computer_4.tStopRefresh)
    this_comp_instr_txt = 'You caught the chicken'
    win.flip()
    agent2_indicator_text.color = "black"
    catch_chick_loop.addData('instr_comp_turn_egg_self_2.started', instr_comp_turn_egg_self_2.tStartRefresh)
    catch_chick_loop.addData('instr_comp_turn_egg_self_2.stopped', instr_comp_turn_egg_self_2.tStopRefresh)
    # the Routine "comp_catch_chick" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 3.0 repeats of 'catch_chick_loop'


# ------Prepare to start Routine "catch_chick_end"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_8.keys = []
key_resp_8.rt = []
_key_resp_8_allKeys = []
GridWorldComponents = [b_0_2, b_0_1, b_3_0, b_2_2, b_1_2, b_2_1, b_2_neg1, b_2_neg2, b_2_0, b_1_neg2, b_1_0, b_0_0, b_neg1_0, b_neg1_2, b_neg1_neg2, b_neg2_0, b_neg2_1, b_neg2_neg1, b_neg2_neg2, b_neg2_2, b_neg3_0, b_0_neg1, b_0_neg2, egg_left, egg_right]

for thisComponent in GridWorldComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

AgentsComponents = [chick1, agent1, agent2]
    
for thisComponent in AgentsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
end_text_5.setText(round_complete_text4)
agent1_indicator_text.setAutoDraw(False)
agent2_indicator_text.setAutoDraw(False)
# keep track of which components have finished
catch_chick_endComponents = [end_txt_egg_self_5, key_resp_8, end_text_5]
for thisComponent in catch_chick_endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
catch_chick_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "catch_chick_end"-------
while continueRoutine:
    # get current time
    t = catch_chick_endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=catch_chick_endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_txt_egg_self_5* updates
    if end_txt_egg_self_5.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
        # keep track of start time/frame for later
        end_txt_egg_self_5.frameNStart = frameN  # exact frame index
        end_txt_egg_self_5.tStart = t  # local t and not account for scr refresh
        end_txt_egg_self_5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_txt_egg_self_5, 'tStartRefresh')  # time at next scr refresh
        end_txt_egg_self_5.setAutoDraw(True)
    
    # *key_resp_8* updates
    waitOnFlip = False
    if key_resp_8.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
        # keep track of start time/frame for later
        key_resp_8.frameNStart = frameN  # exact frame index
        key_resp_8.tStart = t  # local t and not account for scr refresh
        key_resp_8.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_8, 'tStartRefresh')  # time at next scr refresh
        key_resp_8.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_8.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_8.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_8.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_8.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_8_allKeys.extend(theseKeys)
        if len(_key_resp_8_allKeys):
            key_resp_8.keys = _key_resp_8_allKeys[-1].name  # just the last key pressed
            key_resp_8.rt = _key_resp_8_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *end_text_5* updates
    if end_text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end_text_5.frameNStart = frameN  # exact frame index
        end_text_5.tStart = t  # local t and not account for scr refresh
        end_text_5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end_text_5, 'tStartRefresh')  # time at next scr refresh
        end_text_5.setAutoDraw(True)
    if end_text_5.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end_text_5.tStartRefresh + 2-frameTolerance:
            # keep track of stop time/frame for later
            end_text_5.tStop = t  # not accounting for scr refresh
            end_text_5.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end_text_5, 'tStopRefresh')  # time at next scr refresh
            end_text_5.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in catch_chick_endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "catch_chick_end"-------
for thisComponent in catch_chick_endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('end_txt_egg_self_5.started', end_txt_egg_self_5.tStartRefresh)
thisExp.addData('end_txt_egg_self_5.stopped', end_txt_egg_self_5.tStopRefresh)
# check responses
if key_resp_8.keys in ['', [], None]:  # No response was made
    key_resp_8.keys = None
thisExp.addData('key_resp_8.keys',key_resp_8.keys)
if key_resp_8.keys != None:  # we had a response
    thisExp.addData('key_resp_8.rt', key_resp_8.rt)
thisExp.addData('key_resp_8.started', key_resp_8.tStartRefresh)
thisExp.addData('key_resp_8.stopped', key_resp_8.tStopRefresh)
thisExp.nextEntry()
thisExp.addData('end_text_5.started', end_text_5.tStartRefresh)
thisExp.addData('end_text_5.stopped', end_text_5.tStopRefresh)
# the Routine "catch_chick_end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "end_tutorial"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_9.keys = []
key_resp_9.rt = []
_key_resp_9_allKeys = []
# keep track of which components have finished
end_tutorialComponents = [text_2, key_resp_9]
for thisComponent in end_tutorialComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
end_tutorialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end_tutorial"-------
while continueRoutine:
    # get current time
    t = end_tutorialClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=end_tutorialClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_2* updates
    if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_2.frameNStart = frameN  # exact frame index
        text_2.tStart = t  # local t and not account for scr refresh
        text_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
        text_2.setAutoDraw(True)
    
    # *key_resp_9* updates
    waitOnFlip = False
    if key_resp_9.status == NOT_STARTED and tThisFlip >= 3-frameTolerance:
        # keep track of start time/frame for later
        key_resp_9.frameNStart = frameN  # exact frame index
        key_resp_9.tStart = t  # local t and not account for scr refresh
        key_resp_9.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_9, 'tStartRefresh')  # time at next scr refresh
        key_resp_9.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_9.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_9.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_9.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_9.getKeys(keyList=['right','k'], waitRelease=False)
        _key_resp_9_allKeys.extend(theseKeys)
        if len(_key_resp_9_allKeys):
            key_resp_9.keys = _key_resp_9_allKeys[-1].name  # just the last key pressed
            key_resp_9.rt = _key_resp_9_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in end_tutorialComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end_tutorial"-------
for thisComponent in end_tutorialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text_2.started', text_2.tStartRefresh)
thisExp.addData('text_2.stopped', text_2.tStopRefresh)
# check responses
if key_resp_9.keys in ['', [], None]:  # No response was made
    key_resp_9.keys = None
thisExp.addData('key_resp_9.keys',key_resp_9.keys)
if key_resp_9.keys != None:  # we had a response
    thisExp.addData('key_resp_9.rt', key_resp_9.rt)
thisExp.addData('key_resp_9.started', key_resp_9.tStartRefresh)
thisExp.addData('key_resp_9.stopped', key_resp_9.tStopRefresh)
thisExp.nextEntry()
# the Routine "end_tutorial" was not non-slip safe, so reset the non-slip timer
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
