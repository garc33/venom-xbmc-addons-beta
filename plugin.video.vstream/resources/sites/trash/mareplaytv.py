#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re
import xbmc

#src="http://opentostream.com/embed.php?vid=617ef5adb" 

SITE_IDENTIFIER = 'mareplaytv'
SITE_NAME = 'MaReplayTV'
SITE_DESC = 'Replay TV Divers.'

URL_MAIN = 'http://mareplaytv.fr/'

URL_SEARCH = (URL_MAIN + '?post_type=video&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_GENRES = (True, 'showGenre')
REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = (URL_MAIN + 'videos/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_REPLAYTV[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_REPLAYTV[1], 'Toutes les videos', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = 'menu-item-[0-9]+ depth"><a href="([^"]+\/)">(.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    oGui = cGui()

    if (aResult[0] == True):

        for aEntry in aResult[1]:
            oOutputParameterHandler = cOutputParameterHandler()
            sTitle = str(aEntry[1])
            
            if 'Toutes les vidéos' in sTitle:
                break
            
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle , 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):

    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sUrl = sUrl.replace('https','http')
    xbmc.log('>' + sUrl + '<')    
    
    if not (sUrl == URL_MAIN):
        sPattern = '<div class="item-img">.+?<img.+?src="([^"]+)".+?<h3><a href="([^"]+)\/">([^<>]+)<'
    else:
        sPattern = '<div class="item-img"><a href="([^"]+)" title="([^"]+)"><img.+?src="([^"]+)"'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            if not (sUrl == URL_MAIN):
                sTitle = aEntry[2]
                sUrl2 = str(aEntry[1])
                sThumb = str(aEntry[0])
            else:
                sTitle = aEntry[1]
                sUrl2 = str(aEntry[0])
                sThumb = str(aEntry[2])
                
            sTitle = sTitle.replace('Replay du ','')
            sTitle = sTitle.replace('Emission du ','')
            sTitle = re.sub('([0-9]+ [a-zA-Z]+ [0-9]{4})','[\\1]', sTitle)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'replay.png',  sThumb,  sThumb, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class=.page-numbers current.>[0-9]+<\/span><\/li><li><a class=.page-numbers. href=["\']([^"\']+)["\']>[0-9]+<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
