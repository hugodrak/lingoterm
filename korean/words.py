import time
import random

count = 0
corr = 0
done = []
t1 = time.time()
prev = ""

cmap = {}

with open("new_dataset.txt", "r") as f:
    lines = f.read().splitlines()
    for i, line in enumerate(lines):
        sp = line.split("\t")
        try:
            cmap[sp[0]] = {"hang": sp[1], "eng": sp[2], "rom": sp[3]}
        except IndexError:
            print(f"Bad formatting on line: {i+1}")

END = 40
keys = list(cmap.keys())
print("Dataset length:", len(keys))
START = random.randint(0, len(keys)-END)
while True:
    i = random.randint(START, START+END)
    if i in done:
        if len(done) == len(keys):
            print('Time:', int(time.time() - t1), 's')
            break

        continue
    count += 1
    lett = cmap[keys[i]]["rom"].lower()
    eng = cmap[keys[i]]["eng"]
    print(cmap[keys[i]]["hang"])
    ans = input('=> ')
    prev = ""
    if ans == lett:
        done.append(i)
        corr += 1
        prev += '👍 ' + f'{int((corr*100)/count)}% => {eng}'
    else:
        #print("fail! Correct:", lett)
        #break
        prev += '👎 ' + lett + f" => {eng}"
    prev += "\n"
    print(prev)
