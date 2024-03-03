### 받아오는 데이터
---
![image](https://github.com/SsackTeun/NWP-Absence-ExcelDownloadAPI/assets/24308378/5183bb08-1c4e-48fd-8c78-04f032696b5d)

### 사용방법
---
- #### main.py 로 실행
- #### main.py 는 플라스크 서버를 실행함
- #### main.py 와 동일한 경로에 credential.txt 가 필요함
  ![image](https://github.com/SsackTeun/NWP-Absence-ExcelDownloadAPI/assets/24308378/3e38d5c5-fd21-4814-9611-e5bdcd75e619)

### 파일 생성 credential.txt
---
  - username=로그인 아이디
  - password=로그인 패스워드

### Request 방법
---
  ![image](https://github.com/SsackTeun/NWP-Absence-ExcelDownloadAPI/assets/24308378/a5496d97-8a8f-4888-86d6-c399239808d4)

### 요청 형식
---
* http://flaskserverurl:port/download?date={yyyymm}
* 예시) http://localhost:5000/download?date=202402

### 결과
---
* 브라우저에 url 로 요청을 하면, 엑셀 파일이 내려받아짐

![image](https://github.com/SsackTeun/NWP-Absence-ExcelDownloadAPI/assets/24308378/24ba8c06-471c-4705-ae1d-669f259d0259)

* 요청하면, flask 서버에서는 해당연도와 해당월의 첫일,마지막일을 계산하여 요청을 보냄

![image](https://github.com/SsackTeun/NWP-Absence-ExcelDownloadAPI/assets/24308378/a64b4e48-c29b-4c98-9b34-1785e1b6e7ad)
