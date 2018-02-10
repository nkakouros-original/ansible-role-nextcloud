Ansible Role: Nextcloud
=========

Installs and upgrades Nextcloud and apps. It only does that, it does not install a web server, a db server, etc.

Features
--------

- installs, updates and configures Nextcloud core
- installs, updates and configures Nextcloud apps available on the app store
- creates and updates users

Requirements
------------

Ansible >= 2.4

While there are a bunch of other roles around to install Nextcloud, I did not found them useful as they try to do everything in one role, ie setup Apache, then MySQL, then install Nextcloud, etc. This might be useful for users who want to have a Nextcloud instance running as fast as possible. However, I find the approach too limiting as there are many assumptions taking place.

This role does not care where you install Nextcloud. It only downloads, installs and configures Nextcloud itself. Its aim is to be used in a modular way alongside other roles. (Or at least it tries to make no assumptions. If you find any or cannot install nextcloud due to missing functionality, please open an issue or a PR. Currently it has been tested only on Ubuntu 16.04).

See the [Example playbook](#example-playbook) on how a complete playbook that uses 3rd-party roles might look like.

Role Variables
--------------

(copied from defaults/main.yml)

```yaml
nextcloud_enable: yes
# Set this to 'no' to completely disable the role

nextcloud_version: 13
# The major nextcloud version to install. You can use this to upgrade to a new
# major version as well. Even if you set 'nextcloud_download_url' manually (see
# next option), 'nextcloud_version' should be set as it is also used to
# correctly install the apps.

nextcloud_download_url: >-
  {%- if nextcloud_version != '' -%}
    https://download.nextcloud.com/server/releases/latest-{{ nextcloud_version }}.zip
  {%- else -%}
    https://download.nextcloud.com/server/releases/latest.zip
  {%- endif -%}

# The url to download nextcloud from. Currently only the latest stable version
# is supported.

nextcloud_installation_dir: '/var/www/html/nextcloud/'
# Where to extract nextcloud files

nextcloud_file_owner: 'www-data'
# The user that will own nextcloud files.

nextcloud_db_backend: 'mysql'
# The database server that will be used. It should be already installed and
# the database should already exist. For 'mariadb', set this to 'mysql'.

nextcloud_db_name: 'nextcloud'
# The name of the database nextcloud will use. It should already exist on the
# system.

nextcloud_db_user: 'nextcloud'
# The database user that nextcloud will use to access the database. The user
# should already exist in the database backend (together with their password).

nextcloud_db_pass: ''
# The database user's password. This variable should not be empty.

nextcloud_db_host: localhost
# The database host

nextcloud_db_port: 3306
# The port the db server listens on

nextcloud_data_dir: "{{ nextcloud_installation_dir }}/data"
# Path to nextcloud user data directory

nextcloud_admin_user: admin
# The name of the admin user

nextcloud_admin_pass: ''
# The password of the admin user. This variable should not be empty.

nextcloud_enable_pretty_urls: yes
# Set to yes to enable urls of the form https://example.org/calendar replacing
# https://example.org/nextcloud/index.php/s/Sv1b7krAUqmF8QQ.

nextcloud_urls:
  - https://localhost:80/folder

nextcloud_apps: []
# The ansible apps to install and enable
# It is a list of hashes. Eg
#
# nextcloud_apps:
#   - name: calendar
#     version: 1.5.7
#
# If 'version' is not given, then the latest version available for the installed
# nextcloud version will be installed and updated on each plabook run.

nextcloud_upgrade_always: false
# Set this to true to always run Nextcloud's upgrade command, regardless of
# whether there is sth to be upgraded or not.

nextcloud_users: []
# The ansible users to create, other than the admin.
# It is a list of hashes. Eg
#
# nextcloud_users:
#   - name: alice
#     pass: superstrongnot
#     resetpassword: yes  # to reset the passsword every time the playbook is run
#     display_name: Alice B. Charlie
#     settings:
#       - firstrunwizard:
#           show: 0
#       - calendar:
#           showWeekNr: 'yes'
#
# App and core configuration happens per user. To find out what config options are
# available, there are two options. The best is to make the changes manually in
# the admin interface and then check the oc_preferences and oc_appconfig tables
# in your nextcloud database to see what changed and get the names from there.
# The second option is to use your browsers inspection tool to inspect the
# form element in the nextcloud admin interface that you want to change. Try to
# find the ng-model attribute of the <input> tag. It should be sth like 
# 'settingsShowWeekNr'. The config name in this case will be 'showWeekNr'.

```

Example Playbook
----------------

Here is a complete example of how to use this role in conjuction with other roles in order to get a complete server environment running Nextcloud. In this example, I use the well known [geerlingguy](https://github.com/geerlingguy/) roles to install apache, mysql and php, alongside Nextcloud, on Ubuntu 16.04.

```yaml
- hosts: server
  any_errors_fatal: true
  become: yes
  roles:
    - ansible-role-php
    - ansible-role-mysql
    - ansible-role-apache
    - ansible-role-nextcloud
  vars:
    mysql_root_password_update: no
    mysql_databases:
    - name: "nextcloud"
    mysql_users:
    - name: "nextcloud"
      password: "secret_password"
      priv: "nextcloud.*:ALL"
    mysql_packages:
    - mariadb-client
    - mariadb-server
    - python-mysqldb
    php_packages_extra:
    - libapache2-mod-php7.0
    - php-zip
    - php-imap
    - php-gd
    - php-json
    - php-xml
    - php-mbstring
    - php-mysql
    - php-curl
    - php-bz2
    - php-intl
    - php-mcrypt
    - php-gmp
    - php-apcu
    - php-imagick
    apache_remove_default_vhost: true
    apache_vhosts:
    - servername: "nextcloud.example.com"
      documentroot: "/var/www/html/nextcloud"
      extra_parameters: |
        SetEnv HOME /var/www/html/nextcloud
        SetEnv HTTP_HOME /var/www/html/nextcloud
    apache_mods_enabled:
    - rewrite.load
    - php7.0.load
    - headers.load
    - env.load
    - dir.load
    - mime.load
    nextcloud_download_url: https://download.nextcloud.com/server/prereleases/nextcloud-13.0.0RC2.zip
    nextcloud_db_name: "{{ mysql_databases[0].name }}"
    nextcloud_db_user: "{{ mysql_users[0].name }}"
    nextcloud_db_pass: "{{ mysql_users[0].password }}"
    nextcloud_admin_user: "admin"
    nextcloud_admin_pass: "admin_pass"
    nextcloud_urls_tmp: >-
      {{ apache_vhosts
        | map(attribute='servername')
        | list
        | zip_longest([], fillvalue=':80')
        | map('join')
        | list }}
    nextcloud_urls: >-
      {{ []
        | zip_longest(nextcloud_urls_tmp, fillvalue='http://')
        | map('join')
        | list}}
    nextcloud_apps:
      - name: calendar
        version: 1.5.4
      - name: spreedme
    nextcloud_version: 12
    nextcloud_users:
      - name: nikos
        pass: "nikos-pass"
        resetpassword: yes
        display_name: Nikos Surname
        settings:
          - firstrunwizard:
              show: 0
          - calendar:
              showWeekNr: 'yes'
```

License
-------

GPLv3


