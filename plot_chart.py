# Last Modified by:
# Authors: Gong Sicong
# Studentnumbers: 5711932

import matplotlib.pyplot as plt
import numpy as np
import math

labels = ['5000', '500000', '5000000', '50000000']
python = [math.log(172), math.log(685), math.log(69519), math.log(670747)]
cpp_debug = [math.log(195), math.log(515), math.log(3654), math.log(31155)]
cpp_release = [math.log(204), math.log(228), math.log(549), math.log(3876)]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, python, width, label='python')
rects2 = ax.bar(x, cpp_debug, width, label='cpp_debug')
rects3 = ax.bar(x + width, cpp_release, width, label='cpp_release')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('lg(Time Cost)')
ax.set_xlabel('Iteration Times')
ax.set_title('Time Cost for Different Iterations Times and Language')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=1)
ax.bar_label(rects2, padding=2)
ax.bar_label(rects3, padding=3)

fig.tight_layout()

plt.show()