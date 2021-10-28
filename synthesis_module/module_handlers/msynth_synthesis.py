from msynth import Synthesizer
import logging
from synthesis_module.module_handlers.HandlerBase import HandlerBase
class Msynth_synth(HandlerBase):
    def __init__(self):
        self.simplifier = Synthesizer()

    def simplify(self, expr):
        synthesized, score = self.simplifier.synthesize_from_expression(expr,num_samples = 10)
        if score == 0.0:
            return synthesized
        return False

    def get_module_name(self):
        return "msynth-synth"