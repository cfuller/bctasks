# Brightcove Task Runner
Task dispatcher for various utilities

### Dependencies
BCTask depends on several frameworks and utilities:
- [Celery](http://www.celeryproject.org "Celery Project")
- [RabbitMQ](https://www.rabbitmq.com/ "RabbitMQ")
- [Redis](http://redis.io "Redis")
- Optional
  - [Flower](https://github.com/mher/flower "Flower"), if you want a nice UI for monitoring Celery tasks
  - [Jobtastic](https://policystat.github.io/jobtastic/ "Jobtastic") - maybe???
 
### Installation (Dev or Local)

1. Download and install RabbitMQ:
    - [Linux](https://www.rabbitmq.com/install-debian.html "Linux")
    - [Mac](https://www.rabbitmq.com/install-standalone-mac.html "Mac")
2. Download and install Redis:
    - Linux: 
    ```sh
    $ apt-get install redis
    ``` 
    - Mac (with Homebrew):
    ```sh
    $ brew install redis
    ```
    - Mac (without Homebrew - requires Xcode dev tools/compiler):
    ```sh
    $ wget http://download.redis.io/releases/redis-3.0.7.tar.gz
    $ tar xzf redis-3.0.7.tar.gz
    $ cd redis-3.0.7
    $ make   
    $ make install
    ```
3. Configure RabbitMQ user, host and permissions

    ```sh
    $ sudo rabbitmqctl add_user myuser mypassword
    $ sudo rabbitmqctl add_vhost myvhost
    $ sudo rabbitmqctl set_user_tags myuser mytag
    $ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
    ```

4. Install python dependencies

    ```sh
    $ pip install celery
    $ pip install redis
    $ pip install flask
    ```
    Optionally, you can also
    ```sh
    $ pip install flower
    $ pip install jobtastic
    ```
5. Create a celeryconfig.py file by copying the celeryconfig.default and updating the appropriate values as instructed in the file
6. Clone github repo and navigate to bctasks directory
7. Run the celery server
```sh
$ celery -A tasks worker --loglevel=info &
```
8. Start the Flask server
```sh
$ cd taskgui
$ python taskgui.py
```
### Running in Production
There are several things you'll want to do to run this setup in a prodcution environment, most importantly, daemonizing Celery and proxying the Flask web app. 
- [Daemonizing Celery](http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html)
- [Setting up a Flask proxy](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/#proxy-setups)
