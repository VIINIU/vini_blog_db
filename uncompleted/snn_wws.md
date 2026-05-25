---

title : SNN WWS Project
date : 2025-11-19
category : AI & Deep Learning
project: Study
pinned : true
---
### ✔ Background | 연구 배경

---

- **연구 시작 배경**

'25-2학기 학교에 복학하면서 차세대반도체 융합혁신대학의 학점교류 프로그램을 참여하게 되었고, 선우경 교수님의 학부생 연구인턴 프로그램에 참여하여 SNN을 처음 접하게 되었다. 학부생 연구인턴의 대주제는 SNN과 FPGA였고, 나는 SNN 활용 Wake-word Spotting(이하 WWS) System을 주제로 프로젝트를 진행하였다.

SNN은 Spike Neural Network의 준말로 생체 신호를 모방하여 연속된 값이 아닌 불연속적인 Spike 신호를 활용하여 인공신경망을 구현하는 기술이다. 다른 신경망들과 달리 SNN은 Event-Driven 처리가 기본 IDEA이기 때문에 낮은 Power Consumption과 Temporal한 DATA에 강하다는게 장점이다. Power Consumption이 낮아 늘 켜져있는 시스템에 그 중에서도 Temporal한 신호를 다루는 음성 시스템에 SNN을 활용하면 좋겠다는 생각을 하게되었다. 그렇게 전체 시스템을 깨우는 음성 명령에 적용하면 좋겠다는 생각에 이르게 되었다.

내가 생각한 SNN WWS 시스템의 활용가능성은 스마트폰이나 이어버드, 무선 헤드폰과 같이 효율적인 Power 사용이 중요한 모바일 기기의 'Hey, Siri', 'Ok google', 'Alexa' 와 항상 켜져있어야 하는 호출 키워드 감지 기능에 활용할 수 있는 NPU 등으로 활용하는 것이다~!

암튼 이번 프로젝트에 대한 회고를 시작해보겠다.

### 🫧 모델 학습 (python)

---

나는 감지할 target keyword는 Amazon alexa의 호출키워드인 Alexa로 설정했다. (사유 : 학습용 데이터가 많음)
타겟 키워드의 WAV 파일을 받아 FPGA에서 실시간 계산이 가능한 수준으로 sample rate는 16kHz로 설정했고, Bit 해상도는 8bit로 설정했다..ㅎㅎ
Bit 해상도와 Sample rate 둘 중에 하나는 포기를 해야했는데, Sample rate를 낮춰서 학습시키니까 죽어도 60%에서 정확도가 안 올라서 포기하고 Bit 해상도를 줄였다. 그랬더니 나의 아이가 바로 음성을 학습할 줄 아는 똑똑이가 됨
또, 음원 개수가 많으면 오버피팅도 줄고 좋다길래 배경 소음도 깔고, 속도도 늘리고 줄이고, 갖은 짓을 하여 샘플이 1000개가 되었다.
암튼 그렇게 Wav 파일을 준비하고, 이걸 SNN에 돌릴 수 있도록 STFT로 주파수별 데이터를 뽑고, Mel Filter로 걸러서 Spike Train으로 바꿔야 했었는데, 이건 그냥 라이브러리 써서 멋지게 해결했다. . ㅎㅎ

사실 학습 자체는 너무 쉬웠다.. 왜냐면 numpy도 snntorch도 너무너무 자료가 많아서 문제가 생겨도 금방금방 해결할 수 있었다..
자료가 많아서 제미나이도 똑똑해서ㅎㅎ(바이브코더가 되..) 정말 금방금방 해결했다.

하지만, 가장 어려운 부분은 따로 있었다..
바로 Verilog 설계와 파이프라인 맞추기...(이건 정말 퍼즐이 따로 없음)

### 📚 Verilog로 신경망 구현

---

