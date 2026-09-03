---
title: "MINI-V Android : LLM 모델 내장 안드로이드 OS 커스텀"
date: 2026-09-02
category: Android, LLM
project: Android OS
thumbnail: MINI-V_Android/MINI-V_Android.png
---
## 프로젝트 개요

---

<img src="/images/MINI-V_Android/MINI-V_Android.png" width "80%">

- AOSP에 기반을 둔 커스텀 안드로이드 오픈소스인 Lineage OS에 Qualcomm 기반의 LLM 추론 기능을 HAL 레벨에서 구현한 커스텀 Android
- Device
	- Xiaomi 13 (Code Name: fuxi)
- Source
	- NPU Workload
		- Scaling LLM Test-Time Compute with Mobile NPU on Smartphones
			- 이 논문의 htp-ops-lib, llama.cpp-npu 두 개의 라이브러리를 Prebuilt로 Embed 함
	- Xiaomi Vendor Source
		- Vendor 소스코드는 승인된 Device 제조사에만 제공되는 Closed Source
		- [The Muppets라는 닉네임의 Github User](https://github.com/orgs/TheMuppets/repositories)가 많은 기기에서 추출된 Vendor 소스들을 제공하고 있음
	- LineageOS 23.2
		- [Xiaomi 13](https://wiki.lineageos.org/devices/fuxi/)을 포함한 다양한 디바이스를 위한 펌웨어를 제공하고 있고 Instruction이 아주 친절
		- [Xiaomi 13 OS Build를 위한 Instruction Link](https://wiki.lineageos.org/devices/fuxi/build/)
- Model
	- Qwen2.5-1.5B 모델을 Int 4-bit, 8-bit로 Mixed Quantization한 모델을 사용했다.


### 프로젝트 시작 계기

---

이 프로젝트는 System의 어떤 비효율적인 지점을 수정해서 LLM 추론에 더 효율적인 시스템을 만들고자 출발했다기 보다는 Android OS 그 자체 그리고 빌드 과정을 포함한 그 모든 레이어에 대해 학습하고, 구현하고 싶다는 목표가 있어서 시작하게 되었다.

그리고 몇 년 전에 CES에 나와서 온갖 어그로를 끌었다가 하드웨어가 너무 빈약해서 스캠이라고 욕먹고 사라진 Vision 기반 Agent Device Rabbit r1이라는 기기를 갖고싶어서..
OS를 잘 구워삶으면 럭키 Rabbit r1이 될 수 있지 않을까? 라는 생각으로 OS 레벨에서의 Model 내장을 계획했었다..
(이미지 처리에 대해 상당히 무지한 발언)

그런 마음을 품고 있을 때.. 우연하게 [Scaling LLM Test-Time Compute with Mobile NPU on Smartphones](https://arxiv.org/abs/2509.23324) 이런 논문을 봤고,  👩🏻‍💻 ◦ ₒ ° ๐ ○ (NPU를 내맘대로 조물조물 할 수 있구나!) 라는 착각과 함께 목표를 세웠다.
이렇게 야심차게 시작해놓고, 프로젝트 중반까지 CPU 백엔드로 구현한다고 논문 펼쳐보지도 않음..

그렇게 목표를 설정한 유용민군과 나는 Scaling LLM...(중략) 논문에 나온 Snapdragon 8 Elite Gen 2가 탑재된 Bootloader Unlock이 쉬운 Xiaomi 13을 구매했고, 본격적으로 개발을 시작했다.


## Background and Motivation

### 기존 Android Application AI Workload

<img src="/images/MINI-V_Android/Pasted image 20260901142854.png" width="100%"> 
Figure 1. 기존 Android System의 AI 추론 흐름

기존 Android System에서 Application의 AI Model 사용 방식은 크게 두가지가 존재한다. 첫째로 Application의 Assets에 포함시켜 APK 파일에 모델을 직접 미리 넣어 배포하는 방식과 두번째로 AI 기능 활성화 시, 사용자 동의 하에 서버로부터 모델을 다운로드 받는 방식이다. 이 두 가지 방식 모두 문제점을 발생 시키게 된다. 첫번째 방식의 경우 (1) Application 배포파일의 사이즈가 커진다는 문제점을 발생시키는데, 배포파일의 사이즈가 커지면, Application의 유지와 보수를 담당하는 개발사 입장에서 낮은 설치 전환률, 데이터 부하, 지원 기기 축소등의 부담이 증가한다. 두번째 방식을 채택하여 (2) AI 기능을 활성화 할 때에만 사용자 동의 하에 서버로부터 모델을 다운로드 받는 방식은 사용자 동의 UX 구축에 어려움을 준다.

이런 과정을 통해 사용자의 Android 기기에 모델을 다운로드 받더라도 사용 과정에서 문제점이 발생하게 된다. 바로 (3) 여러 개의 Application이 각자 자신의 모델을 가지고 있어서 발생하는 Context Switching Overhead 문제이다. 모바일의 특성 상 AI 워크로드를 처리할 수 있는 가속 Engine(NPU, GPU 등)의 메모리가 크지 않아, 두 개의 모델을 동시에 올리기 어렵기 때문에 두 개 이상의 Application이 동시에 활성화 되면 각각 자신이 가진 모델의 가중치를 Engine에 올렸다가 내리는 과정에서 발생하는 Overhead가 발생하게 된다. 

Local AI Engine을 사용할 때 발생하는 이런 문제점을 해결하기 위해 네트워크 연결을 통해 서버에서 구동되는 AI를 사용하도록 워크로드를 구성하면, (4) Android 기기에서 네트워크 연결이 모바일 데이터 사용설정 혹은 와이파이 연결을 통해 항상 보장되어야 한다는 점과 (5) AI Model 구동을 위한 서버 환경 비용 부담, (6) 민감 데이터의 경우 개인정보 보안 부담 등의 문제점이 발생하게 된다.

위와 같은 문제를 해결하고 Android Application이 부담없이 AI Agent를 활성화 할 수 있는 환경을 마련하기 위해 다양한 Use Case에 맞는 LLM Model을 각 하드웨어에 최적화된 형태로 OS Level에서 Embedding하자는 아이디어를 가지고 이 프로젝트를 시작하게 되었다.

### Mobile NPU를 활용한 LLM 추론

Scaling LLM Test-Time Compute with Mobile NPU on Smartphones[^1]에 따르면, Mobile에서 NPU를 사용하여 LLM 추론을 할 때 그 워크로드의 하드웨어 활용 패턴이 Prefill과 Decode 단계 중 어떤 단계에 있는 지에 따라서 달라지는데, Decoding Phase가 구동되는 동안 NPU에서 Matrix Multiplication을 담당하는 HMX Unit이 Idle 상태에 놓이게 된다. 위 논문에서는 이러한 문제를 해결하기 위해 남는 시간을 활용하여 동일한 Prefill Phase후에 Decoding을 병렬로 한 번에 여러 갈래로 진행한 후, 그 중에 가장 나은 답변을 활용하였고, 이를 통해 Mobile의 작은 Scratch Pad Memory에서 돌아갈 만큼 작은 모델로도 좋은 성능을 낼 수 있다는 결론에 도달하였다. 

우리가 주목한 것은 이 논문의 해결방식이 아닌 구현방식이다. 논문에 나와있는 바에 따르면 Qualcomm이 공개하지 않는 하드웨어 바이너리의 HMX 호출 부분에 대한 논문 저자들의 Reverse Engineering이 진행되었고, 이를 통해 알아낸 HMX 호출 Command를 사용하여 NPU를 사용한다.

위 논문에서 구현한 방식의 NPU 워크로드[^6][^7]를 활용하되, 다양한 어플리케이션이 NPU를 사용할 수 있도록 추론 엔진을 Vendor Level에서 Embedding 하기로 결정하였다. 

### Android Operating System Layer

<img src="/images/MINI-V_Android/Pasted image 20260901151429.png" width="50%"> 
Figure 2. Android System Partition

안드로이드 시스템은 AOSP(Android Open-Source Preject)[^8]의 구글 소유의 소스코드에 기반을 둔 운영체제이다.
초기 안드로이드는 하드웨어 칩셋 제조사의 코드가 변경되면 그에 따라서 기기 제조사가 커스텀한 부분을 업데이트하여 운영체제 업데이트를 지원하였다. 이렇게 업데이트를 진행하다보니 AOSP 소스코드에 변화가 있을 때마다 하드웨어 칩셋 제조사의 바이너리 업데이트가 지원되고 기기 제조사의 업데이트까지 진행되어야만 소비자들이 자신의 기기를 업데이트 할 수 있는 긴 흐름이 생긴다는 문제점이 있었다.

이런 문제점을 해결하기 위해 안드로이드 시스템 Android 8.0부터 Treble이라는 규정을 두고 엄격하게 Vendor 영역과 System 영역을 나누어 두고 AOSP 소스 업데이트에 따라 반영되는 부분은 모두 System 영역으로 규정하였고, 두 부분이 서로 침범하지 않으면서 정보를 주고받도록 Treble 규정을 두었다.

### Target Device와 OS Customization

이 프로젝트에서는 위에서 언급한 논문에서 제공하는 NPU의 OP 구현체를 활용하기 위해 논문에서 활용된 Chipset인 Snapdragon 8 Gen 2를 탑재한 Xiaomi 13을 검증용 기기로 사용하였다.

이 프로젝트에서는 하드웨어 칩셋을 컨트롤하는 소스에 대해 업데이트 되어야 했고, 많은 Application들이 편하게 접근하기 위해서는 System API가 제공되는 편이 낫고, NPU를  판단하여 Vendor와 System의 두 부분 모두에서 구현을 진행하였다. 이 두 부분을 모두 Custom 하기 위해서는 Vendor파트를 포함하는 전체 Operating System에 대한 Custom이 필요했다. 이를 구현하기 위해 이 프로젝트에서는 AOSP에 기반을 두고, 하드웨어 트리를 포함하여 제공하는 Lineage의 Xiaomi 13을 위해 Custom된 OS[^3] 소스 코드를 기반으로 구현하였다.

## Design

### Overveiw
MINI-V Android OS의 구현체는 크게 두가지로 나누어져 존재하도록 디자인하였다. 첫번째는 System 영역에 구현되는 MINI-V AI Service(Framework)이고, 두번째는 Vendor 영역에 구현되는 MINI-V AI Daemon이다. 추가로 정상적인 동작 확인을 위해 MINI-V AI Service를 사용하는 MINI-V Chat이라는 예시 Application을 추가하였다.

<img src="/images/MINI-V_Android/Pasted image 20260901151709.png" width="100%"> 
Figure 3. MINI-V Android OS의 전체 Design

Vendor 파트의 경우 MINI-V AI Daemon 하위에 위치하는 실제 추론 구현체를 두가지 방식으로 구현했는데 첫번째는 CPU만 추론 엔진으로 활용하는 버전과 CPU와 NPU를 사용하는 버전이다. NPU 구조가 다르거나 NPU가 포함되어 있지 않은 기기에서도 MINI-V Android OS의 구현체를 Embedding하기 쉽도록 하기 위하여 두가지 버전으로 나누어 구현을 진행했다. CPU만 활용하는 Vendor 구현체인 `LLMEngine` 의 경우 `llama.cpp`[^5]를 NPU와 CPU를 모두 활용하는 Vendor 구현체의 경우 `llama.cpp-npu`[^6]를 기반으로 구현하였다.

### Session Management

Motivation에서 언급했던 여러 앱이 서로 다른 모델을 쓰면서 발생하는 Context Switching Overhead를 해결하기 위해 Session이 전환되지 않고 이어지도록 하는 Session Management Logic을 Vendor단에 구현하였다. 앱은 `createSession()`을 인자 없이 호출하고, 서비스가 내부 카운터로 발급한 세션ID를 돌려받는다. 이 ID는 이후 모든 요청(`inferStream()`, `cancel()`, `destroySession()`)에 실려 벤더 엔진까지 전달되며, 매 호출마다 세션을 새로 발급하던 기존 방식 대신 여러 턴에 걸친 대화를 하나의 세션으로 유지할 수 있도록 설계했다.

<img src="/images/MINI-V_Android/Pasted image 20260901154616.png" width="100%"> 
Figure 4. MINI-V Android OS의 Session Management Logic

엔진 레벨에서는 동시에 유지 가능한 세션 수가 무한정 늘어나는 것을 막기 위해 Hot/Cold 2단 구조로 세션을 관리하도록 디자인하였다. Hot 세션은 접근이 빠른 RAM에, Cold 세션은 비교적 접근이 느린 Disk에 보관되도록 구성하였다. `LLMEngine` 에서는 Hot은 용량을 기반으로 미리 설정한 용량을 넘어서면, Hot에서 가장 오래된 세션이 Cold 영역으로 넘어가는 정책으로, Cold 영역은 보관 Session의 개수 한도를 넘으면 가장 오래된 세션부터 Kill하는 LRU 정책으로 관리하도록 디자인하였다.

NPU 기반 엔진(`NpuLLMEngine`)에도 동일한 설계 철학을 적용하되 NPU/DSP 자원 제약에 맞춰 DSP 컨텍스트(KV 캐시)를 하나만 유지할 수 있어 Hot 세션은 1개로 제한하였고, 그 밖의 세션은 대화 내용을 Text Transcript 형태로 메모리에 보존한 Cold 상태가 된다. Cold 상태였던 Session이 Hot으로 전환되면 저장해둔 Transcript 전체를 재실행해서 KV 캐시를 그 세션의 마지막 상태로 복원하도록 구현하였다.

### Inference Engine

앞서 언급한 바와 같이 추론엔진은 두 갈래로 Design 하였다. 두 구현 갈래 중 메인에 해당하는 NPU 워크로드를 기반으로 하는 `NpuLLMEngine`의 경우에는 모델 로드 시점에 `DSP_LIBRARY_PATH` 환경변수로 Qualcomm FastRPC 로더가 DSP측 스켈레톤 라이브러리(`libhtp_ops_skel.so`)를 찾을 경로를 지정해줘야 한다. 엔진은 로컬 디버깅용 UDS 소켓(Command Line Test용)과 프레임워크가 쓰는 AIDL HAL(Application용 API) 두 진입점에서 같은 전역 인스턴스를 공유하도록 구현하였다. Background에서 확인한 바와 같이 Qualcomm Chipset의 NPU를 활용하는 부분은 DSP활성화를 위한 Binary 구현체가 필요하고, 이 구현체들은 원본 기기의 Binary File[^4]과 htp-ops-lib[^1]을 통해 직접 빌드한 바이너리를 링크하였다.

CPU 워크로드를 기반으로 하는 `LLMEngine`의 경우에는 LLM Serving Open Source인 `llama.cpp`를 기반으로 구현하였다.

## Implementation

MINI-V는 repo 툴로 관리되는 LineageOS 23.2 소스에 mini-v.xml 매니페스트를 추가해, GitHub organization의 프레임워크·벤더·디바이스 트리 레포를 함께 받아오는 구조이다. 빌드는 `lunch`로 타겟 디바이스를 지정하면 Soong이 각 디렉토리의 `Android.bp`로 의존성 그래프를 만들고, Ninja가 이를 바탕으로 컴파일·링크해 파티션 이미지를 생성하는 순서로 진행된다. 새로 추가한 소스가 결과물에 반영되려면 종류별로 지정된 변수(`PRODUCT_PACKAGES`, `BOARD_VENDOR_SEPOLICY_DIRS`, `DEVICE_MANIFEST_FILE` 등)에 명시적으로 등록되어야 한다. 

다른 소프트웨어 구현과 달리 Android OS Custom 그 중에서도, Vendor와 System 영역 동시 Custom의 경우에는 수많은 git repository가 매 빌드에 오랜 시간이 소요되었다. 빌드가 끝난 이후 기기에 빌드된 OS를 굽는 플래싱은 전체 이미지를 매번 새로 굽는 대신, A/B 업데이트 구조를 이용해 수정된 파티션만 담은 payload를 빌드하고 `adb sideload`로 설치하였다.

### AIDL 기반 HAL 구현

프레임워크-벤더 계층은 세 개의 AIDL 인터페이스로 구성된다. 앱-시스템 서비스 간은 `IMINIVAIService`/`ILLMStreamCallback`, 시스템 서비스 내부 엔진 추상화는 순수 Java 인터페이스인 `LLMEngine`, 시스템 서비스-벤더 데몬 간은 `IMiniVAiHal`/`IMiniVAiStreamCallback`이다. 앱은 벤더 HAL의 존재를 모르고 `IMINIVAIService`만 참조한다.

벤더 AIDL은 `stability: "vintf"`로 선언해 시스템과 벤더가 서로 다른 시점에 빌드되어도 호환성이 유지되도록 했다. freeze가 필요하며, 벤더 인터페이스는 기본적으로 Java 백엔드가 꺼져 있어 `Android.bp`에서 명시적으로 활성화했다. freeze된 인터페이스의 Stub을 직접 구현할 때는 `getInterfaceHash()`/`getInterfaceVersion()`을 구현자를 채워야 컴파일이 통과한다. HAL을 시스템에 등록하려면 VINTF 매니페스트(`DEVICE_MANIFEST_FILE`)에 `<hal>` 블록으로 인터페이스명·버전·인스턴스를 명시해야 하고, 벤더 데몬의 `init.rc`에는 `interface aidl vendor.miniv.ai.IMiniVAiHal/default` 선언이 필요하다. 이 선언이 없으면 servicemanager가 서비스를 lazy-HAL 자동 기동 대상으로 인식하지 못해, 클라이언트가 서비스를 기다리다 타임아웃으로 이어진다.

HAL 단독 동작은 `hal_test_cli`로 검증했다. `create_session` → `infer` → `destroy_session`을 순서대로 호출해 세션 Create/Destroy가 정상 반환되고, 추론 요청이 Hexagon NPU를 거쳐 응답 스트림으로 돌아오는 것을 enforcing 상태 실기기에서 확인했다.

### Android SE Policy

SELinux는 프로세스가 접근 가능한 파일·서비스·IPC 대상을 도메인 단위로 제한하는 MAC 방식이다. 벤더 데몬을 프레임워크에서 호출하려면 프레임워크가 벤더를 부를 수 있어야 하고, 벤더는 프레임워크로부터 불릴 수 있어야 하며, 벤더는 자신의 데이터 디렉토리에 접근할 수 있어야 한다.

이 정책을 위반하여 특정파일의 실행이나 조회가 실패한 경우에도 보안 상의 문제로 왜 실패하였는지 표시되지 않아 디버깅이 어려웠다. sepolicy 디렉토리 등록이 누락되거나 매크로 배치가 잘못되어도 빌드 자체는 에러 없이 성공하고, 실제로 문제가 되는 코드 경로가 처음 실행되는 시점에야 `avc: denied` 로그로 드러난다. 개발 중에는 `setenforce 0`로 전역 permissive를 걸어두는 경우가 많은데, 이 상태에서는 위반이 로그로만 남고 실제 차단은 일어나지 않아 문제가 더 늦게 발견된다. 원인 파악은 `setenforce 0`/`1`을 오가며 permissive에서는 되고 enforcing에서는 안 되는지를 확인해 sepolicy 문제인지부터 좁히고, 이후 빌드 산출물의 CIL 파일에서 `typeattributeset`(속성 배정)과 `allow ... binder`(실제 권한) 존재 여부를 각각 확인하는 방식으로 진행했다.

정책 구성은 다음 순서로 갖췄다. `service_contexts`에 `miniv_ai`, `vendor.miniv.ai.IMiniVAiHal/default` 서비스명을 각각 전용 타입으로 등록하고, 이 타입에 대해 `system_server`에는 `add`, 호출 주체가 되는 앱 도메인(`priv_app`, `platform_app`)에는 `find` 권한을 부여했다. HAL 레벨에서는 `hal_attribute`로 HAL 속성을 선언하고, 프레임워크 쪽에 `hal_client_domain(system_server, hal_miniv_ai)`, 벤더 쪽에 `hal_server_domain(miniv_ai, hal_miniv_ai)`를 선언해 두 도메인 간 binder 통신을 연결했다. system-vendor 양쪽이 공유 참조하는 선언은 `public`, 특정 파티션 안에서만 유효한 권한 부여는 `private`으로 분리했고, 두 디렉토리는 `BoardConfigCommon.mk`의 `SYSTEM_EXT_PUBLIC/PRIVATE_SEPOLICY_DIRS`에 등록해 빌드에 반영되도록 했다.

`system_ext` 파티션이 존재하는 이 기기 구성에서는 `hal_client_domain()` 매크로가 속성 배정까지만 만들고 실제 binder `allow` 규칙은 생성하지 않는 경우가 있어, 다음 규칙을 직접 추가해 보완했다.
```
allow system_server hal_miniv_ai_server:binder { call transfer };
```

### Model

모델은 CPU 워크로드와 NPU 워크로드 두 가지 버전에서 모두 Qwen2-1.5B를 사용하였다.

### On-device execution

디바이스와 연결된 컴퓨터에서 adb tool을 이용해 기기의 터미널 명령어로 `hal_test_cli` 를 실행해보면 아래 그림과 같이 세션이 잘 만들어지고, 추론이 설계한 NpuLLMEngine을 통해 정상적으로 수행되는 것을 확인할 수 있다.

<img src="/images/MINI-V_Android/스크린샷 2026-09-01 오후 3.43.23.png" width="80%"> 
Figure 5. adb tool을 통해 cli로 접근하여 NPU를 활용한 추론을 진행한 모습

디바이스에 구현한 예시 Application으로 추론을 수행한 모습은 아래와 같다.

<img src="/images/MINI-V_Android/스크린샷 2026-09-01 오후 4.54.01.png" width="50%"> 
Figure 6. Application을 통해 추론을 수행한 모습

실제로 추론이 실행되는 부분의 스크린 영상 녹화본은 [추론 동영상 링크](https://youtube.com/shorts/Q6Vg0jByNgI?feature=share)를 통해 확인할 수 있다.

## Contribution and Limitation

### Contribution

Scaling LLM Test-Time Compute with Mobile NPU on Smartphones[^1] 논문에서 Reverse Engineering을 통해 구현한 HMX 모듈을 활성화하는 소스를 활용하여 LLM as a System Service on Mobile Devices[^2] 의 여러 앱이 LLM을 개별로 들고 있는 대신 OS가 하나의 시스템 서비스로 제공해야 한다는 아키텍처 방향을 직접 NPU 워크로드를 활용하는 방식으로 Android OS로 구현했다.

이 프로젝트를 진행하는 동안 위 논문의 아이디어를 LineageOS 기반의 실제 빌드 가능한 OS로 옮기기 위해 여러 아이디어를 적용하였다. AIDL과 VINTF로 시스템-벤더 경계를 정의하고, SELinux sepolicy로 이 경계의 접근 제어를 실제로 완성해, 실기기 enforcing 상태에서 앱부터 NPU 추론까지 이어지는 전체 경로를 검증했다. 논문[^2]이 제안한 세션 관리 개념도 Hot/Cold KV 캐시 스왑과 오래된 토큰 정리 정책으로 직접 구현해, 여러 세션이 동시에 존재할 수 있는 상태에서 메모리 사용량을 제어했다.

### Limitation

하지만, OS Custom 형태로 서비스를 지원하면서 지원 범위가 Xiaomi 13 한 기종에 한정된다. htp-ops-lib과 llama.cpp-npu가 특정 Hexagon 버전을 대상으로 하기 때문에, 다른 NPU 아키텍처나 칩셋으로 옮기려면 해당 레이어를 다시 구현해야 한다는 문제점이 존재한다. 또한 Session Management 파트도 NPU 엔진의 경우에는 DSP 컨텍스트를 하나만 유지할 수 있어 Hot 세션이 사실상 1개로 제한된다는 한계점이 존재한다.

## Conclusion

AI Agent가 우리의 생활속에 녹아드는 과정에서 Android System은 더 많은 Application 들의 AI 추론을 더 효율적으로 Handling하는 방식으로 변화할 것이다. Android System은 제조사마다 하드웨어 구현방식이 달라 System단에서 진행되는 최적화로는 Application 개발자 입장에서 모든 사용자에게 균일한 서비스 경험을 주는데 어려움이 있을 것이라고 생각한다. 

이를 해결하고, 보편화된 AI Agent 제공을 위해서 변화하는 방향은 이 프로젝트에 구현 바와 같이 OS Level 그 중에서도 Vendor Level에서 통일된 AI 추론 HAL API를 제공하는 방식으로 통합될 것이라고 예상한다. 

Hardware와 Software의 Co-Design은 AI Agent의 큰 연산량을 Edge Device에 맞춰 효율화하는 과정에서 더욱 중요한 과제로 부상할 것이고, 이런 Edge Device의 효율적인 AI System 구축을 위한 연구가 필요하다고 생각한다.

## Reference

[1] Zixu Hao, Jianyu Wei, Tuowei Wang, Minxing Huang, Huiqiang Jiang, Shiqi Jiang, Ting Cao, Ju Ren. "Scaling LLM Test-Time Compute with Mobile NPU on Smartphones." European Conference on Computer Systems (EuroSys '26), 2026. arXiv:2509.23324. [https://arxiv.org/abs/2509.23324](https://arxiv.org/abs/2509.23324)
[2] Wangsong Yin, Mengwei Xu, Yuanchun Li, Xuanzhe Liu. "LLM as a System Service on Mobile Devices." arXiv preprint, 2024. arXiv:2403.11805. [https://arxiv.org/abs/2403.11805](https://arxiv.org/abs/2403.11805)
[3] LineageOS Project. LineageOS Android Source Code. GitHub Organization. [https://github.com/LineageOS](https://github.com/LineageOS)
[4] TheMuppets. Extracted Vendor Blobs for Various Android Devices. GitHub Organization. [https://github.com/TheMuppets](https://github.com/TheMuppets)
[5] Georgi Gerganov et al. llama.cpp: LLM Inference in C/C++. GitHub repository. [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
[6] Zixu Hao. llama.cpp with custom Hexagon NPU backend (llama.cpp-npu). GitHub repository, 2025. [https://github.com/haozixu/llama.cpp-npu](https://github.com/haozixu/llama.cpp-npu)
[7] Zixu Hao. Custom Op library for Qualcomm's Hexagon Tensor Processor (htp-ops-lib). GitHub repository, 2025. [https://github.com/haozixu/htp-ops-lib](https://github.com/haozixu/htp-ops-lib)
[8] Google / Android Open Source Project. AOSP Documentation. [https://source.android.com/docs](https://source.android.com/docs)
