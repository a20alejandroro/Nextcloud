<?php
$CONFIG = array (
  'htaccess.RewriteBase' => '/',
  'memcache.local' => '\\OC\\Memcache\\APCu',
  'memcache.distributed' => '\OC\Memcache\Redis',
  'memcache.locking' => '\OC\Memcache\Redis',
  'redis' => [
    'host' => 'redis',
    'port' => 6379,
  ],
  'apps_paths' => 
  array (
    0 => 
    array (
      'path' => '/var/www/html/apps',
      'url' => '/apps',
      'writable' => false,
    ),
    1 => 
    array (
      'path' => '/var/www/html/custom_apps',
      'url' => '/custom_apps',
      'writable' => true,
    ),
  ),
  'upgrade.disable-web' => true,
  'instanceid' => 'oc8dus34agmx',
  'passwordsalt' => 'XA6S6gTx8Zg1qlzNz+R86so0J6NX3O',
  'secret' => 'g1/ZimssgQsZ5DCZ+7zV4c8Un6URBap7I/TNIxY3YkN/dTDO',
  'trusted_domains' => 
  array (
    0 => 'alejandrorey.tech',
  ),
  'datadirectory' => '/var/www/html/data',
  'dbtype' => 'mysql',
  'version' => '31.0.5.1',
  'overwrite.cli.url' => 'https://alejandrorey.tech',
  'dbname' => 'defaultdb',
  'dbhost' => 'mysql-5a7cb1e-nextcloud-a20alejandroro.f.aivencloud.com:11579',
  'dbport' => '',
  'dbtableprefix' => 'oc_',
  'mysql.utf8mb4' => true,
  'dbuser' => 'oc_administrador',
  'dbpassword' => 'DrL/2=7Gq;Y8#wLGkZDdfuf|@-A0.-',
  'installed' => true,
  'overwrite.cli.url' => 'https://alejandrorey.tech',
  'overwritehost' => 'alejandrorey.tech',
  'overwriteprotocol' => 'https',
  'trusted_proxies' => ['172.19.0.10'],
  'default_phone_region' => 'ES',
  'maintenance' => false,
  'maintenance_window_start' => '3',
  'mail_domain' => 'alejandrorey.tech',
  'mail_from_address' => 'nextcloud',
  'mail_smtpmode' => 'smtp',
  'mail_smtphost' => 'smtp.titan.email',
  'mail_smtpport' => '587',
  'mail_smtpauthtype' => 'LOGIN',
  'mail_sendmailmode' => 'smtp',
  'mail_smtpname' => 'nextcloud@alejandrorey.tech',
  'mail_smtppassword' => 'Nextcloud248.',
  'mail_smtpauth' => true,
  'mail_smtpstreamoptions' => 
  array (
    'ssl' => 
    array (
      'allow_self_signed' => true,
      'verify_peer' => false,
      'verify_peer_name' => false,
    ),
  ),
);
