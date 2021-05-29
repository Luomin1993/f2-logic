#!/usr/bin/env python
# -*- coding: utf-8 -*-

__ENV__  =  'python3';
__author__ =  'hanss401';


import numpy as np;
import os;
import sys;
import random;
from pcm_transformation import *;

# =================== CONSTATN DEFINE ===================
COEFF_d    = 0.75300; 
AREA_1     = 0.02550; # m^2;
PRESSURE_1 = 9.17253; # MPa;
PRESSURE_0 = 3.17253; # MPa; 
DENSITY_0  = 0.85200; # g/cm^3;
FLOW_L     = 0.00000; # cm^3/s;
COEFF_L1   = 1.25732;
COEFF_L2   = 0.25652;
EPSILON_L1 = 0.35100;
EPSILON_L2 = 0.54000;
COEFF_mP1  = 13.2350;
COEFF_mP2  = 3.23500;
DELTA_T    = 1.25000;

# =================== SIMULATION FUNCS ===================
# ------- Controlled variable ---------
m_o = 1.0;
m_b = 0.5;
DELTA_m_o = 0.0;
DELTA_m_b = 0.0;
# ------- Variables measured by sensors ---------
SPEED_FIXTURE_X  = 0.0;
SPEED_ROLLING_Y  = 0.0;
POSITION_ROLLING = 0.0;
ACC_ROLLING      = 0.0;

# ------ Simulation the transient conditions ---
def transient_condition():
    POSITION_ROLLING = 1.0 + np.random.rand()*2;
    SPEED_ROLLING_Y = 1.0 + np.random.rand()*3;
    SPEED_FIXTURE_X = 0.5 + np.random.rand();
    ACC_ROLLING = 0.25 + np.random.rand();
    m_o = np.random.rand()*0.75;
    m_b = np.random.rand()*0.75;
    return (m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);

# ------ Simulation the controlling process ---
def impact_process(m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING):
    if m_o>1.0:m_o=1.0;
    if m_o<0.0:m_o=0.0;
    if m_b>1.0:m_b=1.0;
    if m_b<0.0:m_b=0.0;
    PRESSURE_1 = COEFF_mP1*(m_o-m_b);#print(PRESSURE_1);
    BBL = 2.0*(PRESSURE_1 - PRESSURE_0)/DENSITY_0;
    if BBL<0:BBL = 2.27500;
    FLOW_L = COEFF_d*AREA_1*np.sqrt(BBL);
    ACC_ROLLING = COEFF_L1*EPSILON_L1*FLOW_L;
    SPEED_FIXTURE_X = COEFF_L2*EPSILON_L2*FLOW_L*157.125;
    SPEED_ROLLING_Y += ACC_ROLLING*DELTA_T;
    POSITION_ROLLING += SPEED_ROLLING_Y*DELTA_T;
    return (m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);

#print(str((SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING))+' ------ '+str((m_o,m_b)));
#(m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING) = impact_process(m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);
#print(str((SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING))+' ------ '+str((m_o,m_b)));
#sys.exit();
DAT_MAT = [[] for i in range(6)];
IMP_MAT = [[] for i in range(6)];
ACT_MAT = [[] for i in range(2)];
for i in range(200):
    m_o=0.0;m_b=0.0;
    (m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING) = transient_condition();
    if POSITION_ROLLING >= 7.0:
        # Back to init state;
        m_o = 1.0;
        m_b = 0.5;
        SPEED_ROLLING_Y = 0.0;
        ACC_ROLLING     = 0.0;
        POSITION_ROLLING = 0.0;
    if POSITION_ROLLING >= 2.5:
        DELTA_m_o = -0.1;
    if POSITION_ROLLING <= 1.5:
        DELTA_m_o = 0.1;
    if SPEED_ROLLING_Y<=0.2:
        DELTA_m_o = 0.1;
    if SPEED_ROLLING_Y>=0.3:
        DELTA_m_o = -0.1;
    if ACC_ROLLING<=0.5:
        DELTA_m_o = 0.1;
    if ACC_ROLLING>=1.0:
        DELTA_m_o = -0.1;    
    if SPEED_FIXTURE_X<0.8:
        DELTA_m_b = -0.1;
    if SPEED_FIXTURE_X>1.2:
        DELTA_m_b = 0.1;            
    m_b += DELTA_m_b;
    m_o += DELTA_m_o;
    print(str((SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING))+' ------ '+str((m_o,m_b))+' -+-CONTROL-+- '+str((DELTA_m_o,DELTA_m_b)));
    RECORD_DAT = (m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);
    RECORD_ACT = (DELTA_m_o,DELTA_m_b);
    for i in range(len(RECORD_DAT)):DAT_MAT[i].append(RECORD_DAT[i]);
    for i in range(len(RECORD_ACT)):ACT_MAT[i].append(RECORD_ACT[i]);
    (m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING) = impact_process(m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);
    RECORD_IMP = (m_o,m_b,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);
    for i in range(len(RECORD_IMP)):IMP_MAT[i].append(RECORD_IMP[i]);

np.save('TASK_1_ACT_MAT',np.array(ACT_MAT));

for i in range(len(DAT_MAT)):
    PCMCODE_MACHINE = PcmCode(DAT_MAT[i],3);
    PCMCODE_MACHINE.pcm_encode_all();
    print(PCMCODE_MACHINE.COEDS_ARR);
    DAT_MAT[i] = PCMCODE_MACHINE.COEDS_ARR;
np.save('TASK_1_DAT_MAT',np.array(DAT_MAT));    

for i in range(len(IMP_MAT)):
    PCMCODE_MACHINE = PcmCode(IMP_MAT[i],3);
    PCMCODE_MACHINE.pcm_encode_all();
    print(PCMCODE_MACHINE.COEDS_ARR);
    IMP_MAT[i] = PCMCODE_MACHINE.COEDS_ARR;
np.save('TASK_1_IMP_MAT',np.array(IMP_MAT));    