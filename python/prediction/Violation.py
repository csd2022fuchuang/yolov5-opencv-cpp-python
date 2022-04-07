import cv2
import numpy as np

from car import Car
from liness import Line
from liness import Area





# def from_new_to_car_dic_and_obj(id):
#     """
#         从new_car_dic中转移到car_dic中
#     """
#     global new_car_dic, cars_dic
#     cars_dic[id] = new_car_dic[id] #转移数据
#     del new_car_dic[id] #从new_car_dic删除该数据
#
#
# def judge_car_in_lines(bbox, core):
#     """
#         判断车辆在哪条车道线
#     """
#     global lines_dic
#     x1, x2, x3, x4 = [x[0] for x in bbox]
#     y1, y2, y3, y4 = [y[1] for y in bbox]
#     x_core, y_core = core

    #all_line_fit = all_line #所有车道函数-------------------
    #判断core
    #for line in all_line_fit: #line是numpy中的poly1d
     #   if line(y_core) < x_core < line(y_core): #在这条车道上
      #      runrunrun #比较之前的车道位置，若是新的则添加，如果前后车道位置不一则直接判定车辆车道移动
       #     break



    #在判断四点
    #for line in all_line_fit:

     #   if core_shifting: #如果车道偏移直接判定啦，不用再判定4点
      #      break


    ##判断在车道


# def process_violations():
#     """
#         处理违规
#     """
#     global cars_dic
#     for car in cars_dic:
#         if car['violation'][0] == 0: #没有违规则跳过
#             break
#         _, *car_error = car['violations']
#         for error in car_error: #遍历所有违规
#             if error == 'abc': #违规类型：
#                 pass #违规处理
#         car['violation'][0] = 0 #违规处理完毕，初始化
#
#
# def run(bbox):
#     """
#         运行
#     :return:
#     """
#     global lines_dic
#     x1, x2, x3, x4 = [x[0] for x in bbox]
#     y1, y2, y3, y4 = [y[1] for y in bbox]

    #判定车辆车头坐标

    #core = get_car_core(bbox) #车辆中心
    #line_result = judge_car_in_lines(bbox, core) #判断车辆在哪条车道线
    #line_error_result = judge_car_in_line_error(line_result) #判断车辆在车道线的错误  比较之前的车道位置，若是新的则添加，如果前后车道位置不一则直接判定车辆车道移动
    #check_car_have_error() #对结果进行检查，看是否有违规现象并更新数据，可同时对多个违规进行检查，并且保存数据




    #--------- 此程序主要为了实现压线，连续变道，逆行，考虑加上右侧超车



    #--------  不按车道行驶，红灯放后面做，规则复杂








#bbox = car_dic[car_id]['bbox']
#x1, x2, x3, x4 = [x[0] for x in bbox]
#y1, y2, y3, y4 = [y[1] for y in bbox]
#core_x = bbox[0][0] + bbox[1][0] + bbox[2][0] + bbox[3][0] // 4
#core_y = bbox[0][1] + bbox[1][1] + bbox[2][1] + bbox[3][1] // 4



line_point = [(400, 450), (700, 450)] #先标几个点
line_point2 = [(450, 550), (600, 550)]
lines_lis = [line_point] #直线
lines_dic = {} #线



def creat_lines(img):
    """
        实例化line
    """
    global lines_lis, lines_dic
    for num, line in enumerate(lines_lis): #遍历所有line
        line_name = 'line' + f'{num}'
        lines_dic[line_name] = Line(line_name, line[0], line[1]) #实例化线

        cv2.line(img, line[0], line[1], (0, 0, 255), 4, 4) #可视化


new_car_dic = {}  # 新检测到的车辆对象
cars_dic = {}  # 已检测到的车辆


def is_new_car(car_ids, bboxs, plates):
    """
        判断是否为新检测到的车辆，同时建立车辆对象
    """
    global new_car_dic, cars_dic

    for obj in range(len(car_ids)): #遍历所有车辆id
        car_id = car_ids[obj]

        #print(f'\nbboxs[obj]:{bboxs[obj]}, bbox[0]: {bboxs[obj][0]}')

        if car_id in cars_dic: #如果车辆在车辆储存区
            cars_dic[car_id]['bbox'] = bboxs[obj] #更新坐标
        elif car_id in new_car_dic: #如果在车辆临时储存区
            new_car_dic[car_id]['count'] += 1

            #print(f'-----------------------id:{car_id}, count: {new_car_dic[car_id]["count"]}')

            if new_car_dic[car_id]['count'] >= 2: #连续检测值大于3才会视为车辆目标，减少误检测
                cars_dic[car_id] = Car() #实例化car
                cars_dic[car_id]['bbox'] = bboxs[obj] #添加bbox

            #print(f'------------------------creat Car: {car_id}')

        else:
            new_car_dic[car_id] = {'count': 0} #新车辆放到临时存储区

            #print(f'--------------------id:{car_id}, count: {new_car_dic[car_id]["count"]}')

    for car_id in list(cars_dic.keys()): #遍历所有id，更新cars_dic（没检测到对象--，小于-10删除）,和new_car_dic（没检测到对象-- 小于-3删除）
        if car_id not in car_ids:
            cars_dic[car_id]['count'] -= 1
            if cars_dic[car_id]['count'] <= -10:
                del cars_dic[car_id]

    for car_id in list(new_car_dic.keys()):
        if car_id not in car_ids:
            new_car_dic[car_id]['count'] -= 1
            if new_car_dic[car_id]['count'] <= -3:
                del new_car_dic[car_id]


area_point = [(500, 520), (400, 650), (600, 650), (650, 520)] #先标几个点 逆或顺时针，排序算法还在做
#area_point2 = [(700, 600), (1200, 600), (1200, 500), (700, 500)] #先标几个点 逆或顺时针，排序算法还在做
area_point3 = [(560, 300), (560, 400), (660, 400), (660, 300)] #先标几个点 逆或顺时针，排序算法还在做
area_lis = [area_point, area_point3] #区域直线集
area_dic = {} #所有区域字典


def creat_area(img):
    """
        实例化area
    """
    global area_lis, area_dic
    #排序(逆时针)

    #循环建line
    for area_count, area in enumerate(area_lis): #遍历所有area
        area_lines_lis = []
        area_name = 'area' + f'{area_count}'
        area_lines_lis.append(Line('line0', area[0], area[-1])) #建立line

        cv2.line(img, area[0], area[-1], (0, 0, 255), 4, 4)  # 可视化

        for count, point in enumerate(area): #遍历所有area里的point
            if count == len(area)-1:
                break
            line_name = 'line' + f'{count+1}'
            area_lines_lis.append(Line(line_name, area[count], area[count+1]))  # 实例化线

            cv2.line(img, area[count], area[count+1], (0, 0, 255), 4, 4)  # 可视化

        area_dic[area_name] = Area(area_name, area_lines_lis) #实例化Area


# def crash_area_test(car_id, img):
#     """
#         简单地测试一下简单的功能
#     """
#     global cars_dic, area_dic
#     core = cars_dic[car_id].get_core()
#     for area in area_dic.get():  # 遍历所有area
#         area_name = area.get_name()  # 获得当前area名字
#         if area.get_minmaxy()[0] < core[1] < area.get_minmaxy()[1] and \
#                 area.get_minmaxx()[0] < core[0] < area.get_minmaxx()[1]:  # 在检测范围内
#             if area.pointx_in(core[0]) and area.pointy_in(core[1]):  # core在area内部
#                 if area_name in cars_dic[car_id]['violation']:  # 已有记录
#                     cars_dic[car_id]['violation'][area_name][0] = 1  # 添加违规标记
#                 else:
#                     cars_dic[car_id]['violation'][area_name] = [1]  # 添加违规标记，添加记录
#                 continue


def crash_area(car_id, img):
    """
        区域禁行
    """
    global cars_dic, area_dic
    core = cars_dic[car_id].get_core()
    core = (int(core[0]), int(core[1]))
    for area in list(area_dic.keys()): #遍历所有area
        area_name = area_dic[area].get_name() #获得当前area名字
        xmin, xmax, ymin, ymax = area_dic[area_name].get_minmaxxy_area(accurate=True) #获得检测范围

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 255, 255), 2) #检测范围可视化

        if ymin < core[1] < ymax and xmin < core[0] < xmax: #在检测范围内

            #print(f'ID: {car_id}条件符合，碰撞检测！')

            if area_dic[area_name].core_in_area(core, img): #core在area内部

                #print(f'ID: {car_id} 碰撞Area')

                if area_name in cars_dic[car_id]['violations']: #已有记录
                    cars_dic[car_id]['violations'][area_name][0] = 1 #添加违规标记
                else:
                    cars_dic[car_id]['violations'][area_name] = [1, area_name] #添加违规标记，添加记录
                zi = f'YaArea, ID={car_id}'
                cv2.putText(img, zi, (int(cars_dic[car_id]['bbox'][0][0]), int(cars_dic[car_id]['bbox'][0][1])),
                            4, .8, (0, 0, 255), 1)  # 可视化



def crash_line(car_id, img):
    """
        压线检测
    """
    global cars_dic, lines_dic

    #print(f'ID: {car_id}执行压线检测')

    core = cars_dic[car_id].get_core()
    for line_name in list(lines_dic.keys()): #遍历所有线段
        if lines_dic[line_name].get_minmaxy()[0] < core[1] < lines_dic[line_name].get_minmaxy()[1] and \
             lines_dic[line_name].get_minmaxx()[0] < core[0] < lines_dic[line_name].get_minmaxx()[1]: #在检测范围内

            #print(f'ID: {car_id}条件符合，压线检测！')

            if core[0] > lines_dic[line_name].fy_to_x(core[1]): #开始检测
                position = 'R'
            else:
                position = 'L'

            if line_name in cars_dic[car_id]['violations']: #已有记录
                if position != cars_dic[car_id]['violations'][line_name][1]: #与上次位置不同
                    cars_dic[car_id]['violations'][line_name][0] = 1 #添加违规标记
                    zi = f'YaXian, ID={car_id}'
                    cv2.putText(img, zi, (int(cars_dic[car_id]['bbox'][0][0]+30), int(cars_dic[car_id]['bbox'][0][1])),
                                4, .8, (0, 0, 255), 1) #可视化
            else:
                cars_dic[car_id]['violations'][line_name] = [0, position] #保存位置


#violations = [crash_line] #这是所有违规检测项目
#violations = [crash_area]
violations = [crash_line, crash_area]

def detect_violation(car_ids, img):
    """
        违规检测
    """
    global cars_dic, violations

    for violation in violations: #遍历所有违规
        for car_id in car_ids: #遍历所有当前检测车辆
            if car_id in cars_dic: #当前车辆id已经在cars_dic实例化
                car_info = cars_dic[car_id] #当前车辆信息
                violation(car_id, img) #执行检测


# def pre_creat(img):
#     creat_lines(img) #实例化线
#     creat_area(img) #实例化区域


def detect_violation_run(car_ids, bboxs, img):
    """
        违规检测运行
    """
    creat_lines(img) #实例化线

    creat_area(img) #实例化区域

    #车牌


    ###记录每个新侦测到的id到new_car_dic,如果后几次连续检测出，创建Car类，参与违规判定。多次检测不到的车辆进行数据清理
    is_new_car(car_ids, bboxs, plates='NULL')


    #方向检测


    ### 违规预测
    detect_violation(car_ids, img) #传入当前检测到的所有车辆


    ###输出违规


    ###

    if len(cars_dic):
        for car_key in cars_dic.keys():
            zi = f'creatID:{car_key}'
            cv2.putText(img, zi, (int(cars_dic[car_key]['bbox'][0][0]), int(cars_dic[car_key]['bbox'][0][1])-15),
                        4, .5, (0, 0, 255), 1)  # 可视化

    # if len(cars_dic) != 0:
    #     for iid in list(cars_dic.keys()):
    #         print(f'\n{cars_dic[iid]["violations"]}')


if __name__ == '__main__':
    pass
