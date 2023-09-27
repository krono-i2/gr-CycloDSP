#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Ivan Iudice.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from scipy.signal import correlate

class CycXCorr(gr.sync_block):
    """
    docstring for block CycXCorr
    """
    def __init__(self, mode = 0, max_lag = 0, lags = [0], alpha = [0], win_len = 1024, state = 1, conj = False):
        if mode == 0:
            out_sign = (2 * max_lag + 1)*len(alpha)
            self.max_lag = max_lag
            self.alpha = alpha
            self.state = [state]*len(alpha)
            hist = win_len + 2*max_lag
        else:
            out_sign = win_len*len(lags)
            self.lags = lags
            self.state = [state]*win_len
            tmp_set = [lag for lag in self.lags if lag>0]
            self.max_pos_lag = max(tmp_set) if len(tmp_set)>0 else 0
            tmp_set = [lag for lag in self.lags if lag<0]
            self.min_neg_lag = min(tmp_set) if len(tmp_set)>0 else 0
            hist = self.max_pos_lag-self.min_neg_lag+win_le
            
        gr.sync_block.__init__(self,
            name="Cyclic Cross-Correlation",
            in_sig=[np.complex64, np.complex64],
            out_sig=[(np.complex64, out_sign)])

        self.set_history(hist)
        self.mode = mode
        self.win_len = win_len
        self.conj = conj

    def work(self, input_items, output_items):
        x = input_items[0]
        y = input_items[1]
        
        win_len = self.win_len

        noutput_items = np.shape(output_items)[1]
        for i in range(noutput_items):
            if self.mode==0:
                max_lag = self.max_lag
                Nout = 2*max_lag + 1
                x_curr = x[i:2*max_lag+i+win_len]
                if self.conj:
                    y_curr = y[max_lag+i:max_lag+i+win_len].conj()
                else:
                    y_curr = y[max_lag+i:max_lag+i+win_len]
                for ia,a in enumerate(self.alpha):
                    out = correlate(x_curr, self.state[ia]*y_curr*np.exp(1j*2*np.pi*a*np.arange(win_len)), mode="valid")/win_len
                    output_items[0][i][ia*Nout:(ia+1)*Nout] = out
                    self.state[ia] *= np.exp(1j*2*np.pi*a)
            else:
                lags = self.lags
                Nout = win_len
                if self.conj:
                    y_curr = y[-self.min_neg_lag+i:-self.min_neg_lag+i+win_len]
                else:
                    y_curr = y[-self.min_neg_lag+i:-self.min_neg_lag+i+win_len].conj()
                for il,l in enumerate(lags):
                    x_curr = x[-self.min_neg_lag+i+l:-self.min_neg_lag+i+win_len+l]
                    out = x_curr*y_curr*self.state
                    out[1::2] = -out[1::2]
                    out = np.fft.fft(out)/win_len
                    output_items[0][i][il*Nout:(il+1)*Nout] = out
                # self.state *= np.exp(-1j*2*np.pi/win_len*np.arange(-1/2,1/2,1/win_len))
        
        return noutput_items
