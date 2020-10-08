{ printenv; echo ''; cat /var/tms/cron.config; echo ""; } > /var/tms/tmpfile && mv /var/tms/tmpfile /var/tms/cron.config
crontab /var/tms/cron.config
service cron restart
