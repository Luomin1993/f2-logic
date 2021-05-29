#!/usr/bin/env python
# -*- coding: utf-8 -*-

__ENV__  =  'python3';
__author__ =  'hanss401';


import numpy as np;
import os;
import sys;
import random;

# =================== TEST_DAT ==================
DAT_1 = [0.043732174,0.093567154,0.137299329,0.187134308,0.230866483,0.280701462,0.324433637,0.374268616,0.418000791,0.467835770,0.511567945,0.561402924,0.605135099,0.654970079,0.698702254,0.748537233,0.792269408,0.842104387,0.885836562,0.935671541,0.979403716,1.029238695,1.072970870,1.122805849,1.166538024,1.216373004,1.260105178,1.309940158,1.353672333,1.403507312,1.447239487,1.497074466,1.540806641,1.584538816,1.628270991,1.672003166,1.715735341,1.759467516,1.803199691,1.846931866,1.890664041,1.934396215,1.978128390,2.021860565];
DAT_2 = [DAT_1[i]*1000 for i in range(len(DAT_1))];

# =================== PCM ===================
class PcmCode(object):
    """PcmCode:Pulse Code Modulation"""
    def __init__(self,FLOAT_NUM_ARR,ENCODE_LEN):
        super(PcmCode, self).__init__()
        self.FLOAT_NUM_ARR = FLOAT_NUM_ARR;
        self.ENCODE_LEN = ENCODE_LEN;
        self.CODE_LEN = 2**ENCODE_LEN;
        self.MAX_NUM = 0.0;
        self.TIMED_NUM = 1;
        self.DIVIDED_NUM = 1;
        self.INT_NUM_ARR = [];
        self.COEDS_ARR = [];
        self.DECODES_ARR = [];

    def find_first_not0(self,MAX_NUM):
        if MAX_NUM>=1:
            for i in range(1,10):
                if MAX_NUM<10**i:break;
            if i>=self.ENCODE_LEN:
                self.DIVIDED_NUM = 10**(i-self.ENCODE_LEN);
            if i<self.ENCODE_LEN:
                self.TIMED_NUM = 10**(self.ENCODE_LEN-i);
        if MAX_NUM<1:
            for i in range(1,10):
                if 10**(-i)<=MAX_NUM:break;
            self.TIMED_NUM = 10**(i+self.ENCODE_LEN-1);

    def pcm_decode(self):
        pass;

    def pcm_encode_all(self):
        self.MAX_NUM = max(self.FLOAT_NUM_ARR);
        self.find_first_not0(self.MAX_NUM);
        self.INT_NUM_ARR = [int(self.FLOAT_NUM_ARR[i]*self.TIMED_NUM/self.DIVIDED_NUM) for i in range(len(self.FLOAT_NUM_ARR))];
        for INT_NUM in self.INT_NUM_ARR:
            THIS_CODE = list(bin(INT_NUM).replace('0b','').replace('-',''));
            THIS_CODE = [int(CODE) for CODE in THIS_CODE];
            THIS_CODE_LEN = len(THIS_CODE);
            for i in range(self.CODE_LEN-THIS_CODE_LEN):THIS_CODE=[0]+THIS_CODE;
            self.COEDS_ARR.append(THIS_CODE);

    def pcm_decode(self,THIS_CODE):
        THIS_CODE.reverse();
        THIS_INT=0;
        for i in range(len(THIS_CODE)):THIS_INT += THIS_CODE[i]*(2**i);
        return float(THIS_INT)/self.TIMED_NUM*self.DIVIDED_NUM;

    def pcm_decode_all(self):
        for i in range(len(self.COEDS_ARR)):
            self.DECODES_ARR.append(self.pcm_decode(self.COEDS_ARR[i]));

# PCMCODE_MACHINE = PcmCode(DAT_1,3);
# PCMCODE_MACHINE.pcm_encode_all();
# PCMCODE_MACHINE.pcm_decode_all();
# print(PCMCODE_MACHINE.COEDS_ARR);
# print(PCMCODE_MACHINE.DECODES_ARR);