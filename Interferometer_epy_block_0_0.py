"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""


import numpy as np
from gnuradio import gr

class integration(gr.decim_block):
    """
    docstring for block integration
    """
    def __init__(self, vec_length=512, n_integrations=1):
        gr.decim_block.__init__(self,
            name="integration",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=[(np.float32, int(vec_length))], 
            decim = n_integrations)
        self.n_integrations = n_integrations
        self.vec_length = vec_length
        self.set_relative_rate(1.0/n_integrations)
        self.sum = np.zeros(self.vec_length)
        self.integration_count = 0


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        for inp0 in in0:
            if self.integration_count < self.n_integrations:
                self.sum = self.sum + inp0
                self.integration_count += 1
            else:
                out[:] = self.sum[:]/self.n_integrations
                self.sum = np.zeros(self.vec_length)
                self.integration_count = 0
        return len(output_items[0])

    def set_n_integrations(self, n_integrations):
        self.n_integrations = n_integrations
        self.set_relative_rate(1.0/n_integrations)
        print("Rate Updated")