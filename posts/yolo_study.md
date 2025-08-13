---
title : YOLO Study
date : 2025-08-13
category : YOLO, CNN
overview : true
pinned : true
---

## YOLO 공부

### YOLO Input Image

- should be SQUARE (320x320 image)
- ratio 유지가 중요하니 비율을 맞춘 상태로 배경을 넣기
- 모든 color 이미지는 RGB 세개의 color channel이 있음
- configuration of model에서 input size 확인 가능

### CNN Basics

🚩 최고의 자료 그냥 끝까지 읽어보기

[**🔗제발 이걸 봐주세요. .**](https://www.slideshare.net/slideshow/ss-79607172/79607172#3)

- Convolution filter

### Batch normalization

- Internal Covatiate Shift를 막기 위함
    - Internal Covatiate Shift = 트레이닝 중 parameter의 변화에 의한 distirbution 분포의 변화
- normalization method
    - [0,1] 사이의 값이 되도록 scale
        
       <img src="images/yolo/image.png"  width="49%"/>
        
        <img src="images/yolo/Untitled.png"  width="49%"/>
        
    - Whitening
        - data가 zeromean(**μ=0**) and unit variance(**σ=1**)를 갖도록 scale → 이러면 구모양 분포가 됨
            
            <img src="images/yolo/image%201.png"  width="49%"/>
            
            <img src="images/yolo/Untitled%201.png"  width="49%"/>
            

### Maxpooling

<img src="images/yolo/image%202.png"  width="49%"/>

- conv layer에서 이미지 사이즈를 줄여서 선명하고 중요한 feature만 남겨서 강조하는 것
    - 각 칸의 가장 큰 값을 남김!
- 보통 2x2로 화면 전역에 적용
- stride 2 → 좌우로 몇칸 뛸지 결정

<img src="images/yolo/Untitled%202.png"  width="49%"/>

Ex) Max pooling on 4 x 4 Output Activation (Pooling window = 2 x 2

- Max-Pooling after Convolution - Example

<img src="images/yolo/Untitled%203.png"  width="49%"/>

Layer 0→1

<img src="images/yolo/Untitled%204.png"  width="49%"/>

 Layer 4→5

<img src="images/yolo/Untitled%205.png"  width="49%"/>

 Layer 2→3

<img src="images/yolo/Untitled%206.png"  width="49%"/>

### Activation

- ReLU
    
    <img src="images/yolo/Untitled%207.png"  width="49%"/>
    
    - ReLU는 negative에 대해서 모두 0
        
        → 특정 단위가 전혀 활성화되지 않음 → 희소성 문제에서 바람직
        
- Leaky ReLU
    - negative에서 약간의 기울기
    - network의 많은 수의 neuron이 inactive일 때는 "dying ReLU" problem 발생
    - The slope coefficient is determined before training(**NOT learnable**)

### YOLO network

**full images** in **one evaluatio**에서  **bounding boxes** and **class probabilities** **directly** **를 예측하는** 하나의 neural network 

- **Unified Detection**
    
    <img src="images/yolo/Untitled%208.png"  width="49%"/>
    
    Redmon, J. et al., 2016. You Only Look Once: Unified, Real-Time Object Detection. In *2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*. pp. 779–788.
    
    - YOLO는 한번에 모든 Bounding box와 모든 class들을 동시에 예측
        1. input image into an **SxS** grid로 나눔
        2. Each grid cell predicts **B bounding boxes and confidence scores** for those boxes.
            - Each bounding box : 5 predictions: **x, y, w, h, and confidence → Bx5**
            - Each grid cell: **C** conditional **class probabilities** = Pr(Class_i | Object). → **C**
                
                ⇒ **Prediction: SxSx(Bx5+C) tensor**
                
            - Calculate the **class-specific confidence score for each box**
                
                <img src="images/yolo/Untitled%209.png"  width="49%"/>
                

### Tiny-YOLO

봤던 것은 토글 안에 넣어둠, 새로운 개념만 아래에~

- Tiny-YOLO (교수님 자료)
    
    **[**⭐ **Pretrained model for AIX 2024**⭐**]**
    
    The pretrained model provided is defined by two files
    
    1) **tiny-yolo-aix2024.cfg**: Network’s configuration
    
    2) **tiny-yolo-aix2024.weights** (3354 KB): 32-bit floating point parameters
    
    <img src="images/yolo/Untitled%2010.png"  width="49%"/>
    
    <img src="images/yolo/Untitled%2011.png"  width="49%"/>
    
    - Total: **22 layers**
        - **18** **Convolutional** layers
        - **11 convolutional layers**
        - **5** **max-pool** layers with stride =2
        - **1** **max-pool** layer with stride=1
        - **2** **route layer**
        - **1** **upsample layer**
        - **2** **YOLO** layers
    
    - **Inputs**:
        
        **Image** (256x256x3):  an RGB image of 256x256
        
        **filters**
        
    
    - **Outputs**:
        
        **Layer 14(8**x8x195), 
        
        **Layer 20**(16x16x195)
        
    - Number of Operations:
        
        1.035 BFLOPs per inference
        
    
    ### <**tiny-yolo-aix2024.cfg>**
    
     ****The configuration file stores the **model’s structure**. You can find some following important parameters
    
    <img src="images/yolo/Untitled%2012.png"  width="49%"/>
    
    - **width = 256, height = 256, channel = 3**
        
         The input image for the network has a size of 256x256x3. 
        
    - **[convolutional]**
        
        
        <img src="images/yolo/Untitled%2013.png"  width="49%"/>
        
        - Each convolutional (conv) layer is started with the tag. It is defined by the **number of filters, the filter size, stride, padding, and activation.**
        
        - For example, Layer 0 has 16 filters of 3x3x3 for its input 256x256x3.
        - In addition, the stride and the padding are 2 and 1, respectively.
        - Each convolution layer includes **Batch Normalization**
            
            →  more than 2% improvement in mAP.
            
        
        <Convolution Layer overview>
        
        <img src="images/yolo/Untitled%2014.png"  width="49%"/>
        
    
    - **[maxpool]**
    
    <img src="images/yolo/Untitled%2015.png"  width="49%"/>
    
    - size(of the pooling window) = 2, stride=2
        
        ⇒ **reduce width and height by 2x**
        
    
    - Ex) 64x64x64 feature map ⇒ 32x32x64 feature map
    
    <img src="images/yolo/Untitled%2016.png"  width="49%"/>
    
    - Max Pooling layer in code example( @ “C:\skeleton\src\additionally.c”)
        
        ```c
        void forward_maxpool_layer_cpu(const layer l, network_state state)
        {
            if (!state.train) {
                forward_maxpool_layer_avx(state.input, l.output, l.indexes, l.size, l.w, l.h, l.out_w, l.out_h, l.c, l.pad, l.stride, l.batch);
                return;
            }
        
            int b, i, j, k, m, n;
            const int w_offset = -l.pad;
            const int h_offset = -l.pad;
        
            const int h = l.out_h;
            const int w = l.out_w;
            const int c = l.c;
        
            // batch index
            for (b = 0; b < l.batch; ++b) {
                // channel index
                for (k = 0; k < c; ++k) {
                    // y - input
                    for (i = 0; i < h; ++i) {
                        // x - input
                        for (j = 0; j < w; ++j) {
                            int out_index = j + w*(i + h*(k + c*b));
                            float max = -FLT_MAX;
                            int max_i = -1;
                            // pooling x-index
                            for (n = 0; n < l.size; ++n) {
                                // pooling y-index
                                for (m = 0; m < l.size; ++m) {
                                    int cur_h = h_offset + i*l.stride + n;
                                    int cur_w = w_offset + j*l.stride + m;
                                    int index = cur_w + l.w*(cur_h + l.h*(k + b*l.c));
                                    int valid = (cur_h >= 0 && cur_h < l.h &&
                                        cur_w >= 0 && cur_w < l.w);
                                    float val = (valid != 0) ? state.input[index] : -FLT_MAX;
                                    max_i = (val > max) ? index : max_i;    // get max index
                                    max = (val > max) ? val : max;            // get max value
                                }
                            }
                            l.output[out_index] = max;        // store max value
                            l.indexes[out_index] = max_i;    // store max index
        
                            //output size:
                            // l.out_h = (l.h + 2 * l.pad - l.size) / l.stride + 1;
                            // l.out_w = (l.w + 2 * l.pad - l.size) / l.stride + 1;
        
                        }
                    }
                }
            }
        }
        ```
        
    
    - **[route]**
        
        
        <img src="images/yolo/Untitled%2017.png"  width="49%"/>
        
        - In the Tiny YOLO architecture, the "route" layer is used to **concatenate the feature maps.**
        - It takes one or more previous layer outputs and concatenates them along the depth dimension (channel axis).
            - 🧐Why do we concatenate two outputs?(click the toggle)
                1. **Purpose:**
                    - The "route" layer helps to create ****a feature map that contains information from multiple scales in the network
                    - **Concatenated feature map of two layers is then used as input for subsequent layers** in the network.
                    - This is particularly useful for object detection, where **objects of different sizes** may need to be detected.
                2. **Feature Reuse:**
                    - The "route" layer enables feature reuse, allowing the network to use information from earlier layers in the later stages of the network.
        - The **list of concatenated layers** is defined with “Layers= A, B”.
        - If A is **negative**, it indicates the “**relative**” index of the previous layer.
            
            (For example, “layers = **-1, -2**” means to concatenate the outputs from **“one” and “two” layers far from the routing layer**)
            
            <img src="images/yolo/Untitled%2018.png"  width="49%"/>
            
        - If A is **positive**, it indicates the **“absolute”** index of the previous layer.
            
            (For example, “layers = -1, 23” means to concatenate the output of the previous layer and the output of Layer 23. )
            
        - **Note that you must check the order of the concatenated layers**.
            
           <img src="images/yolo/routing.jpg"  width="49%"/>
            
            In routing layer 5, 13, 21, only a subset of the feature map is used when performing the routing
            
    
    - **[upsample]**
    
    <img src="images/yolo/Untitled%2019.png"  width="49%"/>
    
    - Enlarges a convolutional output to **restore the size of the feature map,** which is shrinked during the Max Pooling, **to the original size of the image**
        - ex) 8 x 8 x 64 ⇒ 16 x 16 x 64
        
    
    <img src="images/yolo/Untitled%2020.png"  width="49%"/>
    
    🧐 Still not clear? Go the link below! 
    
    [여러가지 Upsampling 방식들](https://dacon.io/forum/406022)
    
    - **[yolo]**
    
    <img src="images/yolo/Untitled%2021.png"  width="49%"/>
    
    <img src="images/yolo/Untitled%2022.png"  width="49%"/>
    
    - Core of YOLO detection system where the **actual detection and the calculation of the loss are performed**
    - Hyperparameters(click to see the details)
        - **masks** : mask for the anchor boxes to be used
            - ex) masks = 3,4,5 → 4th, 5th, 6th anchor boxes will be used(0-indexed)
        - **anchors**: dimension of the anchor boxes
            - ex) 10,14  ,23,27… → 10x14, 23x27 each
        - **num**: total number of anchor boxes
        - **jitter**: variations to the bboxes(data augmentation parameter)
        - **ignore_thresh**: IoU threshold for for ignoring detection
        - **true_thresh**: IoU threshold for considering a detection as a true positive
        - **random**: random scaling and aspect ratio  adjustment (data augmentation parameter)
    
- **ROUTE**
    - conv 혹은 max를 하기 전의 단계로 돌아가서 input으로 주워올 수 있음
    - layer에서 0보다 큰수를 부르면 그 layer넘버의 output을 다음 input으로 주워옴
    - layer에서 음수를 부른 경우 relative로 주워옴
        - ex) -2면 두단계 전
- **unsample**
    
    <img src="images/yolo/Untitled%2020.png"  width="49%"/>
    
    - conv 출력을 확대해서 MAXpooling하면서 축소된 맵을 원래 크기로 복원

### <**yolov4-tiny-aix2024.weights>**

- `yolov4-tiny-aix2024.weights` 파일은 모델의 가중치(Weights) 데이터를 저장.
- 가중치는 **FP32(32-bit float)** 형식으로 저장됨.
- 각 가중치가 어떤 레이어에 속하는지는 파일 내에서 직접 확인할 수 없음 → **데이터 저장 형식을 이해해야 함**.
- 참고하쇼
    
    <img src="images/yolo/Untitled%2023.png"  width="49%"/>
    
    Weights represented in hex 
    
    - The file stores the model’s parameters. You can open the files with a hex editor, for example, Visual Code or Notepad++ with a hex editor. The file size is **12,391,916 bytes.**
    - Weights are just stored as FP32 format(32-bit floats)
    - There’s nothing to indicate which layer do they belong to. Hence, we must understand **how the weights are stored(data format)** to interpret the parameters.
    
    **<Data format for a layer>**
    
    : Bias → (Scales, Mean, Variance)→ Weights
    
    <img src="images/yolo/Untitled%2024.png"  width="49%"/>
    
   <img src="images/yolo/Untitled%2025.png"  width="49%"/>
    
    9 pixels for R, G, B
    
    ex) If there is a Convolutional layer with 16 filters of 3x3x3, and batch normalization is applied. 
    
    **⇒ The parameters are allocated as follows:**
    
    - 64 bytes(4 bytes x 16 filters) for biases
    - 64 bytes(4 bytes x 16 filters) for scales
    - 64 bytes(4 bytes x 16 filters) for means
    - 64 bytes(4 bytes x 16 filters) for variances
    - **1728 bytes**(4 bytes x 16 filters x 3x3x3) for **weights**
        
        
        **⇒ Data format for the weights**
        
        **1728 Bytes(**above) are aligned as
        
        - 108 bytes(4 bytes x (3x3x3) ) for Filter1
        - 108 bytes(4 bytes x (3x3x3) ) for Filter2
        - 108 bytes(4 bytes x (3x3x3) ) for Filter3
            
            …
            
        - **108 bytes**(4 bytes x (3x3x3) ) for Filter16
        
        ⇒ Each **108 Bytes** are arranged as
        
        - 36 bytes(4 bytes x (3x3)) for Red
        - 36 bytes(4 bytes x (3x3)) for Green
        - **36 bytes**(4 bytes x (3x3)) for Blue
        
        ⇒ Each **36 bytes** are assigned as
        
        - 4 bytes for Pixel1
        - 4 bytes for Pixel2
        - 4 bytes for Pixel3
            
            …
            
        - 4 bytes for Pixel9
    
    <img src="images/yolo/Untitled%2026.png"  width="49%"/>
    
    [https://blog.paperspace.com/how-to-implement-a-yolo-v3-object-detector-from-scratch-in-pytorch-part-3/](https://blog.paperspace.com/how-to-implement-a-yolo-v3-object-detector-from-scratch-in-pytorch-part-3/)
    
    **Header**
    
    The first 5 int32 values are header information(5 x 4Bytes(int32) = **20 Bytes**)
    
    <img src="images/yolo/Untitled%2027.png"  width="49%"/>
    
        1) **Major version number** (4bytes: 0x00 0x00 0x00 0x00)
        2) **Minor Version Number**(4bytes: 0x02 0x00 0x00 0x00)
        3) **Subversion number** (4bytes: 0x05 0x00 0x00 0x00)
        4,5) **Seen mode** (8bytes: 0x00 0xDA 0x61 0x00 0x00 0x00 0x00 0x00)
    
    **Parse**
    
    The file is parsed with the function “**load_weights_upto_cpu**” @ “C:\skeleton\src\additionally.c”
    
    ```c
    void load_weights_upto_cpu(network *net, char *filename, int cutoff)
    {
        fprintf(stderr, "Loading weights from %s...", filename);
        fflush(stdout);
    
        //open the file(which is going to be "yolov4-tiny-aix2024.weights")
        FILE *fp = fopen(filename, "rb");
        if (!fp) file_error(filename);
    
        //PARSING & HEADER
    
        //The first 5 values are header information (5 x 4Bytes(int32) = 20 Bytes)
        int major;  // 1. Major version number 
        int minor;  // 2. Minor Version Number
        int revision;   // 3. Subversion number 
        // 4,5. Images seen by the network (during training)
    
        //read three integers(int32) which represent the version of the weights file and store them in major, minor and revision
        fread(&major, sizeof(int), 1, fp);    //sizeof(int) = 32bits = 4Bytes
        fread(&minor, sizeof(int), 1, fp);
        fread(&revision, sizeof(int), 1, fp);
    
        //check the version and select the appropriate function to load the weights
        if ((major * 10 + minor) >= 2) {    //version>=2
            //net->seen variable: uint64_t 
            //*seen: number of images seen during training
            //reads 1 element of size 64-bit and stores it in net->seen
            fread(net->seen, sizeof(uint64_t), 1, fp);
        }
        else {
            //reads 1 element of size 32-bit and stores it in iseen
            int iseen = 0;
            fread(&iseen, sizeof(int), 1, fp);
    
            //iseen is assigned to net->seen
            *net->seen = iseen;
        }
    
        //LAYER
    
        int i;
    	//fprintf(stderr, "\n Profile the ranges of weights before fusion:\n");
        for (i = 0; i < net->n && i < cutoff; ++i) {
            layer l = net->layers[i];
            if (l.dontload) continue;
            //if the layer is convolutional, load the weights
            if (l.type == CONVOLUTIONAL) {
                load_convolutional_weights_cpu(l, fp);
            }
        }
        fprintf(stderr, "Done!\n");
        fclose(fp);
    }
    ```
    
    **Load Weights**
    
    If layer is convolutional, it loads weights from the file using “**load_convolutional_weights_cpu.**”  (C:\skeleton\src\additionally.c)
    
    ```c
    void load_convolutional_weights_cpu(layer l, FILE *fp)
    {
        int num = l.n*l.c*l.size*l.size;
        fread(l.biases, sizeof(float), l.n, fp);
    
        if (l.batch_normalize && (!l.dontloadscales)) {
            fread(l.scales, sizeof(float), l.n, fp);
            fread(l.rolling_mean, sizeof(float), l.n, fp);
            fread(l.rolling_variance, sizeof(float), l.n, fp);
        }
        fread(l.weights, sizeof(float), num, fp);
    }
    ```
    
    🧐Still not clear? Go to the link below!
    
    Read the section “Understanding the Weights File(in the middle)”
    
    [How to implement a YOLO (v3) object detector from scratch in PyTorch: Part 3](https://blog.paperspace.com/how-to-implement-a-yolo-v3-object-detector-from-scratch-in-pytorch-part-3/)
