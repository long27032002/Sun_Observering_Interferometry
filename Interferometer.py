#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Interferometer
# Author: Nguyen Nhu Hai Long
# Copyright: @Nguyen Nhu Hai Long
# GNU Radio version: 3.10.8.0

from datetime import datetime
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import Interferometer_epy_block_0 as epy_block_0  # embedded python block
import Interferometer_epy_block_0_0 as epy_block_0_0  # embedded python block
import Interferometer_epy_block_1_0 as epy_block_1_0  # embedded python block
import osmosdr
import time




class Interferometer(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Interferometer", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.timenow = timenow = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.path = path = "/home"
        self.Vector_length = Vector_length = 512
        self.Sample = Sample = 2000000
        self.Frequency = Frequency = 610000000
        self.Datetime = Datetime = datetime.now().strftime("%Y_%m_%d")

        ##################################################
        # Blocks
        ##################################################

        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(Sample)
        self.osmosdr_source_0.set_center_freq(Frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(40, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.epy_block_1_0 = epy_block_1_0.csv_filesink(vec_length=Vector_length, samp_rate=Sample, freq=Frequency, prefix=f"{path}/{Datetime}/", save_toggle="True", integration_select=0, short_long_time_scale=0, az="", elev="", location="")
        self.epy_block_0_0 = epy_block_0_0.integration(vec_length=Vector_length, n_integrations=21)
        self.epy_block_0 = epy_block_0.integration(vec_length=Vector_length, n_integrations=int(Frequency/Sample))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, Vector_length, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(100, (1/100), 500, Vector_length)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(Vector_length)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_0_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.epy_block_1_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))


    def get_timenow(self):
        return self.timenow

    def set_timenow(self, timenow):
        self.timenow = timenow

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def get_Vector_length(self):
        return self.Vector_length

    def set_Vector_length(self, Vector_length):
        self.Vector_length = Vector_length
        self.epy_block_0.vec_length = self.Vector_length
        self.epy_block_0_0.vec_length = self.Vector_length
        self.epy_block_1_0.vec_length = self.Vector_length

    def get_Sample(self):
        return self.Sample

    def set_Sample(self, Sample):
        self.Sample = Sample
        self.epy_block_0.n_integrations = int(self.Frequency/self.Sample)
        self.epy_block_1_0.samp_rate = self.Sample
        self.osmosdr_source_0.set_sample_rate(self.Sample)

    def get_Frequency(self):
        return self.Frequency

    def set_Frequency(self, Frequency):
        self.Frequency = Frequency
        self.epy_block_0.n_integrations = int(self.Frequency/self.Sample)
        self.epy_block_1_0.freq = self.Frequency
        self.osmosdr_source_0.set_center_freq(self.Frequency, 0)

    def get_Datetime(self):
        return self.Datetime

    def set_Datetime(self, Datetime):
        self.Datetime = Datetime




def main(top_block_cls=Interferometer, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
