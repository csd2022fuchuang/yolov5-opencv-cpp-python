import cv2
import numpy as np
import sympy as sp


areaPoint_obj = [(500, 520), (400, 650), (600, 650), (650, 520)]


def isAreaDetect(areaPoint, point, img='NULL'):
    """
        判断点在area内
    """
    areaMinX = min(list([k[0] for k in areaPoint]))
    areaMaxX = max(list([k[0] for k in areaPoint]))
    areaMinY = min(list([k[1] for k in areaPoint]))
    areaMaxY = max(list([k[1] for k in areaPoint]))
    if not (areaMinX <= point[0] <= areaMaxX and areaMinY <= point[1] <= areaMaxY): #在区域外
        return False

    base_point = (5, 5) #初始化射线
    base_x = [base_point[0], point[0]]
    base_y = [base_point[1], point[1]]
    base_f = np.polyfit(base_y, base_x, 1)
    base_fy = np.poly1d(base_f)
    base_fy_k = base_fy[1]
    base_fy_b = base_fy[0]

    y = sp.symbols('y')  # 未知数Y
    x = sp.symbols('x')  # 未知数X

    crash = 0
    for count in range(len(areaPoint)-1): #遍历区域边
        point1 = areaPoint[count]
        point2 = areaPoint[count+1]
        xx = [point1[0], point2[0]]
        yy = [point1[1], point2[1]]
        f = np.polyfit(yy, xx, 1)
        fy = np.poly1d(f)
        fy_k = fy[1]
        fy_b = fy[0]

        fy1 = fy_k * y + fy_b - x
        fy2 = base_fy_k * y + base_fy_b - x
        JXY = sp.solve([fy1, fy2], [x, y])  # 求交点坐标
        Jx = JXY[x]
        Jy = JXY[y]

        miny, maxy = min(yy), max(yy)
        minx, maxx = min(xx), max(xx)

        if miny - 5 <= Jy <= maxy + 5 and minx - 5 <= Jx <= maxx + 5 and \
                base_point[1] - 5 <= Jy <= point[1] + 5 and base_point[0] - 5 <= Jx <= point[0] + 5:
            crash += 1

        if not img == 'NULL':
            cv2.line(img, point1, point2, (0, 0, 255), 2, 1)

    point0 = areaPoint[0] #最后一个区域边
    point00 = areaPoint[-1]
    xx = [point0[0], point00[0]]
    yy = [point0[1], point00[1]]
    f = np.polyfit(yy, xx, 1)
    fy = np.poly1d(f)
    fy_k = fy[1]
    fy_b = fy[0]
    fy1 = fy_k * y + fy_b - x
    fy2 = base_fy_k * y + base_fy_b - x
    JXY = sp.solve([fy1, fy2], [x, y])  # 求交点坐标
    Jx = JXY[x]
    Jy = JXY[y]
    miny, maxy = min(yy), max(yy)
    minx, maxx = min(xx), max(xx)
    if miny - 5 <= Jy <= maxy + 5 and minx - 5 <= Jx <= maxx + 5 and \
            base_point[1] - 5 <= Jy <= point[1] + 5 and base_point[0] - 5 <= Jx <= point[0] + 5:
        crash += 1
    if not img == 'NULL':
        cv2.line(img, point0, point00, (0, 0, 255), 2, 1)

    if crash % 2 == 1:
        if not img == 'NULL':
            zi = f'YaArea'
            cv2.putText(img, zi, point, 4, .8, (0, 0, 255), 1)  # 可视化
        return True
    else:
        return False


def getAreaCore(areaPoint):
    """
        返回区域质心->int
    """
    x_sun = 0
    y_sun = 0
    for x, y in areaPoint:
        x_sun += x
        y_sun += y
    return x_sun//len(areaPoint), y_sun//len(areaPoint)


if __name__ == '__main__':
    pass
