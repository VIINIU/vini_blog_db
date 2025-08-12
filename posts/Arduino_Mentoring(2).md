---
title:  Arduino Mentoring ( 2 ) w.ESP32
date: 2024-10-15
category: ESP32 
thumbnail : AM49.jpg
project: Mentoring 
---

### 멘토링 회차별 Summary 3-5회차

3회차 이후에는 모두 실습위주의 멘토링이 진행되어 대체로 사용되는 부품에 대해 소개 후 코드를 직접 작성해보는 순서로 멘도링을 진행하였다.
<br/> 

#### 멘토링 3회차
 <div class="img-row">
<img src="/images/AM/AM19.jpg"  width="49%"/>
<img src="/images/AM/AM20.jpg"  width="49%"/>
</div>
 <div class="img-row">
<img src="/images/AM/AM21.jpg"  width="49%"/>
<img src="/images/AM/AM22.jpg"  width="49%"/>
</div>
 <div class="img-row">
<img src="/images/AM/AM23.jpg"  width="49%"/>
<img src="/images/AM/AM24.jpg"  width="49%"/>
</div>

- **모터 종류 소개**

- 간단한 하드웨어 프로젝트 시 사용하는 모터는 주로 두가지

    - 서보모터
        - 일정 각도로 물체를 움직일 때 자주 사용
        - 180도/완전회전이 가능하며, 크기와 요구전압에 비해
        - 회전력이 세며, 특정 각도로 조절이 필요한 CCTV 등에 자주 쓰임.

    - DC 모터
        - 물체를 회전시킬 때 사용하는 모터
        - 일정 전력을 공급하면 회전, 전극을 반대로 연결하면 모터가 반대로 회전.
        - 공급하는 전력의 크기를 조절하여 회전 세기를 조절할 수 있음

- **모터 드라이버**

    - DC 모터는 양쪽 단자의 극성을 바꾸면 방향이 바뀜
    - 이런 양 단자의 극성변화를 소프트웨어로 제어.
    - PWM(2회차 참고)으로 모터의 출력을 제어할 수 있음.

- 이후 IF문으로 시리얼 입력에 따라 모터의 회전 방향을 바꾸는 실습을 진행


- **택트 스위치의 물리적 구조**
    - 두 라인이 끊여져 있다가 누르는 순간 두 라인이 연결되는 스위치
    - 하드웨어에선 동작의 트리거로 설정하기 좋음!
    
#### 멘토링 4, 5회차

 <div class="img-row">
<img src="/images/AM/AM25.jpg"  width="49%"/>
<img src="/images/AM/AM26.jpg"  width="49%"/>
</div>
 <div class="img-row">
<img src="/images/AM/AM27.jpg"  width="49%"/>
<img src="/images/AM/AM28.jpg"  width="49%"/>
</div>
 <div class="img-row">
<img src="/images/AM/AM29.jpg"  width="49%"/>
<img src="/images/AM/AM30.jpg"  width="49%"/>
</div>
 <div class="img-row">
<img src="/images/AM/AM31.jpg"  width="49%"/>
<img src="/images/AM/AM32.jpg"  width="49%"/>
</div>
 <div class="img-row">
<img src="/images/AM/AM33.jpg"  width="49%"/>
<img src="/images/AM/AM35.jpg"  width="49%"/>
</div>

- **택트 스위치의 사용방법**

    - 플로팅 상태
        - 핀에 아무것도 물려두지 않은 경우 기준점이 없으므로 0과 1의 값을 오락가락하는 값을 받게 됨
        - 해결을 위해서는 풀업, 풀다운으로 기준점을 만들어 줘야 함!

    - 풀업 상태
        - 양극(+, 여기서는 5V핀에서 출력되는 5V 전압)이 기준이 되는 상태

    - 풀다운 상태
        - 음극(-, 여기서는 GND핀의 접지 전압)이 기준이 되는 상태

    - 풀업 풀다운 플로팅의 확인
        - 그림과 같이 회로 연결 후 시리얼 모니터값을 확인

    - LED ON/OFF 제어하기
        - 예시 코드를 채워 풀업/풀다운으로 연결된 버튼으로 LED 제어하기

- 4-5회차는 중간고사 전, 후 회차라서 간단히 진행


#### 멘토링 6회차

- **3D 모델**

  - 모터는 그릇이 올라가는 판 아래 설치
  - 웜기어 사용하여 회전 방향을 수직으로 바꿔주도록 설계함

<img src="/images/AM/AM49.jpg"  width="70%"/>
