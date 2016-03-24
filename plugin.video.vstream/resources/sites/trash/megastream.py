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

import re,urllib2,urllib



SITE_IDENTIFIER = 'megastream'
SITE_NAME = 'Mega-stream'
SITE_DESC = ''

URL_MAIN = 'http://mega-stream.fr/'

MOVIE_NEWS = (URL_MAIN + 'accueil-films', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'accueil-films', 'showMovies')
 
MOVIE_GENRES = (True, 'showGenre')
 
URL_SEARCH = (URL_MAIN + '?s=', 'resultSearch')
FUNCTION_SEARCH = 'resultSearch'
   
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Tout Les Films', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText 
        resultSearch(sUrl)
        oGui.setEndOfDirectory()
        return

    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Animation',URL_MAIN + 'genre.php?g=Animation'] )    
    liste.append( ['Action',URL_MAIN + 'genre.php?g=Action'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'genre.php?g=Arts%20Martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'genre.php?g=Aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'genre.php?g=Biopic'] )
    liste.append( ['Comedie',URL_MAIN + 'genre.php?g=Com%C3%A9die'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'genre.php?g=Com%C3%A9die%20dramatique'] )
    liste.append( ['Documentaire',URL_MAIN + 'genre.php?g=Documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'genre.php?g=Drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'genre.php?g=Epouvante-horreur'] )
    liste.append( ['Espionage',URL_MAIN + 'genre.php?g=Espionnage'] )  
    liste.append( ['Fantastique',URL_MAIN + 'genre.php?g=Fantastique'] )
    liste.append( ['Famille',URL_MAIN + 'genre.php?g=Famille'] )
    liste.append( ['Guerre',URL_MAIN + 'genre.php?g=Guerre'] )
    liste.append( ['Historique',URL_MAIN + 'genre.php?g=Historique'] )
    liste.append( ['Musical',URL_MAIN + 'genre.php?g=Musical'] )
    liste.append( ['Policier',URL_MAIN + 'genre.php?g=Policier'] )
    liste.append( ['Romance',URL_MAIN + 'genre.php?g=Romance'] )
    liste.append( ['Sciense Fiction',URL_MAIN + 'genre.php?g=Science%20fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'genre.php?g=Thriller'] )
    liste.append( ['Western',URL_MAIN + 'genre.php?g=Western'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def resultSearch(sSearch):
    oGui = cGui()  

    sUrl = sSearch
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a class="tile_film" href="(.+?)">.+?<img src="(.+?)"/>.+?<h3>(.+?)</h3>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sThumbnail = URL_MAIN+str(aEntry[0])
            sTitle = str(aEntry[1])
            #sTitle = sTitle.replace('- Film Complet','')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            #oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
      

def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        count_tiles_film = int(oInputParameterHandler.getValue('count_tiles_film'))
    
    if 'infinite_scroll.php' in sUrl:
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        headers = {'User-Agent': UA ,
                   'Host' : 'mega-stream.fr'}
        
        post_data = {'catLatBar' : 'on',
                     'count_tiles_film': str(count_tiles_film),
                     'lat_bar_more_filters': 'dateSortie'}
                     
        req = urllib2.Request(sUrl , urllib.urlencode(post_data), headers)
        
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        response.close()
    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    oParser = cParser()
    
    sPattern = '<a class="tile_film" href="(.+?)">.+?<img src="(.+?)"/>.+?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sThumbnail = URL_MAIN+str(aEntry[1])
            siteUrl = URL_MAIN+str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[2], 'films.png', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oOutputParameterHandler.addParameter('count_tiles_film', str(count_tiles_film + 20))
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
         
def __checkForNextPage(sHtmlContent):
    return 'http://mega-stream.fr/fonctions/infinite_scroll.php'
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="checkShowlistVidQualite"\/>\s+<p>(.+?)<\/p>|<div class="vidQualite vidSelect" id="([0-9]+)">\s+<img class="video_langue_img" src="IMG\/flag\/(.+?).png"\/>\s+<p>(.+?)<\/p>'
    aResult = re.findall(sPattern,sHtmlContent)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[0])+'[/COLOR]')
                
            else:
                sTitle = '[COLOR skyblue]' + aEntry[3]+ '[/COLOR] ' + sMovieTitle
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sId', aEntry[1])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Getlink', sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()
    
def Getlink():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sId = oInputParameterHandler.getValue('sId')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    headers = {'User-Agent': UA ,
               'Host' : 'mega-stream.fr'}
    
    post_data = {'vid' : sId}
                 
    req = urllib2.Request('http://mega-stream.fr/fonctions/video.php' , urllib.urlencode(post_data), headers)
    
    response = urllib2.urlopen(req)
    sHtmlContent = response.read()
    response.close()
    
    oParser = cParser()
    sPattern = 'src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult

    if (aResult[0] == True):
                
            sHosterUrl = str(aResult[1][0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
    
