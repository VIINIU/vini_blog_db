---
title:  "Telechips Topst Internship"
date:   2026-02-06
category: Linux
project: Internship
pinned: true
--- 

## ✔ 세부 사항

---

- **‘26 Winter Semester (2026.01)**
- Telechips 사에서 중앙대학교 차세대 반도체 혁신융합대학 사업부를 통해 모집한 1개월 인턴쉽에 참여
- Telechips의 Topst 보드 3종 (AI-G, D3-G, VCP-G)을 메뉴얼을 따라 브링업
- NPU 보드에 해당하는 AI-G를 이용하여 객체인식을 수행하고, D3-G가 메인 제어부, VCP-G가 실제 모터, LED 등 출력을 수행하는 자율주행 자동차 구현


## 🧰 관련 사이트

- TOPST 커뮤니티
    
    [TOSPT 커뮤니티](https://community.topst.ai/)
    
    TOPST 보드가 다른 개발보드에 비해 용례가 적어 참고할 자료가 많지 않았는데, 커뮤니티에 질문을 올리면 해당 보드의 디테일한 부분들을 현직자들이 답변을 해준다!

- TOPST Education 자료 깃허브 레포지토리

    [TOPST Education](https://github.com/topst-development/Education.git)

    Telechips TOPST 사업부에서 진행하는 TOPST 보드 활용 교육의 다양한 자료들을 그대로 공개하고 있다!
    메뉴얼에 적혀있지 않은 디테일한 개념들이 적혀있어 참고하기 좋다!

- TOPST 공식 Documentation

    [TOPST Docs](https://topst.ai/tech/docs)

    한국어 버전보다는 영어버전이 약간 더 디테일하다.
    Quick 가이드를 보고 브링업한 이후에 모르는 게 생기면 유저가이드 보는 것을 추천!

## 💬 인턴 수기


### 📖 보드 Bring-Up

---

늘 그렇듯 항상 보드의 첫 사용이 참 어렵다.
D3-G와 AI-G 모두 리눅스 기반이고, 일단 Yocto를 사용하여 커스텀 리눅스 OS를 빌드해야했다.
Telechips의 Github에 올라와있는 meta-topst라는 TOPST Linux SDK image를 Clone하여 빌드하고, 각 보드에 맞는 방식으로 구워주었다. (노릇노릇)
자세한 브링업 방법은 Docs에 나와있기에 나는 브링업하며 공부하게 된 것에 대해 짤막하게 설명해보려고 한다.

- VCP-G 브링업과 FreeRTOS

VCP-G를 브링업하며 FreeRTOS에 대해 자세히 공부할 기회가 생겼다.
STM32를 사용하면서 Cmake도 만들고 나름 써봤다고 생각했지만, 전혀 아니란 걸 깨달았다.
STM Cube가 너무 친절한 나머지 RTOS에 대해 전혀 몰랐던 내가 main.c만 찾아서 코딩하고, 펌웨어를 구울 수 있도록 했던 것이다. . 

하여간 RTOS에 대해 공부한 요지는 아래와 같다.



이렇게 각 보드를 브링업하고 보드의 특성에 맞는 작은 프로그램을 하나씩 수정해서 올리다보니 2주하고 절반이 지나간 시점이었다. .. (OMG)