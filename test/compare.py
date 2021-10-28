import json
# a= "/home/plas/work/PLASynth/test/result/data2_qsynth/msynth_synth_qsynth_1023.json"
# a = "/home/plas/work/PLASynth/test/result/data2_qsynth/msynth_simp_qsynth_1023.json"
a=  "/home/plas/work/PLASynth/controller/result/plasynth_qsynth.json"
with open(a) as simp:
    simtime = 0.0
    syntime = 0.0
    time = 0.0
    obf_leng = 0
    result_leng = 0
    obf_var = 0
    result_var = 0
    cnt = 0
    count = 0
    msynth = json.load(simp)
    for i in msynth:
        try:
            # num = "data_%d" % i
            tmp = i
            # print(i["id"]," " ,count)
            # if tmp["obf_leng"] > 100:
            #     continue
            # print(i)

            # simtime += tmp["simtime"]
            # syntime += tmp["syntime"]
            # if tmp["success"]=="no":
            #     continue
            if tmp["result_expr"] =="FAIL":
                continue
            time += tmp["time"]
            obf_leng += tmp["obf_leng"]
            result_leng += tmp["result_leng"]
            obf_var += tmp["obf_var"]
            result_var += tmp["result_var"]
            cnt += 1


        except:
            print("error")

if cnt == 0:
    print("cnt == 0")
else:
    print(simtime)
    print(syntime)
    print(time)
    # print("avg simtime : %f" % float(simtime/float(cnt)))
    # print("avg syntime : %f" % float(syntime/float(cnt)))
    print("avg time : %f" % float(time/float(cnt)))
    print("obf_leng : %f" % (obf_leng/cnt))
    print("result_leng : %f" % (result_leng/cnt))
    print("obf_var : %f" % (obf_var/cnt))
    print("result_var : %f" % (result_var/cnt))
    print(cnt)
    # print(count)