import time
import pandas as pd

stop_data = pd.read_csv('stop_detection.csv')
index = 0
for i in range(len(stop_data)):
    now = int(time.strftime('%H%M%S'))
    if now < stop_data['start'][i]:
        index = i
        break

print(index)

now = int(time.strftime('%H%M%S'))
if stop_data['start'][index] <= now <= stop_data['end'][index]:
    stop_dtct = True
elif now > stop_data['end'][index]:
    stop_dtct = False
    index += 1

print(now)
print(stop_dtct)
print(index)            
