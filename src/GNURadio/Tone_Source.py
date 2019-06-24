#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tone Source
# Author: Peter F Bradshaw
# Description: An audio source for the Radio Test Set program
# Generated: Mon Jun 24 22:53:25 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys


class Tone_Source(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Tone Source")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tone Source")
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

        self.settings = Qt.QSettings("GNU Radio", "Tone_Source")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.audio_freq = audio_freq = 1000
        self.audio_amp = audio_amp = 0.1

        ##################################################
        # Blocks
        ##################################################
        self._audio_freq_range = Range(100, 10000, 100, 1000, 200)
        self._audio_freq_win = RangeWidget(self._audio_freq_range, self.set_audio_freq, "audio_freq", "counter_slider", float)
        self.top_layout.addWidget(self._audio_freq_win)
        self._audio_amp_range = Range(0, 0.2, 0.001, 0.1, 200)
        self._audio_amp_win = RangeWidget(self._audio_amp_range, self.set_audio_amp, "audio_amp", "counter_slider", float)
        self.top_layout.addWidget(self._audio_amp_win)
        self.freq_display = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	'Frequency Display', #name
        	1 #number of inputs
        )
        self.freq_display.set_update_time(0.10)
        self.freq_display.set_y_axis(-140, 10)
        self.freq_display.set_y_label('Relative Gain', 'dB')
        self.freq_display.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.freq_display.enable_autoscale(False)
        self.freq_display.enable_grid(False)
        self.freq_display.set_fft_average(1.0)
        self.freq_display.enable_axis_labels(True)
        self.freq_display.enable_control_panel(False)
        
        if not True:
          self.freq_display.disable_legend()
        
        if "float" == "float" or "float" == "msg_float":
          self.freq_display.set_plot_pos_half(not False)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.freq_display.set_line_label(i, "Data {0}".format(i))
            else:
                self.freq_display.set_line_label(i, labels[i])
            self.freq_display.set_line_width(i, widths[i])
            self.freq_display.set_line_color(i, colors[i])
            self.freq_display.set_line_alpha(i, alphas[i])
        
        self._freq_display_win = sip.wrapinstance(self.freq_display.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._freq_display_win)
        self.audio_sink = audio.sink(samp_rate, '', True)
        self.analog_sig_source = analog.sig_source_f(32000, analog.GR_SIN_WAVE, audio_freq, audio_amp, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source, 0), (self.audio_sink, 0))    
        self.connect((self.analog_sig_source, 0), (self.freq_display, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Tone_Source")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_display.set_frequency_range(0, self.samp_rate)

    def get_audio_freq(self):
        return self.audio_freq

    def set_audio_freq(self, audio_freq):
        self.audio_freq = audio_freq
        self.analog_sig_source.set_frequency(self.audio_freq)

    def get_audio_amp(self):
        return self.audio_amp

    def set_audio_amp(self, audio_amp):
        self.audio_amp = audio_amp
        self.analog_sig_source.set_amplitude(self.audio_amp)


def main(top_block_cls=Tone_Source, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
