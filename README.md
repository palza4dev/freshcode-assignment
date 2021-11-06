# [Assignment 2] Wanted-Freshcode-Preonboarding
원티드x위코드 백엔드 프리온보딩 과제2

- 과제 제출 기업정보
  - 기업명 : 프레쉬코드
  - [프레쉬코드 사이트](https://www.freshcode.me/)
  - [원티드 채용공고 링크](https://www.wanted.co.kr/wd/34118)
## Members

|이름   |github                   |담당 기능|
|-------|-------------------------|--------------------|
|문승준 |[palza4dev](https://github.com/palza4dev)     | DB Modeling, postman api 작성, 로그인, 상품관리 기능, unit test |
|구본욱 |[qhsdnr0](https://github.com/qhsdnr0)   | DB Modeling, 로그인, 상품관리 기능, unit test |
|김지훈 |[kimfa123](https://github.com/kimfa123) | DB Modeling, 로그인, 상품관리 기능, unit test |
|이다빈 |[thisisempty](https://github.com/thisisempty)     | 개발 및 배포 환경 설정, README 작성 |
|양가현 |[chrisyang256](https://github.com/chrisyang256)   | 개발 및 배포 환경 설정, README 작성 |
|김주현 |[kjhabc2002](https://github.com/kjhabc2002) | 개발 및 배포 환경 설정, README 작성 |

## 과제 내용
> 아래 요구사항에 맞춰 상품관리 Restfull API를 개발합니다.

### [필수 포함사항]
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현
  - Swagger 대신 Postman 이용시 API 목록을 Export하여 함께 제출해 주세요
- READ.ME 작성
  - 프로젝트 빌드, 자세한 실행 방법 명시 
  - 구현 방법과 이유에 대한 간략한 설명
  - 완료된 시스템이 배포된 서버의 주소
  - Swagger를 통한 API 테스트할때 필요한 상세 방법
  - 해당 과제를 진행하면서 회고 내용 블로그 포스팅

### [개발 요구사항]
- Database 는 RDBMS를 이용합니다.
- 로그인 기능
    - JWT 인증 방식을 구현합니다.
    
## 사용 기술 및 tools
> - Back-End : PYTHON, Django Framework, My SQL
> - Deploy : AWS EC2
> - ETC : GIT, GITHUB, POSTMAN

## 모델링

<img width="775" alt="스크린샷 2021-11-05 오후 1 53 41" src="https://user-images.githubusercontent.com/41711271/140463861-ecbcffd4-d8d5-48a9-81f5-0c622c1798a9.png">


## API 명세
https://documenter.getpostman.com/view/17676214/UVC3j7dg

## 구현 기능

### 로그인
- 데이터베이스에 등록된 유저는 총 2명으로 사용자 1번은 user, 사용자 2번은 admin입니다.
- Request시 Header에 Authorization 키를 체크 한 후에 Authorization 키의 값이 없거나 인증 실패시 Error Handling하였습니다.
- 로그인이 성공적으로 완료되면, user정보와 admin정보를 토큰으로 반환할 때 양방향 해쉬 알고리즘인 'JWT'를 사용해서 응답을 하였습니다.

### 상품관리
- 사용자는 로그인시에(header에 token이 있는 상태) 상품조회만 가능하도록 하였습니다. 
- 관리자는 로그인시에(header에 token이 있는 상태) 상품 추가/수정/삭제가 가능하도록 하였습니다. 
- 상품 조회의 경우 query string을 이용한 pagination, Q객체와 __contains를 이용한 상품검색, 카테고리 필터링 등의 기능을 구현하였습니다.

### AWS 배포 (DOCKER 구현시도)

 - 도커를 통해 개발용 환경과 배포용 환경을 구축하여 팀원들의 개발환경 셋팅시간을 줄여줘서 구현에 더 집중할 수 있게 적용하려고 하였습니다. 
 - 그러나 도커 내부에 환경변수를 세팅하는 과정에서 docker run 수행시 SECRET KEY ERROR를 포함한 알수없는 에러가 발생하였습니다.
 - 팀원들과 다시 도커 컨테이너 생성부터 시작해서 환경변수를 넘겨주는 과정까지 시도해보았으나 같은 현상이 계속 발생하여 결국에는 AWS EC2로 배포하였습니다.
 - 아무래도 도커를 처음 접하다보니 단지 명령만 실행하고 결과만 보여주면 된다는 생각만 했던 것 같습니다. 
 - 이번 기회에 팀원들과 다시 도커에 대해 공부해보고 다음 프로젝트에서는 도커를 통해 배포하도록 하겠습니다.

## API TEST 방법
1. `원티드 프리온보딩 Fresh Code.postman_collection.json` 파일을 Postman으로 import 합니다.
2. 정의된 hostname이 올바른지 확인 합니다. (13.125.45.93)
![스크린샷 2021-11-06 오전 10 33 11](https://user-images.githubusercontent.com/72376931/140593488-85c5d361-d0ef-4f7a-b3c6-d3ac6f928e0f.png)
4. 정의된 로그인 요청을 이용해서 유저와 어드민의 access_token을 획득합니다.
5. 각 요청에 header 부분에 Authorization 항목에 획득한 access_token을 입력하여 요청을 진행합니다.
![스크린샷, 2021-11-06 09-22-48](https://user-images.githubusercontent.com/41711271/140591363-2693c1d2-d482-4fb2-853e-92485b7fe07f.png)


## 폴더 구조
```bash
.
├── README.md
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── docker-compose.yml
├── dockerfile
├── freshcode
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── products
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── decorator.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```
## TIL Blog
 - 문승준 : 
 - 구본욱 : 
 - 김지훈 : 
 - 이다빈 : 
 - 양가현 : 
 - 김주현 : 
 
# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 freshcode에서 출제한 과제를 기반으로 만들었습니다. 
    
