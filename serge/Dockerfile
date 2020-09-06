ARG BASE_IMAGE=debian:stretch

FROM ${BASE_IMAGE}

ARG INSTALL_PREREQUISITES="apt-get -qq -y update && apt-get -qq -y install make cpanminus libscalar-list-utils-perl libxml-parser-perl libxml-xpath-perl libxml-libxslt-perl libtext-diff-perl libyaml-perl libmime-lite-perl libfile-copy-recursive-perl libauthen-sasl-perl libxml-twig-perl libtext-csv-xs-perl libjson-perl libjson-xs-perl libnet-smtp-ssl-perl libcpan-sqlite-perl libio-string-perl sqlite3 libsqlite3-dev git sudo vim wget unzip"
ARG CLEAN_PREREQUISITES="apt-get -qq -y purge make cpanminus"
ARG GIT_SHA1="CUSTOM BUILD"

LABEL maintainers="Erik Ogan <erik@change.org>, Igor Afanasyev <igor.afanasyev@gmail.com>"
LABEL git_sha1="${GIT_SHA1}"


# The simplest way to handle the escaping contortions is to echo everything into a file and source it.
RUN set -ex \
    && echo ${INSTALL_PREREQUISITES} > /tmp/prereq \
    && . /tmp/prereq


RUN mkdir /serge
RUN cd /serge
RUN wget https://github.com/evernote/serge/archive/1.4.zip -O serge-1.4.zip
RUN unzip serge-1.4.zip
RUN unlink serge-1.4.zip

RUN sudo cpanm --no-wget --installdeps /serge-1.4

RUN sudo ln -s /serge-1.4/bin/serge /usr/local/bin/serge

ENV PATH="/serge-1.4/bin:${PATH}"
ENV PERL5LIB="/serge-1.4/lib${PERL5LIB:+:}${PERL5LIB}"