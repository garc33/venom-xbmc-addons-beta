#-*- coding: utf-8 -*-
#Par jojotango
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

SITE_IDENTIFIER = 'neuf_docu'
SITE_NAME = '9Docu'
SITE_DESC = 'Site pour Telecharger ou Regarder des Documentaires et Emissions TV Gratuitement'

URL_MAIN = 'http://www.9docu.com/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_GENRES = (True, 'showGenre')
DOC_DOCS = (URL_MAIN, 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaire Nouveautées', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Documentaire Genre', 'genres.png', oOutputParameterHandler)

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
    oGui = cGui()
    liste = []
    liste.append( ['[COLOR teal]CATEGORIES[/COLOR]', ''] )
    liste.append( ['Séries Documentaires',  URL_MAIN + 'categorie/series-documentaires/'] )
    liste.append( ['Documentaires Exclus',  URL_MAIN + 'categorie/documentaires-exclus/'] )
    liste.append( ['Documentaires Inédits',  URL_MAIN + 'categorie/documentaires-inedits/'] )
    liste.append( ['Films Documentaires',  URL_MAIN + 'categorie/films-documentaires/'] )
    liste.append( ['Emissions Documentaires / Replay TV',  URL_MAIN + 'categorie/emissions-documentaires-replay-tv/'] )

    liste.append( ['[COLOR teal]GENRES[/COLOR]', ''] )
    liste.append( ['Actualités',  URL_MAIN + 'categorie/actualites/'] )
    liste.append( ['Animaux',  URL_MAIN + 'categorie/animaux/'] )
    liste.append( ['Architecture',  URL_MAIN + 'categorie/architecture/'] )
    liste.append( ['Art martiaux',  URL_MAIN + 'categorie/art-martiaux/'] )
    liste.append( ['Arts',  URL_MAIN + 'categorie/arts/'] )
    liste.append( ['Auto/Moto',  URL_MAIN + 'categorie/auto-moto/'] )
    liste.append( ['Aventure',  URL_MAIN + 'categorie/aventure/'] )
    liste.append( ['Biopic',  URL_MAIN + 'categorie/biopic/'] )
    liste.append( ['Cinéma/Film',  URL_MAIN + 'categorie/cinema-film/'] )
    liste.append( ['Civilisation',  URL_MAIN + 'categorie/civilisation/'] )
    liste.append( ['Consommation',  URL_MAIN + 'categorie/consommation/'] )
    liste.append( ['Cuisine',  URL_MAIN + 'categorie/cuisine/'] )
    liste.append( ['Culture/Littérature',  URL_MAIN + 'categorie/culturelitterature/'] )
    liste.append( ['Divertissement',  URL_MAIN + 'categorie/divertissement/'] )
    liste.append( ['Economie',  URL_MAIN + 'categorie/economie/'] )
    liste.append( ['Education',  URL_MAIN + 'categorie/education/'] )
    liste.append( ['Emission TV',  URL_MAIN + 'categorie/emission/'] )
    liste.append( ['Emploi/Métier',  URL_MAIN + 'categorie/emploi-metier/'] )
    liste.append( ['Enquete',  URL_MAIN + 'categorie/enquete/'] )
    liste.append( ['Environnement',  URL_MAIN + 'categorie/environnement/'] )
    liste.append( ['Espionnage',  URL_MAIN + 'categorie/espionnage/'] )
    liste.append( ['Famille',  URL_MAIN + 'categorie/famille/'] )
    liste.append( ['Guerre',  URL_MAIN + 'categorie/guerre/'] )
    liste.append( ['Histoire',  URL_MAIN + 'categorie/histoire/'] )
    liste.append( ['Humour',  URL_MAIN + 'categorie/humour/'] )
    liste.append( ['Investigations',  URL_MAIN + 'categorie/investigations/'] )
    liste.append( ['Jeux vidéo/TV',  URL_MAIN + 'categorie/jeux-video-tv/'] )
    liste.append( ['Justice/Criminalité',  URL_MAIN + 'categorie/justice-criminalite/'] )
    liste.append( ['Magazine',  URL_MAIN + 'categorie/magazine/'] )
    liste.append( ['Médias',  URL_MAIN + 'categorie/medias/'] )
    liste.append( ['Mode',  URL_MAIN + 'categorie/mode/'] )
    liste.append( ['Musique',  URL_MAIN + 'categorie/musique/'] )
    liste.append( ['Nature',  URL_MAIN + 'categorie/nature/'] )
    liste.append( ['People',  URL_MAIN + 'categorie/people/'] )
    liste.append( ['Politique',  URL_MAIN + 'categorie/politique/'] )
    liste.append( ['Religion',  URL_MAIN + 'categorie/religion/'] )
    liste.append( ['Reportage',  URL_MAIN + 'categorie/reportage/'] )
    liste.append( ['Santé/Bien-etre',  URL_MAIN + 'categorie/sante-bien-etre/'] )
    liste.append( ['Science/Technologie',  URL_MAIN + 'categorie/science-technologie/'] )
    liste.append( ['Sexualité',  URL_MAIN + 'categorie/sexualite/'] )
    liste.append( ['Société',  URL_MAIN + 'categorie/societe/'] )
    liste.append( ['Sport/Football/Auto/Moto',  URL_MAIN + 'categorie/sport-football-auto-moto/'] )
    liste.append( ['Telerealite',  URL_MAIN + 'categorie/telerealite/'] )
    liste.append( ['Tourisme',  URL_MAIN + 'categorie/tourisme/'] )
    liste.append( ['Voyage/Decouverte',  URL_MAIN + 'categorie/voyage-decouverte/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')

    sPattern = '<h2><a href="([^<]+)" rel="bookmark" title="[^"]+">([^<]+)<\/a>.+?" src="([^<]+)" \/>.+?<\/p><p style[^<>]+>(.+?)<\/p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', aEntry[2], aEntry[3], oOutputParameterHandler)

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
    sPattern = '<li class="first_last_page"><a href=".+?">.+?</a></li><li><a href="(.+?)"'
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
    # sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')

    oParser = cParser()
    sPattern = '<span class="15"><a href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
