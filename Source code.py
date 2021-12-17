from matplotlib import pyplot as plt 
import numpy as np   
import cv2              
    


# ------------------- satge1 ------------------- #
def Image_Filtering(img):#필터적용
    
    kernel=np.array([[2,4,5,4,2],
            [4,9,12,9,4],
            [5,12,15,12,15],
            [4,9,12,9,4],
            [2,4,5,4,2]],)/159.0
    
    stage1 = cv2.filter2D(img,-1,kernel)
    return stage1


# ------------------- stage2 ------------------- #

def Intensity_and_angle(stage1,low_threshold_value):
    stage2=stage1.copy()
    stage2=stage2.astype('f')
    
    sobelX = np.array([[-1,0,1],  # 소벨 필터 적용
                       [-2,0,2],
                       [-1,0,1]])
                       
    sobelY = np.array([[-1,-2,-1],
                        [0,0,0],
                        [1,2,1]])
    
    GX = cv2.filter2D(stage2, -1, sobelX)
    GY = cv2.filter2D(stage2, -1, sobelY)
    
    Edge_Gradient = np.hypot(GX, GY)
     
    
       #임계값 이하 값들 삭제
    for i in range(0, x):                      
        for j in range(0, y):                   
            if Edge_Gradient[i,j]<=low_threshold_value: 
                Edge_Gradient[i,j]=0
                
                
        # GX=0이면 안되기 때문에 더해줌.
    for i in range(0, x):
        for j in range(0, y):
            if GX[i,j]==0:
               GX[i,j]=GX[i,j]+0.000000000001
               
    angle = np.arctan2(GY,GX) 
    
    for i in range(0, x):      #방향부여
        for j in range(0, y):
            if Edge_Gradient[i,j]!=0:
            # case 0
                if (angle[i,j] > (- np.pi / 8) and angle[i,j] <= (np.pi / 8)):
                    angle[i,j] = 0
                elif (angle[i,j] > (7 * np.pi / 8) and angle[i,j] <= np.pi):
                    angle[i,j] = 0
                elif (angle[i,j] >= -np.pi and angle[i,j] < (-7 * np.pi / 8)):
                    angle[i,j] = 0
                # case 135
                elif (angle[i,j] > (np.pi / 8) and angle[i,j] <= (3 * np.pi / 8)):
                    angle[i,j] = 135
                elif (angle[i,j] >= (-7 * np.pi / 8) and angle[i,j] < (-5 * np.pi / 8)):
                    angle[i,j] = 135
                # case 90
                elif (angle[i,j] > (3 * np.pi / 8) and angle[i,j] <= (5 * np.pi /8)):
                    angle[i,j] = 90
                elif (angle[i,j] >= (-5 * np.pi / 4) and angle[i,j] < (-3 * np.pi / 8)):
                    angle[i,j] = 90
                # case 45
                elif (angle[i,j] > (5 * np.pi/8) and angle[i,j] <= (7 * np.pi /8)):
                    angle[i,j] = 45
                elif (angle[i,j] >= (-3 * np.pi / 8) and angle[i,j] < (-np.pi / 8)):
                    angle[i,j] = 45
            else:
                angle[i, j]=1#엣지 아닌 부분

    return  Edge_Gradient, angle
    

# ------------------- stage3 ------------------- #
def Suppression(stage2_intensity,stage2_angle):#엣지 방향 선상으로 연결되어 있는 모든 엣지 비교
    a=1
    stage3=stage2_intensity.copy()
    stage2_copy=stage2_intensity.copy()
    for i in range(1, x-1):      
        for j in range(1, y-1): 
            if stage2_copy[i,j]!=0:
                
                if stage2_angle[i,j]==0: #좌우 방향일 경우
                    while True:#우측 검사
                        if stage2_copy[i,j+a]==0:a=1; break
                        if stage3[i,j]<=stage2_copy[i,j+a]:
                            stage3[i,j]=0 ;a=1; break
                        a+=1
                        
                    while True:#좌측 검사
                        if stage3[i,j]!=0:
                            if stage2_copy[i,j-a]==0: a=1;break
                            if stage3[i,j]<=stage2_copy[i,j-a]: stage3[i,j]=0;a=1;break
                        else:
                            break
                        a+=1
   
                            
                elif stage2_angle[i, j]==45: # 방향 45일때
                    while True:#우상측 검사
                        if stage2_copy[i-a,j+a]==0: a=1; break
                        if stage3[i,j]<=stage2_copy[i-a,j+a]:
                            stage3[i,j]=0 ;a=1; break
                        a+=1
                        
                    while True:#좌하측 검사
                        if stage3[i,j]!=0:
                            if stage2_copy[i+a,j-a]==0: a=1;break
                            if stage3[i,j]<=stage2_copy[i+a,j-a]: stage3[i,j]=0;a=1;break
                        else:
                            break
                        a+=1

                        
                elif stage2_angle[i, j]==90: # 방향 90일때
                    while True:#상측 검사
                        if stage2_copy[i-a,j]==0: a=1; break
                        if stage3[i,j]<=stage2_copy[i-a,j]:
                            stage3[i,j]=0 ;a=1; break
                        a+=1
                        
                    while True:#하측 검사
                        if stage3[i,j]!=0:
                            if stage2_copy[i+a,j]==0: a=1;break
                            if stage3[i,j]<=stage2_copy[i+a,j]: stage3[i,j]=0;a=1;break
                        else:
                            break
                        a+=1
                            
                            
                elif stage2_angle[i, j]==135: # 135도 일때
                    while True:#좌상측 검사
                        if stage2_copy[i-a,j-a]==0: a=1; break
                        if stage3[i,j]<=stage2_copy[i-a,j-a]:
                            stage3[i,j]=0 ;a=1; break
                        a+=1
                        
                    while True:#우하측 검사
                        if stage3[i,j]!=0:
                            if stage2_copy[i+a,j+a]==0: a=1;break
                            if stage3[i,j]<=stage2_copy[i+a,j+a]: stage3[i,j]=0;a=1;break
                        else:
                            break
                        a+=1
       
    return stage3

# ------ hysteresis Thresholding에 사용되는 링킹 함수  ------- #
def linking(i, j, M_above_high, M_above_low, M_above_mid): 
    for m in range(-1, 2):       # 엣지일 경우 주변 8개 픽셀 탐색
        for n in range(-1, 2):
            if M_above_high[i+m, j+n]==0 and M_above_low[i+m, j+n]!=0: #주변 픽셀이 엣지와 연결되어 있다면
                M_above_high[i+m, j+n]=2 # 2번 엣지로 결정
                M_above_mid[i+m, j+n]=M_above_low[i+m, j+n]#2번 엣지만 있는 배열
                linking(i+m, j+n, M_above_high, M_above_low,M_above_mid) # 재귀적 반복


# ------------------- stage4 ------------------- #
def Hysteresis_Thresholding(stage3,low_threshold_value,high_threshold_value):
    stage4=stage3.copy()
    M_above_high=np.zeros((x,y), dtype='f') #엣지 모음(# 0:엣지아님 1:강한엣지 2:중간엣지 3:약한엣지(탈락될 엣지들))
    M_above_low=np.zeros((x,y), dtype='f')  
    M_above_mid=np.zeros((x,y), dtype='f')  
                       

    for i in range(0, x):                      
        for j in range(0, y):                   
            if stage4[i,j]>=high_threshold_value: # max값보다 클경우
                M_above_high[i,j] = stage4[i,j]# high에 저장
            if stage4[i,j]>=low_threshold_value:# min보다 클경우
                M_above_low[i,j] = stage4[i,j]# low에 저장

    M_above_low = M_above_low - M_above_high # max와 min 사이에 있는 값들 

    for i in range(0, x):       
        for j in range(0, y):    
            if M_above_high[i,j]:#M_above_high이 0이 아니라면    
                M_above_high[i,j]=1 # high에 있는 값들을 강한엣지로 결정
                
              
    for i in range(1, x-1):       
        for j in range(1, y-1):    
            if M_above_high[i,j]==1:#M_above_high값이 엣지라면
                linking(i, j, M_above_high, M_above_low,M_above_mid)#주변 픽셀 찾기 

    
    result=M_above_high.copy()#최종 결과
    
    color_result=result.astype(np.uint8)
    color_result=cv2.cvtColor(color_result,cv2.COLOR_GRAY2BGR)
    color_result=cv2.cvtColor(color_result,cv2.COLOR_BGR2RGB)
    
    for i in range(0,x):#최종 결과 색 표현(빨 파만 남기기)
        for j in range(0,y):
            if (result[i,j] == 0):
                color_result[i,j] = [0, 0, 0] #검
            elif (result[i,j] == 1):
                color_result[i,j] = [255, 0, 0]#빨
            elif (result[i,j] == 2):
                color_result[i,j] = [0, 0, 255]#파
            elif (result[i,j] == 3):
                color_result[i,j] = [255, 255, 0]#노
                
    M_above_mid=M_above_low-M_above_mid#3번 애들만 있는 배열
    
    for i in range(0, x):       
        for j in range(0, y):    
            if M_above_high[i,j]==0 and M_above_mid[i,j]!=0:#탈락된 엣지를 3으로 저장
                M_above_high[i,j]=3
    
    color_high= M_above_high.astype(np.uint8)
    color_high=cv2.cvtColor(color_high,cv2.COLOR_GRAY2BGR)
    color_high=cv2.cvtColor(color_high,cv2.COLOR_BGR2RGB)
    
    for i in range(0,x):#색 으로 엣지 구별
        for j in range(0,y):
            if (M_above_high[i,j] == 0):
                color_high[i,j] = [0, 0, 0] #검
            elif (M_above_high[i,j] == 1):
                color_high[i,j] = [255, 0, 0]#빨 
            elif (M_above_high[i,j] == 2):
                color_high[i,j] = [0, 0, 255]#파 
            elif (M_above_high[i,j] == 3):
                color_high[i,j] = [255, 255, 0]#노
    
    
                
    return color_result,color_high,result#최종결과 , 엣지구분 결과


#-------------컬러 매핑 함수-----------#
def colormap(img,low_threshold_value,high_threshold_value):#컬러맵핑 함수
    
    plus=(high_threshold_value-low_threshold_value)/5
    img_color=img.astype(np.uint8)
    img_color=cv2.cvtColor(img_color,cv2.COLOR_GRAY2BGR)
    img_color=cv2.cvtColor(img_color,cv2.COLOR_BGR2RGB)
    for i in range(0,x):#색 으로 엣지 구별
        for j in range(0,y):
            if img[i,j] <= low_threshold_value:
                img_color[i,j]=[0,0,0]#검
            elif img[i,j] <= low_threshold_value+plus:
                img_color[i,j]=[255,255,0]#노
            elif img[i,j] <= low_threshold_value+(2*plus):
                img_color[i,j]=[153,51,0]#갈
            elif img[i,j] <= low_threshold_value+(3*plus):
                img_color[i,j]=[100,0,255]#보
            elif img[i,j] <= low_threshold_value+(4*plus):
                img_color[i,j]=[0,255,0]#초
            elif img[i,j] <= high_threshold_value:
                img_color[i,j]=[0,0,255]#파
            else:
                img_color[i,j]=[255,0,0]#빨
                
    return img_color

#-------------컬러 매핑 함수2(각도를 색으로 매핑 stage2에 사용)-----------#
def colormap2(img):
    
    img_color=img.astype(np.uint8)
    img_color=cv2.cvtColor(img_color,cv2.COLOR_GRAY2BGR)
    img_color=cv2.cvtColor(img_color,cv2.COLOR_BGR2RGB)
    
    for i in range(0,x):#색 으로 엣지 구별
        for j in range(0,y):
            if img[i,j] ==1:#엣지 아닌 부분
                img_color[i,j]=[0,0,0]#검
            elif img[i,j] ==0:
                img_color[i,j]=[255,255,0]#노
            elif img[i,j] ==45:
                img_color[i,j]=[153,51,0]#갈
            elif img[i,j] ==90:
                img_color[i,j]=[100,0,255]#보
            elif img[i,j] ==135:
                img_color[i,j]=[0,255,0]#초
                
    return img_color


# 동작순서 #
def Canny_Edge_Detector (image,low_threshold_value,high_threshold_value):
    
    #사전 작업
    global x,y
    image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#RGB순으로 변경
    gray_img=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#그레이 이미지로 변환
    x, y = gray_img.shape

    plt.subplot(3,3,1);plt.axis('off');plt.title('original iamge')
    plt.imshow(image.astype(np.uint8))#오리지널 이미지 그리기
    
    plt.subplot(3,3,2);plt.axis('off');plt.title('gray iamge')
    plt.imshow(gray_img.astype(np.uint8),cmap='gray')#그레이 이미지 그리기
    
    
    # 1단계: 노이즈 감소
    stage1=Image_Filtering(gray_img)#필터링
    plt.subplot(3,3,3);plt.axis('off');plt.title('stage1')
    plt.imshow(stage1.astype(np.uint8),cmap='gray')
    
    
    # 2단계: Edge_Gradient 와 angle 찾기
    stage2_intensity,stage2_angle=Intensity_and_angle(stage1,low_threshold_value)
    stage2_color_intensity=colormap(stage2_intensity,low_threshold_value,high_threshold_value)
    stage2_color_angle=colormap2(stage2_angle)
    
    
    plt.subplot(3,3,4);plt.axis('off');plt.title('stage2_Angle')
    plt.imshow(stage2_color_angle.astype(np.uint8))
    
    plt.subplot(3,3,5);plt.axis('off');plt.title('stage2_Gradient')
    plt.imshow(stage2_color_intensity.astype(np.uint8))

    
    
    # 3단계: Non-maximum Suppression
    stage3=Suppression(stage2_intensity,stage2_angle)
    stage3_color=colormap(stage3,low_threshold_value,high_threshold_value)
    
    plt.subplot(3,3,6); plt.axis('off');plt.title('stage3')
    plt.imshow(stage3_color.astype(np.uint8))

    # 4단계: Hysteresis Thresholding
    
    result,stage4,result_copy= Hysteresis_Thresholding(stage3,low_threshold_value,high_threshold_value)
    plt.subplot(3,3,7); plt.axis('off');plt.title('stage4')
    plt.imshow(stage4.astype(np.uint8))
    
    plt.subplot(3,3,8);plt.axis('off');plt.title('result')
    plt.imshow(result.astype(np.uint8))
    
    
    gray_img2=cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
    for i in range(0,x):#그레이 이미지 위에 엣지 표현
        for j in range(0,y):
            if result_copy[i,j]!=0:
                gray_img2[i,j]=result[i,j]
                
    plt.subplot(3,3,9);plt.axis('off');plt.title('result+gray')
    plt.imshow(gray_img2.astype(np.uint8))
    
    plt.show()
     
#main#
image = cv2.imread("./img.jpg")
Canny_Edge_Detector (image,100,250)
