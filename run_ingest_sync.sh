serge pull serge/configs/caps_ts_config.serge --initialize
while true; do
	python import_export/import-google-docs.py
	serge sync serge/configs/caps_ts_config.serge
	sleep 3
	serge synce serge/configs/caps_ts_config.serge
done
