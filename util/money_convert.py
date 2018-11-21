#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : money_convert.py
# @Author: wu gang
# @Date  : 2018/10/18
# @Desc  : 人民币数字转汉字大写金额
# @Contact: 752820344@qq.com

import warnings
from decimal import Decimal


def convert(value, capital=True, classical=None, prefix=False):
    """
    人民币数字转汉字大写金额
    :param value: 人民币数字
    :param capital: True 大写汉字金额; False 一般汉字金额
    :param classical: True 圆; False  元
    :param prefix: True 以'人民币'开头; False 无开头
    """
    if not isinstance(value, (Decimal, str, int)):
        msg = ''' 由于浮点数精度问题，请使用考虑使用字符串，或者 decimal.Decimal 类。
                因使用浮点数会造成误差而带来的可能风险和损失。
                '''
        warnings.warn(msg, UserWarning)
    # 默认大写金额用圆，一般汉字金额用元
    if classical is None:
        classical = True if capital else False

    # 汉字金额前缀
    if prefix is True:
        prefix = '人民币: '
    else:
        prefix = ''

    # 汉字金额字符定义
    dUnit = ('角', '分')
    if capital:
        num = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')
        iUnit = [None, '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿', '拾', '佰', '仟', '万', '拾', '佰', '仟']
    else:
        num = ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九')
        iUnit = [None, '十', '百', '千', '万', '十', '百', '千', '亿', '十', '百', '千', '万', '十', '百', '千']

    if classical:
        iUnit[0] = '圆' if classical else '元'

    # 转换为Decimal，并截断多余小数
    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))
    # 处理负数
    if value < 0:
        prefix += '负'  # 输出前缀，加负
        value = - value  # 取正数部分，无须过多考虑正负数舍入

    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError('金额超出最大限制。')
    iStr, dStr = s.split('.')  # 小数部分和整数部分分别处理
    iStr = iStr[::-1]  # 翻转整数部分字符串

    result = []  # 用于记录转换结果
    # 零
    if value == 0:
        return prefix + num[0] + iUnit[0]
    hasZero = False  # 用于标记零的使用
    if dStr == '00':
        hasZero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”
    # 处理小数部分
    # 分
    if dStr[1] != '0':
        result.append(dUnit[1])
        result.append(num[int(dStr[1])])
    else:
        result.append('整')  # 无分，则加“整”
    # 角
    if dStr[0] != '0':
        result.append(dUnit[0])
        result.append(num(int(dStr[0])))
    elif dStr[1] != '0':
        result.append(num[0])  # 无角有分，添加“零”
        hasZero = True  # 标记加过零了

    # 无整数部分
    if iStr == '0':
        if hasZero:
            result.pop()  # 既然无整数部分，那么去掉角位置上的零
        result.append(prefix)  # 加前缀
        result.reverse()  # 翻转
        return ''.join(result)

    # 处理整数部分
    for i, n in enumerate(iStr):
        n = int(n)
        if i % 4 == 0:  # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and result[-1] == iUnit[4]:  # 亿和万之间全部为零的情况
                result.pop()  # 去掉万
            result.append(iUnit[i])
            if n == 0:  # 处理这些位上为零的情况
                if not hasZero:  # 如果以前没有加过零
                    result.insert(-1, num[0])  # 则在单位后面加零
                    haszero = True  # 标记加过零了
            else:
                result.append(num[n])
                haszero = False  # 重新开始标记加零的情况
        else:  # 在其他位置上
            if n != 0:  # 不为零的情况
                result.append(iUnit[i])
                result.append(num[n])
                hasZero = False
            else:  # 处理为零的情况
                if not hasZero:  # 如果以前没有加过零
                    result.append(num[0])
                    hasZero = True

    # 最终结果
    result.append(prefix)
    result.reverse()
    return ''.join(result)


if __name__ == '__main__':
    inValue = input('请输入金额：')
    out1 = convert(inValue)
    print("[%s] 转为大写金额为: [%s]" % (inValue, out1))
    print("或")
    out1 = convert(inValue, capital=False, classical=True, prefix=True)
    print("[%s] 转为大写金额为: [%s]" % (inValue, out1))
