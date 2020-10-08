serge pull serge/configs/google_config.serge --initialize
while true; do
	python import_export/import-google-docs.py
	serge sync serge/configs/google_config.serge
	sleep 3
	serge sync serge/configs/google_config.serge
	python import_export/export-google-docs.py
done
