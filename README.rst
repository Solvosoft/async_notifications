Async notifications
=====================

Email notification with celery and administrative view for send email with delay e.g daily

Features
---------

- Celery integration
- Administrative view 
- Enqueued mail system and instantly send
- Problems notification
- User filter email
- Template system with template context
- Send to User, Group or external email
- Django cms integration (djcms_async_notifications) and standalone.

Installation
=============

#. Install from pip 

    .. code:: bash
    
        $ pip install async_notifications


#. Insert *async_notifications* in your settings *INSTALLED_APPS*
#. It's really important set *CELERY_MODULE* pointing to your project celery file, because it's needed for assing task to the current project, and configure some default celery options

    .. code:: python
 
 		from __future__ import absolute_import
 		   
        CELERY_MODULE = "demo.celery"
        CELERY_TIMEZONE = TIME_ZONE
        CELERY_ACCEPT_CONTENT = ['pickle', 'json']
        
        from celery.schedules import crontab
        
        CELERYBEAT_SCHEDULE = {
            # execute 12:30 pm
            'send_daily_emails': {
                'task': 'async_notifications.tasks.send_daily',
                'schedule': crontab(minute=30, hour=0),
            },
        }

#. Configure your email settings, e.g for development

    .. code:: python
    
        DEFAULT_FROM_EMAIL="mail@example.com"
        EMAIL_HOST="localhost"
        EMAIL_PORT="1025"

#. Run migrations 

    .. code:: bash
    
        $ python manage.py migrate

Runing the project
===================

You need to run 3 subsystems for run this app so you need 3 xterm, for this explanation I will use the demo project

1. Run smtp debug client

    .. code:: bash
    
        $ python -m smtpd -n -c DebuggingServer localhost:1025 

2. Run celery, if you aren't setup celery yet see `celery documentation <http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html>`_.

    .. code:: bash
    
        $ celery -A demo worker -l info -B
        
3. Run django

    .. code:: bash
    
        $ python manage.py runserver
