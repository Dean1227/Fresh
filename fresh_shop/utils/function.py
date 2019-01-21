import random
import time


def get_order_sn():
    # 生成订单号
    s = '123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKZXCVBNM'
    order_sn = ''
    for i in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())
    return order_sn


def create_history(list1):
    """
    生成历史记录并去重、限定条数
    :param list1:
    :return:
    """
    temp = []
    for item in list1:
        if not item in temp:
            temp.append(item)
            if len(temp) == 5:
                return temp
