import matplotlib.pyplot as plt
import numpy as np

def acker(m, n, s ="% s"):
    print(s % ("acker(% d, % d)" % (m, n)))
    if m == 0:
        return n + 1
    if n == 0:
        return acker(m - 1, 1, s)
    n2 = acker(m, n - 1, s % ("acker(% d, %% s)" % (m - 1)))
    return acker(m - 1, n2, s)

print(acker(1, 2))

for i in range(10):
    x = 1
y = acker(x,x)

plt.plot(x, y)
plt.show()