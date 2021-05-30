#include <opencv2/opencv.hpp>
#include <fstream>
#include <iostream>
#include <string>
#include <stdlib.h>
using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    // 定义亮度矩阵存放的文件路径
    #define lightMatrixFilePath "E:/testimage/cropped/2lightMatrix.txt"
    // 定义亮度标定列表存放的文件路径
    #define realLightListFilePath "E:/testimage/cropped/2realLightList.txt"
    // 定义饱和标记列表存放的文件路径
    #define tabMatrixFilePath "E:/testimage/cropped/2tabMatrix.txt"

    // 将投影亮度矩阵读到内存的列表中
    fstream listfin;
    listfin.open(lightMatrixFilePath,ios::in);
    if(!listfin)
    {
        cout<<"file can't open!";
        // stdlib.h包含了对函数abort()的定义
        abort();
    }
    vector <int> listVector;
    while(!listfin.eof())
    {
        int l;
        listfin>>l;
        listVector.push_back(l);
    }
    listfin.close();


    // 将饱和标记矩阵读到内存的列表中
    fstream tablistfin;
    tablistfin.open(tabMatrixFilePath,ios::in);
    if(!tablistfin)
    {
        cout<<"file can't open!";
        // stdlib.h包含了对函数abort()的定义
        abort();
    }
    vector <int> tablistVector;
    while(!tablistfin.eof())
    {
        int t;
        tablistfin>>t;
        tablistVector.push_back(t);
    }
    tablistfin.close();


    // 将内存中的投影亮度统计后写入到txt文件reallightlist中
    fstream listfout;
    listfout.open(realLightListFilePath,ios::out);
    if(!listfout)
    {
        cout<<"file can't open!";
        // stdlib.h包含了对函数abort()的定义
        abort();
    }

    int realLightList[256]={0};
    int temp;
    for(int i=0;i<(1024*1280);i++)
    {
        if(tablistVector[i]==1)
        {
            temp = listVector[i];
            realLightList[temp]++;
        }
    }
    // 定义一个放置被选定的亮度vector名为finalVector
    vector <int> finalVector;
    int firstlight = 43;
    finalVector.push_back(firstlight);

    // 将reallightlist存到文件中并在遍历进行亮度的选择(方案一)
    for(int light=0;light<256;light++)
    {
        listfout<<light<<' '<<realLightList[light]<<'\n';
        if(light>43&&light<255)
            if(realLightList[light-1]>realLightList[light]&&realLightList[light+1]>realLightList[light])
                finalVector.push_back(light);
    }

    for(int i=0;i<finalVector.size();i++)
    {
        cout<<finalVector[i]<<endl;
    }

    // // 将reallightlist存到文件中并在遍历进行亮度的选择(方案二)
    // int lightNum = 331780;
    // int frontSum = 0;
    // int por = 1;
    // for(int light=0;light<256;light++)
    // {
    //     listfout<<light<<' '<<realLightList[light]<<'\n';
    //     frontSum += realLightList[light];
    //     if(frontSum>lightNum*(por/5))
    //     {
    //         finalVector.push_back(light);
    //         por++;
    //     }
    // }

    // for(int i=0;i<finalVector.size();i++)
    // {
    //     cout<<finalVector[i]<<endl;
    // }

    return 0;
}