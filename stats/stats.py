testIndex = -1
#threshold = 0.6
data = dict()
for line in open("Hybrid Statistics.txt"):
    if len(line.strip()) == 1:
        testIndex += 1
        data[testIndex] = dict()
        continue
    data[testIndex][float(line.split(' : ')[0])] = eval(line.split(' : ')[1])

thresholds = sorted(list(data[0].keys()))
start = round(thresholds[0] * 100)
stop = round(thresholds[-1] * 100)
step = round((thresholds[1] - thresholds[0]) * 100)
for i in range(start, stop, step):
    threshold = i/100
    print("Threshold:", threshold)
    frr = []
    for i in range(0, testIndex + 1):
        frr.append(data[i][threshold]['falseReject'])

    totalTests = (data[0][threshold]['falseReject'] + data[0][threshold]['trueAccept'])

    print("FRR at threshold", threshold)
    print("Min:", str(round(min(frr)/totalTests, 3) * 100) + "%")
    print("Max:", str(round(max(frr)/totalTests, 3) * 100) + "%")
    print("Avg:", str(round(sum(frr)/len(frr)/totalTests, 3) * 100) + "%")

    far = []
    for i in range(0, testIndex + 1):
        far.append(data[i][threshold]['falseAccept'])

    print("FAR at threshold", threshold)
    print("Min:", str(round(min(far)/totalTests, 3) * 100) + "%")
    print("Max:", str(round(max(far)/totalTests, 3) * 100) + "%")
    print("Avg:", str(round(sum(far)/len(frr)/totalTests, 3) * 100) + "%")
    print("--------------------------------------")