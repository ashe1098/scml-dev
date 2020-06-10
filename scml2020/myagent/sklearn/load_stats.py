import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path

def get_stats(directory):
    for f in Path(directory).glob("**/stats.csv"):
        yield f

# print(Path(__file__).resolve())
path_dir = Path(__file__).parent / "../worlds"  # 提出時はどういうパスにすればいい？
# print(path_dir.resolve())  
# print(list(Path(path_dir).glob("**/stats.csv")))

stats = None
for path in get_stats(path_dir):
    print(path)
    target = np.genfromtxt(path, delimiter=",", skip_header=1)
    print(np.shape(target))
    print(target)
    if stats is None:
        stats = target
    else:
        stats = np.block([[[stats]], [[target]]])  # ステップ数が変わるから次元が合わせられない．どうする？nanで埋めるか
print(stats)