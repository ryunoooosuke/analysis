import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
 
# データ準備
x = np.array([1,2,4,6,7,7,7,7,7,7,7,7,8,9,12,12,13,13,16,17,17,17,17,17,17,17,19,26,28]) # (1)距離
y = np.array([6.6,7.0,6.5,7.4,6.1,6.9,7.0,6.9,6.9,6.9,6.8,7.0,6.1,6.4,6.1,6.1,6.5,7.3,5.5,5.8,5.4,5.6,5.8,5.4,5.8,5.7,5.4,4.1,4.4]) # (2)家賃

# 相関係数の計算
# リストをps.Seriesに変換
s1=pd.Series(x)
s2=pd.Series(y)
# pandasを使用してPearson's rを計算
res=s1.corr(s2)   # numpy.float64 に格納される
print(res)

# 回帰分析　線形
mod = LinearRegression()
df_x = pd.DataFrame(x)
df_y = pd.DataFrame(y)
# 線形回帰モデル、予測値、R^2を評価
mod_lin = mod.fit(df_x, df_y)
y_lin_fit = mod_lin.predict(df_x)
r2_lin = mod.score(df_x, df_y)
plt.plot(df_x, y_lin_fit, color = '#000000', linewidth=0.5)
 
# グラフの装飾
# plt.xlim(15.0, 40.0) # (3)x軸の表示範囲
# plt.ylim(300, 750) # (4)y軸の表示範囲
plt.title("test", fontsize=20) # (5)タイトル
plt.xlabel("x", fontsize=20) # (6)x軸ラベル
plt.ylabel("y", fontsize=20) # (7)y軸ラベル
plt.grid(True) # (8)目盛線の表示
plt.text(1, 5, "r = " + str(res))
plt.text(1, 5.2, '$ R^{2} $=' + str(round(r2_lin, 4)))
plt.tick_params(labelsize = 12) # (9)目盛線のラベルサイズ
 
# グラフの描画
plt.scatter(x, y, s=25, c="b", marker="D", alpha=0.5) #(10)散布図の描画
plt.show()

