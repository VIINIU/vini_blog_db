---
title : NPU 세미나 내용 정리
date : 2026-05-21
category : Embedded, Hardware
pinned : true
thumbnail: NPU/npu_seminar.jpeg
---

### ✔ 세미나 개요
- NPU(Neural Processing Unit) 아키텍처
- 2026년 5월 CUDA 세미나에 이어 진행한 NPU 세미나의 내용을 정리한 글입니다.

### 🧰 NPU란?
Google Cloud에서 2013년부터 본격적으로 음성인식을 도입하면서, 늘어나는 DNN 워크로드를 처리할 디바이스가 필요했고, GPU는 전력 소모가 크고 Lactency를 만족하지 못하기 때문에 Domain Specific한 ASIC 설계를 통해서 Neural Network Workload만 특화되어 처리하는 Printed Circuit을 만드는 프로젝트를 진행하였다.

이 프로젝트를 통해 나온 것이 구글의 **Tensor Processing Unit**이고, 이 TPU로부터 발전하기 시작된 것이 AI 워크로드에 특화된 Domain Specific Custom ASIC인 **Neural Processing Unit**이다.

NPU와 GPU의 하드웨어 설계에 따른 특성은 아래의 표와 같다.

| 하드웨어 | 특징 |
| --- | --- |
| **GPU** | General Purpose (High flexibility), Low Energy Efficiency, Low Area Efficiency |
| **NPU** | Domain Specific (Low flexibility), High Energy Efficiency, High Area Efficiency |
*Table 1. Difference Between GPU and NPU*

위 표를 통해 알 수 있듯 Flexibility와 Efficiency 사이에는 Trade-off가 존재한다. NPU는 Domain Specific한 설계 덕분에 최적화되어 GPU보다 빠르고, 전력을 적게 소모하며 동일한 연산을 수행할 수 있다. 또한 Domain Specific한 특성때문에 GPU보다 범용성이 떨어지고, CNN 워크로드를 위해 만들어진 NPU는 LLM을 돌리는데 큰 이점이 없는 것과 같이 타겟 워크로드와 레이어 구성이 다른 경우 동일한 NPU를 사용하는 것이 효율적이지 않다. 또한, NPU는 CUDA와 같이 통일된 생태계가 존재하지 않고, Vendor마다 다른 구조 때문에 각각의 Vendor에서 제공하는 nntool을 사용해야 한다. 이 tool은 주로 사용할 AI 모델에 맞춰 미리 Sub-graph를 생성하고, edge와 Mobile인 경우 Quantize, 이후에 NPU Unit에서 실행 가능한 형식으로 변환하기 위한 Compile을 수행한다.

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
### TPU
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
    <img src="/images/NPU/TPU_v1_structure.png" width="40%"/>
    <img src="/images/NPU/TPU_v1_Die.png" width="40%"/>
</div>


#### Systolic Array 연산 메커니즘

TPU v1이 대규모 행렬 곱셈을 극도로 낮은 전력과 높은 처리량으로 수행 가능한 것은 **Systolic Array** 덕분이다.

일반적인 CPU나 GPU는 매 연산마다 메모리에서 데이터를 과정을 반복해야 하므로 Memory Bandwidth 병목 현상이 발생한다. 반면 Systolic Array는 세 방향으로 웨이트와 인풋, 아웃풋이 흐르며 연산을 효율적으로 수행한다.

<img src="/images/NPU/TPU_v1_systolic_array.png" width="80%"/>
*Figure 3. 2D Systolic Array Data Flow inside Matrix Unit*

상단에서 Weight가 아래로, 좌측에서 입력 데이터가 오른쪽으로 흐르고, 연산 결과인 Partial Sum은 아래 Accumulator로 내려갑니다.

첫째, Weight Stationary입니다. Weight는 맨 처음 한 번만 각 PE의 레지스터로 로드되고, 이후 입력 데이터가 흘러가면서 같은 weight를 계속 재사용된다. SRAM 읽기 한 번이 수백 pJ 정도의 에너지를 소모하기에 weight읽는 횟수를 최소화하면 Energy의 사용이 크게 줄어듭니다.

둘째로 MMU 안에서 아래방향으로 Partial Sum이 순차적으로 흐르는 Diagonal Wavefront입니다. 클록 사이클마다 256개의 Partial Sum이 동시에 생성되어 Accumulator로 흘러가고, 소프트웨어 입장에서는 Transparent하게 256개가 동시에 처리되는 것으로 보이게 된다.

셋째, Decoupled Access/Execute를 지원하여 Weight를 메모리에서 읽는 명령과 실제 행렬 연산 명령이 분리되어 있어, Weight가 FIFO를 통해 prefetch되는 동안 MAC 배열은 이전 연산을 계속할 수 있도록 구현되어 있다.
GPU와 비교하면, GPU SM은 범용 ALU가 캐시에서 자유롭게 데이터를 읽지만, TPU MAC은 데이터 이동 경로 자체가 하드웨어에 고정되어 있어 Die의 67%가 순수 연산 및 메모리 경로에 할당되고, Control은 2% 정도만 차지한다.


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

#### TPU 성능 평가

<img src="/images/NPU/TPU_v1_roofline.png" width="80%"/>
*Figure 4. Roofline model*

이 그래프의 가로는 바이트당 몇번의 연산을 하는지, 세로축은 연산성는 TOPS/s를 나타내며, 이 모델은 메모리에 의한 보틀넥, 컴퓨팅에의한 보틀넥 두개를 동시에 보여주는 Roofline 모델이다. 여기서 Compute Bound -> Memory Bound로 전환되는 이 부분을 릿지 포인트라고 한다. 선으로 된 부분은 각각 이론적인 TPU, GPU, CPU의 루프라인이며, 별, 세모, 동그라미 모양은 각각 실제 성능을 나타낸다. 두 축이 모두 로그 스케일이기 때문에 Ridge Point를 보면 보이는 것보다 성능의 차이가 큰데, CPU는 약 13, GPU는 약 9, TPU는 1350이다.

TPU의 경우 루프라인에 근접한 정도의 실제 성능을 표현함을 알 수 있지만, GPU와 CPU는 이론적인 루프라인이 낮은데다가 실제 성능 사이의 차이가 큰데 이는 Latency 제약으로 인해 각각의 Batch 사이즈를 작게 설정해야하기 때문이다.


---

이처럼 Costom ASIC은 범용적인 사용은 불가능하지만, 추론에 활용할 때에 한해서는 여러 측면에서 매우 효율적인 수행이 가능하다.
이러한 장점은 엣지나 모바일과 같은 배터리 제약과 레이턴시 제약이 큰 환경에서 더 큰 장점이 된다.

### On-device NPU

두 번째로 등장한 NPU는 Mobile Chipset 내부에 포함되는 NPU이다. Mobile 기기는 하드웨어 특성을 고려했을 때, 주로 On-device Agent, Keyword-spotting, 간단한 LLM 및 이미지 생성, 얼굴·사물 인식 등에 사용된다.

삼성이 Hotchip에서 발표했던 Exynos 내부의 NPU 관련 발표자료를 기반으로 설명하려한다.

모바일 환경은 여러 CPU에 의해 워크로드가 통제되어 있는 서버 환경과는 차이가 크기 때문에 모바일 SoC 환경에서 충분히 유연하게 다양한 워크로드를 처리하기 위해 삼성 Exynos NPU는 하드웨어와 소프트웨어가 결합된 서브시스템을 디자인했다.

<img src="/images/NPU/NPU_DSP.png" width="80%"/>
*Figure 5. Samsung Exynos NPU-DSP Sub-System*









---

### Edge Vision NPU