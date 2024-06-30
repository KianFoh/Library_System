Project code can also be get from https://github.com/KianFoh/Library_System

COMMANDS
These command can only be run in library_System/library_system_backed

Prerequisites:
1) Install PostgreSQL databases using default port, configure django to use the database in library_System/library_system_backed/library_system_backend/setting.py under

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123tkf',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

2) Install rabbitMQ 

Steps to setup:

Step 1: Install Chocolatey on Powershell with Administrator 
run Get-ExecutionPolicy
if restricted run Set-ExecutionPolicy Bypass -Scope Process
then run Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

Step 2: Install rabbitmq with Chocolatey 
run choco install rabbitmq
during installation if got ask for premission yes to all

Step 3: Set Environmental Variable
The rabbitmq should be installed in programfiles 

Step 4: Copy the .erlang.cookie from C:\Windows\System32\config\systemprofile\AppData to replace the .erlang.cookie in C:\Users\user 

Step 5: Disable consumer timeout for Rabbitmq
copy this
[
  {rabbit, [
    {consumer_timeout, undefined}
  ]}
].
put it in C:\Windows\User\user\AppData\Roaming\RabbitMQ\advanced.conf

Step 6: Restart the rabbitmq from Services, run Rabbitmqctl status to check if rabbitmq is running

3) Install all the libraries in the Packages.txt using pip install, recommended to install librarier in a virtual environment


Django
1) Start django server: python manage.py runserver
2) Update changes to existing database: python manage.py makemigrations
3) Update new tables on the database: python manage.py migrate

Celery
1) Start Celery worker: celery -A library_system_backend worker --loglevel=info  -P solo 
2) Start Celery beat to send periodic task: celery -A library_system_backend beat --loglevel=info
