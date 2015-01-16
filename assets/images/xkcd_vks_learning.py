from matplotlib import pyplot as plt
import numpy as np
plt.xkcd()

ymin = -25

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xticks([])
plt.yticks([])
ax.set_ylim([ymin, 10])

data = [5 - .3 * t for t in range(10)]
data += [data[-1] - .8 * t for t in range(10)]
data += [data[-1] + .4 * t for t in range(10)]
data += [data[-1] + 1.5 * t for t in range(10)]

plt.annotate(
    'Start of high school',
    xy=(10, -.01), arrowprops=dict(arrowstyle='->'), xytext=(2, -8))

plt.annotate(
    "Leave me alone I'm \njust not that smart",
    xy=(14, -.6), arrowprops=dict(arrowstyle='->'), xytext=(4, 5))

plt.annotate(
    "Mlle Tayrac",
    xy=(19, -5), arrowprops=dict(arrowstyle='->'), xytext=(10, -20))

plt.annotate(
    "Maybe smarts has \nnothing to do with this...",
    xy=(27, -2), arrowprops=dict(arrowstyle='->'), xytext=(17, -15))

plt.annotate(
    "Bac",
    xy=(30, -1.5), arrowprops=dict(arrowstyle='->'), xytext=(25, 5))

plt.annotate(
    "Working hard \nmakes me happy",
    xy=(35, 5), arrowprops=dict(arrowstyle='->'), xytext=(29, -5))


plt.plot(data)

plt.xlabel('time')
plt.ylabel('my work effort')
plt.savefig('xkcd_vks_learning.png', bbox_inches='tight')
