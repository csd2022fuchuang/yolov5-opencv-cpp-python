import cv2
import numpy as np
import sympy as sp


#areaPoint_obj = [(500, 520), (400, 650), (600, 650), (650, 520)]


def isAreaDetect(areaPoint, point, img='NULL'):
    """
        判断点在area内
    """
    areaMinX = min(list([k[0] for k in areaPoint]))
    areaMaxX = max(list([k[0] for k in areaPoint]))
    areaMinY = min(list([k[1] for k in areaPoint]))
    areaMaxY = max(list([k[1] for k in areaPoint]))
    if not (areaMinX-5 <= point[0] <= areaMaxX+5 and areaMinY-5 <= point[1] <= areaMaxY+5): #在区域外
        return False

    base_point = (10, 10) #初始化射线
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

        if point1[1] == point2[1]: #平行于X轴的线段处理
            Jy = point1[1]
            Jx = base_fy(Jy)
            xx = [point1[0], point2[0]]
            minx, maxx = min(xx), max(xx)

            if not img == 'NULL':
                cv2.circle(img, (int(Jx), int(Jy)), 5, (255, 255, 255), 10) #展示所有平行点

            if minx - 5 <= Jx <= maxx + 5 and base_point[1] - 5 <= Jy <= point[1] + 5:
                crash += 1
                if not img == 'NULL':  # 交点可视化
                    cv2.circle(img, (int(Jx), int(Jy)), 2, (0, 255, 0), 8)
            if not img == 'NULL':  # 车道可视化
                cv2.line(img, point1, point2, (0, 0, 255), 2, 1)
            continue
        else:
            xx = [point1[0], point2[0]] #拟合一次函数
            yy = [point1[1], point2[1]]
            f = np.polyfit(yy, xx, 1)
            fy = np.poly1d(f)
            fy_k = fy[1]
            fy_b = fy[0]

            fy1 = fy_k * y + fy_b - x #求解方程
            fy2 = base_fy_k * y + base_fy_b - x
            JXY = sp.solve([fy1, fy2], [x, y])  # 求交点坐标
            Jx = JXY[x]
            Jy = JXY[y]

            if not img == 'NULL':
                cv2.circle(img, (int(Jx), int(Jy)), 5, (155, 155, 255), 10)  # 展示所有点

            miny, maxy = min(yy), max(yy)
            minx, maxx = min(xx), max(xx)
            if miny - 5 <= Jy <= maxy + 5 and minx - 5 <= Jx <= maxx + 5 and \
                    base_point[1] - 5 <= Jy <= point[1] + 5 and base_point[0] - 5 <= Jx <= point[0] + 5:
                crash += 1
                if not img == 'NULL': #交点可视化
                    cv2.circle(img, (int(Jx), int(Jy)), 2, (0, 255, 0), 8)
            if not img == 'NULL': #车道可视化
                cv2.line(img, point1, point2, (0, 0, 255), 2, 1)

    point1 = areaPoint[0] #最后一个区域边
    point2 = areaPoint[-1]

    if point1[1] == point2[1]:  # 平行于X轴的线段处理
        Jy = (point1[1] + point2[1]) // 2
        Jx = base_fy(Jy)
        xx = [point1[0], point2[0]]
        yy = [point1[1], point2[1]]
        minx, maxx = min(xx), max(xx)

        if not img == 'NULL':
            cv2.circle(img, (int(Jx), int(Jy)), 5, (255, 255, 255), 10)  # 展示所有平行点

        if minx - 5 <= Jx <= maxx + 5 and base_point[1] - 5 <= Jy <= point[1] + 5: #交点在线段内
            crash += 1
            if not img == 'NULL':  # 交点可视化
                cv2.circle(img, (int(Jx), int(Jy)), 2, (0, 255, 0), 4)
        if not img == 'NULL':  # 车道可视化
            cv2.line(img, point1, point2, (0, 0, 255), 2, 1)
    else:
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

        if not img == 'NULL':
            cv2.circle(img, (int(Jx), int(Jy)), 5, (155, 155, 255), 10)  # 展示所有平行点

        miny, maxy = min(yy), max(yy)
        minx, maxx = min(xx), max(xx)
        if miny - 5 <= Jy <= maxy + 5 and minx - 5 <= Jx <= maxx + 5 and \
                base_point[1] - 5 <= Jy <= point[1] + 5 and base_point[0] - 5 <= Jx <= point[0] + 5:
            crash += 1
            if not img == 'NULL':  # 交点可视化
                cv2.circle(img, (int(Jx), int(Jy)), 2, (0, 255, 0), 4)

        if not img == 'NULL': #车道可视化
            cv2.line(img, point1, point2, (0, 0, 255), 2, 1)

    if crash % 2 == 1: #Area判定
        if not img == 'NULL':
            zi = 'YaArea' #可视化
            cv2.putText(img, zi, point, 4, .8, (0, 0, 255), 1)
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
