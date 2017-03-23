<VirtualHost *:80>
ServerAdmin webmaster@{{ item.site }}
ServerName {{ item.site }}
ServerAlias www.{{ item.site }}
DocumentRoot {{ apache2.docroot }}/{{ item.site }}
ErrorLog ${APACHE_LOG_DIR}/{{ item.site }}/error.log
CustomLog ${APACHE_LOG_DIR}/{{ item.site }}/access.log combined
</VirtualHost>
