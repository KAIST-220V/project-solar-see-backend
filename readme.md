# SOLAR-SEE BACKEND

- [SOLAR-SEE BACKEND](#solar-see-backend)
  - [개요](#개요)
  - [시작하기](#시작하기)
    - [1. 소스 코드 내려받기](#1-소스-코드-내려받기)
    - [2. 가상 환경 설정 및 패키지 설치](#2-가상-환경-설정-및-패키지-설치)
    - [3. 개발 서버 관리하기](#3-개발-서버-관리하기)
      - [`manage.py`](#managepy)
      - [`runserver`](#runserver)
      - [`shell`](#shell)
      - [`makemigrations`, `migrate`](#makemigrations-migrate)
    - [4. 배포하기](#4-배포하기)
      - [Gunicorn 설정하기](#gunicorn-설정하기)
      - [Nginx 설정하기](#nginx-설정하기)
  - [What's Next](#whats-next)

## 개요

`project-solar-see-backend`는 `solar-see`의 API 서버 소스 코드입니다.

## 시작하기

해당 장에서는 백엔드 서버를 서버에 구축하고 배포하는 방법을 소개합니다.

### 1. 소스 코드 내려받기

먼저, 서버 레포지토리를 git을 이용해 클론합니다.

```bash
git clone https://github.com/(username)/project-solar-see-backend.git
cd project-solar-see-backend
```

### 2. 가상 환경 설정 및 패키지 설치

백엔드 동작을 위한 기본 요구 프로그램 버전은 다음과 같습니다.

- python 버전 3.10 이상

Ubuntu의 경우 22.04버전 이후부터 해당 python 버전을 기본으로 사용합니다.

로컬 머신에 필수 패키지를 설치해도 무방하지만, 가상 환경을 설정하는 것을 추천드립니다.
`.gitignore`에 환경 변수 폴더는 `venv`로 저장되어 있습니다.

```bash
python -m venv venv
source venv/bin/activate
```

가상 환경 위에서 `requirements.txt`에 정의된 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

일부 폴더는 `.gitignore` 설정으로 인해 소스 코드에 포함되어 있지 않습니다.
해당 폴더를 새로 생성해줍니다.

```bash
mkdir logs staticfiles media
```

### 3. 개발 서버 관리하기

위의 설정을 모두 마쳤다면 `manage.py`를 사용하여 django의 백엔드 서버를 작동시킬 수 있습니다.

#### `manage.py`

`manage.py`는 django 프로젝트를 실행 및 테스트하기 위한 스크립트입니다.
이 장에서는 주로 사용하는 명령어를 정리합니다.

#### `runserver`

`python manage.py runserver`를 사용하여 개발 서버를 실행할 수 있습니다.
기본 호스트와 포트는 `localhost:8000`입니다.

다른 포트로 설정하고 싶다면 다음과 같이 포트 번호를 지정할 수 있습니다.

```bash
python manage.py runserver 8000
```

호스트 또한 다음과 같이 지정할 수 있습니다.

```bash
python manage.py runserver 0.0.0.0:8000
```

#### `shell`

`python manage.py shell`을 사용하여 django setting이 적용된 shell을 실행할 수 있습니다.
일반적인 python shell과 달리 모델에 접근하거나 데이터베이스를 읽고 쓸 수 있는 점이 편리합니다.

#### `makemigrations`, `migrate`

`python manage.py makemigrations`로 django model의 변경 사항을 저장할 수 있습니다.
해당 변경 내용의 추적을 통해 현재 django model과 실제 데이터가 저장되는 데이터베이스가 동일한 형상을 유지할 수 있도록 합니다.

`makemigrations` 이후에 `python manage.py migrate`로 데이터베이스에 변경 사항을 적용할 수 있습니다.

### 4. 배포하기

solar-see는 `Gunicorn`과 `NginX`를 사용하여 배포하고 있습니다.

#### Gunicorn 설정하기

다음과 같이 gunicorn을 실행할 수 있습니다.

`/home/(username)/project-solar-see-backend/venv/bin/gunicorn`에 gunicorn이 설치되어 있다고 가정합니다.

```bash
/home/(username)/project-solar-see-backend/venv/bin/gunicorn \
--workers 4 \
--bind unix:/home/(username)/project-solar-see-backend/gunicorn.sock \
core.wsgi:application
```

해당 스크립트를 daemon으로 등록하면 편리하게 사용할 수 있습니다.

다음과 같이 시스템 디렉토리에 새 파일을 생성하세요.

```bash
cd /etc/systemd/system
sudo touch solar-see.service
```

생성한 파일에 다음과 같이 스크립트를 작성합니다.

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=(username)
Group=(username)
WorkingDirectory=/home/(username)/project-solar-see-backend
#EnvironmentFile=/home/(username)/project-solar-see-backend/.env
ExecStart=/home/(username)/project-solar-see-backend/venv/bin/gunicorn \
        --workers 4 \
        --bind unix:/home/(username)/project-solar-see-backend/gunicorn.sock \
        core.wsgi:application

[Install]
WantedBy=multi-user.target
```

해당 서비스를 `systemctl`로 관리할 수 있습니다.

- 서비스 시작하기
  ```bash
  sudo systemctl start solar-see.service
  ```
- 서비스 중단하기
  ```bash
  sudo systemctl stop solar-see.service
  ```
- 서비스 재시작하기
  ```bash
  sudo systemctl restart solar-see.service
  ```
- 서비스를 데몬에 등록하기
  ```bash
  sudo systemctl enable solar-see.service
  ```
- 서비스를 데몬에서 제거하기
  ```bash
  sudo systemctl disable solar-see.service
  ```

데몬에 서비스를 등록할 경우, 서버를 재시작하더라도 자동으로 시작되므로 편리합니다.

#### Nginx 설정하기

Nginx를 설정하여 백엔드 서버를 실제로 배포할 수 있습니다.

다음과 같이 nginx를 설치하세요.

```bash
sudo apt install nginx
```

Nginx 설정 파일은 `/etc/nginx/sites-available` 디렉토리에 저장됩니다.

해당 폴더에서 새 설정 파일을 생성하세요.

```bash
cd /etc/nginx/sites-available
sudo touch solar-see
```

생성한 폴더에 다음과 같이 설정을 작성합니다.

```nginx
server {
  listen 80;
  server_name (server domain);

  location /static {
      alias /home/(username)/project-solar-see-backend/staticfiles;
  }

  location /media {
      alias /home/(username)/project-solar-see-backend/media;
  }

  location / {
      include proxy_params;
      proxy_pass http://unix:/home/(username)/project-solar-see-backend/gunicorn.sock;
  }
}
```

실제 nginx가 solar-see의 설정을 이용하기 위해서는 등록 폴더에 추가해야 합니다.
다음과 같이 위에서 생성한 설정 파일을 `sites-enabled` 폴더에 링크해 줍니다.

```bash
cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/solar-see
```

이후 nginx를 재시작하면 모든 설정이 완료됩니다.

```bash
sudo systemctl restart nginx
```

## What's Next

내용은 계속 추가될 예정입니다...
