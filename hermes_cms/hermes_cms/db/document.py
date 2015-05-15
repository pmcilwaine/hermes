# /usr/bin/env python
# -*- coding: utf-8 -*-

from sqlobject import SQLObject
from sqlobject.col import StringCol, DateTimeCol, BoolCol, IntCol


class Document(SQLObject):
    gid = IntCol()  # the global document id, is the same across all versions
    url = StringCol()  # this is unique for URL for each GID.
    uuid = StringCol()  # this is the version record to be found in S3
    path = StringCol()  # Uses the gid as parentGID/currentGID etc.
    created = DateTimeCol()
    published = BoolCol(default=False)
    archived = BoolCol(default=False)
    type = StringCol()  # The document type e.g. Page this is found in the Configuration Registry
    name = StringCol()  # the name of the document listed in the administration area
    menutitle = StringCol()  # The title listed in the menu for the document for the publicily visible website
    show_in_menu = BoolCol(default=False)
