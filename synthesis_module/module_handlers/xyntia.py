import os
from miasm.expression.expression import *
from msynth.utils.expr_utils import get_unification_candidates
import re
from synthesis_module.module_handlers.HandlerBase import HandlerBase

class Parser():
    def __init__(self, basepath):
        self.basepath = basepath

    def __insertInt(self,n):
        m = n.group()
        return "ExprInt(%s, size)" % m

    def __get_length(self, expr: str, size=32):
        expr = expr.replace("++", "+")
        expr = expr.replace("/", "*")
        expr = expr.replace("not", "~")
        expr = expr.replace("s", "")
        for i in range(5):
            tmp = "v%d" % i
            expr = expr.replace(tmp, chr(ord('a') + i))
        a = ExprId('a', size)
        b = ExprId('b', size)
        c = ExprId('c', size)
        d = ExprId('d', size)
        e = ExprId('e', size)
        const_1 = ExprInt(1, size)
        const_2 = ExprInt(2, size)

        expr = re.sub(r'\b\d+\b', self.__insertInt, expr)
        expr = re.sub(r'\b0x\w+\b', self.__insertInt, expr)

        try:
            e = eval(expr)
        except:
            print("error")
        return e.length(), len(get_unification_candidates(e))

    def get_parsed_dict(self,expr):
        with open(f"{self.basepath}/result", 'r') as f:
            data = f.read()
            mylist = data.splitlines()

            time = -1.0
            for line in mylist:
                # line = f.readline()[:-1]
                if line.startswith("expression:"):
                    obf = line.split(": ")[-1].replace("<32>", "")
                    obf_leng, obf_var = self.__get_length(obf)
                elif line.startswith("simplified:"):
                    result = line.split(": ")[-1].replace("<32>", "")
                    result_leng, result_var = self.__get_length(result)
                elif line.startswith("success:"):
                    success = line.split(": ")[-1]
                elif line.startswith("synthesis time:"):
                    time = float(line.split(": ")[-1])
                elif line.startswith("simplification time:"):
                    time += float(line.split(": ")[-1])
        if time < 0:
            return False
        return {"obf_expr":str(expr),"obf_expr_xyntia": obf, "obf_leng": obf_leng, "result_expr": result, "result_leng": result_leng,
                              "success": success, "time": time, "obf_var": obf_var,
                              "result_var": result_var}

isput = False
stack = []
for p in reversed(os.getcwd().split("/")):
    if p=="PLASynth":
        isput = True
    if isput:
        stack.append(p)
stack = reversed(stack)
base = "/".join(stack)


xyntia_basepath = os.path.join(base,"synthesis_module/xyntia")
sample = os.path.join(base,"synthesis_module/xyntia/samples/output.json")


class Xyntia(HandlerBase):
    def __init__(self):
        self.result_parser = Parser(xyntia_basepath)

    def replace(self, m):
        n = m.group()
        if n =='a':
            return "v0"
        elif n == 'b':
            return "v1"
        elif n == 'c':
            return "v2"
        elif n == 'd':
            return "v3"
        elif n == 'e':
            return "v4"
        return "fail"

    def simplify(self, expr):
        expr = str(expr)
        expr = re.sub(r'\b[abcde]\b', self.replace, expr)
        out = "/home/plas/work/PLASynth/synthesis_module/xyntia/output.json"
        cmd = f"rm {out}"
        os.system(cmd)
        cmd = f"python3 {xyntia_basepath}/sample.py --expr \"{expr}\" > {sample}"
        os.system(cmd)

        cmd = f"{xyntia_basepath}/xyntia.sh {sample} > {xyntia_basepath}/result"
        try:
            os.system(cmd)
        except:
            print("error-xyntia \n %s" % expr)
        return None


    def getDict_fromExpr(self, expr, simplified):
        tmp = self.result_parser.get_parsed_dict(expr)
        tmp['module'] = self.get_module_name()
        return tmp

    def get_module_name(self):
        return "xyntia"

# simplify("v0+v1+4")
# print(result_parser.get_parsed_dict())
# print(result_parser.get_parsed_dict())
