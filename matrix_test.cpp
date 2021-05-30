#include <opencv2/opencv.hpp>
#include <fstream>
#include <iostream>
#include <string>
#include <stdlib.h>
using namespace std;
using namespace cv;
int main(int argc, char* argv[])
{
    // 将图片文件放入数组中
    char filelist[][100] = {"E:/testimage/cropped/44ScanIm_13.bmp",
    "E:/testimage/cropped/47ScanIm_13.bmp",
    "E:/testimage/cropped/52ScanIm_13.bmp",
    "E:/testimage/cropped/60ScanIm_13.bmp",
    "E:/testimage/cropped/80ScanIm_13.bmp",
    "E:/testimage/cropped/110ScanIm_13.bmp"};

    // 定义亮度矩阵存放的文件路径
    #define lightMatrixFilePath "E:/testimage/cropped/2lightMatrix.txt"
    // 定义亮度标定列表存放的文件路径
    #define realLightListFilePath "E:/testimage/cropped/2realLightList.txt"
    // 定义标记矩阵存放的文件路径
    #define tabMatrixFilePath "E:/testimage/cropped/2tabMatrix.txt"

    // 列向量L包含了均匀灰度图像的强度, 这里s等于6, 所以共有6个亮度
    float L1 = 44,L2 = 47,L3 = 52,L4 = 60,L5 = 80,L6 = 110;
    const int s = 6;
    Vec<float, s> L(L1, L2, L3, L4, L5, L6);

    // 矩阵X包含了投影亮度和曝光时间相关参数
    float kt = 1.5;
    Mat X = Mat(s,2,CV_32FC(1));
    for(int i=0;i<s;i++)
    {
        X.at<float>(i, 0) = L[i];
        X.at<float>(i, 1) = kt;
    }

    // X_T为矩阵X的转置矩阵
    Mat X_T = Mat(2,s,CV_32FC(1));
    for(int i=0;i<s;i++)
    {
        X_T.at<float>(0, i) = L[i];
        X_T.at<float>(1, i) = kt;
    }

    // 计算X_T*X的逆矩阵
    Mat X_TXinv = (X_T*X).inv();

    // 包含a1, a2的未初始化列向量A
    Vec<float, 2> A;

    //读取用于标记饱和区域的均匀灰度图像,获取行列数据，为创建Mask、A_M做准备
    Mat img1 = imread("E:/testimage/cropped/120ScanIm_13.bmp", IMREAD_GRAYSCALE);
    //创建一个全为0的float类型Mask
    Mat Mask = Mat::zeros(img1.rows, img1.cols, CV_32FC(1));
    //给Mask赋一些值
    //将饱和标记矩阵存放到txt文件中
    fstream tabmatFout;
    tabmatFout.open(tabMatrixFilePath,ios::out);
    if(!tabmatFout)
    {
        cout<<"file can't open!";
        // stdlib.h包含了对函数abort()的定义
        abort();
    }

    int lightcount = 0;
    for(int i=0;i<img1.rows;i++)
    {
        float * ptr_mask = Mask.ptr<float>(i);
        uchar * ptr_img1 = img1.ptr<uchar>(i);
        for(int j=0;j<img1.cols;j++)
        {
            if(float(ptr_img1[j])>248.0)
            {
                ptr_mask[j] = 1.0;
                lightcount++;
                // cout<<"("<<i<<","<<j<<")"<<"has been set 1!"<<endl;
            }
            tabmatFout<<ptr_mask[j]<<" ";
        }
        tabmatFout<<"\n";
    }
    tabmatFout.close();
    cout<<"There are "<<lightcount<<" positions that have been tabbed."<<endl;


    // 创建一个与Mask类型相同的用于存放投影亮度的二维矩阵lightMatrix
    Mat lightMatrix = Mat::zeros(img1.rows, img1.cols, CV_32SC(1));
    // 用于存储投影亮度的一维向量，数据量太大得动态申请
    const int lightNum = lightcount;
    int * lightList = new int [lightNum];
    // lightList的下标
    int p=0;
    // 存储四幅图像的Mat列表，名为img
    Mat img[s];
    // 用于亮度浮点数与整数之间的转换
    float templight;
    // 计算每个像素点对应的列向量A,将列向量A放入图像矩阵,得到有值的A_M
    for(int i=0;i<img1.rows;i++)
    {
        //Mask的索引指针
        float * ptr_mask = Mask.ptr<float>(i);
        //lightMatrix的索引指针
        int * ptr_lightMatrix = lightMatrix.ptr<int>(i);

        for(int j=0;j<img1.cols;j++)
        {
            if(ptr_mask[j])
            {
                // 计算每个像素点对应的列向量I
                Vec<float,s> I;
                for(int k=0;k<s;k++)
                {
                    img[k] = imread(filelist[k], IMREAD_GRAYSCALE);
                    uchar* ptr_img = img[k].ptr<uchar>(i);
                    I[k] = float(ptr_img[j]);
                }
                //算出A的两个参数
                Mat dst1;
                gemm(X_TXinv,X_T,1,1,0,dst1,0);
                gemm(dst1,I,1,1,0,A,0);
                templight = (240-kt*A[1])/(kt*A[0]);
                // 用于矫正亮度
                if(templight>=60)
                    templight += 4*(templight-60);
                else
                    templight -= 1*(60-templight);
                lightList[p] = (int)round(templight);
                // 填充到投影亮度矩阵中去
                if(lightList[p]>255||lightList[p]<0)
                    ptr_lightMatrix[j] = 43;
                if(lightList[p]>=0&&lightList[p]<=255)
                    ptr_lightMatrix[j] = lightList[p];
                p++;

            }
        }
        cout<<"Complete the calculating in row "<<i<<endl;
    }

    // 将亮度矩阵存放到txt文件中
    fstream matFout;
    matFout.open(lightMatrixFilePath,ios::out);
    if(!matFout)
    {
        cout<<"file can't open!";
        // stdlib.h包含了对函数abort()的定义
        abort();
    }
    for(int i=0;i<img1.rows;i++)
    {
        //lightMatrix的索引指针
        int * ptr_lightMatrix = lightMatrix.ptr<int>(i);
        for(int j=0;j<img1.cols;j++)
        {
            matFout<<ptr_lightMatrix[j]<<" ";
        }
        matFout<<"\n";
    }
    matFout.close();

    delete []lightList;

    return 0;
}

