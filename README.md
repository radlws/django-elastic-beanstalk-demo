# README #

Download this using archive and configure as a starting base for new projects. Follow the README in the site directory for details on setting up a new project using this template.

### What is this repository for? ###

* A starting template for django projects, now setup for Django 1.7
* Django 1.7
* Optimized for plugging in Grappelli and Sorl Thumbnail


See the README in the module dir for more details.

### Tested Platforms ###
* RHEL Amazon Linux and Elastic Beanstalk, new settings file and requirements.txt file are now included, they are only needed for beanstalk deploys.
* Ubuntu 14.04LTS, Ubuntu 12.04LTS running in AWS EC2 and Rackspace

### AWS Elastic Beanstalk ###
* When deploying to elastic beanstalk, make sure to rename the settings_beanstalk.py.ex file to settings_prod.py and update it accordingly. Some of the options cannot be added till they are setup and configured, i.e. RDS

* Update the wsgi.py file as described in the comments of the file.
* Ensure the requirements.txt file at the root of the project makes sense in terms of versions to use.
* Uncomment in fabfile.py the parts required for Beanstalk, namely for aws-release-tasks to work
* Install python boto, django-storages, and aws-release-tasks (our repo) to project lib folder.
* Assuming that EB CLI is setup, run eb init and follow the steps. When creating a new environment later, use git aws.config
* Create the .ebextensions app settings using the template, by replacing the project name. Some of the geodjango specific repos can be optionally omitted. The only instance that had no issues with geodjango out of the box is Instance AMI ID: ami-35792c5c , use that, otherwise a more up to date x64 AWS Linux Python 2.7 instance can be used. This can auto-created using aws-release-tasks command generate_app_config
* Ensure you switch over to the right credential files, aws-release-tasks command: sw_creds
* Follow the company beanstalk deployment documentation for further details on this.

### Issues ###
* A starting the project, the sites data should be set. A default migration should be created that populates the Site framework data.
* Export json / csv should be added as a master task to the project