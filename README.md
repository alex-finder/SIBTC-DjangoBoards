# SIBTC-DjangoBoards
Following the Simple Is Better Than Complex Tutorial series about Django.

### Managing the virtual Environment
The following command will create the "venv" folder in your current directory, where all of the dependencies will be installed.
> python -m venv venv

To activate the virtual environment, run the activate script under venv/Scripts folder.

Run `pip list` to print all the currently installed pip packages. Initial packages should be pip and setuptools.

After the virtual environment has been created, you can install the packages manually by running 
>pip install *package_name* 

You can also install all the dependencies using one command
> pip install -r requirements.txt

This will install all of the requirements listed in the requirements.txt file.

To write the currently installed dependencies to a text file, which you can then install using the above `pip install -r requirements.txt`, run the following command:
> pip freeze >> requirements.txt

To deactivate the virtual environment, run the deactivate script under venv/Scripts folder.
