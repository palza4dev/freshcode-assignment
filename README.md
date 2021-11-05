# [Assignment 2] Wanted-Freshcode-Preonboarding
원티드x위코드 백엔드 프리온보딩 과제2

- 과제 제출 기업정보
  - 기업명 : 프레쉬코드
  - ![프레쉬코드 사이트](https://www.freshcode.me/)
  - ![원티드 채용공고 링크](https://docs.google.com/forms/d/e/1FAIpQLSd35J7eof4YGkPLMD_6hwj6f52JxMgOfomN_rBM6WUCeU8g-g/viewform)
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
- 상품조회의 경우 query string을 이용한 pagination, 상품검색, Q객체를 이용한 카테고리 필터링, 정렬 등의 기능을 구현하였습니다.

### DOCKER

## API TEST 방법

## 설치 및 실행 방법

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
    
