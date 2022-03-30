import cv2
import numpy as np


lines_dic = {} #车道线 ----------还未弄完
### 车辆四点从第一象限到第四象限


def get_car_core(bbox):
    """
        获得车辆的中心
    :return:
    """
    core_x = bbox[0][0]+bbox[1][0]+bbox[2][0]+bbox[3][0] // 4
    core_y = bbox[0][1]+bbox[1][1]+bbox[2][1]+bbox[3][1] // 4
    return core_x, core_y


def run(bbox):
    """
        运行
    :return:
    """
    global lines_dic
    x1, x2, x3, x4 = [x[0] for x in bbox] #坐标以象限表示
    y1, y2, y3, y4 = [y[1] for y in bbox]
    head_x = x1, x2 #车辆头车轮x
    head_y = y1, y2 #车辆头车轮y
    core = get_car_core(bbox) #车辆中心
    line_result = judge_car_in_lines(bbox) #判断车辆在哪条车道线
    line_error_result = judge_car_in_line_error(line_result) #判断车辆在车道线的错误
    check_car_have_error() #对结果进行检查，看是否有违规现象并更新数据，可同时对多个违规进行检查，并且保存数据








    #--------- 此程序主要为了实现压线，连续变道，逆行，考虑加上右侧超车



    #--------  不按车道行驶，红灯放后面做，规则复杂



def mydetect():
    pass


    ### 对于每个已经侦测到的对象


    ### 假设已经得到车辆车轮坐标


    ### 判断车辆位置(在哪个模块上)


    ### 对检测到的位置进行处理


    ###



if __name__ == '__main__':
    pass
