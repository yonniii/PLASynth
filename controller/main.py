import time
import json
from msynth.utils.expr_utils import get_unification_candidates
from synthesis_module.module_handlers.xyntia import Xyntia
from synthesis_module.module_handlers.msynth_synthesis import Msynth_synth
from synthesis_module.module_handlers.msynth_simplifier import Msynth_simp
from get_sample import get_sample

# modules = [Msynth_synth(), Xyntia(), Msynth_simp()]
modules = [Msynth_synth()]

def run_single_Xyntia(module, expr, outfile):
    tmpdict = {}
    start_time = time.time()
    module.simplify(expr)
    endtime = round(time.time() - start_time, 2)
    tmpdict = module.result_parser.get_parsed_dict()
    tmpdict["time"] = endtime
    return tmpdict

def getDict_fromExpr(expr, simplified):
    tmpdict = {}
    tmpdict['obf_expr'] = str(expr)
    tmpdict['obf_leng'] = expr.length()
    tmpdict['obf_var'] = len(get_unification_candidates(expr))

    if simplified:
        print(f"initial: {expr}")
        print(f"simplified: {simplified}")
        tmpdict['result_expr'] = str(simplified)
        tmpdict['result_leng'] = simplified.length()
        tmpdict['result_var'] = len(get_unification_candidates(simplified))
    else:
        print(f"FAIL initial: {expr}")
        tmpdict['result_expr'] = "FAIL"
        tmpdict['result_leng'] = 0
        tmpdict['result_var'] = 0
    return tmpdict

def sort(a,b):
    aleng = a['result_leng']
    bleng = b['result_leng']


def run_PLASynth(samples, outfile):
    file = open(outfile, "w")
    file.write("[\n")
    i=0
    for i,expr in enumerate(samples):
        if i<12 or i>116:
            continue
        if (i!=0):
            file.write(",")
        print(i)
        module_name = ""
        simplify_result = []
        start_time = time.time()
        for m_num, module in enumerate(modules):
            # if m_num == 0 and expr.length()<150:
            #     continue
            simplified = module.simplify(expr)

            simplify_result.append(module.getDict_fromExpr(expr, simplified))
            if m_num == 0 and simplified:
                break
        if simplify_result:
            simplify_result.sort(key=lambda x:x["result_leng"])
            tmpdict = simplify_result[0]

            # tmpdict = getDict_fromExpr(expr, simplified)
            endtime = round(time.time() - start_time, 2)
            tmpdict['time'] = endtime
            tmpdict["id"] = i
            # tmpdict['module'] = module_name
            file.write(json.dumps(tmpdict, indent=2))

        i+=1
    file.write("\n]")
    file.close()

def run(synthesis_module_type, sample_type):
    filename = "./result/msynth_synth_%s_%s_1028.json" % (synthesis_module_type, sample_type)
    run_PLASynth(samples=samples,outfile=filename)

if __name__ == "__main__":
    # pass
    synthesis_module_type = "msynth_synth"
    sample_type = "tigress"

    samples = get_sample(sample_type)
    run(synthesis_module_type, sample_type)

