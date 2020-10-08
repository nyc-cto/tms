{ printenv; echo ''; cat /var/tms/cron.config; } > /var/tms/tmpfile && mv /var/tms/tmpfile /var/tms/cron.config
crontab -e /var/tms/cron.config
service cron restart
