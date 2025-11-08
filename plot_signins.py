# %%
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
# %%
swipes_file = Path("logs/swipes.txt")
# %%
with swipes_file.open(encoding="utf-8") as f:
    contents = f.readlines()
# %%
swipes = list(map(lambda d: datetime.strptime(d, "%Y-%m-%d %H:%M:%S\n"), contents))
# %%
df = pd.DataFrame({"date": swipes})
df['weekday'] = df['date'].dt.weekday
df['hour'] = df['date'].dt.hour
df.head()
# %%
heatmap_data = np.zeros((7, 24))

for idx,row in df.iterrows():
    heatmap_data[row['weekday'], row['hour']] += 1
# %%
xlabel = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
ylabel = list(map(lambda h: str(h%12) + (" pm" if h//12 else " am"), np.arange(0, 24)))
ylabel[0] = "12 am"
ylabel[12] = "12 pm"
# %%
plt.rcParams.update({'font.size': 20})

fig, ax = plt.subplots(figsize=(15, 10))
cmap = ax.imshow(heatmap_data.T, aspect='auto', cmap="Blues")
fig.colorbar(cmap, ax=ax, label="Swipes per Hour")
ax.set_xticks(np.arange(0,7), xlabel)
ax.set_yticks(np.arange(0,24), ylabel)

ax.set_ylim(6, 24)
ax.invert_yaxis()
# ax.legend()

ax.set_title(f"Swipes per Hour from {df.iloc[0].date.strftime('%m/%d/%Y')} to {df.iloc[-1].date.strftime('%m/%d/%Y')}")

plt.savefig("logs/swipes.pdf")
# %%
