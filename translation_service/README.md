# Translation Service Module

This module acts as a connector between a continuous localization service 
(currently [Serge](https://serge.io/)) and a Translator 
(currently [Google Translate](https://cloud.google.com/translate/docs/apis)), 
and manages tracking which `.po` translation interchange files have been added/updated 
and need localization (translation). 

## serge_ts_connector.py

This program connects to Serge, a continuous localization service, providing two functions that Serge
requires for connection (`serge_pull_ts` and `serge_push_ts`), which handle copying data to/from Serge
and localizing (translating) any new or updated `.po` translation interchange files.

To set up this connection appropriately, Serge must be run with a 
[configuration file](https://github.com/nyc-cto/tms/tree/master/serge/configs) that calls 
`serge_ts_connector.py` with the appropriate arguments.

### Examples

This program can be called by specifying the mode, paths, and translator to be used.
```
# For serge_pull_ts, only the mode and paths are needed
python serge_ts_connector.py --mode pull_ts --serge_ts path/to/serge/ts --ts_serge_copy path/to/ts_serge_copy --ts_inbox path/to/ts_inbox --ts_outbox path/to/ts_outbox

# For serge_push_ts, the translator should also be specified unless using the default (caps) translator
python serge_ts_connector.py --mode push_ts --serge_ts path/to/serge/ts --ts_serge_copy path/to/ts_serge_copy --ts_inbox path/to/ts_inbox --ts_outbox path/to/ts_outbox --translation_api google --google_key_path path/to/TranslationGoogleKey.json
```


Alternatively, the paths can be set as ENV variables, which will be used as the default for running the program.
If you use the [`.env.template`](https://github.com/nyc-cto/tms/blob/master/.env.template)
to create a `.env` file with the appropriate paths and build a Docker image using 
the [`docker-compose.yml`](https://github.com/nyc-cto/tms/blob/master/docker-compose.yml),
it will use these as defaults.
```
# ENV variables for paths that need to be set
SERGE_TS
TS_SERGE_COPY
TS_INBOX
TS_OUTBOX
TRANSLATION_GOOGLE_KEY

# For serge_pull_ts, only the mode needs to be specified
python serge_ts_connector.py --mode pull_ts 

# For serge_push_ts, the translator should also be specified unless using the default (caps) translator
python serge_ts_connector.py --mode push_ts --translation_api google
```

## project_localizer.py

This program will localize (translate) all `.po` translation interchange files in a project 
directory which has subdirectories that are named by their ISO-639-1 code (ex. 'es', 'fr'). 
Currently, there is a filter to limit the languages supported to the 10 languages 
required by NYC Local Law 30:
```
SUPPORTED_LANGUAGES = {'es', 'zh', 'ru', 'bn', 'ht', 'ko', 'ar', 'fr', 'ur', 'pl'}
```
However, this can be changed to whichever languages the program would like to support that the 
translator API can also support.

If running the translation service module via the Serge configuration file, this program will not
need to be called individually as `serge_ts_connector.py` will do so.

## po_file.py

This program includes a PoFile class and a MsgElement class, both of which are used to handle
representing a `.po` translation interchange file (see 
[gnu.org](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html) for details on the structure
of a `.po` file), 
including parsing, updating translations, 
and writing to file. 

Note the assumptions about the structure of any `.po` file used with these classes:

- File starts with a header.
- A single blank line proceeds each message element.
- Each message element has a message header, msgid, and msgstr.

## translators.py

This program provides a Translator metaclass and TranslatorFactory. Currently there are two
translators implemented: GoogleTranslator (for the Google Translation API) and 
CapsTranslator (which simply capitalizes strings, mainly used for testing). 

For the GoogleTranslator,
a Google Service Account key must be provided as the `google_key_path`.

Additional translators can easily be added.

## Developer Notes

Please use [requirements.txt](https://github.com/nyc-cto/tms/blob/master/translation_service/requirements.txt) 
to install appropriate packages in your env/venv, or use 
the [Dockerfile](https://github.com/nyc-cto/tms/blob/master/Dockerfile), which will do so for you.
