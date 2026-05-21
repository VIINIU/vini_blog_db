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
이 프로젝트를 통해 나온 것이 구글의 Tensor Processing Unit이고, 이 TPU로부터 발전하기 시작된 것이 AI 워크로드에 특화된 Domain Specific Custom ASIC인 Neural Processing Unit이다.

NPU는 Domain Specific한 특성 덕분에 최적화되어 GPU보다 빠르고, 전력을 적게 소모하며 동일한 연산을 수행할 수 있다. 또한 Domain Specific한 특성때문에 GPU보다 범용성이 떨어지고, CNN 워크로드를 위해 만들어진 NPU는 LLM을 돌리는데 큰 이점이 없는 것과 같이 타겟 워크로드와 레이어 구성이 다른 경우 동일한 NPU를 사용하는 것이 어렵다.

NPU의 발전 역사는 아래와 같다.

| Generation | Period | Description |
| --- | --- | --- |
| **First** | 2015-2017 | Focus on data centers, basic TPU, matrix units for 8-bit operations, efficient for inference, no sparse optimization |
| **Second** | 2017-2019 | Integration into mobile devices, local DNN model processing, real-time inference, lower precision (FP16/INT8), lower energy consumption |
| **Third** | 2019-2022 | Higher scalability and energy efficiency, systolic array matrices, support for BF16, liquid cooling, higher throughput |
| **Fourth** | 2022 - present | Advanced optimization for servers and mobile devices, support for large models (LLM, multimodal), software optimizations (XLA, TensorFlow Lite, Core ML), high energy efficiency per watt |

*Table 1. Overview of NPU Generations And Key Characteristics*

Generation에 따라서 












---

### 1. GPU와 NPU의 특성 및 효율성 비교 (4페이지)



| 하드웨어 구분 | 특성 및 효율성 |
| --- | --- |
| **GPU** | General Purpose (High flexibility), Low Energy Efficiency, Low Area Efficiency |
| **NPU** | Domain Specific (Low flexibility), High Energy Efficiency, High Area Efficiency |

---

### 2. CPU, GPU, NPU 종합 특성 비교 (7~8페이지)



| Characteristics | CPU | GPU | NPU |
| --- | --- | --- | --- |
| **Primary Purpose** | General-purpose instruction processing, serial execution | Massively parallel data processing, graphics and AI tasks | Specialized parallel processing for AI algorithms and neural networks |
| **Parallelism** | Low (6-64 cores) | hundreds-thousands of cores | thousands-millions of MAC units |
| **Energy Efficiency** | Low for AI tasks | Medium, high for parallel AI operations | High, especially for inference and quantized models |
| **Precision** | FP32/FP64 | FP32/FP16/INT8 | FP32/BF16/INT8 |
| **Optimal AI Tasks** | Logic, data preparation, control | Model training, large matrix processing | Inference, real-time processing, LLM, CNN, diffusion and multimodal models |
| **Typical Devices** | Desktop, server, mobile CPU | Server, HPC, desktop, laptop | Mobile devices, IoT, servers, AI accelerators |
| **Latency** | Higher for parallel AI tasks | Medium | Lowest for specific AI operations |

---

### 3. 구글 TPU(Tensor Processing Unit) 세대별 발전 과정 (10, 17페이지)



| Generation | Period | Description |
| --- | --- | --- |
| **First** | 2015-2017 | Focus on data centers, basic TPU, matrix units for 8-bit operations, efficient for inference, no sparse optimization |
| **Second** | 2017-2019 | Integration into mobile devices, local DNN model processing, real-time inference, lower precision (FP16/INT8), lower energy consumption |
| **Third** | 2019-2022 | Higher scalability and energy efficiency, systolic array matrices, support for BF16, liquid cooling, higher throughput |
| **Fourth** | 2022 - present | Advanced optimization for servers and mobile devices, support for large models (LLM, multimodal), software optimizations (XLA, TensorFlow Lite, Core ML), high energy efficiency per watt |

---

### 4. TPU의 주요 CISC 명령어 (14페이지)



| 명령어 (Instruction) | 설명 (Description) |
| --- | --- |
| **Read_Host_Memory** | CPU 호스트 메모리에서 Unified Buffer로 데이터를 읽어옴 |
| **Read_Weights** | Weight Memory에서 가중치를 읽어 Matrix Unit의 입력으로 사용될 Weight FIFO로 가져옴 |
| **MatrixMultiply / Convolve** | 행렬 곱셈 유닛이 통합 버퍼의 데이터를 바탕으로 행렬 곱셈이나 합성곱 연산을 수행 $\rightarrow$ 결과를 Accumulators에 저장 |
| **Activate** | Accumulator의 값 $\rightarrow$ ReLU, Sigmoid 수행 $\rightarrow$ Unified Buffer 저장 |
| **Write_Host_Memory** | Unified Buffer $\rightarrow$ CPU Host Memory에 쓰기 |

---
