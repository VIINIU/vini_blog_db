---
title: NPU란 무엇인가..
date: 2026-05-21
category: AI & Deep Learning
project: Internship
pinned: true
thumbnail: seminar_npu/seminar_npu_1.png
---
---

### ✔ 세미나 개요
- NPU(Neural Processing Unit) 아키텍처
- 2026년 5월 CUDA 세미나에 이어 진행한 NPU 세미나의 내용을 정리한 글입니다.

---

### 🎛️ NPU란?
Google Cloud에서 2013년부터 본격적으로 음성인식을 도입하면서, 늘어나는 DNN 워크로드를 처리할 디바이스가 필요했고, GPU는 전력 소모가 크고 Lactency를 만족하지 못하기 때문에 Domain Specific한 ASIC 설계를 통해서 Neural Network Workload만 특화되어 처리하는 Printed Circuit을 만드는 프로젝트를 진행하였다.

이 프로젝트를 통해 나온 것이 구글의 **Tensor Processing Unit**이고, 이 TPU로부터 발전하기 시작된 것이 AI 워크로드에 특화된 Domain Specific Custom ASIC인 **Neural Processing Unit**이다.

NPU와 GPU의 하드웨어 설계에 따른 특성은 아래의 표와 같다.

| 하드웨어 | 특징 |
| --- | --- |
| **GPU** | General Purpose (High flexibility), Low Energy Efficiency, Low Area Efficiency |
| **NPU** | Domain Specific (Low flexibility), High Energy Efficiency, High Area Efficiency |

*Table 1. Difference Between GPU and NPU*

위 표를 통해 알 수 있듯 Flexibility와 Efficiency 사이에는 Trade-off가 존재한다. NPU는 Domain Specific한 설계 덕분에 최적화되어 GPU보다 빠르고, 전력을 적게 소모하며 동일한 연산을 수행할 수 있다. 또한 Domain Specific한 특성때문에 GPU보다 범용성이 떨어지고, CNN 워크로드를 위해 만들어진 NPU는 LLM을 돌리는데 큰 이점이 없는 것과 같이 타겟 워크로드와 레이어 구성이 다른 경우 동일한 NPU를 사용하는 것이 효율적이지 않다. 또한, NPU는 CUDA와 같이 통일된 생태계가 존재하지 않고, Vendor마다 다른 구조 때문에 각각의 Vendor에서 제공하는 nntool을 사용해야 한다. 이 tool은 주로 사용할 AI model에 맞춰 미리 Sub-graph를 생성하고, edge와 Mobile인 경우 Quantize, 이후에 NPU Unit에서 실행 가능한 형식으로 변환하기 위한 Compile을 수행한다.

GPU는 앞서 공부한 바와 같이 개발자가 원하는 연산을 직접 구현할 수 있는 CUDA Kernel을 제공하고 GPGPU(General Purpose Graphic Processing Unit)의 개념이 등장하면서 범용성을 위해 각각의 SM이 각자 자신의 PC를 갖고, 심지어 최근에는 각각의 Thread들까지도 각각의 PC를 갖기 때문에 유연한 연산 변화가 가능하다.

그럼에도 불구하고 전력 제한과 빠른 Response가 강조되는 Edge Device와 Mobile에서는 전력 소모를 줄이는 것이 중요하기 때문에 NPU가 주로 사용된다. 이때는 Sparse를 고려하여 연산량을 최대한 줄여 전력소모를 줄이는 여러가지 컨트롤 레이어가 추가되기도 한다.


| Generation | Period | Description |
| --- | --- | --- |
| **First** | 2015-2017 | Focus on data centers, basic TPU, matrix units for 8-bit operations, efficient for inference, no sparse optimization |
| **Second** | 2017-2019 | Integration into mobile devices, local DNN model processing, real-time inference, lower precision (FP16/INT8), lower energy consumption |
| **Third** | 2019-2022 | Higher scalability and energy efficiency, systolic array matrices, support for BF16, liquid cooling, higher throughput |
| **Fourth** | 2022 - present | Advanced optimization for servers and mobile devices, support for large models (LLM, multimodal), software optimizations (XLA, TensorFlow Lite, Core ML), high energy efficiency per watt |

*Table 2. Overview of NPU Generations And Key Characteristics*

NPU는 사용되는 Device에 따라 특성이 달라 세 가지 정도로 구별하여 설명하려 한다.
첫째는 Mobile과 Wearable에 사용되는 SoC 내부에 들어가는 NPU이다. 디바이스의 특성상 Energy-efficiency와 real-time inference가 강조된다. 해당하는 디바이스로는 삼성의 Exynos NPU Core, 화웨이 Kirin의 NPU Core, Qualcomm의 Snapdragon의 Hexagon 등이 있다.
둘째는 IoT나 Embedded와 같은 Edge Device에 들어가는 NPU 칩셋이다.
이 경우 Real-time이 강조되는 경우가 많아서 Low Latency가 중요하고, 대부분의  디바이스가 Network 연결에 관련 없이 On-device Inference를 Minimal Energy Use와 함께 수행되어야 한다.
셋째는 Server-side에서 사용되는 TPU와 같은 Accelerator이다.
이 디바이스의 경우 Large Model을 적절히 Serving하는 것이 중요하기 때문에 Low-latency와 High performance가 강조된다. 또한, Quantization없이 BF16, FP32등의 Precision이 그대로 사용된다.
NPU의 Generation에 따라서 TPU -> Mobile -> Edge 순으로 설명해보려 한다. 

---

### 👾 TPU
TPU의 경우 2015년 Google의 데이터 센터에서 도입되어 해당 유닛의 효용가치가 아래 논문을 통해서 증명되었다. 이 글의 TPU에 대한 설명은 아래 논문을 바탕으로 구성하였다.
In-Data center Performance Analysis of a Tensor Processing Unit (2017)

2015년에 나온 TPU v1의 경우 2013년 도입된 음성 검색의 DNN 수요가 데이터 센터의 연산량을 2배로 늘릴 것으로 예측하여 이 워크로드 처리를 위해 CPU를 사용하는 경우 병렬 연산으로 인한 Cost가 크고, GPU의 경우 Latency 충족이 어렵고 전력이 제한된다는 것이 문제가 되었다.
이를 위해 Domain-Specific ASIC인 TPU를 만드는 프로젝트를 시작하여 15개월의 짧은 기간만에 설계부터 배포까지 모든 사이클을 완료하였다.

이렇게 만들어진 TPU의 구조도는 Figure 1와 같고, Die 구성은 Figure 2와 같다.

TPU는 Server 환경이 타겟이기 때문에 Scalability를 고려하여 PCIe를 사용하여 CPU와 통신하도록 Co-processor로 디자인하였다. TPU는 PCIe 유닛을 통해 호스트에서 명령어가 오면, Host Interface를 통해 Instruction Buffer에 저장된다. 동시에 Input이 되는 Feature Map의 경우 Unified Buffer에 저장되며, 이에 상응하는 Weight는 DRAM에서 불러와 Weight FIFO에 쌓이게 된다.
MatrixMultiply 명령어를 통해 연산이 시작되면, Unified Buffer에 있던 데이터는 Systolic Array의 왼쪽에서 가로방향으로 들어간다. MAC 연산이 완료된 후 Output은 다시 Unified Buffer에 저장되어 다시 연산을 반복한다.
모든 연산이 완료된 후 마지막에 딱 한 번 호스트 메모리에 아웃풋이 작성된다.

이때, TPU에서 수행되는 연산에는 캐시 관리와 분기 에측 등의 제어가 필요하지 않기에 Flexibility를 위한 General한 기능은 모두 제거하여 Die의 67%를 연산과 Data path에 할당하고 Control Part의 면적은 2% 정도만 할당하여 Area Efficiency를 높였다.

<div class="img-row">
    <div style="width: 40%;">
        <img src="/images/seminar_npu/seminar_npu_2.png" width="100%"/>
        <br/>
        Figure 1. TPU Structure
    </div>
    <div style="width: 40%;">
        <img src="/images/seminar_npu/seminar_npu_3.png" width="100%"/>
        <br/>
        Figure 2. TPU Die
    </div>

</div>


---


#### Systolic Array 연산 메커니즘

TPU v1이 대규모 행렬 곱셈을 극도로 낮은 전력과 높은 처리량으로 수행 가능한 것은 **Systolic Array** 덕분이다.

일반적인 CPU나 GPU는 매 연산마다 메모리에서 데이터를 과정을 반복해야 하므로 Memory Bandwidth 병목 현상이 발생한다. 반면 Systolic Array는 세 방향으로 웨이트와 인풋, 아웃풋이 흐르며 연산을 효율적으로 수행한다.

<img src="/images/seminar_npu/seminar_npu_4.png" width="80%"/>

*Figure 3. 2D Systolic Array Data Flow inside Matrix Unit*

상단에서 Weight가 아래로, 좌측에서 입력 데이터가 오른쪽으로 흐르고, 연산 결과인 Partial Sum은 아래 Accumulator로 내려갑니다.

첫째, Weight Stationary 
Weight는 맨 처음 한 번만 각 PE의 레지스터로 로드되고, 이후 입력 데이터가 흘러가면서 같은 weight를 계속 재사용된다. SRAM 읽기 한 번이 수백 pJ 정도의 에너지를 소모하기에 weight읽는 횟수를 최소화하면 Energy의 사용이 크게 줄어들게 된다.

둘째로 MMU 안에서 아래방향으로 Partial Sum이 순차적으로 흐르는 Diagonal Wavefront입니다. 클록 사이클마다 256개의 Partial Sum이 동시에 생성되어 Accumulator로 흘러가고, 소프트웨어 입장에서는 Transparent하게 256개가 동시에 처리되는 것으로 보이게 된다.

셋째, Decoupled Access/Execute를 지원하여 Weight를 메모리에서 읽는 명령과 실제 행렬 연산 명령이 분리되어 있어, Weight가 FIFO를 통해 prefetch되는 동안 MAC 배열은 이전 연산을 계속할 수 있도록 구현되어 있다.
GPU와 비교하면, GPU SM은 범용 ALU가 캐시에서 자유롭게 데이터를 읽지만, TPU MAC은 데이터 이동 경로 자체가 하드웨어에 고정되어 있어 Die의 67%가 순수 연산 및 메모리 경로에 할당되고, Control은 2% 정도만 차지한다.

---


#### TPU 전용 CISC 명령어 셋

TPU v1은 하드웨어 복잡도를 낮추고 호스트 CPU가 직접 태스크를 제어할 수 있도록 12개 미만의 전용 Complex Instruction Set Computer(CISC) 명령어를 사용한다. 핵심 명령어 5가지는 다음과 같이 정의된다.

| Instruction | Description |
| :--- | :--- |
| **Read_Host_Memory** | CPU 호스트 메모리에서 Unified Buffer로 데이터를 읽어옴 |
| **Read_Weights** | Weight Memory에서 가중치를 읽어 Matrix Unit의 입력으로 사용될 Weight FIFO로 가져옴 |
| **MatrixMultiply / Convolve** | 행렬 곱셈 유닛이 통합 버퍼의 데이터를 바탕으로 행렬 곱셈이나 합성곱 연산을 수행하고 결과를 Accumulators에 저장 |
| **Activate** | Accumulator의 값에 ReLU, Sigmoid 등 활성화 함수 연산을 수행하여 Unified Buffer에 저장 |
| **Write_Host_Memory** | Unified Buffer에 저장된 최종 연산 결과를 호스트 CPU 메모리로 전송 |

*Table 3. Key CISC Instructions for TPU v1*

이 외에 7개의 명령어가 있어 총 12개의 명령어로 구성되어있으며, 이는 PCIe Unit을 통해 전달되며, 하나의 명령어가 평균 10~20 사이클의 연산을 커버한다.

---

#### TPU 성능 평가

<img src="/images/seminar_npu/seminar_npu_5.png" width="80%"/>

*Figure 4. Roofline model*

이 그래프의 가로는 바이트당 몇번의 연산을 하는지, 세로축은 연산성는 TOPS/s를 나타내며, 이 model은 메모리에 의한 보틀넥, 컴퓨팅에의한 보틀넥 두개를 동시에 보여주는 Roofline model이다. 여기서 Compute Bound -> Memory Bound로 전환되는 이 부분을 릿지 포인트라고 한다. 선으로 된 부분은 각각 이론적인 TPU, GPU, CPU의 루프라인이며, 별, 세모, 동그라미 모양은 각각 실제 성능을 나타낸다. 두 축이 모두 로그 스케일이기 때문에 Ridge Point를 보면 보이는 것보다 성능의 차이가 큰데, CPU는 약 13, GPU는 약 9, TPU는 1350이다.

TPU의 경우 루프라인에 근접한 정도의 실제 성능을 표현함을 알 수 있지만, GPU와 CPU는 이론적인 루프라인이 낮은데다가 실제 성능 사이의 차이가 큰데 이는 Latency 제약으로 인해 각각의 Batch 사이즈를 작게 설정해야하기 때문이다.



이처럼 Costom ASIC은 범용적인 사용은 불가능하지만, 추론에 활용할 때에 한해서는 여러 측면에서 매우 효율적인 수행이 가능하다.
이러한 장점은 엣지나 모바일과 같은 배터리 제약과 레이턴시 제약이 큰 환경에서 더 큰 장점이 된다.

---


### 📲 On-device NPU

두 번째로 등장한 NPU는 Mobile Chipset 내부에 포함되는 NPU이다. Mobile 기기는 하드웨어 특성을 고려했을 때, 주로 On-device Agent, Keyword-spotting, 간단한 LLM 및 이미지 생성, 얼굴·사물 인식 등에 사용된다.

삼성이 Hotchip에서 발표했던 Exynos 내부의 NPU 관련 발표자료를 기반으로 설명하려한다.

모바일 환경은 여러 CPU에 의해 워크로드가 통제되어 있는 서버 환경과는 차이가 크기 때문에 모바일 SoC 환경에서 충분히 유연하게 다양한 워크로드를 처리하기 위해 삼성 Exynos NPU는 하드웨어와 소프트웨어가 결합된 서브시스템을 디자인했다.

<img src="/images/seminar_npu/seminar_npu_6.png" width="80%"/>

*Figure 5. Samsung Exynos NPU-DSP Sub-System*

- **Multi-Core 및 데이터 병렬성 구성** 정격 전압 조건에서 936MHz의 클록 주파수로 동작하는 3개의 하드웨어 코어를 보유하고 있다. 코어당 2,048개의 Multiply-Accumulate(MAC) 유닛이 할당되어 총 6,144 MAC 규모를 자랑한다. 이는 합성곱 연산 시 32개의 입력 채널(Input Channel)과 64개의 출력 채널(Output Channel)을 동시에 처리할 수 있는 고성능 Data Parallelism 연산 구조이다. 이를 통해 최종 11.5 TOPS의 강력한 고정소수점 연산 성능을 확보해 낸다.
- **지원 데이터 정밀도** 저전력 가속의 표준인 INT8 데이터 포맷 연산뿐만 아니라, 오차율 민감도가 높은 고정밀 레이어 연산 처리를 위해 INT16 연산까지 하드웨어 단에서 전용 네이티브 패스로 지원한다.
- **인프라 및 버퍼링** 각 코어 내부에는 1MB 용량의 대용량 Scratchpad Memory가 캐시 메모리 대용으로 배치되어 내부 연산 데이터를 유지하며, Shared DMA와 전용 DMA Pool을 이용해 외부 Dynamic Random Access Memory(DRAM)와의 데이터 트랜잭션 오버헤드를 구조적으로 차단한다.

---

#### Adder-tree 기반의 데이터패스 설계 기믹

대다수의 NPU 가속기들이 Accumulator와 Flip-Flop 조합으로 구성된 직렬 방식의 Dot-product Engine을 사용하는데 반해 Adder-tree 기반 data-path를 사용한다.

- **전력 소비 저감 메커니즘** Adder-tree 구조는 병렬 배열된 product들의 최종 결과를 Accumulator 단계로 넘겨주어 Partial Sum을 여러번 읽고 쓰는 과정을 생략하여 연산 유닛 자체의 전력 소모량을 크게 줄인다.
- **Flexibility 확보** 이런 메커니즘을 통해 연산의 유연성을 확보하여 여러가지 Convolution이 가능하다.

---

#### 하드웨어 레벨의 Zero Skipping 연산 가속

일반적인 Deep learning infrastructure에서 Feature Map은 50% 이상이 0으로 채워져 큰 Sparsity 특성을 보인다. 이 과정에서 연산 유닛이 Idle에 놓이는 상황을 줄이기 위해 Zero-skipping을 적용하였다.

<img src="/images/seminar_npu/seminar_npu_7.png" width="80%"/>

*Figure 6. Zero Skipping 데이터 흐름 메커니즘*

- Fetching Unit 내부의 Input Feature Map(IFM) Fetcher가 Scratchpad Memory로부터 Tensor를 읽어 들일 때, 가속기 내부의 Dispatching Unit에 결합된 Sparsity Controller가 각 데이터 라인을 모니터링 하다가 0을 발견하면 해당 연산 파이프라인을 홀딩하고 오직 유효한 Non-zero 성분만을 선별하여 하위 16x16 MAC Array로 전달한다.

---

#### Quad-tree 기반의 Feature-map Lossless Compressor

DRAM Memory Bus의 Bottle Neck을 줄이고, 메모리 트랜잭션을 최소화하기 위해  Exynos NPU 시스템은 Quad-tree 기반의 Feature-map Lossless Compressor를 사용한다.

<img src="/images/seminar_npu/seminar_npu_8.png" width="80%"/>

*Figure 7. Quad-tree 클러스터링을 이용한 Compressor*

- Zero Feature 값들이 특정 행렬 영역에 클러스터링되어 뭉쳐 있는 공간 특성을 계층적으로 스캔하기 위해 **Level 2 -> Level 1 -> Level 0 구조의 Quad-tree** Meta-data 기법을 사용한다.
- 스트림 포맷 데이터 구조 실시간 디코더 하드웨어가 읽어 들이는 압축 스트림 포맷은 다음과 같이 엄격하게 정렬되어 직렬화된다.
    - Stream Length | 전체 Data Stream length
    - Truncated Nonzero Bitwidth | 유효 데이터들의 bit precision
    - Quad-tree Header | Zero 값의 분포 상태를 트리 인덱스로 압축한 Meta Data
    - Nonzero Features | 0을 제외하고 남은 data들의 Array
- 하드웨어 디코딩 가속
Indexing metadata와 Non-zero 데이터만 DRAM에 저장하고, 코어로 전송되면, On-chip HW Decoder가 Overhead 거의 없이 실시간으로 Decompression하여 한정된 Memory Bandwidth를 좀 더 효율적으로 사용한다.

---

#### Fast Resource Scheduling 파이프라인 제어

컴퓨팅 코어가 연산을 도는 시간 동안 DMA Time 숨겨 파이프라인 버블을 제거하기 위해, 하드웨어 Command Queue(CMDQ) 제어 루틴이 밀리초 단위 이하로 작동한다.

<img src="/images/seminar_npu/seminar_npu_9.png" width="80%"/>

*Figure 8. parallelization을 위한 Fast Resource Scheduling Timeline 및 Synchronization*

- 동적 파이프라인 관리
    컴파일러가 Neural Network 구조를 Sub-Graph 단위의 이진화 바이너리로 쪼개면, 하드웨어 내의 CMDQ가 각 실행 장치 간의 인터럽트를 수십 사이클 단위 내에서 가져와 처리한다.
- 이전 레이어의 출력을 외부로 내보내는 Write OFM 프로세스, 현재 레이어를 연산하는 NPU Core 엔진 구동, 다음 레이어 처리를 미리 준비하는 Read IFM 및 Read Weight 태스크가 각 단계별 Synchronization Fence를 기준으로 엇갈려 병렬 실행된다. 이를 통해 높은 Core Utilization이 가능하다.

---

#### Host Driver와 SW Frame Work Stack

ENN toolchain은 유저가 설계한 model 가속을 위해 프론트엔드부터 커널 드라이버까지 전체 워크로드를 따라 구성되어있다.

- Samsung ConVersion Tool (SCVT) 
    PyTorch, TensorFlow, ONNX 및 Caffe model을 입력받아 최적의 전처리를 수행한다. 복잡도가 높은 컴비네이션 오퍼레이션을 단순화하는 그래프 최적화(예: `SpaceToBatchND` + `Conv2D` + `BatchToSpaceND` -> `Dilated Conv`로 완전 치환)를 수행하며, 무의미한 `Add`/`Mul`/`Activation` 레이어들을 가중치 및 바이어스 내부로 접어 넣는 Folding 최적화를 감행한다.
- MQ Tools 
    NPU에서 모델을 돌리기 위해서는 Quantization이 필수적인데 이에 필요한 툴들이다.
    1. *Profiling*  |  샘플 데이터를 입력해 각 Channel과 Layer의 Activation의 통계적 분포 데이터를 추출
    2. *Quantization*  | Profile 지표를 기반으로 최적의 Fractional Length를 결정해 INT 정밀도로 변환
    3. *Compensation*  | 원본 model 대비 Quantization error를 분석하여 bias 값을 보정
- Performance Estimator (PE)
     드라이버 레벨의 스케줄링 환경을 에뮬레이션 -> Layer-by-layer 단위의 Compute 및 DMA 타임 소요량을 미리 뽑아내는 성능 예측 시뮬레이터 역할을 수행
전반적인 동작과정은 아래 이미지와 같다.

<img src="/images/seminar_npu/seminar_npu_10.png" width="80%"/>

*Figure 9. 전체 동작과정*

이처럼 Mobile NPU는 다양한 워크로드에 적용하기 위하여 내부에 Computing Unit과 Command를 Handle하는 컨트롤 로직이 포함되어 있어, 앞서 살펴본 TPU보다는 Flexibility에 신경을 쓴 디바이스이다. 모바일 Workload는 다양하기에 GPU를 사용하면 범용성 확보에 이점이 있겠지만, 전력소모와 레이턴시 측면에서 잃는 부분도 그만큼 많기에 NPU가 주로 사용된다.

---


### 👀 Edge Vision NPU

#### 텔레칩스 TOPST AI-G


<img src="/images/seminar_npu/seminar_npu_1.png" width="80%"/>

*Figure 10. TOPST AI-G*

모바일 인프라와 달리 고신뢰성 및 실시간성이 요구되는 스마트 모빌리티 및 로봇 공학 환경에서는 주로 MCU나 CPU 등의 Main Processor 옆에 내장된 형태로 NPU가 제공된다. 이번 세미나에서는 지난 인턴쉽을 통해 사용해본 텔레칩스 TOPST AI-G 개발 보드와 여기에 내장된 N-dolphin NPU의 아키텍처를 중심으로 발표하게 되었다. 모든 사진 자료와 내용은 [🔗Topst 공식 홈페이지](https://topst.ai/tech/docs)와 [🔗Topst 공식 깃허브 교육자료](https://github.com/topst-development/Education/tree/edu/Fabless/LectureNote)에서 찾아 정리하였다.

---

#### 듀얼 클러스터 독립 연산 파이프라인

N-dolphin NPU는 앞서 설명한 바와 같이 Main Processor 역할을 하는 CPU와 같은 보드에 NPU를 넣은 구조이다. Telechips는 차량과 자율주행을 위한 Chipset을 생산하는 회사이기 때문에 자율주행을 위한 이미지 처리에 Focusing된 형태로 디자인된 NPU이다.

- Dual Cluster 
    내부적으로 4TOPS의 연산력을 지닌 독립 클러스터 2개가 결합된 4TOPS + 4TOPS 듀얼 클러스터 시스템 아키텍처를 채택했다. 각 Accelator가 독립적인 레지스터 맵과 파이프라인 컨텍스트를 점유하기에 단일 칩 내부에서 격리된 2가지 계통의 Neural Model Inference을 동시 병렬 실행하는 Multitasking Accelation 능력을 내포하고 있다.
- 임베디드 호스트 CPU 통합 
    내부에 Cortex-A53 Quad Core CPU를 내장하고 있어, Custom Build한 Linux OS를 올리고 NPU Accelation 제어와 추론 이후 디스플레이 후처리까지 단일 보드에서 가능하다.


#### model 포팅

대부분의 NPU Vendor는 공급한 NPU Chipset에서 가장 효율적으로 연산이 수행되도록 NPU binary 실행파일을 만들수 있도록 하는 툴을 제공하는데 Telechips에서 이를 위해 제공하는 툴은 tc-nn-toolkit이다.

<img src="/images/seminar_npu/seminar_npu_11.png" width="80%"/>

*Figure 11. tc-nn-toolkit model 변환 및 추론 과정*

- Neural Network Converter
    PyTorch, TensorFlow, Darknet 등 다양한 포맷으로 학습된 model 파일 구조를 입력받아 NPU 고유 하드웨어 가속 추상화 계층 인터페이스인 Enlight 포맷 model(`example.enlight`)로 변환한다. 이 단계에서 토폴로지를 스캔하여 하드웨어가 지원하지 못하는 Unsupported Layer가 있는지 판별한다.

- Neural Network Quantizer
    수집된 Activation 데이터를 기반으로 기존 FP32 형태의 weight를 INT8 model(`example_quantize.enlight`)로 변환한다.

- Neural Network Compiler & Simulator
    Quantization이 완료된 모델을 기반으로 NPU Binary Set 으로 최종 컴파일 아웃풋을 생성한다. 
    
---

#### 실제 모델 포팅 결과

<img src="/images/seminar_npu/seminar_npu_12.png" width="80%"/>

*Figure 12. TOPST AI-G 추론 결과*

모델을 실제로 포팅해서 추론을 수행해보면, 30FPS 정도의 추론 속도가 나온다. 정상적으로 추론되어 Object Detection이 수행되는 것을 볼 수 있다.
동시에 두개의 모델을 돌려도 FPS는 거의 변화하지 않는다. NPU는 하드웨어적 특성 상 지원되는 레이어의 범위가 정해져있기 때문에 이 지원 레이어의 범위는 Telechips의 보드 브랜드 페이지인 Topst.ai의 docs 페이지에서 확인할 수 있다.
지원하지 않는 레이어가 포함된 경우 해당 레이어부터 CPU로 Fall back하여 이후 레이어를 모두 CPU에서 처리하는 방식을 지원하지만, 특정 레이어를 CPU에서 처리한 후 다시 NPU로 올려 이후 레이어를 연산하는 기능은 아직 지원하지 않기 때문에,
지원하지 않는 레이어가 없는 모델을 사용하거나, 레이어를 커스텀하여 사용하는 것이 성능 상의 Gain이 크다.

---


### 📚 References
[1] N. Davidović, S. Nogo, and D. Bilinac, ["A Survey of Neural Processing Unit Architectures and Performance,"](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=11477735) in Proceedings of IEEE INFOTEH-JAHORINA, Mar. 2026.
[2] N. P. Jouppi, et al., ["In-Datacenter Performance Analysis of a Tensor Processing Unit,"](https://dl.acm.org/doi/abs/10.1145/3079856.3080246) Google, Inc., ISCA, 2017.
[3] J. S. Park, et al., ["Samsung Neural Processing Unit: An AI accelerator and SDK for flagship mobile AP,"]( https://hc33.hotchips.org/assets/program/posters/Hotchip%202021%20NPU.PDF.pdf) Hot Chips 33, 2021.
[4] Telechips Inc., ["TOPST AI-G Hardware Manual and Education Guideline,"](https://topst.ai/tech/docs) TOPST Development Team, 2026.