# Description

This is a project related to the following course: [fastapi-the-complete-course](https://www.udemy.com/course/fastapi-the-complete-course)  

### Project Description

Creating and enhancing books with CRUD operations.

### Python virtual environments

A virtual environment is a Python environment that is isolated from those    
in other Python environments.

Get pip version:
> python -m pip --version

### Creating a new virtual environment and activating it

> pip list # list all dependencies in the virtual env    
> python -m venv fastapienv # creating the virtual environment    
> source fastapienv/bin/activate # activate the virtual environment    
> deactivate # simply exit the virtual environment

### Starting our server

> uvicorn books:app --reload
or
> fastapi run <filename>.py # need fastapi[standard] installed