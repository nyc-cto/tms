# Usage

This program can be used to localize all the .po files in a directory.
It takes the following arguments:
- `--input`: the input filepath where the .po files are located.
- `--output`: (optional) the output filepath where you would like the localized files to be written to. If specified, must already exist. If not, will create a `localized` directory inside the input directory.
- `--lang`: the ISO-639-1 language code for the target localization

## Examples

```
python po_localizer.py --input /path/to/input_dir/ --output /path/to/output_dir/ --lang es

python po_localizer.py --input /path/to/input_dir/ --lang ru
```
