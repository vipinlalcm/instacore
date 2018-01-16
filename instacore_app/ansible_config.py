from passlib.hash import sha512_crypt
import os
import yaml
import jinja2
from .models import Webserver


class Ansible_Config():

    class Get_Values():
        def __init__(self, pk_id):
            data = Webserver.objects.filter(pk=pk_id).values()
            for key in data:
                self.pk_id = key['id']
                self.ip_address = key['ip_address']
                self.selectos = key['selectos']
                self.user = key['user']
                self.rootpassword = key['rootpassword']
                self.port = key['port']
                self.webserver = key['webserver']
                self.documentroot = key['documentroot']
                self.sitecount = key['sitecount']
                self.sitename = key['sitename']
                self.ftpserver = key['ftpserver']
                self.ftpuser = key['ftpuser']
                self.ftppassword = key['ftppassword']
                self.phpversion = key['phpversion']
                self.phpmod = key['phpmod']
                self.sqlserver = key['sqlserver']
                self.databasename = key['databasename']
                self.sqlusername = key['sqlusername']
                self.dbuserpassword = key['dbuserpassword']
                self.sqlrootpassword = key['sqlrootpassword']
                self.instance_path = ('instances/' +
                                      str(self.pk_id) + '-' + self.ip_address)
                self.var_path = (os.path.join(self.instance_path, 'vars'))
                self.l_path = ('./logs/instace.log')
                self.r_path = ('./roles/')
                self.i_path = ('./inventories/')
                self.log_path = (self.instance_path + '/logs/')
                self.role_path = (self.instance_path +
                                  self.r_path.split('.')[1])
                self.inventory_path = (self.instance_path +
                                       self.i_path.split('.')[1])

    class ConfigFile(Get_Values):

        def __init__(self, pk_id):
            super().__init__(pk_id)

            config = """[defaults]
log_path = {{ log_file }}
transport = ssh
inventory = {{ inventory_path }}
roles_path = {{ role_path }}
host_key_checking = False

[ssh_connection]
ssh_args = -o ForwardAgent=yes -o StrictHostKeyChecking=no

"""
            rendered_config = jinja2.Template(config).render({
                'log_file': self.l_path,
                'inventory_path': self.i_path,
                'role_path': self.r_path
            })
            os.makedirs(self.log_path)
            open(os.path.join(self.log_path, 'instance.log'), 'w+').close
            with open(os.path.join(self.instance_path,
                      'ansible.cfg'), 'w') as conf_file:
                conf_file.write(rendered_config)

    class Inventory(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)

            inv_template = """{{customer}}
{{ ipaddress }} keys=false ansible_ssh_port={{port}} ansible_become=true ansible_become_user=root ansible_become_method=sudo ansible_ssh_user={{usr}} ansible_ssh_pass={{passwd}}

"""
            rendered_inventory = jinja2.Template(inv_template).render({
                'customer': "[customer]",
                'ipaddress': self.ip_address,
                'port': self.port,
                'usr': self.user,
                'passwd': self.rootpassword
            })

            os.makedirs(self.inventory_path)
            with open(os.path.join(self.inventory_path,
                      'production'), 'w') as inv_file:
                inv_file.write(rendered_inventory)

    class Apache(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)
            self.apache_template()
            self.apache_handlers()
            self.apache_tasks()

        def apache_template(self):
            a_template = """<VirtualHost *:80>
ServerAdmin webmaster@{{ domain }}
ServerName {{ domain }}
ServerAlias www.{{ domain }}
DocumentRoot {{docroot}}/{{ domain }}
ErrorLog ${APACHE_LOG_DIR}/{{domain}}/error.log
CustomLog ${APACHE_LOG_DIR}/{{domain}}/access.log combined
</VirtualHost>

"""
            rendered_apache_template = jinja2.Template(a_template).render({
                'domain': "{" + "{" + " " + "item.site }}",
                'docroot': "{" + "{" + " " + "apache2.docroot }}"
            })

            apache_role_path = os.path.join(self.role_path, self.webserver,
                                            'templates')
            os.makedirs(apache_role_path)
            with open(os.path.join(apache_role_path,
                                   'default.tpl'), 'w') as apache_template:
                apache_template.write(rendered_apache_template)

        def apache_handlers(self):
            a_handler_template = """---
- name: restart {{handler}}
  service: name={{handler}} enabled=yes state=restarted

"""
            render_apache_handler = jinja2.Template(a_handler_template).render({
                'handler': self.webserver
            })

            apache_handler_path = os.path.join(self.role_path,
                                               self.webserver,
                                               'handlers')
            os.makedirs(apache_handler_path)
            with open(os.path.join(apache_handler_path, 'main.yml'), 'w') as f:
                    f.write(render_apache_handler)

        def apache_tasks(self):
            a_tasks_template = """---
- name: Installing {{webserver}}
  apt: pkg={{item}} update_cache=yes state=latest
  with_items:
    - {{webserver}}
    - libapache2-mod-php7.0

- name: Create user with home directory
  user: name={{ftpuser}} password={{ passd }} home={{ docroot }} shell=/usr/sbin/nologin

- name: Create vhost directory
  file: path={{ docroot }}/{{ site }} state=directory recurse=yes owner={{ftpuser}} group={{ftpuser}} mode=0775
  with_items:
    - "{{ sitename }}"

- name: Creating vhosts
  template: src=default.tpl dest=/etc/apache2/sites-available/{{site}}.conf
  with_items:
     - "{{ sitename }}"
  notify: restart {{handler}}

- name: Create logfile path directory
  file: path=/var/log/apache2/{{ site }} state=directory
  with_items:
    - "{{ sitename }}"

- name: enabled mod_rewrite
  apache2_module: name=rewrite state=present
  notify:
    - restart {{handler}}

- name: Disable the default sites.
  command: a2dissite {{item}}
  with_items:
    - 000-default.conf
    - default-ssl.conf

- name: a2ensite {{ site }}
  command: a2ensite {{ site }}
  args:
    creates: /etc/apache2/sites-enabled/{{ site }}.conf
  with_items:
    - "{{ sitename }}"
  notify:
    - restart {{handler}}

"""
            render_apache_tasks = jinja2.Template(a_tasks_template).render({
                'item': "{" + "{" + " " + "item }}",
                'site': "{" + "{" + " " + "item.site }}",
                'docroot': "{" + "{" + " " + "apache2.docroot }}",
                'sitename': "{" + "{" + " " + "sitename }}",
                'ftpuser': "{" + "{" + " " + "vsftpd.user }}",
                'passd': "{" + "{" + " " + "vsftpd.password }}",
                'handler': self.webserver,
                'webserver': self.webserver
            })

            apache_tasks_path = os.path.join(self.role_path,
                                             self.webserver,
                                             'tasks')
            os.makedirs(apache_tasks_path)
            with open(os.path.join(apache_tasks_path,
                      'main.yml'), 'w') as a_tasks:
                a_tasks.write(render_apache_tasks)

    class Nginx(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)
            self.ngnix_template()
            self.ngnix_handlers()
            self.ngnix_tasks()

        def ngnix_template(self):
            ng_tpl = """server {
listen  80;

root {{ docroot }}/{{ websitename }};
index index.html index.php;

server_name {{ websitename }};

location / {
    try_files $uri $uri/ /index.php?$query_string;
    }

error_page 404 /404.html;

error_page 500 502 503 504 /50x.html;
    location = /50x.html {
    root /usr/share/nginx/www;
    }

location ~ \.php$ {
    fastcgi_split_path_info ^(.+\.php)(/.+)$;
    fastcgi_pass unix:/var/run/php5-fpm.sock;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
    }
}

"""
            render_nginx_template = jinja2.Template(ng_tpl).render({
                'docroot': "{" + "{" + " " + "nginx.docroot }}",
                'websitename': "{" + "{" + " " + "item.site }}"
            })

            ngnix_template_path = os.path.join(self.role_path,
                                               self.webserver,
                                               'templates')
            os.makedirs(ngnix_template_path)
            with open(os.path.join(ngnix_template_path,
                                   'default.tpl'), 'w') as ng_file:
                ng_file.write(render_nginx_template)

        def ngnix_handlers(self):
            ng_handler_tpl = """---
- name: restart {{handler}}
  service: name={{handler}} enabled=yes state=restarted

"""
            render_nginx_handler = jinja2.Template(ng_handler_tpl).render({
                'handler': self.webserver
            })

            ng_handler_path = os.path.join(self.role_path,
                                           self.webserver,
                                           'handlers')
            os.makedirs(ng_handler_path)
            with open(os.path.join(ng_handler_path,
                                   'main.yml'), 'w') as ng_hand_file:
                ng_hand_file.write(render_nginx_handler)

        def ngnix_tasks(self):
            ng_tasks_tpl = """---
- name: Installing {{pkg}}
  apt: pkg={{pkg}} update_cache=yes state=latest

- name: Create user with home directory
  user: name={{ftpuser}} password={{ passd }} home={{ docroot }} shell=/usr/sbin/nologin

- name: Create vhost directory
  file: path={{ docroot }}/{{ site }} state=directory recurse=yes owner={{ftpuser}} group={{ftpuser}} mode=0775
  with_items:
    - "{{ sitename }}"

- name: Create site configuration
  template: src=default.tpl dest=/etc/nginx/sites-available/{{site}}.conf
  with_items:
    - "{{ sitename }}"

- name: Enabling the sites.
  file: path=/etc/nginx/sites-enabled/{{site}}.conf state=link src=/etc/nginx/sites-available/{{site}}.conf
  with_items:
    - "{{ sitename }}"
  notify: restart {{pkg}}

"""
            render_nginx_tasks = jinja2.Template(ng_tasks_tpl).render({
                'pkg': self.webserver,
                'site': "{" + "{" + " " + "item.site }}",
                'docroot': "{" + "{" + " " + "nginx.docroot }}",
                'sitename': "{" + "{" + " " + "sitename }}",
                'ftpuser': "{" + "{" + " " + "vsftpd.user }}",
                'passd': "{" + "{" + " " + "vsftpd.password }}"
            })

            ngnix_tasks_path = os.path.join(self.role_path,
                                            self.webserver,
                                            'tasks')
            os.makedirs(ngnix_tasks_path)
            with open(os.path.join(ngnix_tasks_path,
                                   'main.yml'), 'w') as ng_task_file:
                ng_task_file.write(render_nginx_tasks)

    class PHP(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)
            self.php_tasks()

        def php_tasks(self):
            php_tasks_tpl = """---
- name: Install php with selected modules.
  become: yes
  apt: pkg={{ item }} state=latest
  with_items:
    "{{php_packages}}"

"""
            render_php_tasks = jinja2.Template(php_tasks_tpl).render({
                'item': "{" + "{" + " " + "item }}",
                'php_packages': "{" + "{" + " " + 'php' + " " + "}}"
            })

            php_task_path = os.path.join(self.role_path,
                                         self.phpversion,
                                         'tasks')
            os.makedirs(php_task_path)
            with open(os.path.join(php_task_path,
                                   'main.yml'), 'w') as php_task_file:
                php_task_file.write(render_php_tasks)

    class FTP(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)
            self.ftp_handlers()
            self.ftp_tasks()

        def ftp_handlers(self):
            ftp_handler_template = """---
- name: restart {{handler}}
  service: name={{handler}} enabled=yes state=restarted

"""
            render_handler_tpl = jinja2.Template(ftp_handler_template).render({
                'handler': self.ftpserver
            })

            ftp_handler_path = os.path.join(self.role_path,
                                            self.ftpserver,
                                            'handlers')
            os.makedirs(ftp_handler_path)
            with open(os.path.join(ftp_handler_path,
                                   'main.yml'), 'w') as handler_file:
                handler_file.write(render_handler_tpl)

        def ftp_tasks(self):
            ftp_task_template = """---
- name: Install {{pkg}}
  apt: pkg={{pkg}} update_cache=no state=latest
  notify: restart {{pkg}}

"""
            render_ftp_tasks = jinja2.Template(ftp_task_template).render({
                'pkg': self.ftpserver
            })

            ftp_task_path = os.path.join(self.role_path,
                                         self.ftpserver,
                                         'tasks')
            os.makedirs(ftp_task_path)
            with open(os.path.join(ftp_task_path,
                                   'main.yml'), 'w') as ftp_file:
                ftp_file.write(render_ftp_tasks)

    class SQL(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)
            self.sql_handlers()
            self.sql_tasks()

        def sql_handlers(self):
            sql_handler_tpl = """---
- name: restart {{handler}}
  service: name={{handler}} enabled=yes state=restarted

"""
            sql_handler = jinja2.Template(sql_handler_tpl).render({
                'handler': 'mysql'
            })
            sql_handler_path = os.path.join(self.role_path,
                                            self.sqlserver,
                                            'handlers')
            os.makedirs(sql_handler_path)
            with open(os.path.join(sql_handler_path,
                      'main.yml'), 'w') as sql_handler_file:
                sql_handler_file.write(sql_handler)

        def sql_tasks(self):
            sql_task_tpl = """---
- name: Install MySQL packages
  apt: pkg={{item}} state=installed
  when: ansible_os_family == 'Debian'
  with_items:
  - python-mysqldb
  - {{srvpkg}}
- name: mysql | Update root password for all root accounts
  mysql_user: name=root host={{ item }} check_implicit_admin=yes password={{ mysql_root_pass }} login_user=root login_password={{ mysql_root_pass }} update_password=on_create
  with_items:
  - 127.0.0.1
  - ::1
  - localhost

- name: Deletes anonymous MySQL server user for localhost
  mysql_user: user="" state="absent" login_password="{{ mysql_root_pass }}" login_user="root"

- name: mysql | Create databases
  mysql_db: name={{ db }} state=present login_user=root login_password={{ mysql_root_pass }}

- name: mysql | Create users
  mysql_user: name={{ db_user }} password={{ db_user_pass }} priv={{ db }}.*:ALL state=present login_user=root login_password={{ mysql_root_pass }}

- name: Removes the MySQL test database
  mysql_db: db=test state=absent login_password="{{ mysql_root_pass }}" login_user=root

"""
            render_sql_tasks = jinja2.Template(sql_task_tpl).render({
                'srvpkg': self.sqlserver,
                'item': "{" + "{" + " " + "item }}",
                'mysql_root_pass': "{" + "{" + " " + "mysql.root_password }}",
                'db': "{" + "{" + " " + "mysql.database }}",
                'db_user': "{" + "{" + " " + "mysql.user }}",
                'db_user_pass': "{" + "{" + " " + "mysql.password }}"
            })
            sql_tasks_path = os.path.join(self.role_path,
                                          self.sqlserver,
                                          'tasks')
            os.makedirs(sql_tasks_path)
            with open(os.path.join(sql_tasks_path,
                      'main.yml'), 'w') as sql_taks_file:
                sql_taks_file.write(render_sql_tasks)

    class Variables(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)
            self.web_vars()
            self.ftp_vars()
            self.php_vars()
            self.sql_vars()

        def web_vars(self):
            if self.sitecount >= 1:
                if ',' in self.sitename:
                    s = self.sitename.split(',')
                    f = [str(x) for x in s]
                    split = list(map(str.strip, f))
                    length = len(split)
                    if self.sitecount == length:
                        sites_list = []
                        for i in range(0, length):
                            sites = dict(site=str(split[i]))
                            sites_list.append(sites)
                        sites_yaml = yaml.load(str(sites_list))
                        dic = {'sitename': sites_yaml,
                               yaml.load(self.webserver):
                               {'docroot': yaml.load(self.documentroot)}}
                        var_data = yaml.dump(dic)
                        os.makedirs(self.var_path)
                        with open(os.path.join(self.var_path, 'all.yml'),
                                  'w') as web_yaml:
                            yaml.dump(yaml.load(var_data),
                                      web_yaml, default_flow_style=False)
                else:
                    sites_list = [{'site': self.sitename}]
                    sites_yaml = yaml.load(str(sites_list))
                    dic = {'sitename': sites_yaml,
                           yaml.load(self.webserver):
                           {'docroot': yaml.load(self.documentroot)}}
                    var_data = yaml.dump(dic)
                    os.makedirs(self.var_path)
                    with open(os.path.join(self.var_path, 'all.yml'),
                              'w') as web_yaml:
                        yaml.dump(yaml.load(var_data),
                                  web_yaml, default_flow_style=False)

        def php_vars(self):
            dic_php_mod = {yaml.load('php'):
                           yaml.load(str(self.phpmod))}
            phpmods_var_data = yaml.dump(dic_php_mod)
            with open(os.path.join(self.var_path, 'all.yml'),
                      'a') as php_yaml:
                yaml.dump(yaml.load(phpmods_var_data),
                          php_yaml, default_flow_style=False)

        def ftp_vars(self):
            ftpusr_yaml = yaml.load(self.ftpuser)
            ftpserver_yaml = yaml.load(self.ftpserver)
            # Genertate password
            pass_yaml = yaml.load(sha512_crypt.encrypt(self.ftppassword,
                                  rounds=5000))
            ftp = {ftpserver_yaml: {'user': ftpusr_yaml,
                   'password': pass_yaml}}
            ftp_var_data = yaml.dump(ftp)
            with open(os.path.join(self.var_path, 'all.yml'), 'a') as ftp_yaml:
                yaml.dump(yaml.load(ftp_var_data),
                          ftp_yaml, default_flow_style=False)

        def sql_vars(self):
            sqlyaml_dic = {'mysql':
                           {'database': yaml.load(self.databasename),
                            'password': yaml.load(self.dbuserpassword),
                            'user': yaml.load(self.sqlusername),
                            'root_password': yaml.load(self.sqlrootpassword)}}

            sql_yaml_data = yaml.dump(sqlyaml_dic)
            with open(os.path.join(self.var_path, 'all.yml'), 'a') as sql_yaml:
                yaml.dump(yaml.load(sql_yaml_data),
                          sql_yaml, default_flow_style=False)

    class Playbook(Get_Values):
        def __init__(self, pk_id):
            super().__init__(pk_id)
            self.playbook()

        def playbook(self):
            roles = [self.webserver, self.ftpserver,
                     self.phpversion, self.sqlserver]
            play_data = [{'hosts': 'all',
                         'roles': roles,
                          'vars_files': ['vars/all.yml']}]
            play = yaml.dump(play_data)
            with open(os.path.join(self.instance_path,
                      'playbook.yml'), 'w') as play_file:
                yaml.dump(yaml.load(play), play_file, default_flow_style=False)


class Generate(Ansible_Config.Get_Values):
    def __init__(self, pk_id):
        super().__init__(pk_id)

        Ansible_Config.ConfigFile(pk_id)
        Ansible_Config.Inventory(pk_id)
        if 'apache2' in self.webserver:
            Ansible_Config.Apache(pk_id)
        else:
            Ansible_Config.Nginx(pk_id)
        Ansible_Config.PHP(pk_id)
        Ansible_Config.FTP(pk_id)
        Ansible_Config.SQL(pk_id)
        Ansible_Config.Variables(pk_id)
        Ansible_Config.Playbook(pk_id)
