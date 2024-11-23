#!/usr/bin/env bash

# docx2txt, a command-line utility to convert Docx documents to text format.
# A simple .docx to .txt converter
# This script is a wrapper around core docx2txt.pl and saves text output for
# (filename or) filename.docx in filename.txt .


MYLOC=`dirname "$0"`	# invoked perl script docx2txt.pl is expected here.

function usage ()
{
    cat << _USAGE_

Usage : $0 <file.docx>

	<file.docx> can also specify a directory holding the unzipped
	content of a .docx file.

_USAGE_

    exit 1
}

[ $# != 1 ] && usage


# Remove trailing '/'s if any, when input specifies a directory.

shopt -s extglob
set "${1%%+(/)}"

if [ -d "$1" ]
then
    if ! [ -r "$1" -a -x "$1" ]
    then
        echo -e "\nCan't access/read input directory <$1>!\n"
        exit 1
    fi
elif ! [ -f "$1" -a -r "$1" -a -s "$1" ]
then
    echo -e "\nCheck if <$1> exists, is readable and has non-zero size!\n"
    exit 1
fi


TEXTFILE=${1/%.docx/.txt}
[ "$1" == "$TEXTFILE" ] && TEXTFILE="$1.txt" 



# $1 : filename to check for existence
# $2 : message regarding file

function check_for_existence ()
{
    if [ -f "$1" ]
    then
        read -p "overwrite $2 <$1> [y/n] ? " yn
        if [ "$yn" != "y" ]
        then
            echo -e "\nPlease copy <$1> somewhere before running the script.\n"
            echeck=1
        fi
    fi
}

echeck=0
check_for_existence "$TEXTFILE" "Output text file"
[ $echeck -ne 0 ] && exit 1


# Invoke perl script to do the actual text extraction


"$MYLOC/docx2txt.pl" "$1" "$TEXTFILE"
if [ $? == 0 ]
then
    echo -e "\nText extracted from <$1> is available in <$TEXTFILE>.\n"
else
    echo -e "\nFailed to extract text from <$1>!\n"
fi

