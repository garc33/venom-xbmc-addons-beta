#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.contextElement import cContextElement
from resources.lib.gui.guiElement import cGuiElement

from resources.lib.config import cConfig
from resources.lib.db import cDb
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.epg import cePg
from resources.lib.parser import cParser

import xbmc,sys
import xbmcgui
import xbmcplugin
import urllib
import unicodedata,re
import xbmc

def CleanName(str):
    
    #vire accent et '\'
    try:
        str = unicode(str, 'utf-8')#converti en unicode pour aider aux convertions
    except:
        pass
    str = unicodedata.normalize('NFD', str).encode('ascii', 'ignore').decode("unicode_escape")
    str = str.encode("utf-8") #on repasse en utf-8
    
    #vire tag
    str = re.sub('[\(\[].+?[\)\]]','', str)
    #vire caractere special
    str = re.sub("[^a-zA-Z0-9 ]", "",str)
    #tout en minuscule
    str = str.lower()
    #vire espace double
    str = re.sub(' +',' ',str)

    #vire espace a la fin
    if str.endswith(' '):
        str = str[:-1]
        

    return str



class cGui():

    SITE_NAME = 'cGui'
    CONTENT = 'files'

    def addMovie(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
        cGui.CONTENT = "movies"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMeta(1)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setMovieFanart()
        oGuiElement.setCat(1)
        
        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        self.addFolder(oGuiElement, oOutputParameterHandler)
        
        
    def addTV(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
        cGui.CONTENT = "tvshows"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMeta(2)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setTvFanart()
        oGuiElement.setCat(2)
        
        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)
        
        
        self.addFolder(oGuiElement, oOutputParameterHandler)
        
    def addMisc(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
        cGui.CONTENT = "files"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMeta(0)
        oGuiElement.setDirFanart(sIcon)
        oGuiElement.setCat(5)
        
        oGuiElement.setDescription(sDesc)
        
        self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
        
        self.addFolder(oGuiElement, oOutputParameterHandler)
        
    def addFav(self, sId, sFunction, sLabel, sIcon, sThumbnail, fanart, oOutputParameterHandler = ''):
        cGui.CONTENT = "files"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(0)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(fanart)
        
        self.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)
        
        self.addFolder(oGuiElement, oOutputParameterHandler, False)     
    
        
    def addDir(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler = ''):
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(0)

        oGuiElement.setDirFanart(sIcon)
        
        #oGuiElement.setFanart(self.sFanart)
        
        
            
        # if oOutputParameterHandler.getValue('sFanart'):
            # sFanart = oOutputParameterHandler.getValue('sFanart')
            # oGuiElement.setFanart(sFanart)
        
        oOutputParameterHandler.addParameter('sFav', sFunction)
        
        self.addFolder(oGuiElement, oOutputParameterHandler)
        
    def addNext(self, sId, sFunction, sLabel, oOutputParameterHandler):
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon('next.png')
        oGuiElement.setMeta(0)

        oGuiElement.setDirFanart('next.png')
        
        self.createContexMenuPageSelect(oGuiElement, oOutputParameterHandler)
        
        self.addFolder(oGuiElement, oOutputParameterHandler)

    def addNone(self, sId):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction('load')
        oGuiElement.setTitle('[COLOR= red]'+cConfig().getlanguage(30204)+'[/COLOR]')
        oGuiElement.setIcon('none.png')
        oGuiElement.setMeta(0)

        oOutputParameterHandler = cOutputParameterHandler()
        #oOutputParameterHandler.addParameter('siteUrl', 'none')

        self.addFolder(oGuiElement, oOutputParameterHandler)
        
    def addText(self, sId, sLabel,oOutputParameterHandler = ''):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction('DoNothing')
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon('none.png')
        oGuiElement.setMeta(0)

        oOutputParameterHandler = cOutputParameterHandler()
        #oOutputParameterHandler.addParameter('siteUrl', 'none')

        self.addFolder(oGuiElement, oOutputParameterHandler)    

    def addMovieDB(self, sId, sFunction, sLabel, sIcon, sThumbnail, sFanart, oOutputParameterHandler = ''):
        
        cGui.CONTENT = "movies"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(1)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sFanart)
        
        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)
        
        self.addFolder(oGuiElement, oOutputParameterHandler)
        
    def addTVDB(self, sId, sFunction, sLabel, sIcon, sThumbnail, sFanart, oOutputParameterHandler = ''):
        
        cGui.CONTENT = "tvshows"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(2)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sFanart)
        
        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)
        
        self.addFolder(oGuiElement, oOutputParameterHandler)

    def addDirectTV(self, sId, sFunction, sLabel, sIcon, sThumbnail, oOutputParameterHandler = ''):
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(0)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDirectTvFanart()
        oGuiElement.setCat(6)
        
        self.createContexMenuEpg(oGuiElement, oOutputParameterHandler)
        self.createContexMenuFav(oGuiElement, oOutputParameterHandler)

        self.addFolder(oGuiElement, oOutputParameterHandler)          

    
    def addFolder(self, oGuiElement, oOutputParameterHandler='', isFolder=True):
        
        if oOutputParameterHandler.getValue('siteUrl'):
            sSiteUrl = oOutputParameterHandler.getValue('siteUrl')
            oGuiElement.setSiteUrl(sSiteUrl)
            
        oListItem = self.createListItem(oGuiElement)
        
        # if oGuiElement.getMeta():
            # oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())
        
        
        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)
        
        #new context prend en charge les metas
        if cGui.CONTENT == "movies":
            self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
            #self.createContexMenuSimil(oGuiElement, oOutputParameterHandler)
            self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
            self.createContexMenuFav(oGuiElement, oOutputParameterHandler)

        elif cGui.CONTENT == "tvshows":
            self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
            self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
            self.createContexMenuFav(oGuiElement, oOutputParameterHandler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)
       
        sPluginHandle = cPluginHandler().getPluginHandle();

        xbmcplugin.addDirectoryItem(sPluginHandle, sItemUrl, oListItem, isFolder=isFolder)      
        

    def createListItem(self, oGuiElement):        

        oListItem = xbmcgui.ListItem(oGuiElement.getTitle(), oGuiElement.getTitleSecond(), oGuiElement.getIcon())
        oListItem.setInfo(oGuiElement.getType(), oGuiElement.getItemValues())
        oListItem.setThumbnailImage(oGuiElement.getThumbnail())
        
        #modif le 26/08
        oListItem.setProperty("IsPlayable", "true")
        oListItem.setProperty("Video", "true")
        #

        aProperties = oGuiElement.getItemProperties()
        for sPropertyKey in aProperties.keys():
            oListItem.setProperty(sPropertyKey, aProperties[sPropertyKey])

        return oListItem

    def createContexMenuWatch(self, oGuiElement, oOutputParameterHandler= ''):
        # oContext = cContextElement()
        # oContext.setFile('cGui')
        # oContext.setSiteName(oGuiElement.getSiteName())
        # oContext.setFunction('setWatched')
        # oContext.setTitle('[COLOR azure]Marquer vu/Non vu[/COLOR]')
        # oContext.setOutputParameterHandler(oOutputParameterHandler)
        # oGuiElement.addContextItem(oContext)
        self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cGui',oGuiElement.getSiteName(),'setWatched','[COLOR azure]Marquer vu/Non vu[/COLOR]')
        
    def createContexMenuPageSelect(self, oGuiElement, oOutputParameterHandler):
        #sSiteUrl = oGuiElement.getSiteName()
        
        oContext = cContextElement()
        
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        
        oContext.setFunction('selectpage')
        oContext.setTitle('[COLOR azure]Selectionner page[/COLOR]')
        oOutputParameterHandler.addParameter('OldFunction', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)
        
        oContext = cContextElement()
        
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        
        oContext.setFunction('viewback')
        oContext.setTitle('[COLOR azure]Retour Site[/COLOR]')
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)
        
        
    def createContexMenuFav(self, oGuiElement, oOutputParameterHandler= ''):
        oContext = cContextElement()     
        oContext.setFile('cFav')
        oContext.setSiteName('cFav')
        oContext.setFunction('setFavorite')
        oContext.setTitle('[COLOR teal]Marque-Page[/COLOR]')
        
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sFav', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())
        oContext.setOutputParameterHandler(oOutputParameterHandler)

        oGuiElement.addContextItem(oContext)  
        
    def createContexMenuDownload(self, oGuiElement, oOutputParameterHandler= '', status = '0'):

        if status == '0':
            # oContext = cContextElement()
            # oContext.setFile('cDownload')
            # oContext.setSiteName('cDownload')
            # oContext.setFunction('StartDownloadOneFile')
            # oContext.setTitle('Demarrer ce telechargement')
            # oContext.setOutputParameterHandler(oOutputParameterHandler)
            # oGuiElement.addContextItem(oContext)
            self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cDownload','cDownload','StartDownloadOneFile','Demarrer ce telechargement')
        
        if status == '0' or status == '2':
            # oContext = cContextElement()
            # oContext.setFile('cDownload')
            # oContext.setSiteName('cDownload')
            # oContext.setFunction('delDownload')
            # oContext.setTitle('Supprimer de la liste')
            # oContext.setOutputParameterHandler(oOutputParameterHandler)
            # oGuiElement.addContextItem(oContext)
            self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cDownload','cDownload','delDownload','Supprimer de la liste')
            
            # oContext = cContextElement()
            # oContext.setFile('cDownload')
            # oContext.setSiteName('cDownload')
            # oContext.setFunction('DelFile')
            # oContext.setTitle('[COLOR=red]Supprimer definitivement[/COLOR]')
            # oContext.setOutputParameterHandler(oOutputParameterHandler)
            # oGuiElement.addContextItem(oContext)
            self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cDownload','cDownload','DelFile','[COLOR=red]Supprimer definitivement[/COLOR]')
            
        if status == '1':
            # oContext = cContextElement()
            # oContext.setFile('cDownload')
            # oContext.setSiteName('cDownload')
            # oContext.setFunction('StopDownloadList')
            # oContext.setTitle('Arreter le telechargement')
            # oContext.setOutputParameterHandler(oOutputParameterHandler)
            # oGuiElement.addContextItem(oContext)
            self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cDownload','cDownload','StopDownloadList','Arreter le telechargement')
            
        if status == '2':
            # oContext = cContextElement()
            # oContext.setFile('cDownload')
            # oContext.setSiteName('cDownload')
            # oContext.setFunction('ReadDownload')
            # oContext.setTitle('Lire')
            # oContext.setOutputParameterHandler(oOutputParameterHandler)
            # oGuiElement.addContextItem(oContext)
            self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cDownload','cDownload','ReadDownload','Lire')
            self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cDownload','cDownload','ResetDownload','Reset')
        
    def createContexMenuinfo(self, oGuiElement, oOutputParameterHandler= ''):
        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName(oGuiElement.getSiteName())
        oContext.setFunction('viewinfo')
        oContext.setTitle('[COLOR azure]Information[/COLOR]')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())
      
        oContext.setOutputParameterHandler(oOutputParameterHandler)

        oGuiElement.addContextItem(oContext)
        

    
    def createContexMenuSimil(self, oGuiElement, oOutputParameterHandler= ''):
        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName(oGuiElement.getSiteName())
        oContext.setFunction('viewsimil')
        oContext.setTitle('[COLOR azure]Recherche Similaire[/COLOR]')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getFileName())
      
        oContext.setOutputParameterHandler(oOutputParameterHandler)

        oGuiElement.addContextItem(oContext)
        
    def CreateSimpleMenu(self,oGuiElement,oOutputParameterHandler,file,name,function,title):
        oContext = cContextElement()     
        oContext.setFile(file)
        oContext.setSiteName(name)
        oContext.setFunction(function)
        oContext.setTitle(title)
        
        oContext.setOutputParameterHandler(oOutputParameterHandler)

        oGuiElement.addContextItem(oContext)
        
    def createContexMenuDelFav(self, oGuiElement, oOutputParameterHandler= ''):
        #oContext = cContextElement()
        #oContext.setFile('cFav')
        #oContext.setSiteName('cFav')
        #oContext.setFunction('delFavourites')
        #oContext.setTitle('[COLOR red]'+cConfig().getlanguage(30209)+'[/COLOR]')      
        #oContext.setOutputParameterHandler(oOutputParameterHandler)
        #oGuiElement.addContextItem(oContext)
        self.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cFav','cFav','delFavourites','[COLOR red]'+cConfig().getlanguage(30209)+'[/COLOR]')
        
    def createContexMenuEpg(self, oGuiElement, oOutputParameterHandler= ''):

        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        oContext.setFunction('direct_epg')
        oContext.setTitle('Guide tv direct')
      
        oContext.setOutputParameterHandler(oOutputParameterHandler)

        oGuiElement.addContextItem(oContext)
        
        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        oContext.setFunction('soir_epg')
        oContext.setTitle('Guide tv soir')
      
        oContext.setOutputParameterHandler(oOutputParameterHandler)

        oGuiElement.addContextItem(oContext)
    
    
    def __createContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath();
        aContextMenus = []

        #Menus classiques reglés a la base
        if (len(oGuiElement.getContextItems()) > 0):
            for oContextItem in oGuiElement.getContextItems():                
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)                
                aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

            #oListItem.addContextMenuItems(aContextMenus)
            oListItem.addContextMenuItems(aContextMenus, True)    

        #Ajout de voir marque page
        oContextItem = cContextElement()
        oContextItem.setFile('cFav')
        oContextItem.setSiteName('cFav')
        oContextItem.setTitle('[COLOR teal]'+cConfig().getlanguage(30210)+'[/COLOR]')
        oContextItem.setFunction('getFavourites')
        oOutputParameterHandler = oContextItem.getOutputParameterHandler()
        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&contextFav=true&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
        aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.Container.Update(%s)" % (sTest,),)]
        oListItem.addContextMenuItems(aContextMenus)
        
        #Menu speciaux si metadata
        if  oGuiElement.getTrailerUrl(): 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sHosterIdentifier', 'youtube')
            oOutputParameterHandler.addParameter('sMediaUrl', oGuiElement.getTrailerUrl())
            oOutputParameterHandler.addParameter('sFileName', oGuiElement.getTitle())
            oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
            oContextItem = cContextElement()
            oContextItem.setFile('cHosterGui')
            oContextItem.setSiteName('cHosterGui')
            oContextItem.setTitle('[COLOR azure]Bande Annonce[/COLOR]')
            oContextItem.setFunction('play')
            oContextItem.setOutputParameterHandler(oOutputParameterHandler)
            
            oOutputParameterHandler = oContextItem.getOutputParameterHandler()
            sParams = oOutputParameterHandler.getParameterAsUri()
            sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
            aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]
            oListItem.addContextMenuItems(aContextMenus)
        
        return oListItem
        
    def __ContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath();
        aContextMenus = []

        if (len(oGuiElement.getContextItems()) > 0):
            for oContextItem in oGuiElement.getContextItems():                
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)                
                aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

            oListItem.addContextMenuItems(aContextMenus)
            #oListItem.addContextMenuItems(aContextMenus, True)

        return oListItem
     
    def __ContextMenuPlay(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath();
        aContextMenus = []

        if (len(oGuiElement.getContextItems()) > 0):
            for oContextItem in oGuiElement.getContextItems():                
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)                
                aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

            oListItem.addContextMenuItems(aContextMenus)
            #oListItem.addContextMenuItems(aContextMenus, True)

        return oListItem

    def setEndOfDirectory(self):
        iHandler = cPluginHandler().getPluginHandle()
        xbmcplugin.setPluginCategory(iHandler, "")
        xbmcplugin.setContent(iHandler, cGui.CONTENT)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(iHandler, True)

    def updateDirectory(self):
        xbmc.executebuiltin("Container.Refresh")
        
    def viewback(self):
        sPluginPath = cPluginHandler().getPluginPath();
        oInputParameterHandler = cInputParameterHandler()        
        sParams = oInputParameterHandler.getAllParameter()
        
        sId = oInputParameterHandler.getValue('sId')
        
        sTest = '%s?site=%s' % (sPluginPath, sId)
        xbmc.executebuiltin('XBMC.Container.Update(%s, replace)' % sTest )
        
    def viewsimil(self):
        sPluginPath = cPluginHandler().getPluginPath();
        oInputParameterHandler = cInputParameterHandler()        
        sTitle = oInputParameterHandler.getValue('sTitle')
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('searchtext', sTitle)
        oOutputParameterHandler.addParameter('disp', 'search1')
        oOutputParameterHandler.addParameter('readdb', 'False')
         
        sParams = oOutputParameterHandler.getParameterAsUri()               
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, 'cHome', 'searchMovie', sParams)
        xbmc.executebuiltin('XBMC.Container.Update(%s)' % sTest )
        return False
        
     
    def selectpage(self):
        sPluginPath = cPluginHandler().getPluginPath();
        oInputParameterHandler = cInputParameterHandler()        
        #sParams = oInputParameterHandler.getAllParameter()

        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        
        oParser = cParser()
        oldNum = oParser.getNumberFromString(siteUrl)
        newNum = 0
        if oldNum:
            newNum = self.showNumBoard()
        if newNum:
            try:
                siteUrl = siteUrl.replace(oldNum,newNum)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)                
                xbmc.executebuiltin('XBMC.Container.Update(%s)' % sTest )
            except:
                return False
        
        return False     

        
    def selectpage2(self):
        sPluginPath = cPluginHandler().getPluginPath();
        oInputParameterHandler = cInputParameterHandler()        
        #sParams = oInputParameterHandler.getAllParameter()

        sId = oInputParameterHandler.getValue('sId')
        sUrlBase = oInputParameterHandler.getValue('siteUrlbase')
        sMaxpage = oInputParameterHandler.getValue('MaxPage')
        
        sTest = '%s?site=%s' % (sPluginPath, sId)
        sTest = sTest +'&function=showPage&siteUrlbase=' + urllib.quote(sUrlBase) + '&MaxPage=' + str(sMaxpage)
        xbmc.executebuiltin('XBMC.Container.Update(%s, replace)' % sTest )
    
    def setWatched(self):

        oInputParameterHandler = cInputParameterHandler()
       
        #aParams = oInputParameterHandler.getAllParameter()
        #print aParams
        
        sSite = oInputParameterHandler.getValue('siteUrl')
        sTitle = xbmc.getInfoLabel('ListItem.label')

        meta = {}      
        meta['title'] = sTitle
        meta['site'] = sSite

        row = cDb().get_watched(meta)
        if row:
            cDb().del_watched(meta)
            cDb().del_resume(meta)
        else:
            cDb().insert_watched(meta)
        xbmc.executebuiltin( 'Container.Refresh' )
        
        
    def viewinfo(self):
 
        oGuiElement = cGuiElement()
        oInputParameterHandler = cInputParameterHandler()

        sTitle = oInputParameterHandler.getValue('sTitle')
        sId = oInputParameterHandler.getValue('sId')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sYear = oInputParameterHandler.getValue('sYear')
        sMeta = oInputParameterHandler.getValue('sMeta')
 
        #sMeta = 1 >> film sMeta = 2 >> serie
        sCleanTitle = CleanName(sFileName)
        
        #on vire saison et episode
        if (True):#sMeta == 2:
            sCleanTitle = re.sub('(?i).pisode [0-9]+', '',sCleanTitle)
            sCleanTitle = re.sub('(?i)saison [0-9]+', '',sCleanTitle)
            sCleanTitle = re.sub('(?i)S[0-9]+E[0-9]+', '',sCleanTitle)
            sCleanTitle = re.sub('(?i)[S|E][0-9]+', '',sCleanTitle)
        
        ui = cConfig().WindowsBoxes(sTitle,sCleanTitle, sMeta,sYear)
    
    # def viewinfo2(self):
 
        # oInputParameterHandler = cInputParameterHandler()

        # sTitle = oInputParameterHandler.getValue('sTitle')
        # sId = oInputParameterHandler.getValue('sId')
        # sFileName = oInputParameterHandler.getValue('sFileName')          
        
        # xbmc.executebuiltin("Action(Info)")
        
    def direct_epg(self):
        oGuiElement = cGuiElement()
        oInputParameterHandler = cInputParameterHandler()
        #aParams = oInputParameterHandler.getAllParameter()
        #print aParams
        sTitle = oInputParameterHandler.getValue('sMovieTitle')
        sCom = cePg().get_epg(sTitle,'direct')
        
        
    def soir_epg(self):
        oGuiElement = cGuiElement()
        oInputParameterHandler = cInputParameterHandler()

        sTitle = oInputParameterHandler.getValue('sMovieTitle')
        sCom = cePg().get_epg(sTitle,'soir')


    def __createItemUrl(self, oGuiElement, oOutputParameterHandler=''):
        if (oOutputParameterHandler == ''):
            oOutputParameterHandler = cOutputParameterHandler()
            
        sParams = oOutputParameterHandler.getParameterAsUri()
        
        #cree une id unique
        # if oGuiElement.getSiteUrl():
            # print  str(hash(oGuiElement.getSiteUrl()))
            
        
        sPluginPath = cPluginHandler().getPluginPath();

        if (len(oGuiElement.getFunction()) == 0):
            sItemUrl = '%s?site=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), urllib.quote_plus(oGuiElement.getTitle()), sParams)
        else:
            sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), oGuiElement.getFunction(), urllib.quote_plus(oGuiElement.getTitle()), sParams)
            
        #print sItemUrl
        return sItemUrl

    def showKeyBoard(self, sDefaultText=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False
        
    def showNumBoard(self, sDefaultNum=''):
        dialog = xbmcgui.Dialog()
        numboard = dialog.numeric(0, 'Entrer la page', sDefaultNum)
        #numboard.doModal()
        if numboard != None:
                return numboard

        return False
      

    def openSettings(self):
        cConfig().showSettingsWindow()

    def showNofication(self, sTitle, iSeconds=0):
        if (cConfig().isDharma() == False):
            return

	if (iSeconds == 0):
            iSeconds = 1000
	else:
            iSeconds = iSeconds * 1000
        
        xbmc.executebuiltin("Notification(%s,%s,%s)" % (cConfig().getlanguage(30308), (cConfig().getlanguage(30309) % str(sTitle)), iSeconds))

    def showError(self, sTitle, sDescription, iSeconds=0):
        if (cConfig().isDharma() == False):
            return

	if (iSeconds == 0):
            iSeconds = 1000
	else:
            iSeconds = iSeconds * 1000

        xbmc.executebuiltin("Notification(%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds))

    def showInfo(self, sTitle, sDescription, iSeconds=0):
        if (cConfig().isDharma() == False):
            return

	if (iSeconds == 0):
            iSeconds = 1000
	else:
            iSeconds = iSeconds * 1000

        xbmc.executebuiltin("Notification(%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds))
