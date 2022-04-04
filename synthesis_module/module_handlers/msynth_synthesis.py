from msynth import Synthesizer
import logging
from synthesis_module.module_handlers.HandlerBase import HandlerBase
import time

class Msynth_synth(HandlerBase):
    def __init__(self):
        self.simplifier = Synthesizer()

    def simplify(self, expr):
        # synthesized, score = self.simplifier.synthesize_from_expression(expr,num_samples = 10)
        timeout = 10.0
        # timeoutlist = [2.5 for _ in range(10)]
        ils_list = [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,64]
        timeoutlist = [3.0, 30.0, 30.0, 10.0, 5.0, 5.0]
        score_list = [-1, -1, -1]
        time_list = [-1, -1, -1]
        try_count = -1
        count = 0

        # while(count<3):
        start = time.time()
        for to in range(1):
        # while time.time()-start<4 :
            start_time_each = time.time()
            timeout = ils_list[count]
            count = count + 1
            synthesized, score = self.simplifier.synthesize_from_expression_parallel(expr, num_samples = 10, timeout=timeout)
            # synthesized, score = self.simplifier.synthesize_from_expression(expr, num_samples=10, timeout=timeout)
            # print(f"score : {score}      new timeout : {timeout} ")


            # score_list[to] = score
            end_time_each = round(time.time() - start_time_each, 2)
            # time_list[to] = end_time_each
            # try_count = to+1



            if score == 0.0:
                if self.semantically_equal(expr, synthesized):
                    # return synthesized, True, [score_list,time_list,try_count]
                    return synthesized, True
                # else:
                #     return synthesized, False, [score_list,time_list,try_count]
            # timeout = timeout + 2.0

            # if to == 0:
            #     timeout = timeoutlist[0]
            #     count = 1
            # elif to == 1:
            #     timeout = 1.0
###########
            # if score < 20 and score > 0:
            if score < 10 :
                # timeout = 5.0
                # count += 0.5
                # pass
                timeout = timeoutlist[count]
                count = count+1
            #     # print(f"score : {score}      new timeout : {timeout}   count :{count}")

            # timeout = timeoutlist[count]
            # count = count + 1
###########

            # else:
            #     count += 1
        return False, False

    def simplify_try2(self, expr,timeout = 1):
        # synthesized, score = self.simplifier.synthesize_from_expression(expr,num_samples = 10)
        timeout = 1.0
        timeoutlist = [3.0, 6.0, 7.0, 10.0, 5.0, 5.0]

        # while(count<3):
        for to in range(2):
            # synthesized, score = self.simplifier.synthesize_from_expression_parallel(expr, num_samples = 10, timeout=timeout)
            synthesized, score = self.simplifier.synthesize_from_expression(expr, num_samples=10, timeout=timeout)
            print(f"score : {score}      new timeout : {timeout} ")

            if score == 0.0:
                if self.semantically_equal(expr, synthesized):
                    # return synthesized, True, [score_list,time_list,try_count]
                    return synthesized, True

        return False, False




    def get_module_name(self):
        return "msynth-synth"