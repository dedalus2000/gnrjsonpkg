#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='jsonpkg package',sqlschema='jsonpkg',sqlprefix=True,
                    name_short='Jsonpkg', name_long='Jsonpkg', name_full='Jsonpkg')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
