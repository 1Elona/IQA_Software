import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置字体以便支持中文（根据您系统支持的字体进行选择）
plt.rcParams['font.sans-serif'] = ['Songti SC']
#or
plt.rcParams['font.sans-serif'] = ['Wawati TC']
#or
plt.rcParams['font.sans-serif'] = ['STHeiti']
#or
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# 读取CSV文件
df = pd.read_csv('../quant.csv')

# 构造一个新的 DataFrame 来存储 combined 列
combined_df = df.iloc[:, 0:5].astype(str).agg('_'.join, axis=1)
df['combined'] = combined_df

# 设置图表的颜色和选取需要绘图的指标列名称
colors = ['red']
metrics = df.columns[-7:]  # 最后7列为度量值











# 遍历所有指标列，并为每个指标绘制图表
for i, metric in enumerate(metrics):





    plt.figure(figsize=(50, 20))  # 设置每个指标图表的大小

    # ... (省略之前的代码)

    # 获取度量数据并计算最大值和最小值来设定步长
    df[metric] = pd.to_numeric(df[metric], errors='coerce')
    y_min, y_max = df[metric].min(), df[metric].max()

    # 动态设置步长，确保最小步长为一个较小的正数
    min_step = 0.01  # 设定一个最小步长阈值，避免步长为零
    if y_max - y_min > 1:
        step = 0.5
    elif y_max - y_min > 0.1:
        step = 0.1
    else:
        step = min_step  # 如果计算出的步长太小，使用最小步长阈值

    # 确保步长不为零
    step = max(step, min_step)

    # 设置 y 轴的步长
    plt.yticks(np.arange(np.floor(y_min), np.ceil(y_max) + step, step))

    # 绘制数据
    plt.plot(df['combined'], df[metric], linestyle='-', marker='o', linewidth=2, label=metric,
             color=colors[0])

    # 绘图后添加标题、轴标签和图例
    plt.title(metric + ' vs Combined Parameters')
    plt.xlabel('Combined Parameters')
    plt.ylabel(metric)
    plt.legend()  # 将图例放在合适的位置

    # 设置图标布局优化和x轴标签的旋转，以确保标签不重叠
    plt.xticks(rotation=45, ha='right')  # ha参数用于设置对齐方式
    plt.tight_layout()
    plt.grid(True)  # 显示网格线

    # 调整坐标轴标签之间的间隔
    ax = plt.gca()  # 获取当前图表的坐标轴信息
    ax.tick_params(axis='x', which='major', pad=15)  # 增加x轴标签与刻度线之间的距离
    ax.tick_params(axis='y', which='major', pad=15)  # 增加y轴标签与刻度线之间的距离

    # 保存每个指标的图表到文件
    filename = f'chart_{metric}.png'
    plt.savefig(filename)
