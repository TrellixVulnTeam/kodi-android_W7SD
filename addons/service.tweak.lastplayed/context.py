import sys
import xbmc

from lib import watchedcount

# DEPRECATED: StringCompare in addon.xml is deprecated in Krypton, gone in Leia,
#  but both resolve to False when unrecognized so the result is the same for all versions

def main(mode):
    listitem = sys.listitem
    mediatype = get_mediatype(listitem)
    dbid = get_dbid(listitem)
    if not dbid or not mediatype:
        return

    if mode == 'add':
        watchedcount.add_one(dbid, mediatype)
    elif mode == 'remove':
        watchedcount.remove_one(dbid, mediatype)
    elif mode == 'clearresume':
        watchedcount.clear_resume(dbid, mediatype)

def get_mediatype(listitem):
    try:
        return listitem.getVideoInfoTag().getMediaType()
    except AttributeError:
        # DEPRECATED: Before Krypton
        pass
    count = 0
    mediatype = xbmc.getInfoLabel('ListItem.DBTYPE')
    while not mediatype and count < 5:
        count += 1
        xbmc.sleep(200)
        mediatype = xbmc.getInfoLabel('ListItem.DBTYPE')
    if not mediatype:
        xbmc.executebuiltin('Notification(Watched status toolbox cannot proceed, "Got an unexpected media type. Try again, it should work.", 6000, DefaultIconWarning.png)')
    return mediatype

def get_dbid(listitem):
    try:
        return listitem.getVideoInfoTag().getDbId()
    except AttributeError:
        # DEPRECATED: Before Krypton
        pass
    if listitem.getLabel() != xbmc.getInfoLabel('ListItem.Label'):
        # InfoLabels can report the wrong item
        return int(listitem.getfilename().split('?')[0].rstrip('/').split('/')[-1])
    else:
        return int(xbmc.getInfoLabel('ListItem.DBID'))


if __name__ == '__main__':
    main('add')
