# How to setup

## Check python version
Open Your terminal

Run `python --version`

It should show `Python 3.10.11`, if not, please install or update python version

## Navigate to desired location
for example:
```
PS C:\Users\User> cd .\Desktop\
PS C:\Users\User\Desktop> cd .\127\
PS C:\Users\User\Desktop\127>
```

## Install Git
https://gitforwindows.org


## Clone the repo
Open your terminal
```
git clone https://github.com/cup-noodlehS/art-gallery-api.git 
```
```
cd art-gallery-api
```

## Install dependencies
### Enable virtual environment
```
venv/scripts/activate
```
it should show something like this `(venv) PS C:\Users\User\Desktop\127>`, there should be a 'venv'

### Install packages
```
pip install requirements.txt
```
### Migrate
```
python manage.py migrate
```
### Run the program
```
python manage.py runserver
```
Please tell me if there are errors on your end
###

## Try django admin to create, read, update, and delete data
Open `http://127.0.0.1:8000/admin/` on your browser

> email: don@gmail.com

> password: 123

### Create admin account (optional)
You could also create your own admin account
```
python manage.py createsuperuser
```

## What to do if there are new changes pushed to the github repository
Navigate to the repository
```
git fetch origin
```
```
git pull
```
please tell me if there are errors with pulling
```
bin manage.py migrate
```

## How to run the program
> let's say you terminated the program and closed the terminal

### Navigate to the repository
For example:
```
PS C:\Users\User> cd .\Desktop\
PS C:\Users\User\Desktop> cd .\127\
PS C:\Users\User\Desktop\127>
```
### Run virtual environment
`venv/scripts/activate`

### Check if there are updtes in github repository
```git fetch origin```

```git status```

It shoud show this if there are no changes:
```
On branch main
Your branch is up to date with 'origin/main'.
```
If not, please do the instructions above this -> **What to do if there are new changes pushed to the github repository**

### Run the program
`python manage.py runserver`