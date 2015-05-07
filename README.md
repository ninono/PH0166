Web-based automatic assessment for comprehension questions in PSLE Chinese
===========================================================================

Installation
-----------------
1. Make sure Python 2.x is installed
2. Install [pip][http://pip.readthedocs.org/en/latest/installing.html]
3. Install [Django][https://www.djangoproject.com/download/]: version 1.7.5 is used in development
4. Install mysql
5. Install mysql-python : `pip install mysql-python`
6. `pip install django-extensions`
7. Install [django-nested-inline][https://github.com/s-block/django-nested-inline]: `pip install django-nested-inline`
8. Install [django-smart-selects][ https://github.com/digi604/django-smart-selects.git] : already included 
9. Install [django-wysiwyg-redactor][https://github.com/douglasmiranda/django-wysiwyg-redactor.git]: `pip install django-wysiwyg-redactor`
10. Install jieba: `pip install jieba`
11. Install gensim: `pip install gensim`
12. Install django-suit: `pip install django-suit`
13. Install djangoajax: `pip install djangoajax`

Database setup
--------------------
1. Create database and user according to `settings.py`
2. In `pslech/` folder, run:
    `python db_manage reset`
    to restore database

To run the server
---------------------
1. In `LanguageTool-2.9-SNAPSHOT` folder, run:
    `./startserver.sh`
    to run syntex checking server
2. In `pslech` folder, run:
    `python manage.py runserver`
    
