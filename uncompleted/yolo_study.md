---
title: CNN 공부
date: 2025-08-13
category: AI & Deep Learning
project: Study
---
## YOLO 공부

### YOLO Input Image

- should be SQUARE (320x320 image)
- ratio 유지가 중요하니 비율을 맞춘 상태로 배경을 넣기
- 모든 color 이미지는 RGB 세개의 color channel이 있음
- configuration of model에서 input size 확인 가능

### CNN Basics

🚩 최고의 자료 그냥 끝까지 읽어보기

[bookmark:https://www.slideshare.net/slideshow/ss-79607172/79607172#3]

- Convolution filter

### Batch normalization

- Internal Covatiate Shift를 막기 위함
    - Internal Covatiate Shift = 트레이닝 중 parameter의 변화에 의한 distirbution 분포의 변화
- normalization method
    - [0,1] 사이의 값이 되도록 scale
        
       <img src="/images/yolo_study/yolo_study_1.png"  width="49%"/>
        
        <img src="/images/yolo_study/yolo_study_2.png"  width="49%"/>
        
    - Whitening
        - data가 zeromean(**μ=0**) and unit variance(**σ=1**)를 갖도록 scale → 이러면 구모양 분포가 됨
            
            <img src="/images/yolo_study/yolo_study_3.png"  width="49%"/>
            
            <img src="/images/yolo_study/yolo_study_4.png"  width="49%"/>
            

### Maxpooling

<img src="/images/yolo_study/yolo_study_5.png"  width="49%"/>

- conv layer에서 이미지 사이즈를 줄여서 선명하고 중요한 feature만 남겨서 강조하는 것
    - 각 칸의 가장 큰 값을 남김!
- 보통 2x2로 화면 전역에 적용
- stride 2 → 좌우로 몇칸 뛸지 결정

<img src="/images/yolo_study/yolo_study_6.png"  width="49%"/>

Ex) Max pooling on 4 x 4 Output Activation (Pooling window = 2 x 2

- Max-Pooling after Convolution - Example

<img src="/images/yolo_study/yolo_study_7.png"  width="49%"/>

Layer 0→1

<img src="/images/yolo_study/yolo_study_8.png"  width="49%"/>

 Layer 4→5

<img src="/images/yolo_study/yolo_study_9.png"  width="49%"/>

 Layer 2→3

<img src="/images/yolo_study/yolo_study_10.png"  width="49%"/>

### Activation

- ReLU
    
    <img src="/images/yolo_study/yolo_study_11.png"  width="49%"/>
    
    - ReLU는 negative에 대해서 모두 0
        
        → 특정 단위가 전혀 활성화되지 않음 → 희소성 문제에서 바람직
        
- Leaky ReLU
    - negative에서 약간의 기울기
    - network의 많은 수의 neuron이 inactive일 때는 "dying ReLU" problem 발생
    - The slope coefficient is determined before training(**NOT learnable**)

### YOLO network

**full images** in **one evaluatio**에서  **bounding boxes** and **class probabilities** **directly** **를 예측하는** 하나의 neural network 

- **Unified Detection**
    
    <img src="/images/yolo_study/yolo_study_12.png"  width="49%"/>
    
    Redmon, J. et al., 2016. You Only Look Once: Unified, Real-Time Object Detection. In *2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*. pp. 779–788.
    
    - YOLO는 한번에 모든 Bounding box와 모든 class들을 동시에 예측
        1. input image into an **SxS** grid로 나눔
        2. Each grid cell predicts **B bounding boxes and confidence scores** for those boxes.
            - Each bounding box : 5 predictions: **x, y, w, h, and confidence → Bx5**
            - Each grid cell: **C** conditional **class probabilities** = Pr(Class_i | Object). → **C**
                
                ⇒ **Prediction: SxSx(Bx5+C) tensor**
                
            - Calculate the **class-specific confidence score for each box**
                
                <img src="/images/yolo_study/yolo_study_13.png"  width="49%"/>
                
