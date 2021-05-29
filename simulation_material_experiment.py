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
COEFF_THETA = 0.25100; 
THETA_6     = 12.2550; # rad;
LENGTH_CD   = 2.92000; # m;
LENGTH_D    = 1.25000; # m; 
LENGTH_C    = 3.25000; # m; 
COEFF_d    = 0.75300; 

AREA_1     = 0.01550; # m^2;
PRESSURE_1 = 4.12200; # MPa;
PRESSURE_0 = 1.52300; # MPa; 
DENSITY_0  = 0.85200; # g/cm^3;
FLOW_L     = 0.00000; # cm^3/s;

COEFF_Q1 = 0.42500;
ALPHA_0  = 0.24500;
PRESSURE_s = 135.00;
AREA_s = 0.00172;
TEMPERATURE_s = 195.00;
PRESSURE_e = 112.50;
COEFF_I1 = 0.62750;
EPSILON_I1 = 0.27800;
POWER_0 = 129.750;
VOLTAGE_0 = 333.25;
COEFF_T1 = 0.73500;
EPSILON_T1 = 0.80500;
ELECTRIC_I = 15.000;
COEFF_P1 = 0.62780;
EPSILON_P1 = 0.71350;
COEFF_V1 = 0.43950;
EPSILON_V1 = 0.36850;

DELTA_T    = 1.25000;

# =================== SIMULATION FUNCS ===================
# ------- Controlled variable ---------
m_o = 0.5;
m_x = 0.5;
e_i = 0.4;
DELTA_m_o = 0.0;
DELTA_m_x = 0.0;
DELTA_e_i = 0.0;
# ------- Variables measured by sensors ---------
SPEED_PROBE       = 0.00;
POSITION_PROBE    = 0.00;
PRESSURE_MATRL    = 0.00;
TEMPERATURE_MATRL = 25.00;

# ------ Simulation the transient conditions ---
def transient_condition():
    SPEED_PROBE    = 1.8 + np.random.rand();
    POSITION_PROBE = 0.8 + np.random.rand();
    PRESSURE_MATRL = 280 + np.random.rand()*100;
    TEMPERATURE_MATRL = 180 + np.random.rand()*100;
    m_o = np.random.rand()*0.75;
    m_x = np.random.rand()*0.75;
    e_i = np.random.rand()*0.75;
    return (m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL);

# ------ Simulation the controlling process ---
def impact_process(m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL):
    if m_o>1.0:m_o=1.0;
    if m_o<0.0:m_o=0.0;
    if m_x>1.0:m_x=1.0;
    if m_x<0.0:m_x=0.0;
    if e_i>1.0:e_i=1.0;
    if e_i<0.0:e_i=0.0;
    FLOW_m0 = ALPHA_0*COEFF_Q1*AREA_s*(PRESSURE_s/np.sqrt(TEMPERATURE_s))*np.exp(PRESSURE_e/PRESSURE_s);
    ELECTRIC_I = COEFF_I1*EPSILON_I1*POWER_0*e_i/VOLTAGE_0;
    TEMPERATURE_MATRL = COEFF_T1*EPSILON_T1*ELECTRIC_I*10774.05;
    PRESSURE_MATRL = COEFF_P1*EPSILON_P1*m_o*795.250;
    SPEED_PROBE = FLOW_m0 * COEFF_V1 * EPSILON_V1 * m_x *5.735;
    POSITION_PROBE += SPEED_PROBE*DELTA_T*10.0;
    return (m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL);

#print(str((SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING))+' ------ '+str((m_o,e_i)));
#(m_o,e_i,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING) = impact_process(m_o,e_i,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);
#print(str((SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING))+' ------ '+str((m_o,e_i)));
#sys.exit();

DAT_MAT = [[] for i in range(7)];
IMP_MAT = [[] for i in range(7)];
ACT_MAT = [[] for i in range(3)];
for i in range(200):
    DELTA_m_o = 0.0;DELTA_m_x=0.0;DELTA_e_i = 0.0;
    (m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL) = transient_condition();
    if TEMPERATURE_MATRL >= 630.0 or POSITION_PROBE>2.4:
        # Back to init state;
        m_o = 0.5;
        m_x = 0.5;
        e_i = 0.4;
        DELTA_m_o = 0.0;
        DELTA_m_x = 0.0;
        DELTA_e_i = 0.0;
        SPEED_PROBE       = 0.00;
        POSITION_PROBE    = 0.00;
        PRESSURE_MATRL    = 0.00;
        TEMPERATURE_MATRL = 25.00;   
    if TEMPERATURE_MATRL >= 250.0:
        DELTA_e_i = -0.1;
    if TEMPERATURE_MATRL <= 200.0:
        DELTA_e_i = 0.1;    
    if POSITION_PROBE <= 1.0:
        DELTA_m_x = 0.1;
    if POSITION_PROBE >= 1.5:
        DELTA_m_x = -0.1;
    if SPEED_PROBE <= 2.0:
        DELTA_m_x = 0.1;
    if SPEED_PROBE >= 2.5:
        DELTA_m_x = -0.1;        
    if PRESSURE_MATRL <= 300.0:
        DELTA_m_o = 0.1;    
    if PRESSURE_MATRL >=350.0:
        DELTA_m_o = -0.1;    
    e_i += DELTA_e_i;
    m_o += DELTA_m_o;
    m_x += DELTA_m_x;
    print(str((SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL))+' ---- '+str((m_o,m_x,e_i))+' --CONTROL-- '+str((DELTA_m_o,DELTA_m_x,DELTA_e_i)));    
    RECORD_DAT = (m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL);
    RECORD_ACT = (DELTA_m_o,DELTA_m_x,DELTA_e_i);
    for i in range(len(RECORD_DAT)):DAT_MAT[i].append(RECORD_DAT[i]);
    for i in range(len(RECORD_ACT)):ACT_MAT[i].append(RECORD_ACT[i]);
    (m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL) = impact_process(m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL);
    RECORD_IMP = (m_o,m_x,e_i,SPEED_PROBE,POSITION_PROBE,PRESSURE_MATRL,TEMPERATURE_MATRL);
    for i in range(len(RECORD_IMP)):IMP_MAT[i].append(RECORD_IMP[i]);

np.save('TASK_3_ACT_MAT',np.array(ACT_MAT));

for i in range(len(DAT_MAT)):
    PCMCODE_MACHINE = PcmCode(DAT_MAT[i],3);
    PCMCODE_MACHINE.pcm_encode_all();
    print(PCMCODE_MACHINE.COEDS_ARR);
    DAT_MAT[i] = PCMCODE_MACHINE.COEDS_ARR;
np.save('TASK_3_DAT_MAT',np.array(DAT_MAT));  

for i in range(len(IMP_MAT)):
    PCMCODE_MACHINE = PcmCode(IMP_MAT[i],3);
    PCMCODE_MACHINE.pcm_encode_all();
    print(PCMCODE_MACHINE.COEDS_ARR);
    IMP_MAT[i] = PCMCODE_MACHINE.COEDS_ARR;
np.save('TASK_3_IMP_MAT',np.array(IMP_MAT));  