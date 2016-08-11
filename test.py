#coding:GBK
import numpy as np
import csv

import ctypes
import os
import sys

if getattr(sys, 'frozen', False):
    # Override dll search path.
    ctypes.windll.kernel32.SetDllDirectoryW('C:/Anaconda2/Library/bin')
    # Init code to load external dll
    ctypes.CDLL('mkl_avx2.dll')
    ctypes.CDLL('mkl_def.dll')
    ctypes.CDLL('mkl_vml_avx2.dll')
    ctypes.CDLL('mkl_vml_def.dll')

    # Restore dll search path.
    ctypes.windll.kernel32.SetDllDirectoryW(sys._MEIPASS)


def get_feature_name():
    print 'input feature:'
    print 'end with \'done\''
    feature_name_now = []
    feature_num = 0
    tmp = raw_input()
    while tmp!='done':
        feature_name_now.append(tmp)
        feature_num += 1
        tmp = raw_input()
    #print feature_name_now
    return  feature_name_now

def get_feature_name_from_file():
    reader = csv.reader(open("config.txt"))
    feature_name_now = []
    for m in reader:
        for tmp in m:
            feature_name_now.append(str(tmp))
    #print feature_name_now
    return feature_name_now

def construct_matrix(feature_all):
    feature_num = len(feature_all)
    matrix = [ [1 for i in range(0,feature_num)] for j in range(0,feature_num)]
    for i in range(0,feature_num):
        for j in range(0,feature_num):
            if i!=j:
                print feature_all[j]+' 的权重为1时 '+feature_all[i]+' 权重为：'

                while(True):
                    tmp = raw_input()
                    try:
                        matrix[i][j] = float(tmp)
                        break
                    except:
                        print '输入非法，请重新输入'

    print 'construct_matrix has done'
    #print matrix
    return matrix

class kpi_estimater:
    weights = None
    RI = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1.49,1.51,1.54]
    CI = None
    CR = None
    com_matrix = None
    dim = None

    def __init__(self,matrix):
        self.com_matrix = np.array(matrix)
        self.dim = int(self.com_matrix.shape[0])

    def compute_weigths(self):
        prod_sum = []
        n = self.dim
        now_matrix  = self.com_matrix.copy()
        for i in range(0,n):
            tmp = now_matrix[i].prod()
            prod_sum.append(tmp)
        prod_sum = np.power(prod_sum,1.0/self.dim)
        sum = np.sum(prod_sum)
        self.weights = prod_sum/sum

        for_CI = np.dot(self.com_matrix,self.weights)
        for_CI = for_CI/self.weights
        for_CI = for_CI/self.dim
        lam = np.sum(for_CI)
        self.CI = (lam-self.dim)/(self.dim-1)
        now_ri = self.RI[self.dim-1]
        self.CR = self.CI/self.RI[self.dim-1]
        return self.weights


def test01():
    feature_name = get_feature_name_from_file()
    print '属性名称为'
    for item in feature_name:
        print item,

    print ''
    print '------------------'
    print '输入0：开始输入矩阵，\n输入1：使用默认数据'
    choose = raw_input()

    if choose =='0':
        now_matrix = construct_matrix(feature_name)
    else:
        now_matrix = [[1,0.5,0.5,0.333333333,0.333333333,0.25,0.333333333],
                      [2,1,0.5,0.333333333,0.333333333,0.25,0.333333333],
                      [2,2,1,0.5,0.333333333,0.333333333,0.333333333],
                      [3,3,2,1,0.5,0.5,0.333333333],
                      [3,3,3,2,1,0.5,0.5],
                      [4,4,3,2,2,1,0.5],
                      [3,3,3,3,2,2,1]]

    print 'matrix ='
    print now_matrix
    estimater = kpi_estimater(now_matrix)
    weighs = estimater.compute_weigths()

    writer = csv.writer(open('result.csv','wb'))

    writer.writerow(['feature_name'] +feature_name)
    writer.writerow(['weighs']+weighs.tolist())
    writer.writerow(['CI',estimater.CI])
    writer.writerow(['CR', estimater.CR])
    print '----------------------------'
    print 'weighs',weighs
    print 'CR',estimater.CR

    raw_input('press any key to exit...')
test01()