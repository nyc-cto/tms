# ELSA Localization Pipeline

The NYC Mayor’s Office of the CTO (MOCTO) is developing an open-source translation pipeline that aims to streamline the process of translation management for itself and potentially other city agencies. 

- **Open-source:** We are committed to making our entire platform publicly accessible. 
- **Easy setup:** Our service should be easy to understand and set up. 
- **Modular:** The separate components of our pipeline should be easily adaptable. We hope to eventually expand our integrations with more version control systems and translation service plugins. 

For a high-level overview of the pipeline, please see our [presentation slide deck](https://docs.google.com/presentation/d/1HAfbpOXG-ksyBjDpF-ZmOaoArvrinVd6iLmhdn6lkg0/edit?usp=sharing)

**Please reach out to [jiman@cto.nyc.gov](mailto:jiman@cto.nyc.gov) if you would like to get involved!**

## FAQ

### General
#### What is localization?
According to GALA (Globalization and Localization Association), “localization (also referred to as ‘l10n’) is the process of adapting a product or content to a specific locale or market. Translation is only one of several elements of the localization process.” Translations should incorporate specific contexts and dialects based on the target audience. 

#### What is translation versus interpretation? 
According to GALA, “translation is the communication of meaning from one language (the source) to another language (the target). Translation refers to written information, whereas interpretation refers to spoken information. The purpose of translation is to convey the original tone and intent of a message, taking into account cultural and regional differences between source and target languages.”

#### What is language access?
Language access is the ability for users to access government resources and services in their preferred language. 

#### What is continuous localization?
Continuous localization automatically determines the portion of updated content that needs to be translated, uses translation memory (TM) to store and reuse previously translated content, and pushes back updated content once it is translated. As we have gathered so far from conversations with the Mayor’s Office of Immigrant Affairs (MOIA), fully automated continuous localization does not yet exist in city government. 

#### What is a TMS, CMS, VCS, and CAT tool?
* A TMS (translation management system) “is a type of software for automating many parts of the human language translation process and maximizing translator efficiency. The idea of a translation management system is to automate all repeatable and non-essential work that can be done by software/systems and leaving only the creative work of translation and review to be done by human beings” (Wikipedia).
    * E.g. Mojito
* A CMS (content management system) “is a software application that can be used to manage the creation and modification of digital content” (Wikipedia). A CMS allows content managers to write, upload, and update content without needing to understand the technical details of how the content is eventually distributed.
    * E.g. WordPress
* A VCS (version control system) “helps record changes to files by keeping a track of modifications done to the code” (GeeksForGeeks). 
    * E.g. GitHub
* A CAT (computer-assisted translation) tool “assists a human translator in the translation process” (Wikipedia). 
    * E.g. Zing

### Governmental
#### What is MOCTO?
MOCTO (Mayor’s Office of the Chief Technology Officer) is a city government agency that collaborates with other agencies to ensure that technology is inclusive, accessible, human-centered, and works for all New Yorkers. Focus areas include universal broadband, digital services, inclusive innovation, and tech policy.

#### What is MOIA?
MOIA (Mayor’s Office of Immigrant Affairs) promotes the well-being of immigrant communities, partly by promoting language accessibility and working with translation vendors. MOCTO works with MOIA to request translation of content. 

### Technical
#### What is a .po file?
The PO file format is a translation interchange file format. .pot input files are processed into .po output files for each language, which are then used by translation services to return translated strings.

#### What is Serge?
Serge “is a continuous localization solution that allows you to configure robust localization automation scenarios in minutes, and integrate localization processes into your everyday development, content authoring and CI/CD workflows.” It is open-source, written in Perl, and primarily a back-end tool. It is built for modularity, functioning via plugins into VCS’s and TMS’s.

#### What is Mojito?
Mojito is another open-source continuous localization tool. It is open-source, written in Java, and offers both a front-end and back-end.

### Operational
#### Who are the key stakeholders?
The key stakeholder for the first iteration of the pipeline will be MOCTO, but we hope to make the pipeline useful to other government agencies as well. 

#### Who are end readers?
The end readers are members of the public who will be consuming translated content. They will not be aware of the existence of the pipeline. 

#### What is an internal implementer / maintainer?
The internal implementer is responsible for setting up and configuring the pipeline for their organization based on their organization’s unique needs, the structure of their translation team, and their organization’s preferred CMS and translation service. 

#### What is the open-source community?
The open-source community is a community of software developers who believe that good code should be shared and built upon collaboratively, rather than monetized. While MOCTO will be maintaining and supporting ELSA for the foreseeable future, the construction of this pipeline depends on the continued support, guidance, and labor of the open-source community. All code involved in ELSA will be under the Apache License 2.0. 

### Drilldown
#### What are other TMS’s out there?
MOCTO closely explored Serge, Zing, Pootle, and Mojito. A comparison of these tools may be found in the Serge + Mojito Setup Notes. A variety of other open-source TMS’s exist, along with some proprietary services. 

#### How does the translation process happen?
Ideally, steps involved in the translation process include translation, editing/revision, proofreading, and maintenance. Roles include translators, editors, proofreaders, and subject matter experts. The extent to which organizations can follow this entire process depends upon their resources, especially as most city government agencies cannot hire formal in-house translators. 
