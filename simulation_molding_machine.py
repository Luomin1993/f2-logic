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

COEFF_L1   = 1.25732;
COEFF_L2   = 0.25652;
COEFF_Q1   = 0.47500;
COEFF_Q2   = 0.41300;
COEFF_I1   = 0.46750;
COEFF_T1   = 0.38950;
EPSILON_L1 = 0.35100;
EPSILON_L2 = 0.54000;
EPSILON_Q1 = 0.13500;
EPSILON_Q2 = 0.22500;
EPSILON_I1 = 0.37250;
EPSILON_T1 = 0.62570;

TEMPERATURE_COOL_0 = 40.00;
VOLTAGE_0 = 220.000;
POWER_0   = 125.265;
COEFF_mP1  = 13.2350;
COEFF_mP2  = 3.23500;

DELTA_T    = 1.25000;

# =================== SIMULATION FUNCS ===================
# ------- Controlled variable ---------
m_o = 0.5;
e_i = 0.2;
DELTA_m_o = 0.0;
DELTA_e_i = 0.0;
# ------- Variables measured by sensors ---------
PRESSURE_FLUID   = 0.00;
POSITION_MODEL   = 0.00;
TEMPERATURE_HEAT = 170.0;
TEMPERATURE_COOL = 20.00;

# ------ Simulation the transient conditions ---
def transient_condition():
    TEMPERATURE_HEAT = np.random.rand()*300;
    TEMPERATURE_COOL = np.random.rand()*35;
    POSITION_MODEL   = 0.5 + np.random.rand()*3.0;
    PRESSURE_FLUID   = 0.5 + np.random.rand()*9.0;
    m_o = np.random.rand()*0.75;
    e_i = np.random.rand()*0.75;
    return (m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL);

# ------ Simulation the controlling process ---
def impact_process(m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL):
    if m_o>1.0:m_o=1.0;
    if m_o<0.0:m_o=0.0;
    if e_i>1.0:e_i=1.0;
    if e_i<0.0:e_i=0.0;
    PRESSURE_1 = COEFF_mP1*(m_o-0.15);#print(PRESSURE_1);
    BBL = 2.0*(PRESSURE_1 - PRESSURE_0)/DENSITY_0;
    if BBL<0:BBL = 2.27500;
    FLOW_L = COEFF_d*AREA_1*np.sqrt(BBL);
    PRESSURE_FLUID = (LENGTH_C/LENGTH_D) * FLOW_L * COEFF_Q1 * EPSILON_Q1 * 1000.0;
    SPEED_MODEL = FLOW_L * COEFF_Q2 * EPSILON_Q2;
    POSITION_MODEL += SPEED_MODEL*DELTA_T*10.0;
    ELECTRIC_I = COEFF_I1*EPSILON_I1*POWER_0*e_i/VOLTAGE_0;
    TEMPERATURE_HEAT = COEFF_T1*EPSILON_T1*ELECTRIC_I*12200.00;
    TEMPERATURE_COOL = TEMPERATURE_COOL_0 - COEFF_T1*EPSILON_T1*ELECTRIC_I*1220.500;
    return (m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL);

#print(str((SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING))+' ------ '+str((m_o,e_i)));
#(m_o,e_i,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING) = impact_process(m_o,e_i,SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING);
#print(str((SPEED_FIXTURE_X,ACC_ROLLING,SPEED_ROLLING_Y,POSITION_ROLLING))+' ------ '+str((m_o,e_i)));
#sys.exit();

DAT_MAT = [[] for i in range(6)];
IMP_MAT = [[] for i in range(6)];
ACT_MAT = [[] for i in range(2)];
for i in range(200):
    DELTA_m_o = 0.0;DELTA_e_i = 0.0;
    (m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL) = transient_condition();
    if TEMPERATURE_HEAT >= 230.0 and POSITION_MODEL>3.0:
        # Back to init state;
        m_o = 0.5;
        e_i = 0.2;
        DELTA_m_o = 0.0;
        DELTA_e_i = 0.0;
        PRESSURE_FLUID   = 0.00;
        POSITION_MODEL   = 0.00;
        TEMPERATURE_HEAT = 170.0;
        TEMPERATURE_COOL = 20.00;   
    if TEMPERATURE_HEAT >= 200.0:
        DELTA_e_i = -0.1;
    if TEMPERATURE_HEAT <= 100.0:
        DELTA_e_i = 0.1;    
    if TEMPERATURE_COOL >= 25.0:
        DELTA_e_i = 0.1;
    if TEMPERATURE_COOL <= 10.0:
        DELTA_e_i = -0.1;        
    if POSITION_MODEL <= 1.5:
        DELTA_m_o = 0.1;
    if POSITION_MODEL >= 2.5:
        DELTA_m_o = -0.1;        
    if PRESSURE_FLUID >=6.5:
        DELTA_m_o = -0.1;
    if PRESSURE_FLUID <=3.5:
        DELTA_m_o = 0.1;        
    e_i += DELTA_e_i;
    m_o += DELTA_m_o;
    print(str((PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL))+' ------ '+str((m_o,e_i))+' -+-CONTROL-+- '+str((DELTA_m_o,DELTA_e_i)));
    RECORD_DAT = (m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL);
    RECORD_ACT = (DELTA_m_o,DELTA_e_i);
    for i in range(len(RECORD_DAT)):DAT_MAT[i].append(RECORD_DAT[i]);
    for i in range(len(RECORD_ACT)):ACT_MAT[i].append(RECORD_ACT[i]);
    (m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL) = impact_process(m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL);
    RECORD_IMP = (m_o,e_i,PRESSURE_FLUID,POSITION_MODEL,TEMPERATURE_HEAT,TEMPERATURE_COOL);
    for i in range(len(RECORD_IMP)):IMP_MAT[i].append(RECORD_IMP[i]);

np.save('TASK_2_ACT_MAT',np.array(ACT_MAT));

for i in range(len(DAT_MAT)):
    PCMCODE_MACHINE = PcmCode(DAT_MAT[i],3);
    PCMCODE_MACHINE.pcm_encode_all();
    print(PCMCODE_MACHINE.COEDS_ARR);
    DAT_MAT[i] = PCMCODE_MACHINE.COEDS_ARR;
np.save('TASK_2_DAT_MAT',np.array(DAT_MAT));    

for i in range(len(IMP_MAT)):
    PCMCODE_MACHINE = PcmCode(IMP_MAT[i],3);
    PCMCODE_MACHINE.pcm_encode_all();
    print(PCMCODE_MACHINE.COEDS_ARR);
    IMP_MAT[i] = PCMCODE_MACHINE.COEDS_ARR;
np.save('TASK_2_IMP_MAT',np.array(IMP_MAT));