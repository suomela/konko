Konko
=====


Usage
-----

    ./konko CONFIGURATION
    ./konko-server CONFIGURATION

Example:

    ./konko example/ice.json
    ./konko-server example/ice.json

The server is needed so that you can click hyperlinks in the Excel
files. Press ctrl-c to stop the server.


Dependencies
------------

Python 3, XlsxWriter, and lxml.

If you have OS X and Homebrew, use the following commands to install
everything:

    brew install python3
    pip3 install lxml xlsxwriter


Configuration
-------------

See subdirectory `example` for some examples.


### source

Which input files to read.


### output-dir

Where to store output: concordance tables, summary tables, log files,
and HTML versions of the input files.

#### encoding

The character encoding of the input files.


### context

How many characters of context to show in the concordance table.

(The tool picks words until it has at least this many characters of
context, both before the match and after the match.)


### word

What is considered a "word". A regular expession. Matching is case
insensitive if word-ignore-case is true.


### tag

What is considered a "tag". A regular expession. Matching is case
insensitive if tag-ignore-case is true.

Tags have a higher priority than words, so if something looks
like both a tag and a word, it will be considered a tag.

Everything that is neither a word nor a tag is considered a separator
(typically whitespace or punctuation).


### search

What to search. Each search term is a regular expression. Matching
is case insensitive if search-ignore-case is true.

The search terms are matched agains "words" only.


### text

Text identifier. Regular expression, matched againts "tags" only.
Matching is case insensitive if tag-ignore-case is true.

May contain parentheses that capture the text identifier. Otherwise
the entire tag is considered the text identifier.

Multiple occurrences of the same text identifier are supported.
By default there is no text separator, and each file is considered
to be a text.


### sample

Sample identifier. Regular expression, matched againts "tags" only.
Matching is case insensitive if tag-ignore-case is true.

May contain parentheses that capture the sample identifier. Otherwise
the entire tag is considered the sample identifier.

Multiple occurrences of the same sample identifier are supported.
By default there is no sample separator, and each text is considered
to be a sample.


### delete

What to delete. A list of regular expressions and/or pairs of regular
expressions. Each regular expression is matched againts "tags" only.
Matching is case insensitive if tag-ignore-case is true.

A pair of regular expressions can be used to indicate a region that
is to be deleted. For example, the following rules delete regions of
text that are indicated with `<O>...</O>` or `<X>...</X>`

    "tag": "<[^<>]+>",
    "delete": [
        ["<O>", "</O>"],
        ["<X>", "</X>"],
    ]

Deletion is conservative if there are non-matching delimiters.
In the following two examples, "a" is kept and "b" is deleted:

    a <X> a <X> b </X> a

    a <X> b </X> a </X> a

The delimiters do not need to be properly nested. In the following
examples, "a" is kept and "b" is deleted:

    a <X> b <O> b </X> b </O> a

Deletion takes place on the level of *texts*. Nothing is remembered
between texts.

Deletion takes place *after* we have identified words, tags,
texts, and samples.

Deletion takes place *before* searching.

Deleted words are not reported as matches, and they are not included
in word counts. Deleted tags are not shown in the context. Deleted
parts are shown with a gray colour in the HTML files.


### server-port

TCP/IP port number for konko-server (default: 8000).



