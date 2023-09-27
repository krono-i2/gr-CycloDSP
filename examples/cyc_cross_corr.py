#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Cyclic Cross-Correlation
# Author: Ivan Iudice
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import CycloDSP
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np



from gnuradio import qtgui

class cyc_cross_corr(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Cyclic Cross-Correlation", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Cyclic Cross-Correlation")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "cyc_cross_corr")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.win_len = win_len = 4096
        self.samp_sym = samp_sym = 8
        self.samp_rate = samp_rate = 32000
        self.refresh_rate = refresh_rate = 0.1
        self.max_lag = max_lag = 256
        self.constellation = constellation = digital.constellation_qpsk().base()
        self.alpha = alpha = [0, 1/8]

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_vector_sink_f_0_1 = qtgui.vector_sink_f(
            (2*max_lag+1),
            (-max_lag*1000/samp_rate),
            (1000/samp_rate),
            "Tau (ms)",
            "CCF",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1.set_update_time(refresh_rate)
        self.qtgui_vector_sink_f_0_1.set_y_axis(0, 4)
        self.qtgui_vector_sink_f_0_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_ref_level(0)


        labels = ["alpha="+str(alpha[1]), '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_1_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            (2*max_lag+1),
            (-max_lag*1000/samp_rate),
            (1000/samp_rate),
            "Tau (ms)",
            "CCF",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(refresh_rate)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 4)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ["alpha="+str(alpha[0]), '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=constellation,
            differential=False,
            samples_per_symbol=samp_sym,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_gr_complex*(2*max_lag+1), 2)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_complex_to_mag_2_1 = blocks.complex_to_mag((2*max_lag+1))
        self.blocks_complex_to_mag_2 = blocks.complex_to_mag((2*max_lag+1))
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, win_len))), True)
        self.CycloDSP_CycXCorr_0 = CycloDSP.CycXCorr(0, max_lag, [0], [0,1/samp_sym], win_len, 1, False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.CycloDSP_CycXCorr_0, 0), (self.blocks_vector_to_streams_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_complex_to_mag_2, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_complex_to_mag_2_1, 0), (self.qtgui_vector_sink_f_0_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.CycloDSP_CycXCorr_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.CycloDSP_CycXCorr_0, 1))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.blocks_complex_to_mag_2, 0))
        self.connect((self.blocks_vector_to_streams_0, 1), (self.blocks_complex_to_mag_2_1, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "cyc_cross_corr")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_win_len(self):
        return self.win_len

    def set_win_len(self, win_len):
        self.win_len = win_len

    def get_samp_sym(self):
        return self.samp_sym

    def set_samp_sym(self, samp_sym):
        self.samp_sym = samp_sym

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis((-self.max_lag*1000/self.samp_rate), (1000/self.samp_rate))
        self.qtgui_vector_sink_f_0_1.set_x_axis((-self.max_lag*1000/self.samp_rate), (1000/self.samp_rate))

    def get_refresh_rate(self):
        return self.refresh_rate

    def set_refresh_rate(self, refresh_rate):
        self.refresh_rate = refresh_rate
        self.qtgui_vector_sink_f_0.set_update_time(self.refresh_rate)
        self.qtgui_vector_sink_f_0_1.set_update_time(self.refresh_rate)

    def get_max_lag(self):
        return self.max_lag

    def set_max_lag(self, max_lag):
        self.max_lag = max_lag
        self.qtgui_vector_sink_f_0.set_x_axis((-self.max_lag*1000/self.samp_rate), (1000/self.samp_rate))
        self.qtgui_vector_sink_f_0_1.set_x_axis((-self.max_lag*1000/self.samp_rate), (1000/self.samp_rate))

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha




def main(top_block_cls=cyc_cross_corr, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
