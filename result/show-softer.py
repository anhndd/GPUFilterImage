import matplotlib.pyplot as plt
import numpy as np
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}

plt.rc('font', **font)

maina = open("LimogesBenedictins/CPU_Program/main_a_softer.txt", "r")
ya = maina.read().split("\n")
ya.remove('')
sumlinesa = ya[1000]
ya.remove(sumlinesa)
ya = np.array(ya)
ya = ya.astype(np.float)
x = range(0, len(ya))

mainb = open("LimogesBenedictins/GPU_NonSharedMem/main_b_softer.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[1000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)

mainc = open("LimogesBenedictins/GPU_SharedMem/main_c_softer.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[1000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)

fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.plot(x, yb, label="None Shared Mem")
axs.plot(x, yc, label="Shared Mem")
axs.plot(x, ya, label="CPU Program")
axs.set_title('Filter Softer - Running time every instance')
axs.set_xlabel('instances')
axs.set_ylabel('Execution Time (ms)')
axs.legend(loc='best')
#mintemp = min(np.concatenate((yb,yc)))
#axs.set_ylim(mintemp - 0.01,0.15)

plt.show()
