#coding: utf-8
#
#Vstream : https://github.com/LordVenom/venom-xbmc-addon
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.jjdecode import JJDecoder
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.gui.gui import cGui
import re,urllib2, base64, math

#https://github.com/jcrocholl/pypng/blob/master/lib/png.py
from resources.lib.png import Reader
#or more powerfull https://github.com/Scondo/purepng/blob/master/code/png/png.py
import xbmc

#If you want to use this code, don't forget the credit this time, thx.

def parseInt(sin):
    return int(''.join([c for c in re.split(r'[,.]',str(sin))[0] if c.isdigit()])) if re.match(r'\d+', str(sin), re.M) and not callable(sin) else None

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Openload'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'#[COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'openload'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('openload.io','openload.co')
        #self.__sUrl = self.__sUrl.replace('/embed/', '/f/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        
        api_call = ''
        
        oParser = cParser()        
        
        #recuperation de la page
        xbmc.log('url teste : ' + self.__sUrl)
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent',UA)
        sHtmlContent = oRequest.request()
        #fh = open('c:\\openload2.htm', "r")
        #sHtmlContent = fh.read()
        #fh.close()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        linkimg = ""
        sPattern = '<img id="linkimg" src="data:image\/png;base64,(.+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            linkimg = aResult[1][0]
        
        #recuperation cle
        cle = ''
        oRequest = cRequestHandler("https://openload.co/assets/js/obfuscator/numbers.js")
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        oRequest.addHeaderEntry('User-Agent',UA)
        sHtmlContent = oRequest.request()

        sPattern = "window\.signatureNumbers='([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            cle = aResult[1][0]
           
        #recuperation donnee codage, non utilise encore, j'attend de voir ce qu'ils vont chnager
        oRequest = cRequestHandler("https://openload.co/assets/js/obfuscator/final.js")
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        oRequest.addHeaderEntry('User-Agent',UA)
        sHtmlContent = oRequest.request()
        
        #-------------------------------------
        #          Debut algorythme
        #-------------------------------------
        
        TabUrl = []
        subscribers = []

        decoded = base64.decodestring(linkimg)
        
        #g = open("c://out.png", "wb")
        #g.write(decoded)
        #g.close()
        
        #return width, height, pixels and image metadata
        r = Reader(pixels=decoded)
        Png_Data = r.read()
        
        tabpixelchar = ''
        for i in Png_Data[2]:
            tabpixelchar = tabpixelchar + chr(i)
        
        j = 0;
        tab2 = []
        for i in tabpixelchar:
            v = (j + 1) % 4
            v = v and (i != "\x00")
            tab2.append(v)
            j= j + 1
        

        tab3 = []
        nbr = int(len(tabpixelchar) / (20 * 10))
        pattern = ".{1," + str(nbr * 20) + "}"
        r1 = re.findall(pattern, tabpixelchar)
        
        pattern = ".{1,20}"
        for i in r1:
            r2 = re.findall(pattern, i)
            #TODO correct this hack
            if '\x00' not in r2[0]:
                tab3.append(r2)
        
        tabcle = []
        nbr = int(len(cle) / (26 * 10))
        pattern = ".{1," + str(nbr * 26) + "}"
        r2 = re.findall(pattern, cle)
        
        pattern = ".{1,26}"
        for i in r2:
            r2 = re.findall(pattern, i)
            tabcle.append(r2)
        
        currentValue = 0
        id = 0
        i = 0
        
        subscribers = []
        
        while (id < len(tab3) ):
            
            subscribers.append([])
            subscribers[id] = []
            
            stri = "1" * id

            if re.match('^1?$|^(11+?)\1+$',stri,re.IGNORECASE):
                id += 1
                continue
                
            currentValue = 99
        
            i = 0
            while (i <= len(tabcle) ):

                recordName = 0
                    
                while (recordName < len(tabcle[id][i]) ):
                    if (currentValue > 122):
                        currentValue = 98

                    vv = chr(int(math.floor(currentValue)))
                    
                    if (tabcle[id][i][recordName] == vv) :
                       
                        if (len(subscribers[id]) > i ):
                            recordName +=1
                            continue
                            
                        currentValue += 2.5
                        
                        try:
                            subscribers[id].append(tab3[id][i][recordName])
                        except:
                            pass
                            
                        
                    recordName +=1
              
                i = i + 1 
            
            id = id + 1

        TabUrl = []

        id = 0;
        while (id < 10):
            stri = "1" * id
            #TODO : why this fucking regex don't work ???
            #if not re.match('^1?$|^(11+?)\1+$',stri):
            if str(id) in '2357':
                v = "".join(subscribers[id]).replace(',','')
                TabUrl.append(v)
            id = id +1
        
        xbmc.log(str(TabUrl))
        
        streamurl = TabUrl[3] + "~" + TabUrl[1] + "~" + TabUrl[2] + "~" + TabUrl[0]
        
        api_call = "https://openload.co/stream/" + streamurl + "?mime=true"
        
        xbmc.log(api_call)
        
        if (api_call):
            
            if 'openload.co/stream' in api_call:
                
                headers = {'User-Agent': UA }
                          
                req = urllib2.Request(api_call,None,headers)
                res = urllib2.urlopen(req)
                finalurl = res.geturl()
                #xbmc.log(finalurl)
                api_call = finalurl

            return True, api_call
            
        return False, False
