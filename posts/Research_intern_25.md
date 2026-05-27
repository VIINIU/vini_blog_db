---

title : Research | FPGA Based WWS System
date : 2026-01-20
category : AI & Deep Learning
project: Research
pinned : False
thumbnail: Research_intern_25/Research_intern_25_1.png
---

<img src="/images/Research_intern_25/Research_intern_25_1.png" width="100%"/>

### 프로젝트 개요

- 2025학년도 2학기 진행된 차세대 반도체 혁신융합대학 프로그램 중 서울대학교 학점 교류 학부생 연구인턴으로 진행한 프로젝트
- 2026년 1월 [차세대 반도체 페스티벌 SIF 2026](https://polargate.disu.ac.kr/contest/SIF2026/final?sc=y)에 출품하여 작품부문 3등상(장려상)을 수상 (장학금 180만원)
- SNN 기반의 Wake-Word Spotting System을 FPGA상에서 구현하여 PC에서 Wake-word가 호출되면 Board에서 Wake-word를 구별하는 시스템 

### 프로젝트 시작 배경

학부생 연구인턴 프로그램이 시작되면서, SNN과 FPGA의 사용에 대한 전반적인 부분을 공식 문서와 관련 논문을 통해 학습하였고, 이후 각자 한 학기동안 연구할 연구 주제를 잡아 프로젝트를 진행하는 형식으로 진행되었습니다. SNN의 저전력, Event-Driven한 특성을 고려했을 때, 이 두 특성을 모두 활용하기 위해서는 전력 사용이 제한되는 엣지 디바이스 환경에서 항상 켜져있는 기능인 음성 에이전트 호출 키워드를 걸러내는 역할을 SNN을 사용하여 하드웨어상에서 구현한다면, 전력 사용을 최소화하면서도 빠르게 키워드를 걸러낼 수 있을 것이라고 판단하였다.
이런 과정을 통해 SNN을 베이스로하는 Wake-Word Spotting 시스템 구현을 시작하게 되었다.

### 데이터 전처리 및 SNN 모델링

타겟 키워드는 캐글에 오픈된 Amazon의 "Alexa"로 설정하였다. 오픈된 데이터셋을 가지고 배경 소음을 합성하고, 음성 높낮이 및 길이 변경을 통해서 학습데이터를 확보하였다. 음성데이터는 FPGA의 연산 자원을 고려하여 8KHz, 16bit의 해상도로 변환하였다. 

음성 신호는 32ms씩 Windowing하고, FFT하여 음성을 걸러내는데 주로 사용되는 Mel-filter를 통과하도록 설계되었다. 추출된 Magnitude 값은 Rate Coding을 통해서  Spike Train으로 변환되어 SNN의 입력으로 사용했고, 모델은 snnTorch를 활용하여 LIF 뉴런 기반의 Fully Connected 레이어 구조로 설계했다. ANN 학습 후 가중치를 변환하는 방식과 SNN 직접학습 두가지의 학습 방법이 있는데, SNN 직접학습을 위해서 역전파 과정에서 Surrogate Gradient 학습법을 적용하였다.

나는 이 모든 과정을 노트북 한 대를 가지고 수행했는데, 매번 학습 중인 노트북을 덮으면, 발열이 너무 심해 노트북을 열고 이곳 저곳 돌아다니며 학습을 시켰던 기억이 있다. 이 이후 노트북의 성능이 크게 떨어져서 이 프로젝트를 통해 탄 상금으로 새 맥북 에어를 구매하였다..👍

### Quantization

PC 환경에서 학습된 Float32 가중치를 FPGA에 포팅하기 위해 INT8로 변환하는 과정이 필요했는데, 여타 NPU들은 Quantization + Quantization 전·후 모델의 성능 비교 및 평가를 위한 NN tool들을 제공하지만, FPGA도 모델도 모두 커스텀이었기 때문에 직접 Quantization 후 도출값을 비교하였다. 이때, Quantization으로 인해 하락하는 정확도 보정을 위해 QAT를 적용하였다.

### SNN 가속기 하드웨어 아키텍처 설계 및 구현

<img src="/images/Research_intern_25/Research_intern_25_2.png" width="100%"/>
Figure 2. System HW Architecture

Python으로 구성된 모델 아키텍처를 Verilog로 재구성하였다. 초기 계획은 위 이미지의 음성의 전처리부도 FPGA상에 구현하는 것이었기 때문에 음성을 받아와 FFT 하는 모듈을 설계하였다. 이후 SNN 모델과 LIF 뉴런 레이어 들을 모두 verilog 모듈로 구현하고, UART 통신과 LED를 통해 FPGA상에서 타겟 키워드의 검출 결과를 PC로 재전송하도록 모듈을 구성하였다.

 <div class="img-row">
    <img src="/images/Research_intern_25/Research_intern_25_3.png" 
    width="49%"/>
    <br/>
    Figure 3. Verilog SNN Modules
    <img src="/images/Research_intern_25/Research_intern_25_4.png" 
    width="49%"/>
    <br/>
    Figure 4. (도입되지 못한) Verilog SNN 오디오 전처리 모듈..ㅠㅠ
</div>

중간중간 TestBench를 통해 개별 모듈의 정상 동작을 확인하였으며, 데이터 전처리를 담당하는 Top module과 뉴런 레이어를 구성하는 Top module 각각의 중간 확인을 마친 상태라 문제 없이 끝날 것으로 생각되었다. 하지만, 모든 모듈을 하나의 Top Module로 합치는 과정에서 문제가 생겼다. Top Module에서 Clock을 준수하는 Layout 합성이 불가능했다. Pipe lining을 통해 연산 유닛의 동시사용을 최소화하는 등의 여러 노력을 하였으나, 학부생 연구인턴 마감일이 다가와 결국 PC에서 음성 전처리를 수행한 후 결과로 나온 Spike Train을 FPGA로 전송하면 FPGA 상에서는 Spike Train을 가지고 가중치를 통과하는 SNN Layer 연산만을 수행하도록 재구성하였다.

### 결과 및 소회

<img src="/images/Research_intern_25/Research_intern_25_5.png" 
    width="70%"/>
Figure 5. SNN 모델 FPGA 포팅 후 실행 결과

결론적으로 모델 학습 과정에서 충분히 다양한 샘플 데이터를 확보하지 못해 결과적으로 Over-fitting이 발생하기도 했고, 초반에는 Bias 조절과 같은 Neural Network관련 백그라운드가 부족하여 발생한 실수가 많았어서 성공한 프로젝트라고 말하기는 어렵지만, FPGA도, Neural Network 학습도 처음으로 내 손으로 직접해본 프로젝트라 뿌듯한 프로젝트였다. 
하지만, 음성 전처리부를 PC에서 수행하도록 하여 전체 시스템을 FPGA 상에서 구현하지 못한 점, 모델 트레이닝이 깔끔하지 못했던 점 등 아쉬움이 많이 남았다. 다음 번에는 더 괜찮은 NN 시스템을 구현해보고싶다.

### 수상

이 프로젝트를 기반으로 [POLARIS SIF 2026(차세대반도체 페스티벌)](https://polargate.disu.ac.kr/contest/SIF2026/final?sc=y) 작품 부문에 출품하여 3등상(장학금 180만원)을 최종 수상하였다. 처음 해본 도메인의 프로젝트였지만, 이 프로젝트를 통해 큰 상을 받을 수 있어 기뻤다.

이 프로젝트를 기반으로 **엣지 디바이스에서 Custom ASIC**의 적절한 사용이 얼마나 중요한 지, 또 효율적인 **AI Model의 서빙 방식**에 큰 관심을 갖게 되어 System Software 연구실에서 학부 연구생을 시작하게 되었다. 새로운 분야를 접할 좋은 기회와 큰 상을 모두 주신 차세대 반도체 혁신융합대학에 감사드리며, 나와 같은 학부생들이 이 기회를 잡을 수 있었으면 좋겠다.
