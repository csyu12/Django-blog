# Multi-person-blog-system

> 一个基于Python3.7 + Django 3.0.8 制作的 “多人博客Demo“

------

### IDE

- Pycharm

### DataBase

- MySQL：5.7版

### 依赖环境

- Django：3.0.8
- Python：3.7
- mistune：0.8.4
- mysqlclient：1.4.6
- xadmin（部署：[sshwsfc-xadmin](https://github.com/sshwsfc/xadmin)）


------

### 项目部署（Windows系统）

1. 下载项目

   > 访问[Multi-person-blog-system]( https://github.com/csyu12/Multi-person-blog-system) 下载本项目源码解压

   > 也可以通过配置PyCharm环境直接Git

2. 安装项目依赖

   ```python
   pip install -r requirements.txt
   # 建议创建虚拟环境，在虚拟环境下安装本项目依赖，以免污染本地包
   ```

3. 创建MySQL数据库（根据实际使用的数据库进行配置，不必照本宣科）

   > MySQL数据库中执行：

   ```mysql
   CREATE DATABASE `HLS` CHARSET UTF8;
   ```

   > 在`HLSWebsit/setting.py` 修改数据库配置，如下所示：

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'HOST': 'localhost',
           'PORT': '3306',
           'NAME': 'PLS',
           'USER': 'root',
           'PASSWORD': '123456',
       }
   }
   ```

   > 在终端下执行:

   ```python
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

4. 创建后台管理员账户

   ```python
   python3 manage.py createsuperuser
   # 按要求输入用户名、邮箱（格式要合法）、密码
   ```

5. 运行服务器

   > 在终端中输入

   ```python
   python3 manage.py runserver
   #在浏览器打开 http://127.0.0.1:8000/ 即可访问项目主页
   ```

   > 也可以运行manage.py文件，修改配置，如下图。后续只需要运行manage.py即可

     ![Image text](./README_IMG/3.png)
     ![Image text](./README_IMG/manage.jpg)

6. 进入后台

   > 在浏览器输入`http://127.0.0.1:8000/admin`，使用第5步创建的超级管理员账户进行登录

   > 注：建议使用Django后台添加测试数据，比较方便