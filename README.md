This is a Genropy standalone package that allow you to use JSON-RPC with whithin your webapages

**INSTALLATION**

Look at your "packages" node inside your environment file ~/.gnr/environment.xml ; that node contains one or more paths (or you can add a new one) that can contains standalone projects.
For example:
```
  <packages>
    <genropy path="/var/mdssd/genro/single_packages"/>
  </packages>
```

Pull this repositoy in that folder; Genropy framework will be able to see it if you refer to it in your projects.
In order to make it "visibile" modify your project's instanceconfig.xml file by adding the following row:

```
<?xml version="1.0" ?>
<GenRoBag>
  ...
  <packages>
    ...
    <gnrjsonpkg pkgcode='gnrjsonpkg' />
    ...
  </packages>
  ...
</GenRoBag>
```

Now you can use this package:
```
class GnrCustomWebPage(object):
    py_requires='json_component:JsonRpc'
    
    @public_method
    def json_login(self, data):
        pass
        return {'this':'is a test'}
```

Look at the example; to make it working you can move/copy it in your "webpages" folder

Enjoy
