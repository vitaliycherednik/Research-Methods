import random
import time

start_time = time.clock()

a0 = random.randint(1, 20)
a1 = random.randint(1, 20)
a2 = random.randint(1, 20)
a3 = random.randint(1, 20)

x1 = [random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),
      random.randint(1, 20),random.randint(1, 20),random.randint(1, 20)]
x2 = [random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),
      random.randint(1, 20),random.randint(1, 20),random.randint(1, 20)]
x3 = [random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),random.randint(1, 20),
      random.randint(1, 20),random.randint(1, 20),random.randint(1, 20)]

Y = [0] * 8

for i in range(8):
    Y[i] = a0 + a1*x1[i] + a2*x2[i] + a3*x3[i]

x01 = (max(x1) + min(x1)) / 2
x02 = (max(x2) + min(x2)) / 2
x03 = (max(x3) + min(x3)) / 2

dx1 = max(x1) - x01
dx2 = max(x2) - x02
dx3 = max(x3) - x03

xn1 = [0] * 8
xn2 = [0] * 8
xn3 = [0] * 8

for i in range(8):
    xn1[i] = (x1[i] -x01) / dx1
    xn2[i] = (x2[i] - x02) / dx2
    xn3[i] = (x3[i] - x03) / dx3

Yet = a0 + a1*x01 + a2*x02 + a3*x03

# variant 226
max_y = [0] * 8
for i in range(8):
    max_y[i] = (Y[i] - Yet)**2
max_value = max(max_y)

print("Коефіцієнти : a0 =", a0,", a1 =", a1, ", a2 =", a2,", a3 =", a3 ,"\n")
print("X1 = ", x1)
print("X2 = ", x2)
print("X3 = ", x3)
print("x01 =", x01, ", x02 =", x02,", x03 =", x03)
print("dx1 =", dx1, ", dx2 =", dx2,", dx3 =", dx3, "\n")
print("Y = ", Y, "\n")
print("xn1 =", xn1)
print("xn2 =", xn2)
print("xn3 =", xn3, "\n")
print("Еталонне значення Y:", Yet)
print("max((Y - Yet)^2) =", max_value)

print("Час виконання програми:" , (time.clock() - start_time), "seconds")
