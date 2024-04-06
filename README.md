# project name : payment_mall

__부제: 결제 기능을 추가한 쇼핑몰__

장고 프로젝트
쇼핑몰 개발자 결제 시스템 추가
아임 포트를 활용한 쇼핑몰 및 결제 시스템 프로그램

---

## use
jquery
bootstrap5
django
sqllite

## 환경세팅

### 아나콘다 세팅
 - conda env list (가상환경 리스트)
 - conda create -n payment python=3.11.4
 - conda activate payment
### 설치해야할것 설치 
 - pip install -r requirements.txt
 - (linux의 경우) 패키지 설치 안 될 시 수동으로 설치
  
### 장고 세팅
 - python manage.py makemigrations
 - python manage.py migrate
 - python manage.py createsuperuser
 - python manage.py runserver

db 관리자에 등록 admin.py


