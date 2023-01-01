# Introduction
This project aims to provide an easy-to-use set of APIs to perform classic CRUD operations on a music library database: 

1) You can add a new CD in the database.
2) You can retrieve all/specific CDs from the database.
3) You can update existing CDs that are stored in the database.
4) You can delete CDs from the database.

You can use these api, for instance, to develop a website that allow people to publish and sell their CDs.
The "main character" of our project is the CD model. A cd model has the following fields:
- name -> this field stores the cd title.
- artist -> this field stores the name of the artist who created the CD.
- record_company -> this field stores the name of the record company that has released the CD.
- genre -> this field tells you which genre the CD belongs to.
- ean_code -> this field stores the ean code of the CD.
- published_by -> this field tells you which user published this CD into the database.
- price -> this field stores the price of the CD.
- created_at -> the first time a cd is added to the database, the exact moment of publication is stored in this field.
- updated_at -> every time a cd is updated, this field stores the exact moment of update.

We developed 2 applications that consume our API:

1) musics_frontend: this application has been developed using Angular, a development platform built on TypeScript. 
To import the application on your laptop, just clone the repository at https://github.com/ssd-sbm/musics_frontend.git 
and follow the instructions included in the readme file.

2) musics_tui: a terminal based application developed in python. 
If you have installed pycharm on your laptop is quite simple to import the application, 
just clone the repository at https://github.com/ssd-sbm/musics_tui.git
and follow the same steps described in the **quick start** section of this documentation.

# Prerequisite
To use our API you should know django and django rest framework (the basics), you can find a lot of information about the topic in the official documentation
at https://www.django-rest-framework.org , also check the secure software design course webpage at https://sites.google.com/unical.it/inf-ssd.

# Quick start
If you have installed pycharm on your laptop is quite simple to import this project on your laptop, just follow these STEPS:
1) Create a folder that will contain the project.
2) Clone this repository in the folder created at **step 1**.
3) Open the cloned project with pycharm.
4) Make sure to use the right python interpreter in the existing **"music_api"** run configuration. If you don't have one, just create it.
5) Open the **requirements.txt** file.
6) click on **"install all required packages"**.
7) run the project.
8) Go at http://127.0.0.1:8000/api/v1/musics/ and enjoy our API.




