# Import/Export Files

## Overview

This folder includes the code for importing data from and exporting data to various external data sources where original documents and translated content is hosted.

## Setup

To properly import/export Google docs with Serge, you need to set up the following:

1. A Gmail account

2. OAuth redentials allowing you to access the Google Drive/Docs API via your Gmail account. To set up these credentials:
```
	a. Go to the [Google API Console](https://console.developers.google.com/apis/credentials)
	b. Create a project, if you have not already
	c. Navigate to the Dashboard page. Click on `Enable APIs and Services` and enable the Google Drive API for the project (it will take a few minutes for the permissions to propogate).
	d. Navigate to the Credentials page. Go to `Create Credentials --> OAuth client ID`
	e. Create the credentials, download then, and save 2 copies, one as `credentials_drive.json` and another as `credentials_docs.json`, in a credentials folder called `secrets` in the root level of the git project.
	f. In a terminal window, run the following command to pickle the credential files:

	python import_export/import-google-docs.py --noauth_local_webserver

	Follow the instructions in the terminal to complete the authentication. You will have to set up two authentications, one for Google Drive access and one for Google Docs access.

```

3. A Google drive folder which will contain all of the original and translated documents in folders. The original documents lie in the `en` folder, and each language you are translating into will have documents in ISO 639-1 standard language code-named folders. For example, if in your Google Drive you create a root folder named `Translations` and want to translate into Spanish (es) and Mandarin (zh), the directory structure would be as follows:

```
Translations
|
|____en
|
|____es
|
|____zh
```

The original documents would placed in the `en` folder under the `Translations` subfolder, and the Spanish/Mandarin translations of those documents will appear in the `es` and `zh` folders, respectively, after the import/export cycle runs.

Since Google's API refers to folders and files by their ID, we need to map the names of the language folders to their respective folder IDs in Google Drive. The folder ID can be found by navigating to the folder in Drive, where the URL will look like https://drive.google.com/drive/u/1/folders/<folder ID>. The folder ID can be copied from that part of the URL and will be around 25 characters. Make a copy of `drive_config.yaml.template` called `drive_config.yaml` and add all languages and folder ids you are using.

## Running

To run the full import/export cycle exactly once, navigate to the /var/tms directory of a running Serge container and execute the following in the terminal:

```
sh run_ingest_sync_simple.sh
```

This executes the Google Docs import to send new documents and changes to existing documents to the version control system; serge sync to execute the translations and update the translation memory; and the Google Docs export to push the translated documents and updates back to Google Docs. If you would like to continously run the import/export cycle, run the following command:

```
sh run_ingest_sync.sh
```

Note that running this command requires forcefully terminating the script if you wish to stop running it and may result in residual intermediate files -- execute `sh run_ingest_sync_simple.sh` to clean these up properly.