# Installation Notes

## Introduction and Notes.
The following document prescribes commands to install all “Country Node” applications in the HVPA tool chain on a single server.  Along the way you will setup administrator accounts and passwords for a number of items. We recommend saving those usernames and passwords in a root-read-only file /etc/hvp.secrets to not lose them.  This document cannot be executed as a script at this stage and requires manual intervention. However, most commands are
copy-paste-able to the terminal blocks at a time.

Assumes debian based linux distribution


## Get software dependencies
You are about the install the tools and libraries required to build the node

```
sudo apt-get install git
sudo apt-get install python-pip
sudo apt-get install apache2 libapache2-mod-wsgi
```

## Get source code
You are about to install the HVP tool chain in /var/HVP as root

```
sudo su
cd /var
mkdir HVP
cd HVP
git clone https://bt_alanlo@bitbucket.org/hvpa/portal.git Portal
git clone https://bt_alanlo@bitbucket.org/hvpa/siteconf.git SiteConf
git clone https://bt_alanlo@bitbucket.org/hvpa/variantimporter.git VariantImporter
git clone https://bt_alanlo@bitbucket.org/hvpa/variantindexer.git VariantIndexer
git clone https://bt_alanlo@bitbucket.org/hvpa/orghashgenerator.git OrgHashGenerator
```
Add the HGVS_Parser library to the Portal
```
pushd Portal/search/hgvs_parser
git clone https://bt_alanlo@bitbucket.org/hvpa/hgvs_nomenclatureparser.git .
popd
```
Add the HGVS_Parser library to the VariantImporter
```
pushd VariantImporter/Utils/HGVS
git clone https://bt_alanlo@bitbucket.org/hvpa/hgvs_nomenclatureparser.git .
popd
```

## Install and Setup databases

```
sudo apt-get install mysql-server
```
You will be asked to enter a password for 'root' user
Please make note of it in /etc/hvp.secrets
```
sudo mysql_install_db
sudo /usr/bin/mysql_secure_installation
```
You will be asked questions after password entry
Answer the following:
> Remove anonymous users? [Y/n] y                                           

> Disallow root login remotely? [Y/n] y

> Remove test database and access to it? [Y/n] y

> Reload privilege tables now? [Y/n] y
```
sudo apt-get install python-dev libmysqlclient-dev
```
Make databases for the Node
```
mysql -u root -p
```
NOTE: In theory you can host the Labs database on different server/credentials for extra security
But for the purposes of these instructions we will combine them in the one database
```
mysql> CREATE DATABASE Portal;
mysql> CREATE DATABASE SiteConf;
```
Make a db user for the portal. Please note the username and password for later
```
mysql> CREATE USER 'portalproxy'@'localhost' IDENTIFIED BY 'pr0xyPASS';
mysql> GRANT ALL PRIVILEGES ON Portal.* to 'portalproxy'@'localhost';
mysql> GRANT ALL PRIVILEGES ON SiteConf.* to 'portalproxy'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> exit
```
Test by
```
mysql -u portalproxy -p Portal
```

## Setup django and dependencies under virtual env for Apache/WSGI to run

`sudo pip install virtualenv

`cd HVP/
`virtualenv hvpenv
`source hvpenv/bin/activate

`pip install django==1.4.2
`pip install django-taggit==0.12.2
`pip install PyJWT
`pip install MySQL-python
`pip install tox

For SiteConf
`pip install django-tastypie==0.9.14

For VariantIndexer
`pip install suds
For VariantImporter
`pip install pyCrypto
`pip install biopython


Setup portal
`cd Portal/
`tox

Edit settings.py with preferred editor. e.g. vim settings.py
1) Under DATABASES, ‘default’ ensure:
   ’NAME’ (of database), 
   ’USER’,
   and ‘PASSWORD’
are set to connect to Portal database
2) Under TEMPLATE_DIR
add ‘/var/HVP/hvpenv/django/contrib/admin/templates’ to the list


Create database schemas using DJANGO
`python manage.py syncdb
You will be asked to make django superuser
Answer the following:
> Would you like to create one now? (yes/no): yes
> Username (leave blank to use 'alan'): admin
> E-mail address: admin@example.com
> Password: 
> Password (again): 
Please make note of it in /etc/hvp.secrets

Load initial data. You may want to alter the data first depending on your node’s needs
`python manage.py loaddata hvp/fixtures/gene.json 
`python manage.py loaddata hvp/fixtures/ref.json 
`python manage.py loaddata hvp/fixtures/hg_build.json 

Edit Portal/apache/django.wsgi
Insert value for portal_site_path variable to the parent directory of Portal. e.g. /var/HVP/



## Setup apache

There is an example apache configuration file in the Portal repository
The following instructions help guide how to use it
`cp Portal/apache/example-apache.conf /etc/apache2/sites-available/hvpportal.conf
`cd /etc/apache2/sites-enabled
`ln -s ../sites-available/hvpportal.conf 

Review the hvpportal.conf file for location differences if you have used different paths
Review the hvpportal.conf file for apache changes required if the server you are using has existing apache services


Enable proxy pass for WebReceiver to be hosted on the same server
`cd /etc/apache2/mods-enabled
`ln -s ../mods-available/proxy.conf 
`ln -s ../mods-available/proxy_connect.load 
`ln -s ../mods-available/proxy_ftp.conf 
`ln -s ../mods-available/proxy_ftp.load 
`ln -s ../mods-available/proxy_http.load 
`ln -s ../mods-available/proxy.load

Test the config to see if there are any errors
`apachectl configtest

Restart Apache for changes to take affect
`apachectl restart



## Setup OrgHashGenerator
This is a simple tool for the operator to create new Organisation Hashes

Edit /var/HVP/OrgHashGenerator/OrgHashGenerator.py
Look for the variable ‘path’ in the first few lines of the file. Set this to /var/HVP


## Setup VariantIndexer
These are applications that support the portal. They are executed routinely on the server

Edit /var/HVP/VariantIndexer/cDNAIndexer.py
Look for the variable ‘path’ in the first few lines of the file. Set this to /var/HVP

Edit /var/HVP/VariantIndexer/GenomicMutalyzer.py
Look for the variable ‘path’ in the first few lines of the file. Set this to /var/HVP

You can setup a cron job to run these commands on a periodic basis. 
Review the frequency and path locations of VariantIndexer/crontab-example.txt and change as needed
Copy the contents of VariantIndexer/crontab-example.txt
`crontab -e
Paste the contents into the crontab, save and exit


## Setup Variant Importer
There are two applications here:
   WebReceiver.py - a web service which waits for incoming submissions
   VariantImporter.py - an application executed nightly to process the submissions from the previous day

`cd /var/HVP/VariantImporter/
`mkdir -p temp output diff complete keys


Generate the node's public/private key
`pushd Utils/
`python HVP_Encryption.py -c --keyname=hvp
This generates a public private key pair.
   The private one in the main VariantImporter folder
   The public one in the VariantImporter/keys folder. This is freely given to the labs
`mv hvp.private ../
`mv hvp.public ../keys/
`popd

Edit WebReceive.py.cfg
There shouldn’t be anything here to change if you followed the above instructions
If you gave your key a different name, make sure the ‘private_key’ variable is updated


Edit Importer.py.cfg
Ensure the ‘username’, ‘password’, and ‘database’ values are set to the Portal database



## Site conf
This is a service the VariantExporters communicate with for settings and configurations
It allows a HVP operator to support some of the configurations of the system at the remote sites

`cd /var/HVP/SiteConf/

Edit SiteConf/settings.py
Under DATABASES, ‘default’ ensure:
   ’NAME’ (of database), 
   ’USER’,
   and ‘PASSWORD’
are set to connect to SiteConf database

Create the database schema
`python manage.py syncdb
You will be asked to make django superuser
Answer the following:
> Would you like to create one now? (yes/no): yes
> Username (leave blank to use 'alan'): siteconf
> E-mail address: admin@example.com
> Password: 
> Password (again): 
Please make note of it in /etc/hvp.secrets

Create an API key that allows VariantExporters to speak to SiteConf
`mysql -u portalproxy -p SiteConf
`mysql> INSERT INTO tastypie_apikey (user_id, `key`) VALUES (1,'3020577c5bd111b889bb5cdd0cda80aee376fd2c');
You can use a different key value if you like



## Adding the first admin user for HVP Portal
For the purposes of approving users and requests, there should be at least one user appointed with the responsibility of
‘HVP_Admin’. This is likely to be the first user you add to the system. As such, it requires special instructions to do so
1) Go to the main node site http://(server address)
   You should see the front page for the portal.
2) Sign up for an account
   Fill in the details for this administrator user
3) Go to the admin page for the site http://(server address)/admin
   Log in with the django admin user made previously when setting up the database of the portal. 
4) Add a Laboratory Group for the node. Click +Add under HVP > Laboratory groups
   Fill in details for the HVP Node you are setting up. Save and return to home
5) Edit the user profile for the user you registered before. Click on User profiles under HVP > User profiles
   Set ‘Is HVP Admin’ to ‘Yes’
   Set ‘AccessStatus’ to ‘Application Granted’
   Set ‘LaboratoryGroup’ to the group you have just added in #4
   Set ‘Joomla User ID’ to 1 (deprecated)

Using this user, you can now approve future user requests after logging into the portal under Pending applications


## Adding a Site
A Site is an individual laboratory group with their own instance of the VariantExporter who will be submitting data.

Generate a new hash code for this organisation. You can use anything you like as long as you stick to the same generator.
We have implemented a simple generator for this purpose.
`cd OrgHashGenerator
`python OrgHashGenerator
Copy it the result. You will need to reference this multiple times


Use the DJANGO administrator to assist adding new data you will need to use both the Portal’s administrator and the SiteConf to complete this process.

Start with Portal administrator
Using a web browser, go to your portal’s URL with /admin/ at the end of the url
E.g. http://xx.xx.xx.xx/admin/

Login with your administrator user name and password for the Portal site
Under Hvp > Organisations, click ‘+Add’, and paste the hash code in the text box. Click ‘Save’
Click Home under breadcrumbs to return
Under Hvp > Lab details, click ‘+Add’
> Here we enter the details of this organisation. You will need to paste the Hash code here too
Click Home under breadcrumbs to return
Under Hvp > Lab contacts, click ‘+add’
> Here we enter the person who is the main contact for that site

You can also use this administrator to update details for these labs as they change.



Next, we set the SiteConf
Using a web browser, go to your portal’s URL with /siteconf/admin/ at the end of the url
E.g. http://xx.xx.xx.xx/siteconf/admin/

Login with your administrator user name and password for the SiteConf site
Under Orgsite > Org sites, click ‘+Add’
> Here we enter the hash code again and the ID of the Organisation ID from Portal
Click Home under breadcrumbs to return
Under Upload > Uploads, click ‘+Add’
> Here we initialise the details for a plugin the lab will receive from the exporter. A brief explanation of the fields are as
follows:
>   Name: Name of this plugin for this site
>   DataSourceType: The type of the plugin. Refer to the Exporter codebase
>   DataSourceName: This can be left blank for the initial setup. It is the location of any file/folder it is expecting to load from locally
>   Databasename: Equivalent of DataSourceName for database connections
>   UserName: A default name of uploaders submitting data for this plugin
>   Password: A Secret used to encrypt information with. It will be compiled into the Exporter for this site in the Configuration.xml
>   Plugin: The name of the .dll (locally)
>   RefMapper: The name of the local xml file it will use to map local terminology to HVP
>   OrgSite: The site for this plugin


An example URL to access a value assuming the above values have been used:
http://localhost:8000/api/v1/orgsite/1/?OrgHashCode=123_test&username=siteconf&api_key=3020577c5bd111b889bb5cdd0cda80aee376fd2c



