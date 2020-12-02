serge pull serge/configs/caps_config.serge --initialize --noauth_local_webserver
while true; do
	# python import_export/import-google-docs.py --noauth_local_webserver
	serge sync serge/configs/caps_config.serge
	sleep 3
	serge sync serge/configs/caps_config.serge
	# python import_export/export-google-docs.py
done
