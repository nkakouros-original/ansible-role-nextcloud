[![Build Status](https://travis-ci.com/nkakouros-original/ansible-role-nextcloud.svg?branch=master)](https://travis-ci.com/nkakouros-original/ansible-role-nextcloud)
[![Galaxy](https://img.shields.io/badge/galaxy-nkakouros.nextcloud-blue.svg)](https://galaxy.ansible.com/nkakouros/nextcloud/)

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

See [defaults/main.yml](https://github.com/nkakouros-original/ansible-role-nextcloud/blob/master/defaults/main.yml) for a full list of variables together with documentation on how to use them to configure this role.

Example Playbook
----------------

See [molecule/default/prepare.yml](molecule/default/prepare.yml) and [molecule/default/playbook.yml](molecule/default/playbook.yml) for a working example of how to use this role in conjuction with other roles to get a complete server environment that runs Nextcloud.

License
-------

GPLv3
