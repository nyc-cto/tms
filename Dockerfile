ARG BASE_IMAGE=python:3-buster
FROM ${BASE_IMAGE}
ARG INSTALL_PREREQUISITES="apt-get -qq -y update && apt-get -qq -y -o Acquire::http=true install make cpanminus libscalar-list-utils-perl libxml-parser-perl libxml-xpath-perl libxml-libxslt-perl libtext-diff-perl libyaml-perl libmime-lite-perl libfile-copy-recursive-perl libauthen-sasl-perl libxml-twig-perl libtext-csv-xs-perl libjson-perl libjson-xs-perl libnet-smtp-ssl-perl libcpan-sqlite-perl libio-string-perl sqlite3 libsqlite3-dev git sudo vim wget unzip cron"
ARG CLEAN_PREREQUISITES="apt-get -qq -y purge make cpanminus"
ARG GIT_SHA1="CUSTOM BUILD"
LABEL maintainers=" Shannon Ladymon <sladymon@usdigitalresponse.org>, Matt Silver <msilver@usdigitalresponse.org>, Aditya Sridhar <asridhar@usdigitalresponse.org>, Steve Young <syoung@usdigitalresponse.org>"
LABEL git_sha1="${GIT_SHA1}"

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get -qq -y update
RUN apt-get -qq -y upgrade
RUN apt-get -qq -y purge make cpanminus
RUN apt-get -qq -y install make
RUN apt-get -qq -y install git
RUN apt-get -qq -y install sudo
RUN apt-get -qq -y install vim
RUN apt-get -qq -y install wget
RUN apt-get -qq -y install unzip
RUN apt-get -qq -y install cron
RUN apt-get -qq -y install sqlite3
RUN apt-get -o Acquire::http=true install cpanminus
RUN apt-get -o Acquire::http=true install libscalar-list-utils-perl
RUN apt-get -o Acquire::http=true install libxml-libxslt-perl
RUN apt-get -o Acquire::http=true install libtext-diff-perl
RUN apt-get -o Acquire::http=true install libyaml-perl
RUN apt-get -o Acquire::http=true install libmime-lite-perl
RUN apt-get -o Acquire::http=true install libfile-copy-recursive-perl
RUN apt-get -o Acquire::http=true install libauthen-sasl-perl
RUN apt-get -o Acquire::http=true install libxml-twig-perl
RUN apt-get -o Acquire::http=true install libtext-csv-xs-perl
RUN apt-get -o Acquire::http=true install libjson-perl
RUN apt-get -o Acquire::http=true install libjson-xs-perl
RUN apt-get -o Acquire::http=true install libnet-smtp-ssl-perl
RUN apt-get -o Acquire::http=true install libcpan-sqlite-perl
RUN apt-get -o Acquire::http=true install libio-string-perl
RUN apt-get -o Acquire::http=true install libsqlite3-dev
RUN apt-get -o Acquire::http=true install libxml-xpath-perl
RUN apt-get -o Acquire::http=true install libxml-parser-perl

# The simplest way to handle the escaping contortions is to echo everything into a file and source it.
# RUN set -ex \
#   && echo ${INSTALL_PREREQUISITES} > /tmp/prereq \
#    && . /tmp/prereq

WORKDIR /
RUN wget https://github.com/evernote/serge/archive/1.4.zip -O serge-1.4.zip
RUN unzip serge-1.4.zip
RUN unlink serge-1.4.zip
# RUN sudo cpanm --no-wget --installdeps /serge-1.4
# RUN sudo ln -s /serge-1.4/bin/serge /usr/local/bin/serge
# ENV PATH="/serge-1.4/bin:${PATH}"
# ENV PERL5LIB="/serge-1.4/lib${PERL5LIB:+:}${PERL5LIB}"
# We copy just the requirements.txt first to leverage Docker cache
COPY ./translation_service/requirements.txt /var/tms/translation_service/requirements.txt
COPY ./import_export/requirements.txt /var/tms/import_export/requirements.txt


RUN pip install -r /var/tms/translation_service/requirements.txt
RUN pip install -r /var/tms/import_export/requirements.txt

COPY . /var/tms

RUN mkdir /var/.ssh_keys
RUN ssh-keygen -t rsa -N "" -f /var/.ssh_keys/github_deploy_key
RUN chmod 700 /var/.ssh_keys/github_deploy_key
RUN chmod 755 /var/tms/run_serge.sh
RUN chmod 755 /var/tms/setup_cron.sh
