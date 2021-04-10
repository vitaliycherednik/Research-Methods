import random
import numpy as np
from numpy.linalg import solve
from scipy.stats import f,t

x1min = -25
x1max = -5
x2min = 15
x2max = 50
x3min = -25
x3max = -15

ymax = 200 + (x1max + x2max + x3max) / 3
ymin = 200 + (x1min + x2min + x3min) / 3

xn = [[1, 1, 1, 1, 1, 1, 1, 1],
      [-1, -1, 1, 1, -1, -1, 1, 1],
      [-1, 1, -1, 1, -1, 1, -1, 1],
      [-1, 1, 1, -1, 1, -1, -1, 1]]

x1x2_norm = [0] * 8
x1x3_norm = [0] * 8
x2x3_norm = [0] * 8
x1x2x3_norm = [0] * 8
for i in range(8):
    x1x2_norm[i] = xn[1][i] * xn[2][i]
    x1x3_norm[i] = xn[1][i] * xn[3][i]
    x2x3_norm[i] = xn[2][i] * xn[3][i]
    x1x2x3_norm[i] = xn[1][i] * xn[2][i] * xn[3][i]

y1 = [random.randint(int(ymin), int(ymax)) for i in range(8)]
y2 = [random.randint(int(ymin), int(ymax)) for i in range(8)]
y3 = [random.randint(int(ymin), int(ymax)) for i in range(8)]

Y = [[y1[0], y2[0], y3[0]],
     [y1[1], y2[1], y3[1]],
     [y1[2], y2[2], y3[2]],
     [y1[3], y2[3], y3[3]],
     [y1[4], y2[4], y3[4]],
     [y1[5], y2[5], y3[5]],
     [y1[6], y2[6], y3[6]],
     [y1[7], y2[7], y3[7]]]
print("Матриця планування Y (m=3):")
for i in range(8):
    print(Y[i])

x0 = [1, 1, 1, 1, 1, 1, 1, 1]
x1 = [-25, -25, -5, -5, -25, -25, -5, -5]
x2 = [15, 50, 15, 50, 15, 50, 15, 50]
x3 = [-25, -15, -15, -25, -15, -25, -25, -15]
x1x2 = [0] * 8
x1x3 = [0] * 8
x2x3 = [0] * 8
x1x2x3 = [0] * 8
for i in range(8):
    x1x2[i] = x1[i] * x2[i]
    x1x3[i] = x1[i] * x3[i]
    x2x3[i] = x2[i] * x3[i]
    x1x2x3[i] = x1[i] * x2[i] * x3[i]

Y_average = []
for i in range(len(Y)):
    Y_average.append(np.mean(Y[i], axis=0))

list_for_b = [xn[0], xn[1], xn[2], xn[3], x1x2_norm, x1x3_norm, x2x3_norm, x1x2x3_norm]
list_for_a = list(zip(x0, x1, x2, x3, x1x2, x1x3, x2x3, x1x2x3))
print("Матриця планування X:")
for i in range(8):
    print(list_for_a[i])
bi = []
for k in range(8):
    S = 0
    for i in range(8):
        S += (list_for_b[k][i] * Y_average[i]) / 8
    bi.append(round(S, 5))

ai = [round(i, 5) for i in solve(list_for_a, Y_average)]
print("Рівняння регресії: \n" "y = {} + {}*x1 + {}*x2 + {}*x3 + {}*x1x2 + {}*x1x3 + {}*x2x3 + {}*x1x2x3".format(ai[0], ai[1],
                                                                            ai[2], ai[3],ai[4], ai[5], ai[6], ai[7]))

print("Рівняння регресії для нормованих факторів: \n" "y = {} + {}*x1 + {}*x2 + {}*x3 + {}*x1x2 + {}*x1x3 + {}*x2x3 + {"
      "}*x1x2x3".format(bi[0], bi[1], bi[2], bi[3], bi[4], bi[5], bi[6], bi[7]))

print("------------------------------- Перевірка за критерієм Кохрена -------------------------------")
print("Середні значення відгуку за рядками:", "\n", +Y_average[0], Y_average[1], Y_average[2], Y_average[3],
      Y_average[4], Y_average[5], Y_average[6], Y_average[7])
dispersions = []
for i in range(len(Y)):
    a = 0
    for k in Y[i]:
        a += (k - np.mean(Y[i], axis=0)) ** 2
    dispersions.append(a / len(Y[i]))

Gp = max(dispersions) / sum(dispersions)
Gt = 0.5157
if Gp < Gt:
    print("Дисперсія однорідна")
else:
    print("Дисперсія неоднорідна")

print("------------------ Перевірка значущості коефіцієнтів за критерієм Стьюдента ------------------")
sb = sum(dispersions) / len(dispersions)
sbs = (sb / (8 * 3)) ** 0.5

t_list = [abs(bi[i]) / sbs for i in range(0, 8)]

d = 0
res = [0] * 8
coefs1 = []
coefs2 = []
m = 3
n = 8
F3 = (m - 1) * n
for i in range(8):
    if t_list[i] < t.ppf(q=0.975, df=F3):
        coefs2.append(bi[i])
        res[i] = 0
    else:
        coefs1.append(bi[i])
        res[i] = bi[i]
        d += 1
print("Значущі коефіцієнти регресії:", coefs1)
print("Незначущі коефіцієнти регресії:", coefs2)

y_st = []
for i in range(8):
    y_st.append(res[0] + res[1] * xn[1][i] + res[2] * xn[2][i] + res[3] * xn[3][i] + res[4] * x1x2_norm[i]\
                + res[5] * x1x3_norm[i] + res[6] * x2x3_norm[i] + res[7] * x1x2x3_norm[i])
print("Значення з отриманими коефіцієнтами:", y_st)

print("------------------------- Перевірка адекватності за критерієм Фішера -------------------------")
Sad = m * sum([(y_st[i] - Y_average[i] ) ** 2 for i in range(8)]) / (n - d)
Fp = Sad / sb
F4 = n - d
if Fp < f.ppf(q=0.95, dfn=F4, dfd=F3):
    print("Рівняння регресії адекватне при рівні значимості 0.05")
else:
    print("Рівняння регресії неадекватне при рівні значимості 0.05")

