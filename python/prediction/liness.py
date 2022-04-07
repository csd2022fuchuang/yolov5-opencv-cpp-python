import cv2
import numpy as np
import sympy as sp

#生成车道字典-------------------------------------------------
# for number in range(1, chedao_num + 1):
#     #生成车道名字
#     first_name = 'cd'
#     name = first_name + f'{number}'
#     #生成车道空字典
#     lines_dic[name] = {}
#     #组装左右车道线
#     lines_dic[name]['L'] = 1
#     lines_dic[name]['R'] = 2
#     #组装车道方向 far or close or no
#     lines_dic[name]['direction'] = 'far'
#     #组装车道位置模块 true 可通行， false 不可通行
#     lines_dic[name]['mod'] = {'L': True, 'R': False}

#线的拟合方式：暂时用两点确定一条直线
#得到X=KY+B


class Line:
    """
        线段实例化
    """
    def __init__(self, n, point1, point2):
        self.name = n
        self.fy, self.fy_k, self.fy_b = self.get_fit(point1, point2)
        self.point = [point1, point2]

    def get_name(self):
        """
            得到线的名字
        """
        return self.name

    def get_minmaxx(self, accurate=False):
        """
            返回最小,最大的x
        """
        # minx = min(self.point, key=lambda x: x[0])
        # maxx = max(self.point, key=lambda x: x[0])
        x = self.point[0][0], self.point[1][0]
        minx = min(x)
        maxx = max(x)
        if not accurate:
            if maxx - minx < 200: #保证最小有200像素点
                _ = (200 - maxx + minx) // 2
                minx -= _
                maxx += _
        return minx, maxx

    def get_minmaxy(self, accurate=False):
        """
            返回最小，最大的y
        """
        # miny = min(self.point, key=lambda y: y[1])
        # maxy = max(self.point, key=lambda y: y[1])
        y = self.point[0][1], self.point[1][1]
        miny = min(y)
        maxy = max(y)
        if not accurate:
            if maxy - miny < 200: #保证最小有200像素点
                _ = (200 - maxy + miny) // 2
                miny -= _
                maxy += _
        return miny, maxy

    def fy_to_x(self, y):
        return self.fy(y)

    @classmethod
    def get_fit(cls, point1, point2):
        """
            得到一次直线拟合
        """
        x = (point1[0], point2[0])
        y = (point1[1], point2[1])
        f = np.polyfit(y, x, 1)
        fy = np.poly1d(f)
        fy_k = fy[1]
        fy_b = fy[0]
        return fy, fy_k, fy_b

    def get_point(self):
        return self.point

    def get_fy_k_b(self):
        return self.fy, self.fy_k, self.fy_b


class Area:
    """
        area实例化
        先生成lines，再由lines生成area
    """
    def __init__(self, n, lines):
        self.name = n #Area的id
        self.lines = lines #多个线对象组成的list

    def get_name(self):
        return self.name

    # def get_point(self, name):
    #     return self.lines[name].get_point

    def get_minmaxxy_area(self, accurate=False):
        """
            返回一个最小区域
        """
        lines = self.lines
        x = []
        y = []
        for line in lines:
            x.append(line.get_minmaxx(accurate=True)[0])
            x.append(line.get_minmaxx(accurate=True)[1])
            y.append(line.get_minmaxy(accurate=True)[0])
            y.append(line.get_minmaxy(accurate=True)[1])
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        if not accurate:
            if x_max - x_min < 100: #保证最小区域有100*100
                _ = (100 - x_max + x_min) / 2
                x_max += _
                x_min -= _
            if y_max - y_min < 100:
                _ = (100 - y_max + y_min) / 2
                y_max += _
                y_min -= _
        return x_min, x_max, y_min, y_max

    def core_in_area(self, core, img):
        """
            判断点在area内
        """
        lines = self.lines
        base_point = (10, 10)  # 原点
        base_line = Line('base', core, base_point)  # 向原点发出一条射线

        cv2.line(img, core, base_point, (155, 155, 255), 2, 4) #DEBUG

        base_k, base_b = base_line.get_fy_k_b()[1:]  # 斜率K,b
        y = sp.symbols('y') #未知数Y
        x = sp.symbols('x') #未知数X
        crash = 0
        for line in lines: #遍历所有line
            fy, fy_k, fy_b = line.get_fy_k_b()

            fy1 = fy_k * y + fy_b - x
            fy2 = base_k * y + base_b - x
            temp = sp.solve([fy1, fy2], [x, y]) #求交点坐标
            Jx = temp[x]
            Jy = temp[y]

            miny, maxy = line.get_minmaxy(accurate=True)
            minx, maxx = line.get_minmaxx(accurate=True)
            if miny-5 <= Jy <= maxy+5 and minx-5 <= Jx <= maxx+5 and \
                    base_point[1]-5 <= Jy <= core[1]+5 and base_point[0]-5 <= Jx <= core[0]+5:
                crash += 1

                #print(f'miny: {miny}, Y: {y}, maxy: {maxy}') #DEBUG

                cv2.circle(img, (int(Jx), int(Jy)), 8, (255, 0, 155), 8)  # DEBUG

            #cv2.circle(img, (int(line.fy_to_x(Y)), int(Y)), 4, (255, 0, 155), 4) #DEBUG

        #print('crash: ', crash) #DEBUG

        if crash % 2 == 1:
            return True
        else:
            return False













        #如果相交，并且交点在两个线段内，则判定穿过该线段













# class Lane:
#     def __init__(self, go, n, fitl, fitr):
#         self.go = go
#         self.Name = n
#         self.FitL = fitl
#         self.FitR = fitr
#
#     def is_position(self):
#         l_function = self.FitL
#         r_function = self.FitR
#
#
#
# class StopArea:
#     pass
#
#
# class StopLine:
#     pass
#
# #------------------------------------------#
#
#
# def creat_line(name, l, r):
#     pass
#    # return Lines(name, l, r)
#
#
# def trans_lane(go, n, fitl, fitr):
#     pass
#     #return Lanes(go, n, fitl, fitr)


if __name__ == '__main__':
    pass
