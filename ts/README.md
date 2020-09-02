# Usage

This program can be used to localize all the .po files from an input project directory into an output project directory.
It takes the following arguments:
- `--input_dir`: The filepath for the input project directory. This input directory must have a subdirectory structure based on language ISO-639-1 code for each localization, with any .po files to localize inside (ex. `input_dir/es/untranslated_file.po` for Spanish localization).
- `--output_dir`: The filepath for the output project directory where the localization subdirectories and their localized files should be written to.
- `--translation_api`: The translation API to use ("google" for Google Translate, "caps" for capitalization).
- `--google_key_path`: The path for the Google Service Account JSON keyfile.

## Examples

```
python project_localizer.py --input_dir /path/to/input_dir/ --output_dir /path/to/output_dir/ --translation_api caps

python project_localizer.py --input_dir /path/to/input_dir/ --output_dir /path/to/output_dir/ --translation_api google --google_key_path /path/to/google_service_key.json
```
