# [Assignment 2] Wanted-Freshcode-Preonboarding
원티드x위코드 백엔드 프리온보딩 과제2

- 과제 제출 기업정보
  - 기업명 : 프레쉬코드
  - ![프레쉬코드 사이트](https://www.freshcode.me/)
  - ![원티드 채용공고 링크](https://www.wanted.co.kr/wd/34118)
## Members

|이름   |github                   |담당 기능|
|-------|-------------------------|--------------------|
|문승준 |[palza4dev](https://github.com/palza4dev)     | DB Modeling, postman api 작성, 로그인, 상품관리 기능 |
|구본욱 |[qhsdnr0](https://github.com/qhsdnr0)   | DB Modeling, 로그인, 상품관리 기능  |
|김지훈 |[kimfa123](https://github.com/kimfa123) | DB Modeling, 로그인, 상품관리 기능 |
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
> - Deploy : AWS EC2, DOCKER
> - ETC : GIT, GITHUB, POSTMAN

## 모델링
<img width="775" alt="스크린샷 2021-11-05 오후 1 53 41" src="https://user-images.githubusercontent.com/41711271/140467324-cf03a130-4175-4e4c-bf00-e3ce75f132b5.png">

## API
https://documenter.getpostman.com/view/17676214/UVC2H9AU

## 구현 기능

### 로그인
- 데이터베이스에 등록된 유저는 총 2명으로 사용자 1번은 user, 사용자 2번은 admin입니다.
- Request시 Header에 Authorization 키를 체크 한 후에 Authorization 키의 값이 없거나 인증 실패시 Error Handling하였습니다.
- 로그인이 성공적으로 완료되면, user정보와 admin정보를 토큰으로 반환할 때 양방향 해쉬 알고리즘인 'JWT'를 사용해서 응답을 하였습니다.

### 상품관리
- 사용자는 로그인시에(header에 token이 있는 상태) 상품조회만 가능하도록 하였습니다. 
- 관리자는 로그인시에(header에 token이 있는 상태) 상품 추가/수정/삭제가 가능하도록 하였습니다. 
- 상품조회의 경우 query string을 이용한 pagination, Q객체와 __contains를 이용한 상품검색, 카테고리 필터링 등의 기능을 구현하였습니다.

### DOCKER

- 팀원들의 빠른 개발환경 셋팅을 위해서 로컬 개발용과 배포용 docker-compose 파일을 만들어서 적용하였습니다.
- 개발용 환경을 구축했을 시 장점은 팀원들의 개발환경 셋팅시간을 줄여줘서 구현에 더 집중 할 수 있습니다.
- 배포용 환경을 구축했을 시에는 일일이 셋팅을 한다고하면, 아무래도 서버와 로컬간의 OS 같은 환경에 차이로 인해서 시간를 낭비 할 수도 있으며 특히, 배포시마다 이러한 상황이 반복될 수 있다는 것인데, docker를 통해서 이러한 시간낭비를 줄 일 수 있다는 장점이 있습니다.

## API TEST 방법

1. 우측 링크를 클릭해서 postman으로 들어갑니다. 링크
2. 정의된 SERVER_URL이 올바른지 확인 합니다. (18.188.189.173:8000)
3. 정의된 회원가입, 로그인 요청을 이용해서 access_token을 획득합니다.
4. 각 요청에 header 부분에 Authorization 항목에 획득한 access_token을 입력하여 요청을 진행합니다. 회원가입, 로그인을 제외한 요청에는 access_token이 필요합니다.
5. 만약 Send버튼이 비활성화가 될 시 fork를 이용해서 해당 postman project를 복사해서 시도하길 바랍니다. 

## 설치 및 실행 방법

### Local 개발 및 테스트용

1. miniconda를 설치한다. (https://docs.conda.io/en/latest/miniconda.html)
2. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
```
git clone https://github.com/palza4dev/wanted-freshcode-assignment.git
cd wanted-freshcode-assignment
```
3. 가상 환경 생성 후 프로젝트에 사용한 python package를 받는다.
```
conda create -n freshcode python=3.8
conda activate freshcode
pip install -r requirements.txt
```
4. .dockerenv.local_dev 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
```
# .dockerenv.local_dev

DJANGO_SECRECT_KEY='django프로젝트 SECRECT_KEY'
```
5. docker-compose를 통해서 db와 서버를 실행시킨다.
```
docker-compose -f docker-compose-local-dev.yml up
```
6. 만약 백그라운드에서 실행하고 싶을 시 -d 옵션을 추가한다.
```
docker-compose -f docker-compose-local-dev.yml up -d
```

### 배포용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
```
git clone https://github.com/palza4dev/wanted-freshcode-assignment.git
cd wanted-freshcode-assignment
```
2. .dockerenv.deploy 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
```
# .dockerenv.deploy

DJANGO_SECRECT_KEY='django프로젝트 SECRECT_KEY'
DB_PORT=DB포트번호
DB_NAME='DB이름'
```
3. docker-compose를 통해서 db와 서버를 실행시킨다.
```
docker-compose -f docker-compose-deploy.yml up
```
4. 만약 백그라운드에서 실행하고 싶을 시 ```-d``` 옵션을 추가한다.
```
docker-compose -f docker-compose-deploy.yml up -d
```
## 폴더 구조
```bash

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
    
