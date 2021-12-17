# Canny_Edge_Detector
파이썬을 이용한 Canny_Edge_Detector 구현입니다.

<사전 단계>
Smoothing filters를 적용하여 노이즈를 감소시키는 1단계를 진행하기 전, 이미지를 RGB 채널로 변경하고 grayscale로 변환

<1단계>
영상에 노이즈가 있으면 edges 검출에 어려울 수 있기 때문에, 노이즈를 감소시키기 위해 필터 적용.

![image](https://user-images.githubusercontent.com/63800086/146578551-709b3435-6e59-4b91-aa94-939ec11e091e.png)


<2단계>
2단계에서는 1단계에서 필터를 적용하여 노이즈가 감소된 영상에 sobel 커널을 수평방향, 수직 방향으로 적용.
수평방향의 gradient는 GX로 수직 방향의 gradient는 GY로 구한 다음, 아래 수식으로 gradient와 방향(Angle) 값을 계산한다. 

![image](https://user-images.githubusercontent.com/63800086/146578496-4568306f-b251-45d6-8659-470e15aa3e8a.png)

다음, low_threshold_value보다 낮은 값을 갖는 픽셀들을 탈락 즉, candidate pixels 남게된다.
3단계의 Non-maximum suppression진행을 위해 각도를 4등분.

![image](https://user-images.githubusercontent.com/63800086/146578997-30951cbc-e2d5-4893-9a20-8a8dc135e93b.png)


-2단계에서는 각 픽셀의 Edge_Gradient 와 angle을 구하고 low_threshold_value 값 보다 낮
은 픽셀들을 탈락시켰다. Gradient 크기와 임계값을 비교해서 나온 결과이므로
stage2_Gradient의 edges가 두껍게 검출된 것을 볼 수 있다. stage2_Gradient에서 색은 각
픽셀이 얼마나 높은 Gradient를 가지고 있는지를 나타낸다. (아래 색을 참조 -검정색=엣지 아님, 빨간색 = 강한 엣지)

![image](https://user-images.githubusercontent.com/63800086/146579133-20479728-dbbb-4de3-b567-0506ad5ce648.png)


stage2_Angle또한 육안을 확인하기 위해 컬러맵 표시(아래 색을 참조)

![image](https://user-images.githubusercontent.com/63800086/146579239-fd76275c-893d-43c1-a07a-a69c28e9fda0.png)



<3단계>
2단계 결과를 보면 edges가 두껍게 검출된 것을 볼 수 있다. 3단계에서는 두껍게 검출된
edges을 non-maximum suppression 방식으로 얇게 만든다. non-maximum suppression은 픽셀이
가지는 방향으로 연결된 엣지 픽셀들을 비교하여 Gradient 값이 최대인 픽셀만 남기는 과정을 의미한다. (색은 2단계 색상표와 동일)

![image](https://user-images.githubusercontent.com/63800086/146579463-7f069f40-f5b4-484f-aa54-a70eb931553a.png)

<4단계>
4단계에서는 3단계까지 거치고 남은 엣지중에 진짜 엣지를 선별하는 Hysteresis 
Thresholding을 진행한다. 픽셀의 gradient값이 high_threshold_value보다 높으면 확실한
엣지로 결정한다. Gradient 값이 low_threshold_value~high_threshold_value 사이에 있는 픽
셀은 해당 픽셀이 확실한 엣지와 연결되어 있으면 엣지로 선정하고 그렇지 않다면 엣지에서 탈락한다.

![image](https://user-images.githubusercontent.com/63800086/146579750-33a6674f-01b5-4060-8c60-f7b8df42f45b.png)

해당 결과에서 빨간색은 gradient가 high_threshold_value보다 확실히 높은 엣지이고, 파란
색은 gradient가 high_threshold_value와 low_threshold_value 사이에 있지만 확실한 엣지
들과 연결되어 엣지로 검출된 엣지이다. 노란색은 gradient가 high_threshold_value와
low_threshold_value 사이에 있지만 확실한 엣지와 연결돼있지 않아 최종 엣지에 검출되지
못하는 엣지이다. 최종 엣지 검출은 해당 결과에서 노란색을 제외한 부분이며 다음과 같다.

![image](https://user-images.githubusercontent.com/63800086/146579875-24af15c4-a136-4bba-a732-62100955244f.png)


실제 검출된 엣지를 원본 이미지위에 그린 결과는 다음과 같다.

![image](https://user-images.githubusercontent.com/63800086/146579994-8179acf4-826e-44b1-a8aa-decc45bd9d84.png)

<전체 과정>

![image](https://user-images.githubusercontent.com/63800086/146580295-0b9316b8-e5d9-43ab-a93d-fd3bfb709f0f.png)


