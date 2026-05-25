---

title:  "Appium, Python 활용 앱 조작 자동화하기"
date:   2025-08-19
category: Software & Automation
project: Study
---
### ✔ APPIUM 이란
---
 - Selenium으로 웹 크롤링하듯 에뮬레이터나 휴대전화에 연결하여 앱 UI요소들을 자동으로 조작할 수 있도록 하는 소프트웨어
    QA용으로 많이들 쓰는 것 같은데. . 난 앱에서 내가 원하는 정보를 찾기 위해서 사용했다.

### 🚩 APPIUM을 사용하게 된 이유
---
앱으로만 제공하고 있는 서비스를 이용하다보면, 이게 웹이면 참 조작이 쉬울텐데 앱이라서 그렇지 않은 부분이 많다는 것을 느낀다. 특히 업무에서 앱을 계속 쳐다보는 일이 생기다보니 이대로 진행하기보다는 앱 요소들의 조작을 자동화해서 좀 더 편하게 앱 내부를 살피고 싶다는 욕망이 생겼다. .👾 

앱피움을 이용한 앱 조작 자동화는 앱으로만 제공하는 자사 서비스에 등록된 특정 데이터를 직접 까보기 힘든 사람, 앱으로 진행해야할 노가다가 있는 사람, 특정 서비스에 대해 분석해보고 싶은 사람, 그리고 태생이 QA툴이니 QA를 진행하고 싶은 사람에게 추천한다. 

난 쇼핑앱 장바구니가 너무 쌓였을 때 빠른 전체 삭제를 위해서도 활용했었다. .

Python은 거의 처음 써보는 상황이었고, C/C++ 이외의 개발 경험은 그리 많지 않기 때문에 초보자 시점에서 내가 수행한 것들을 차근차근 설명해보겠다.


### 기초 설정
---
- **나의 환경**

    운영체제는 Windows이고, VS code 사용

- **안드로이드 스튜디오** 설치

    나는 에뮬레이터와 휴대전화 직접 연결 두가지 방법으로 사용을 해봤는데, 
    휴대폰으로 연결해서만 진행하려면 SCRCPY를 깔아야하는데 조금 귀찮으니 모든 것들이 한번에 깔리는 안드로이드 스튜디오를 설치하는 것을 추천한다. (빌드 툴도 사용하니 커맨드라인으로 설치는 비추)

    스튜디오 열 필요 없이 커맨드로 에뮬레이터를 오픈하고 싶다면 ANDROID_HOME 시스템 환경 변수 설정까지 완료해야 한다.
    
    설치 시 ANDROID_HOME 기본 경로 : `C:\Users\[user_name]\AppData\Local\Android\Sdk`

    - [🔗 안드로이드 스튜디오 설치 아카이브 링크](https://developer.android.com/studio/archive)

        나는 미어캣을 깔아두었으므로 미어캣버전을 기준으로 진행하겠다!
        설치 화면은 영어로 바꾸면 나옴!

- **JAVA** 설치

    - [🔗 JAVA 설치 링크](https://www.java.com/ko/download/windows_manual.jsp)
        
        JAVA 설치 후 경로를 찾아서 시스템 환경 변수 설정(변수명 JAVA_HOME)을 해주어야 한다.

    설치 시 JAVA_HOME 기본 경로 : `C:\Program Files\Java\jdk-[version]`

- **Python** 설치

    - [🔗 Python 설치 링크](https://www.python.org/downloads/)

        나는 3.13.3으로 진행하였고, 가상환경은 설정하면 좋지만, , 안해도 잘 돌아가더라.
        Python 설치 후 pip의 경로를 찾아서 사용자 환경 변수 path 설정을 해줘야 한다.
        설치하면서 뭔갈 잘못 선택하면 Python이 pip랑 다른 경로에 생기는데 직접 옮겨야 윈도우 커맨드에서 pip가 잘 작동함. .ㅠ3ㅠ

    - 설치 시 pip 기본 경로 : `C:\Users\[user_name]\AppData\Local\Programs\Python\Python313\Scripts\`

- **Node.js** 설치
    
    - [🔗 node.js 설치 링크](https://nodejs.org/ko/download)
        
        node.js 설치 후 npm의 경로를 찾아서 사용자 환경 변수 path 설정을 해줘야 한다.
    - 설치 시 npm 기본 경로 : `C:\Users\[user_name]\AppData\Roaming\npm`

- **APPIUM** 설치

    커맨드창을 띄우고 아래 명령어로 appium을 설치해준다.

    최근 APPIUM 업데이트와 함께 커맨드 라인에서 APPIUM INSPECTOR를 설치할 수 있게 되었으므로, APPIUM과 드라이버, inspector를 모두 커맨드창에서 설치해준다!
    ```
    npm install -g appium
    appium driver install uiautomator2
    appium plugin install --source=npm appium-inspector-plugin
    ```


### 원하는 요소의 XPATH 따오기  
---
- **APPIUM INSPECTOR** 실행하기

    ```
    emulator -avd [device_name]
    appium --use-plugins=inspector --allow-cors
    ```
    두 명령어를 시간차를 두고 실행하여 emulator와 appium 서버를 모두 열어준다.
    실행이 완료되면 http://127.0.0.1:4723/inspector 로 이동한다.
    
    JSON Representation에는 아래와 같이 적어준다.
    ``` JSON
    {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "emulator-5554" // 포트 넘버는 알아서 수정
    }
    ```


<div class="img-row">
    <img src="/images/Appium/Appium_1.jpg"  width="32%"/>
    <img src="/images/Appium/Appium_2.jpg"  width="66%"/>
</div>

짜잔... 
휴대전화 화면에서 요소를 클릭하면 우측의 Selected Element에서 내가 원하는 요소의 XPATH를 확인할 수 있다!!


### 자동화 시작하기
---

먼저 고생해서 설치한 에뮬레이터와 appium 서버를 열어줄 차례!

path 설정을 모두 잘 해두었다면 커맨드로 열면 된다.
[device_name]은 안드로이드 스튜디오에서 에뮬레이터 만들 때 정한 Device Name이며, `C:\Users\[user_name]\.android\avd` 경로에서 확인 할 수 있다!

```
emulator -avd [device_name]
appium
```
두 줄의 명령어를 각기 다른 cmd창에 입력해서 열어주면 되는데,
에뮬레이터가 두 개 이상 실행중이라면, 아래 커맨드로 연결·지정해서 열어줄 수도 있다.
(포트 번호는 당연히 알아서 바꾸셔도 됩니당)

```
emulator -avd [device_name] -port 5554 
appium --default-capabilities "{\"udid\": \"emulator-5554\"}" --port 4723
```

이제 Visual Studio Code를 열고 test.py 파일을 하나 만든다.

그런 다음 [🔗 APPIUM INSPECTOR](https://appium.io/docs/en/latest/quickstart/test-py/) Quick start에 나온 CODE를 복붙 후 내게 맞춰 변경해주었다.

``` python
import unittest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    udid = 'emulator-5554', # 에뮬레이터가 하나 켜진 경우 port_num은 5554
    autoGrantPermissions = True,
    autoAcceptAlerts = True,
    noReset = True
)
appium_server_url = 'http://localhost:4723' # 서버 하나만 켜진 경우 4723

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_getinsettings(self):
        keycode_home = 3
        keycode_back = 4
        self.driver.implicitly_wait(1)
        self.driver.press_keycode(keycode_home) # home btn = 3 back btn =  4
        youtube_icon = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="YouTube"]') 
        youtube_icon.click()
        time.sleep(5)
        self.driver.press_keycode(keycode_back) 

if __name__ == '__main__':
    TestAppium.main()
```

이제 테스트 코드를 실행하면 픽셀 홈화면에 당연히 있는.. . 유튜브 앱에 들어갔다 나올것이다. .

이제 이 test 코드를 적당히 입맛에 맞게 변형해서 자신이 원하는 앱에 들어가 원하는 방식으로 자동화 하면 된다.
참고로 capabilities의 appPackage는 잘 작동하지 않는 경우가 많으니 홈화면에 아이콘을 빼두고 홈화면에서 클릭해서 접근하는 방식으로 시작하는 것이 낫다.

### 자주 쓰는 method
---
APPIUM의 기반이 selenium이기 때문에 selenium을 이용한 크롤러를 만들어 본 적 있으면 알겠지만, 몇가지 자주쓰는 함수가 있다.

- 객체 Driver
    - `find_element(by=AppiumBy.XPATH, value="")`
        
        value를 넣는 곳에 XPATH를 넣으면 일치하는 element 주소를 하나 반환한다.
        여러 개 조회되는 경우 가장 첫번째 element 하나만 반환한다.
        이게 싫다면 바로 아래 함수를 사용하면 된다.
        
    - `find_elements(by=AppiumBy.XPATH, value="")`
        
        value를 넣는 곳에 XPATH를 넣으면 일치하는 element 주소를 리스트로 여러개 반환한다.
        ```
        youtube_icon = self.driver.find_elements(by=AppiumBy.XPATH, value='//android widget.TextView[@content-desc="YouTube"]') 
        youtube_icon[0].click()
        ```
        위와 같이 list에서 필요한 요소를 꺼내 쓰면 된다

    - `press_keycode(int)`

        press_keycode는 android의 keycode를 눌러주는 함수인데,
        나는 HOME과 BACK만 사용해서 다른 건 [🔗 ANDROID KEYEVENT](https://developer.android.com/reference/android/view/KeyEvent) 여기서 확인할 수 있다!

    - `implicitly_wait(int)`

        요소가 나타날 때까지 기다리는 시간인데 unit은 sec.
        find_elements 함수의 경우 요소를 다수 찾는 함수이다 보니까 implicit wait 시간만큼 요소가 다 나왔든 그렇지 않든 무조건 기다리게 된다.
        불필요한 시간 낭비가 넘 클 수 있으니 필요한 만큼만 써야한다.

- 객체 element

    find_element 를 이용하여 찾은 요소들 뒤에 붙여 클릭, text 긁어오기 등의 동작을 할 수 있다.

    - click()   
    - get_attribute()

        'content-desc' 등 원하는 속성의 이름을 넣어 가져올 수 있다.
    - text

        method는 아니지만 요소의 text를 긁어온다.


---

자 이제 이 메소드를 예쁘게 잘 조리해서 원하는 기능을 하도록 만들면 된다.
Python 기초가 없었는데. . 이 프로젝트를 통해서 파이썬 기초를 갈고 닦게되었다.
님들도 화이팅!
