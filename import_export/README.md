# Import/Export Files

## Overview

This folder includes the code for importing data from and exporting data to various external data sources where original documents and translated content is hosted. Currently, Google documents and Wordpress sites are the two data sources integrated into the ELSA continuous localization pipeline.

### Google Docs

To properly import/export Google docs with Serge, you need to set up the following:

1. A Gmail account
2. OAuth redentials allowing you to access the Google Drive/Docs API via your Gmail account. To set up these credentials:
	a. Go to the [Google API Console](https://console.developers.google.com/apis/credentials)
	b. Create a project, if you have not already
	c. Go to `Create Credentials --> OAuth client ID`
	d. Create the credentials, download then, and save 2 copies, one as `credentials_drive.json` and another as `credentials_docs.json`, in a credentials folder called `secrets` in the root level of the git project. 
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

The original documents would placed in the `en` folder under the `Translations` subfolder, and the Spanish/Mandarin translations of those documents will go into the `es` and `zh` folders, respectively.

Since Google's API refers to folders and files by their ID, we need to map the names of the language folders to their respective folder IDs. The folder ID can be found by going to the folder, where the URL will look like https://drive.google.com/drive/u/1/folders/<folder ID>. The folder ID can be copied from that part of the URL and will be around 25 characters. The mapping should be put in a new file called `drive_config.yaml` and will look like the following:

language_folders:
  en:
    abc123
  es:
    def456  

Where abc123 and def456 are the folder IDs for the en and es folders, respectively (example strings in this case).