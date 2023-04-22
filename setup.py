import setuptools
setuptools.setup(
    # Includes all other files that are within your project folder 
    include_package_data=True,
  
    # Name of your Package
    name='DnD-bro',
 
    # Project Version
    version='1.0',
     
    # Description of your Package
    description='Check if your number is odd or even',
     
    # Website for your Project or Github repo
    url="https://github.com/myGitHubRepo",
 
    # Name of the Creator
    author='Author Name',
 
    # Creator's mail address
    author_email='authorname@gmail.com',
     
    # Projects you want to include in your Package
    packages=setuptools.find_packages (),
    
    # Dependencies/Other modules required for your package to work
    install_requires=['telebot', 'python-dotenv','setuptools','psycopg2'],
 
    # Detailed description of your package
    #long_description='This module provides one function that determines whether the provided number is either odd, even, or neither (in the cases of 0)',
 
    # Format of your Detailed Description
    #long_description_content_type="text/markdown",
      
    # Classifiers allow your Package to be categorized based on functionality
    #classifiers = [
    #    "Programming Language :: Python :: 3",
    #     "Operating System :: OS Independent",
    #],

    entry_points = { 'console_scripts': ['myCommand=myCommand.command_line:main'], },
    #package_data={'exampleproject': ['data/schema.json']}

)
