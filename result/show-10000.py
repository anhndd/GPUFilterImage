import matplotlib.pyplot as plt
import numpy as np

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)

x = range(0, 10000)


fig, axs = plt.subplots(3, 2, tight_layout=True)
#########################################################
mainb = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_NonSharedMem/main_b_soften.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[10000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)
mainc = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_SharedMem/main_c_soften.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[10000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)
#axs.plot(x, ya, label="main_a")
axs[0][0].plot(x, yb, label="None Shared Mem")
axs[0][0].plot(x, yc, label="Shared Mem")
#    axs[0].plot(x,y, label="DQN model")
axs[0][0].set_title('Filter Soften - Running time every instance')
axs[0][0].set_xlabel('instances')
axs[0][0].set_ylabel('Execution Time (ms)')
axs[0][0].legend(loc='best')

#########################################################
mainb = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_NonSharedMem/main_b_sharpen.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[10000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)
mainc = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_SharedMem/main_c_sharpen.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[10000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)
#axs.plot(x, ya, label="main_a")
axs[0][1].plot(x, yb, label="None Shared Mem")
axs[0][1].plot(x, yc, label="Shared Mem")
#    axs[0].plot(x,y, label="DQN model")
axs[0][1].set_title('Filter Sharpen - Running time every instance')
axs[0][1].set_xlabel('instances')
axs[0][1].set_ylabel('Execution Time (ms)')
axs[0][1].legend(loc='best')
mintemp = min(np.concatenate((yb,yc)))
axs[0][1].set_ylim(mintemp - 0.01,0.15)

#########################################################
mainb = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_NonSharedMem/main_b_shatter.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[10000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)
mainc = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_SharedMem/main_c_shatter.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[10000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)
#axs.plot(x, ya, label="main_a")
axs[1][0].plot(x, yb, label="None Shared Mem")
axs[1][0].plot(x, yc, label="Shared Mem")
#    axs[0].plot(x,y, label="DQN model")
axs[1][0].set_title('Filter Shatter - Running time every instance')
axs[1][0].set_xlabel('instances')
axs[1][0].set_ylabel('Execution Time (ms)')
axs[1][0].legend(loc='best')
mintemp = min(np.concatenate((yb,yc)))
axs[1][0].set_ylim(mintemp - 0.01,0.15)

#########################################################
mainb = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_NonSharedMem/main_b_blur.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[10000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)
mainc = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_SharedMem/main_c_blur.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[10000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)
#axs.plot(x, ya, label="main_a")
axs[1][1].plot(x, yb, label="None Shared Mem")
axs[1][1].plot(x, yc, label="Shared Mem")
#    axs[0].plot(x,y, label="DQN model")
axs[1][1].set_title('Filter Blur - Running time every instance')
axs[1][1].set_xlabel('instances')
axs[1][1].set_ylabel('Execution Time (ms)')
axs[1][1].legend(loc='best')
mintemp = min(np.concatenate((yb,yc)))
axs[1][1].set_ylim(mintemp - 0.01,0.15)

#########################################################
mainb = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_NonSharedMem/main_b_horisobel.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[10000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)
mainc = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_SharedMem/main_c_horisobel.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[10000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)
#axs.plot(x, ya, label="main_a")
axs[2][0].plot(x, yb, label="None Shared Mem")
axs[2][0].plot(x, yc, label="Shared Mem")
#    axs[0].plot(x,y, label="DQN model")
axs[2][0].set_title('Filter Horisobel - Running time every instance')
axs[2][0].set_xlabel('instances')
axs[2][0].set_ylabel('Execution Time (ms)')
axs[2][0].legend(loc='best')
mintemp = min(np.concatenate((yb,yc)))
axs[2][0].set_ylim(mintemp - 0.01,0.15)

#########################################################
mainb = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_NonSharedMem/main_b_versobel.txt", "r")
yb = mainb.read().split("\n")
yb.remove('')
sumlinesb = yb[10000]
yb.remove(sumlinesb)
yb = np.array(yb)
yb = yb.astype(np.float)
mainc = open("LimogesBenedictins/LimogesBenedictins_10000/GPU_SharedMem/main_c_versobel.txt", "r")
yc = mainc.read().split("\n")
yc.remove('')
sumlinesc = yc[10000]
yc.remove(sumlinesc)
yc = np.array(yc)
yc = yc.astype(np.float)
#axs.plot(x, ya, label="main_a")
axs[2][1].plot(x, yb, label="None Shared Mem")
axs[2][1].plot(x, yc, label="Shared Mem")
#    axs[0].plot(x,y, label="DQN model")
axs[2][1].set_title('Filter Versobel - Running time every instance')
axs[2][1].set_xlabel('instances')
axs[2][1].set_ylabel('Execution Time (ms)')
axs[2][1].legend(loc='best')
mintemp = min(np.concatenate((yb,yc)))
axs[2][1].set_ylim(mintemp - 0.01,0.15)

plt.show()
