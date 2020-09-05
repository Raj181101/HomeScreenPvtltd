step1 - Download Python 3+
step2 - Install virtualenv (pip install virtualenv)
step3 - activate virtualenv
        a)virtualenv venv
        b)cd venv
        c)cd Scripts
        d)activate
        follow above commands for activating virtualenv

step4 - install modules from requirements.text file(pip install -r requirements.txt)
step5 - migrate models(python manage.py migrate)
step6 - runserver(python manage.py runserver)

Note:
   Api urls are mentioned in functions doc ,u can test that apis in postman