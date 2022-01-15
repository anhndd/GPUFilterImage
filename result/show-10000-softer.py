import matplotlib.pyplot as plt
import numpy as np

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}

plt.rc('font', **font)

x = range(0, 10000)

mainb = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_NonSharedMem/main_b_softer.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[10000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)

mainc = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_SharedMem/main_c_softer.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[10000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)

fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.plot(x, yb, label="None Shared Mem")
axs.plot(x, yc, label="Shared Mem")
axs.set_title('Filter Softer - Running time every instance')
axs.set_xlabel('instances')
axs.set_ylabel('Execution Time (ms)')
axs.legend(loc='best')

plt.show()
