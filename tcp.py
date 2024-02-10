# andrzej-skuridin
# python 3.11

import matplotlib.pyplot as plt
import numpy as np


def angle_from_cos_theorem(side1: int | float,
                           side2: int | float,
                           side3: int | float) -> float:
    """Возвращает угол, входящий в теорему косинусов (в радианах).
    side3 - сторона, противолежащая углу, остальные - прилежащие."""
    return np.arccos(
        (side1 ** 2 + side2 ** 2 - side3 ** 2) / (2 * side1 * side2)
    )


def angle_theta(side1: int | float,
                side2: int | float,
                side3: int | float) -> int | float:
    """Возвращает угол между side2 и воображаемым продолжением side1 (в градусах).
    side1 - локоть перед сочленением,
    side2 - локоть после сочленения,
    side3 - достраиваемая сторона для формирования треугольника."""
    return 180 - np.degrees(angle_from_cos_theorem(side1, side2, side3))


# Ввод данных - координаты TCP и длины локтей.
tcp_x = float(input('Enter TCP x-coordinate: '))
B_y = float(input('Enter TCP y-coordinate: '))

OA = float(input('Enter L1: '))
AB = float(input('Enter L2: '))
BC = float(input('Enter L3: '))

# Вспомогательные вычисления
B_x = tcp_x - BC
OB = np.linalg.norm(np.array([B_x, B_y]))

angle_AOB = angle_from_cos_theorem(OA, OB, AB)
angle_BOX = np.arctan(B_y / B_x)

switcher = 0
while switcher not in (1, 2):
    print('Роборука выгнута вверх или вниз на узле А? 1 - вверх, 2 - вниз.')
    switcher = int(input())

if switcher == 1:
    # рука выгнута вверх
    angle_theta_1 = angle_AOB + angle_BOX

    A_y = OA * np.sin(angle_theta_1)
    A_x = OA * np.cos(angle_theta_1)

else:
    # рука выгнута вниз
    angle_theta_1 = angle_BOX - angle_AOB
    A_y = OA * np.sin(angle_theta_1)
    A_x = OA * np.cos(angle_theta_1)

AC = np.linalg.norm(np.array([tcp_x - A_x, B_y - A_y]))

angle_theta_2 = angle_theta(OA, AB, OB)
angle_theta_3 = angle_theta(AB, BC, AC)

print(f'angle_theta_1 {np.degrees(angle_theta_1)}')
print(f'angle_theta_2: {angle_theta_2}')
print(f'angle_theta_3: {angle_theta_3}')

# plot
plt.plot([0, A_x], [0, A_y], marker='o')
plt.plot([A_x, B_x], [A_y, B_y], marker='o')
plt.plot([B_x, tcp_x], [B_y, B_y], marker='o')
plt.grid()

# annotation
plt.text(0, 0, f'O(0; 0)')
plt.text(A_x, A_y, f'A({round(A_x, 2)}; {round(A_y, 2)})')
plt.text(B_x, B_y, f'B({B_x}; {B_y})')
plt.text(tcp_x, B_y, f'C({tcp_x}; {B_y})\nTCP')

plt.show()
