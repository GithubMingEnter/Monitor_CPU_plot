import psutil
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import pandas as pd
# CSV 文件路径
csv_file_path = "cpu_usage.csv"
plt.style.use("bmh")
# 创建 CSV 文件并写入表头
with open(csv_file_path, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Timestamp"] + [f"Core {i+1}" for i in range(psutil.cpu_count())])

# 设置图形
plt.ion()  # 开启交互模式
fig, ax = plt.subplots()
bar_container = ax.bar([], [])
ax.set_ylim(0, 100)
ax.set_xlabel("CPU core")
ax.set_ylabel("CPU Usage rate (%)")
ax.set_title("CPU Usage rate display")
plt.xticks(range(psutil.cpu_count()), [f"Core {i+1}" for i in range(psutil.cpu_count())])

# 动态更新图和写入到 CSV
try:
    while True:
        # 获取 CPU 占用率
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

        # 输出到 CSV
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(csv_file_path, "a", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([timestamp] + cpu_usage)

        # 动态绘制图
        if not bar_container:
            bar_container = ax.bar(range(len(cpu_usage)), cpu_usage)
        else:
            for bar, usage in zip(bar_container, cpu_usage):
                bar.set_height(usage)

        # 重新绘制图形
        plt.draw()
        plt.pause(0.1)  # 刷新速度

except KeyboardInterrupt:
    print("动态更新已停止。")

# 结束时关闭plt
plt.ioff()
plt.figure(2)
try:
    #read data
    with open('cpu_usage.csv',"r") as f:
        reader = pd.read_csv(f)
    reader['Timestamp'] = pd.to_datetime(reader['Timestamp'])
    reader['Time_Elapsed'] = (reader['Timestamp']-reader['Timestamp'].iloc[0]).dt.total_seconds()
    # plt.figure(figsize=(10, 5))
    for i in range(1,len(reader.columns)-1):
        plt.plot(reader['Time_Elapsed'],reader.iloc[:,i],label=f"Core {i}")
    
    plt.legend(loc='upper left')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage')
    plt.title('CPU Usage changes over time')
    plt.show()
    plt.savefig('cpu_usage.png',dpi=300) # save fig
except Exception as e:
    print(f"{e=}")