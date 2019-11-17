#=======
**Whatsapp Scraping**
#=======

## **Technologies**

### **Server-side**
* [Python 3.5+](http://www.python.org): The language of choice.


#### **Other assorted packages**

From inside the repository, run:

    pip install -r requirements/default.txt
    
    python manage.py db migrate
    
    python manage.py db upgrade

    python manage.py cron -n Whatsapp
    
    python manage.py runserver
