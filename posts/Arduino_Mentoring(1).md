---
title: Arduino Mentoring ( 1 ) w.ESP32
date: 2024-10-13
author: VINI
category: ESP32
project: Mentoring
overview: true
thumbnail: AM49.jpg
---

### 회차별 Summary
--- 

#### 아두이노 멘토링을 시작하게 된 계기
CECOM의 '24-2 운영진 첫회의에서 CECOM의 앞으로의 진행 방향에 대하여 아주 긴 시간 논의하였다.
컴퓨터 하드웨어 동아리이니 만큼(컴퓨터, 하드웨어 아니고 컴퓨터 하드웨어) 하드웨어 프로젝트 중심으로 되돌아가는 것으로 의견을 취합하여
부원들이 부담감없이 하드웨어 프로젝트를 시작할 수 있도록 다양한 방식의 지원을 하기로 결론지었다.

이러한 __CECOM 하드웨어 플젝 부흥을 위한 프로젝트__ 의 일환으로 이전의 참여율이 저조하고 지속성이 떨어지는 언어 멘토링보다는
토이 프로젝트를 통해 아두이노를 배우는 프로젝트형 멘토링을 모든 요일 열게되었다. 
아두이노와 가까워진 후 프로젝트에 들어가면 그 외의 필요한 것들 (C++ 심화 문법이나 또다른 프레임워크 등)은
필요에 따라 직접 구글링을 통해 혹은 스터디를 통해 각자 배워갈 수 있다고 판단했기 떄문이다.

그래서 나는 **아두이노 멘토링 월요일반** 의 멘토가 되었다. ..

그렇게 맡은 아두이노 월요일반의 진행기를 요기에 써보도록 하겠다!<br/> 
아두이노 멘토링은 매일 1시간 ~ 1시간 반정도만 진행되기 때문에 조금만 심화되는 내용을 다루기에도 시간이 모자란 경우가 잦아서
나는 초밥기계를 굴리기 위한 아주 기본적인 뼈대만 설명하고 나머지는 멘티들에게 
아두이노 포럼과 [lastminuteengineers의 esp32 포럼 링크]를 같이 뿌려서 참고할 수 있도록 하였다!

#### 💻 멘토링 1회차 (9/29)
- **간단한 자기소개 시간**
<div class="img-row">
    <img src="/images/AM/AM1.jpg"  width="49%"/>
    <img src="/images/AM/AM2.jpg"  width="49%"/>
</div>
<div class="img-row">
    <img src="/images/AM/AM3.jpg"  width="49%"/>
    <img src="/images/AM/AM4.jpg"  width="49%"/>
</div>
<div class="img-row">
    <img src="/images/AM/AM5.jpg"  width="49%"/>
    <img src="/images/AM/AM6.jpg"  width="49%"/>
</div>
<div class="img-row">
    <img src="/images/AM/AM7.jpg"  width="49%"/>
    <img src="/images/AM/AM8.jpg"  width="49%"/>
</div>

- **아두이노 멘토링이 필수여야 한다고 생각했던 이유**
    - 토이 프로젝트 경험을 쌓아주기 위함
        - 아두이노 멘토링은 강의가 아닌 체험형 토이 프로젝트
        - 이번 간단한 프로젝트가 여러분의 다음 프로젝트의 발판이 되었으면 함
    - 친목 도모
        - 신입부원의 오프라인 학술활동 참여 권장
        - 친목 도모를 통한 새로운 아이디어 공유 및 재밌는 플젝 시작

- **아두이노 알아보기**
    - 아두이노는 아두이노사에서 만든 개발 환경, 개발 보드 등등 여러가지를 통칭
        - 아두이노 보드 (MCU)
            - MCU는 마이크로 컨트롤러 유닛
            - 말 그대로 하드웨어를 컨트롤 하는데 필요한 모든 것들을 하나의 쪼고만 개발보드에 모두 때려 넣은 것.
        - 아두이노 IDE
            - 통합 개발 환경!
            - 기능이 아주 간결함
            - 비전공자용이라 모든 것들이 직관적이고 아주아주 쉬움

- **ESP32에 대해 알아보기**
    - 상하이에 있는 Espressif사의 개발보드

    - 장점
        - 블루투스 두가지(클래식/BLE) 모두 가능
            - 다른 보드 쓰고 HM-10 납땜한 거 보믄 짱큼 →BT를 칩 하나에 올린 게 정말 큰 장점
        - wifi 통신도 사용가능
        - 듀얼코어
        - gpio핀도 꽤 많음
            - 모듈 하나 당 gnd, Vcc 핀을 제외하고도 4-5개의 핀을 사용함
            - 많은 모듈을 붙여서 여러 기능을 구현하려면 gpio핀 개수도 꽤 중요하게 고려해야할 요인임
        - 여러가지 개발 환경을 통해 개발할 수 있음
            - 라이브러리가 꽤 짱짱해서 espressif SDK를 이용해서 C언어로 개발하는 것도 나쁘지 않음!
            - 하지만 우리는 가장 접근성이 좋은 아두이노를 통해 개발을 진행할 것..
            - 아두이노 멘토링이니 당근..

- **내가 왜 멘토되었냐면…**
    - ESP32와 아두이노로 진행한 프로젝트

        - **나비잠**
            - 신생아 분리수면시 위험상황을 감지해서 부모에게 알림
            - 사용 센서 : 심박 센서, 기울기 센서 등
        - **세콤네컷 1.0**
            - esp32는 모듈 하나로 BT, 와이파이 통신을 다 함.
            - 사진 찍어서 BT로 프린터로 보내고, 와이파이로 서버에 업로드 함.
            - esp32의 한계
                - 앞에서는 장점만 설명하였으나, ESP32는 이미지를 처리하고, BLE 연결, wifi로 서버 개방까지 모든 걸 수행하기에는 성능이 조금(많이) 떨어졌음
                - 원한다면 eeprom을 추가하여 해결 할 수 있긴 함
            -  더이상 수정 절차를 거치고 싶지 않아 RPI4를 활용하여 세콤네컷 2.0 프로젝트를 다시 시작하였음.
    - 기타 플젝(UNO)
        - 가전제품 작동완료 알림이
        - 급식 태깅기     
 
<br/> 

#### 💻 멘토링 2회차 (10/7)

<div class="img-row">
    <img src="/images/AM/AM12.jpg"  width="49%"/>
    <img src="/images/AM/AM13.jpg"  width="49%"/>
</div>
<div class="img-row">
    <img src="/images/AM/AM14.jpg"  width="49%"/>
    <img src="/images/AM/AM15.jpg"  width="49%"/>
</div>
<div class="img-row">
    <img src="/images/AM/AM16.jpg"  width="49%"/>
    <img src="/images/AM/AM17.jpg"  width="49%"/>
</div>


- **GPIO**
    - General Purpose Input/Output
    - **pinMode(**디지털핀넘버**);** 로 선언 후 digital(analog)Write(Read)로 제어

- **Analog 신호 쓰기/읽기**
    - ADC
        - 0~3.3V까지의 인풋을 256단계로 쪼개어(2^8) 측정함
        - 왜 256단계?
            - 8비트의 분해능 2^8
    - PWM
        - Purse Width Moduration
        - Purse의 켜진 부분의 너비(Duty Ratio)를 조정하여 밝기를 아날로그 신호로 조정한 것과 유사한 효과를 냄

- **회로**
    - 빵판(브레드보드)
        - 빵판의 각 끝부분의 두 줄은 세로로 연결되어있음
        - 가운데 줄은 각각 a~e까지, f~j까지 가로로 연결되어있으며,
        e와 f 사이는 연결되어있지 않으므로 주의해야 함.
    - LED
        - 발광 다이오드
        - 애노드(+)과 캐소드(-)이 존재함.
        - **CODE**
            
            ```jsx
            int LED_BUILTIN =2;
            
            void setup() {
              // initialize digital pin LED_BUILTIN as an output.
              pinMode(LED_BUILTIN, OUTPUT);
            }
            
            // the loop function runs over and over again forever
            void loop() {
              digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
              delay(1000);                      // wait for a second
              digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
              delay(1000);                      // wait for a second
            }
            ```
            
    - 저항
        - 220옴 쓰면 됨

- **TOUCHpin**
    - touchRead(핀넘버); 를 통해 이용
    - 256단계의 아날로그 시그널로 읽혀 esp32에서 정전용량 모니터링 가능
    - 원리
        - ESP32 has 10 capacitive touch-sensing GPIOs. When a capacitive load (such as a human skin) is in close proximity to the GPIO, ESP32 detects a change in capacitance.
    - **CODE**
        ```jsx
        int LED = 12;
        
        void setup() {
        Serial.begin(115200);
        delay(1000); // give me time to bring up serial monitor
        Serial.println("ESP32 Touch Test");
        pinMode(LED,OUTPUT);
        }
        
        void loop() {
        if (touchRead(4) <= 50) {
            digitalWrite (LED, HIGH);
        } else {
            digitalWrite(LED, LOW);
        }
        delay(1000);
        }
        
        ```


[lastminuteengineers의 esp32 포럼 링크]: https://lastminuteengineers.com/electronics/esp32-projects/






