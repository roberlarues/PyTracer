import pandas as pd
import matplotlib.pyplot as plt





df = pd.read_csv('time_list.data')

# Seleccionar setosa y versicolor

values = df.iloc[:, [0]].values



plt.plot(values)
plt.ylabel('Time per pixel each 50px (ms)')
plt.show()