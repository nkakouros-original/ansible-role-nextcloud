[![Build Status](https://travis-ci.com/tterranigma/ansible-role-nextcloud.svg?branch=master)](https://travis-ci.com/tterranigma/ansible-role-nextcloud)

Ansible Role: Nextcloud
=========

Installs and upgrades Nextcloud and apps. **It only does that**, it does not install a web server, a db server, etc.

Features
--------

This role allows you to:
- install, update and configure Nextcloud core
- install, update and configure Nextcloud apps available on the app store
- create and update users and groups

Requirements
------------

Ansible >= 2.7

While there are a bunch of other roles around to install Nextcloud, I did not found them useful as they try to do everything in one role, ie setup Apache, then MySQL, then install Nextcloud, etc. This might be useful for users who want to have a Nextcloud instance running as fast as possible. However, I find the approach too limiting as there are too many assumptions taking place.

This role does not care where you install Nextcloud. It only downloads, installs and configures Nextcloud itself. Its aim is to be used in a modular way alongside other roles. (Or at least it tries to make no assumptions. If you find any or cannot install nextcloud due to missing functionality, please open an issue or a PR. Currently it has been tested only on Ubuntu 16.04).

See the [Example playbook](#example-playbook) on how a complete playbook that uses 3rd-party roles might look like.

Versions
---

- _Supported Nextcloud versions_: Each release of the role will support all officially supported Nextcloud versions, starting from version 14. That is, versions older than Nextcloud 14 will not be supported ever by this role (for instance Nextcloud 13, although it is supported officially as of this writing). Also, with each new major version of Nextcloud, the version that this role installs by default will be updated to match that latest major release.

- _Supported Ansible versions_: I am using an installation of Ansible that is daily checked out from their [development branch](https://github.com/ansible/ansible/tree/devel/). With each new Ansible stable version (currently 2.7), a new release of this role will be created that will be compatible with that new Ansible version. Work following such a release will take place with the in-development next version of Ansible and might use new Ansible features.

For this above reasons, role releases will have names such as `v14-2.7-1.0`, where:

- `14` is the version of Nextcloud that this role will install by default
- `2.7` is the Ansible version that the release will be compatible with
- `1.0` is semantic versioning of the role itself (reset when either of the two components above gets updated)

The above release will of course also be compatible with later Ansible versions that are compatible with Ansible 2.7.

Role Variables
--------------

(copied from [defaults/main.yml](https://github.com/tterranigma/ansible-role-nextcloud/blob/master/defaults/main.yml))

```yaml
---

nextcloud_enable: yes
# Set this to 'no' to completely disable the role

nextcloud_version: 14
# The major nextcloud version to install. You can use this to upgrade to a new
# major version as well. Even if you set 'nextcloud_download_url' manually (see
# next option), 'nextcloud_version' should be set as it is also used to
# correctly install the apps.

# TODO This is useless as `nextcloud_version` is required
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

nextcloud_data_dir: "{{ nextcloud_installation_dir }}/data"
# Path to nextcloud user data directory

nextcloud_file_owner: 'www-data'
# The user that will own nextcloud files.

nextcloud_database:
  backend: mysql
  # The database server that will be used. It should be already installed and
  # the database should already exist. For 'mariadb', set this to 'mysql'.

  name: nextcloud
  # The name of the database nextcloud will use. It should already exist on the
  # system.

  user: nextcloud
  # The database user that nextcloud will use to access the database. The user
  # should already exist in the database backend (together with their password).

  pass: ''
  # The database user's password. This variable should not be empty.

  host: localhost
  # The database host

  port: 3306
  # The port the db server listens on

nextcloud_admin_user: admin
# The name of the admin user

nextcloud_admin_pass: ''
# The password of the admin user. This variable should not be empty.

# TODO make this part of nextcloud_config_system
nextcloud_enable_pretty_urls: yes
# Set to yes to enable urls of the form https://example.org/calendar replacing
# https://example.org/nextcloud/index.php/s/Sv1b7krAUqmF8QQ.

# TODO make this part of nextcloud_config_system
nextcloud_urls:
  - https://localhost:80/folder
# This is a list of urls where your nextcloud installation should be accessible.
# You would normally need only one. If you specify more than one, the first one
# will be as the "main" one, for pretty urls, etc.

nextcloud_apps: []
# The ansible apps to install and enable
# It is a list of hashes. Eg
#
# nextcloud_apps:
#   - name: calendar
#     version: 1.5.7
#
# If 'version' is not given, then the latest version available for the installed
# nextcloud version will be installed.

nextcloud_config_global: {}

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
# available, either make the changes manually and then the oc_preferences table
# in your nextcloud database or use the `occ config:list` command on your server
# to get a listing of the current configuration options.

```

Example Playbook
----------------

Here is a complete example of how to use this role in conjuction with other roles in order to get a complete server environment running Nextcloud. In this example, I use the well known [geerlingguy](https://github.com/geerlingguy/) roles to install apache, mysql and php, alongside Nextcloud, on Ubuntu 16.04.

```yaml
---

- hosts: server
  become: yes
  vars:
    mysql_root_password_update: no
    mysql_databases:
      - name: "nextcloud"
    mysql_users:
      - name: "nextcloud"
        password: pass
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
      - php-curl
    apache_remove_default_vhost: true
    apache_vhosts:
      # TODO: disable htaccess and load it directly
      # TODO: enable ssl with certbot
      - servername: "my.server.net"
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
    apache_state: restarted
    firewall_allowed_tcp_ports:
      - 22
      - 80
    manala_cron_files:
      - file: nextcloud
        user: www-data
        jobs:
          - name: Run nextcloud cron
            job: "php-cli -f {{ apache_vhosts.0.documentroot }}/cron.php"
            minute: "*/15"
    nextcloud_database:
      name: "{{ mysql_databases[0].name }}"
      user: "{{ mysql_users[0].name }}"
      pass: "{{ mysql_users[0].password }}"
    nextcloud_admin_user: "admin"
    nextcloud_admin_pass: "pass"
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
      - name: tasks
      - name: news
    nextcloud_version: 14
    nextcloud_config_global:
      backgroundjobs_mode: cron
    nextcloud_users:
      - name: myuser
        pass: pass
        groups:
          - admin
        resetpassword: true
        display_name: My Name
        settings:
          - firstrunwizard:
              show: 0
          - calendar:
              showWeekNr: 'yes'
  pre_tasks:
    - setup:
      become: no
  tasks:
    - include_role:
        name: ansible-role-php
    - include_role:
        name: ansible-role-mysql
    - include_role:
        name: ansible-role-apache
    - include_role:
        name: ansible-role-firewall
    - include_role:
        name: ansible-role-cron
    - include_role:
        name: ansible-role-nextcloud
  post_tasks:
    - name: Save passwords
      copy:
        content: |
          mysql_nextcloud_password: {{ mysql_users[0].password }}
          nextcloud_admin_pass: {{ nextcloud_admin_pass }}
          nextcloud_nikos_pass: {{ nextcloud_users[0].pass }}
        dest: "{{ project_dir }}/files/server/passwords"
        mode: 0755
      tags: pass
      become: no
      delegate_to: localhost
```

License
-------

GPLv3
