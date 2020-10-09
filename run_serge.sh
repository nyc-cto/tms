cd /var/tms
python import_export/import-google-docs.py
serge sync /var/tms/serge/configs/google_config.serge
sleep 3
serge sync /var/tms/serge/configs/google_config.serge
python import_export/export-google-docs.py