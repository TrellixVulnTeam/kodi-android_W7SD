import xbmc
import xbmcgui

home = xbmcgui.Window(10000)
skin=home.getProperty("CurrentSkin")
if skin == "skin.sync.pro":
    xbmc.executebuiltin("ActivateWindow(1132)")
else:
    pass 
