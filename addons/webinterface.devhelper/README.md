## Devhelper web

A web interface to debug some bits of Kodi. Enable the web server and remote control, then install
and access the web interface at "http://[hostname]:[port]/addons/webinterface.devhelper/", no need to
change the 'Web interface' setting. With most browsers you can also unpack it and open 'index.html'
right from your local file system without installing it as an add-on.

Latest stable [installable zip](https://github.com/rmrector/repository.rector.stuff/raw/master/latest/webinterface.devhelper-latest.zip).

It can also be installed from my [development repo], which will keep it updated.

[development repo]: (https://github.com/rmrector/repository.rector.stuff/raw/master/latest/repository.rector.stuff-latest.zip).

There is a running data section that watches InfoLabels and InfoBooleans available to skins. This
provides access to much of the information that would be used in a debug overlay during skinning,
and there is plenty of room to show more info without obscuring your design.

![Running data](resources/screenshot1.jpg)

It also includes a JSON-RPC browser to navigate and execute JSON-RPC methods; a beefed up take on
The Lab in Chorus and [this JSON-RPC browser](https://forum.kodi.tv/showthread.php?tid=172734).

![JSON-RPC browser](resources/screenshot2.jpg)

This is still a bit raw, but has been quite useful for me already so I wanted to share. It uses modern
web technologies and requires a modern browser to run. Chrome and Firefox are tested working, Safari
and Opera should also work. Edge still doesn't work very well.
