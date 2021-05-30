function [AbsolutePhaseMap,P2] = PhaseUnwarppingEx(RootPath,PhaseShiftingType,CCDImageWidth,CCDImageHeight,file_name)


% 
% PhaseShiftingType = 4;
% CCDImageWidth = 1280;
% CCDImageHeight = 1024;
% % RootPath = 'C:\PowerScanCZA\ScanImages-32\ScanDevice1\4\Camera2\';
% RootPath = 'E:\工作学习\Working\LAB\项目\论文\测冰\实验\相位图\8位\';

P1 = zeros(CCDImageHeight,CCDImageWidth);
P2 = zeros(CCDImageHeight,CCDImageWidth);
P3 = zeros(CCDImageHeight,CCDImageWidth);

I = zeros(3*PhaseShiftingType,CCDImageHeight,CCDImageWidth);

switch PhaseShiftingType
    case 3
%         RootPath = [RootPath '3step\'];
        for i = 1:(3*PhaseShiftingType)
            FileName = [RootPath 'ScanIm_' int2str(i) '.BMP'];
            I(i,:,:) = double( imread(FileName) );
        end
        for i = 1:CCDImageHeight
            for j = 1:CCDImageWidth
                P1(i,j) = atan2( sqrt(3)*(I(1,i,j)-I(3,i,j)),(2*I(2,i,j)-I(1,i,j)-I(3,i,j)) ) + pi;
                P2(i,j) = atan2( sqrt(3)*(I(4,i,j)-I(6,i,j)),(2*I(5,i,j)-I(4,i,j)-I(6,i,j)) ) + pi;
                P3(i,j) = atan2( sqrt(3)*(I(7,i,j)-I(9,i,j)),(2*I(8,i,j)-I(7,i,j)-I(9,i,j)) ) + pi;
            end
        end
    case 4
%         RootPath = [RootPath '4step\'];
        for i = 1:(3*PhaseShiftingType)
            FileName = strcat(RootPath,file_name,int2str(i),'.bmp');
%             FileName = [RootPath,int2str(i),'_8bit.bmp'];
            I(i,:,:) = double(imread(char(FileName)) );
        end
%         P1 = atan2( (I(4,:,:)-I(2,:,:)),(I(1,:,:)-I(3,:,:)) ) + pi;
%         P2 = atan2( (I(8,:,:)-I(6,:,:)),(I(5,:,:)-I(7,:,:)) ) + pi;
%         P3 = atan2( (I(12,:,:)-I(10,:,:)),(I(9,:,:)-I(11,:,:)) ) + pi;
        for i = 1:CCDImageHeight
            for j = 1:CCDImageWidth
                P1(i,j) = atan2( (I(4,i,j)-I(2,i,j)),(I(1,i,j)-I(3,i,j)) ) + pi;
                P2(i,j) = atan2( (I(8,i,j)-I(6,i,j)),(I(5,i,j)-I(7,i,j)) ) + pi;
                P3(i,j) = atan2( (I(12,i,j)-I(10,i,j)),(I(9,i,j)-I(11,i,j)) ) + pi;
            end
        end
    otherwise
%         RootPath = [RootPath int2str(PhaseShiftingType) 'step\'];
        for i = 1:(3*PhaseShiftingType)
            FileName = [RootPath 'ScanIm_' int2str(i) '.BMP'];
            I(i,:,:) = double( imread(FileName) );
        end
        for i = 1:CCDImageHeight
            for j = 1:CCDImageWidth
                ArctanAboveP1 = 0;
                ArctanBelowP1 = 0;
                ArctanAboveP2 = 0;
                ArctanBelowP2 = 0;
                ArctanAboveP3 = 0;
                ArctanBelowP3 = 0;
                for k = 1:PhaseShiftingType
                    InitPhase = 2*pi*(k-1)/PhaseShiftingType;    %与生成光栅图像时保持一致
                    ArctanAboveP1 = ArctanAboveP1+I(k,i,j)*sin(InitPhase);
                    ArctanBelowP1 = ArctanBelowP1+I(k,i,j)*cos(InitPhase);
                    ArctanAboveP2 = ArctanAboveP2+I((k+PhaseShiftingType),i,j)*sin(InitPhase);
                    ArctanBelowP2 = ArctanBelowP2+I((k+PhaseShiftingType),i,j)*cos(InitPhase);
                    ArctanAboveP3 = ArctanAboveP3+I((k+2*PhaseShiftingType),i,j)*sin(InitPhase);
                    ArctanBelowP3 = ArctanBelowP3+I((k+2*PhaseShiftingType),i,j)*cos(InitPhase);
                end
                P1(i,j) = -atan2(ArctanAboveP1,ArctanBelowP1) + pi;
                P2(i,j) = -atan2(ArctanAboveP2,ArctanBelowP2) + pi;
                P3(i,j) = -atan2(ArctanAboveP3,ArctanBelowP3) + pi;
            end
        end
end

DetaAdd = 6;
DetaSub = 5;
Frequency2 = 108;%第二个频率
Frequency1 = Frequency2+DetaAdd;
Frequency3 = Frequency2-DetaSub;
Margin = 1;
P12 = P1 - P2;
P23 = P2 - P3;
%按照相位差，先正弦、余弦化后滤波，然后取反正切。
P12 = phase_filter(P12);
P23 = phase_filter(P23);
P123 = P12 - P23;
P123 = phase_filter(P123);

AbsolutePhaseMap = zeros(CCDImageHeight,CCDImageWidth);
UP12 = zeros(CCDImageHeight,CCDImageWidth);
R1_2 = Frequency2/DetaAdd;

%计算P12的绝对相位值
OrderP12  = floor( ( P123*DetaAdd - P12)/(2*pi)+0.5 );
UP12 = P12+2*pi*OrderP12;

%根据P12的绝对相位值求解P2绝对相位值
OrderP2 = floor( ( UP12*R1_2 - P2 )/(2*pi) );
AbsolutePhaseMap = P2+2*pi*OrderP2;

% R2_1 = Frequency1/DetaAdd;
% OrderP1 = floor( ( UP12*R2_1 - P1 )/(2*pi) );
% AbsolutePhaseMap = P1+2*pi*OrderP1;

% 显示
% figure,imshow(mat2gray(P12));title('1,2外差');   imwrite(mat2gray(P12),'12外差.bmp');
% figure,imshow(mat2gray(P23));title('2,3外差');   imwrite(mat2gray(P23),'23外差.bmp');
% figure,imshow(mat2gray(P123));title('1,2,3外差');imwrite(mat2gray(P123),'E:\毕业论文\A测试工程文件\测试90亮度\123外差.bmp');
% figure,imshow(mat2gray(P1));title('1相位主值');  imwrite(mat2gray(P1),'E:\毕业论文\A测试工程文件\测试90亮度\1相位主值.bmp');  
% figure,imshow(mat2gray(P2));title('2相位主值');  imwrite(mat2gray(P2),'E:\毕业论文\A测试工程文件\测试90亮度\2相位主值.bmp');  
% figure,imshow(mat2gray(P3));title('3相位主值');  imwrite(mat2gray(P3),'E:\毕业论文\A测试工程文件\测试90亮度\3相位主值.bmp');
% figure,imshow(mat2gray(AbsolutePhaseMap));title('AbsolutePhaseMap');  imwrite(mat2gray(AbsolutePhaseMap),'E:\毕业论文\A测试工程文件\测试90亮度\AbsolutePhaseMap.bmp');

% for i = Margin:(CCDImageHeight-Margin)
%     for j = Margin:(CCDImageWidth-Margin)
%         OrderP12 = floor( ( P123(i,j)*DetaAdd - P12(i,j) )/(2*pi)+0.5 );
%         UP12(i,j) = P12(i,j)+2*pi*OrderP12;
%         OrderP2 = floor( ( UP12(i,j)*R1_2 - P2(i,j) )/(2*pi) );
%         AbsolutePhaseMap(i,j) = P2(i,j)+2*pi*OrderP2;
%     end
% end
% AbsolutePhaseMap = medfilt2(AbsolutePhaseMap);
end
