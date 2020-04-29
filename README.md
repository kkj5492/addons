# kkj5492 Add-on: RS485 To MQTT 

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

## About
PYTHON PROJECT TEST

## Version : 1.0.0
- 2020-04-29 테스트 시작

## Installation

1. 홈어시스턴트의 Hass.io > ADD-ON STORE에서 Add new repository by URL에 https://github.com/kkj5492/addons 를 입력한 다음 ADD 버튼을 누릅니다.
2. ADD-ON STORE 페이지 하단에서 "RS485 To MQTT" 클릭합니다.
3. "INSTALL" 버튼을 누르면 애드온이 설치됩니다. 최대 약 10분 정도 소요. 
4. INSTALL 버튼위에 설치 애니메이션이 동작하는데 이것이 멈추더라도 REBUILD, START 버튼이 나타나지 않는 경우가 있습니다.
5. 이 애드온은 이미지를 내려받는 것이 아니라 직접 여러분의 Hassio에서 이미지를 만듭니다. 따라서 컴퓨터성능과 인터넷 속도에 따라서 시간이 좀 걸립니다. 
6. INSTALL 버튼을 누른다음 설치 애니메이션이 실행되면 제대로 설치중인 것입니다. INSTALL을 여러번 누르지 마시고 기다리다 지치면 브라우저 페이지를 리프리시 하세요. 
7. 애드온 페이지에서 Config을 본인의 환경에 맞게 수정합니다.
8. "START" 버튼으로 애드온을 실행합니다.

만일 rs485.py 파일을 수정하시려면 한번 실행한 후 애드온을 Stop 하시고 share/ 폴더에 있는 파일을 알맞게 수정하신 다음 애드온을 Start 하시면 이후부터는 수정된 파일을 적용합니다.

## Configuration

Add-on configuration:

```yaml
RS485:
  type: Serial
Serial:
  port1: /dev/ttyUSB0
SerialDevice:
  port1: kocom
MQTT:
  anonymous: false
  server: 192.168.x.x
  username: id
  password: pw

### Option: `RS485` (required)
```yaml
type: Serial                    // Serial 혹은 Socket
```
### Option: `Serial` (required)
```yaml
port1: /dev/ttyUSB0        // serial 쓸 경우 (월패드 혹은 그렉스)의 장치경로 작성
```
### Option `MQTT` (required)
```yaml
anonymous: false           // MQTT 설정
server: 192.168.x.xx         // MQTT 서버
username: id                 // MQTT ID
password: pw                // MQTT PW
```