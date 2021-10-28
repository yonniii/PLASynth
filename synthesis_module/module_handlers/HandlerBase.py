from msynth.utils.expr_utils import get_unification_candidates
import sys

class HandlerBase():

    def getDict_fromExpr(self, expr, simplified):
        tmpdict = {}
        tmpdict['module'] = self.get_module_name()
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
            tmpdict['result_leng'] = sys.maxsize
            tmpdict['result_var'] = 0
        return tmpdict

    def get_module_name(self):
        return "no_defined"