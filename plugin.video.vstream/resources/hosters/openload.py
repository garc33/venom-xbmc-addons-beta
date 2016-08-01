#coding: utf-8
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
        #self.__sUrl = self.__sUrl.replace('/embed/', '/f/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
            #'Referer' : url ,
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Accept-Encoding' : 'gzip, deflate, br',
            #'Accept-Charset' : '',
            }
        
        api_call = ''
        
        oParser = cParser()        
        
        #recuperation donnee codage, non utilise encore, j'attend de voir ce qu'ils vont chnager
        oRequest = cRequestHandler("https://openload.co/assets/js/obfuscator/final.js")
        sHtmlContent = oRequest.request()
        
        #recuperation de la page
        xbmc.log(self.__sUrl)

        request = urllib2.Request(self.__sUrl,None,headers)
        try: 
            reponse = urllib2.urlopen(request)
        except urllib2.URLError, e:
            cGui().showInfo("Erreur", 'Probleme site' , 5)
            xbmc.log( str(e.reason))
            xbmc.log( e.read())
            return False,False
        sHtmlContent = reponse.read()
        reponse.close()
        
        linkimg = ""
        sPattern = '<img id="linkimg" src="data:image\/png;base64,(.+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            linkimg = aResult[1][0]
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        TabUrl = []
        subscribers = []


        decoded = base64.decodestring(linkimg)
        
        #g = open("c://out.png", "wb")
        #g.write(decoded)
        #g.close()
        
        #return width, height, pixels and image metadata
        r = Reader(pixels=decoded)
        Png_Data = r.read()
        #xbmc.log(str(Png_Data[2]))
        
        tabpixelchar = ''
        for i in Png_Data[2]:
            tabpixelchar = tabpixelchar + chr(i)
            
        #xbmc.log(str(tabpixelchar))
        
        j = 0;
        tab2 = []
        for i in tabpixelchar:
            v = (j + 1) % 4
            v = v and (i != "\x00")
            tab2.append(v)
            j= j + 1
        
        # parsed = document.getElementById(linkimg)
        # buff = document.getElementById(canvas).getContext("2d");

        # #buff[_0xcd25[5]](parsed, 0, 0);
        # var subscriptions = [].map.call(buff.getImageData(0, 0, parsed.width, parsed.height)["data"], function(deepDataAndEvents) {
          # return String.fromCharCode(deepDataAndEvents);
        # }).filter(function(dataAndEvents, deepDataAndEvents) {
          # return(deepDataAndEvents + 1) % 4 && dataAndEvents !== "\x00";
        # }).join("");
        
        #recuperation cle
        cle = ''
        oRequest = cRequestHandler("https://openload.co/assets/js/obfuscator/numbers.js")
        sHtmlContent = oRequest.request()
        sPattern = "window\.signatureNumbers='([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            cle = aResult[1][0]
        
        
        
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
            
            #http://www.dotnetperls.com/2d-python
            subscribers.append([])
            subscribers[id] = []
            
            stri = "1" * id

            if re.match('^1?$|^(11+?)\1+$',stri,re.IGNORECASE):
                id += 1
                continue
                
            currentValue = 99
        
            i = 0
            while (i < len(tabcle) ):

                recordName = 0
                    
                while (recordName < len(tabcle[id][i]) ):
                    if (currentValue > 122):
                        currentValue = 98

                    vv = chr(int(math.floor(currentValue)))
                    
                    if (tabcle[id][i][recordName] == vv) :
                       
                        #if (subscribers[id][i]):
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
            if not re.match('^1?$|^(11+?)\1+$',stri,re.IGNORECASE):
                v = "".join(subscribers[id]).replace(',','')
                TabUrl.append(v)
            id = id +1
        

        streamurl = TabUrl[2] + "~" + TabUrl[1] + "~" + TabUrl[3] + "~" + TabUrl[0]
                
        # if (!Array(id + 1).join(1).match(/^1?$|^(11+?)\1+$/)) {
        # TabUrl.push(subscribers[id].filter(function(dataAndEvents) {
          # return dataAndEvents !== ',';
        # }).join(""));
        
        api_call = "https://openload.co/stream/" + streamurl + "?mime=true"
        
        xbmc.log(api_call)
        return False
        
        if (api_call):
            
            if 'openload.co/stream' in api_call:
                UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
                headers = {'User-Agent': UA }
                          
                req = urllib2.Request(api_call,None,headers)
                res = urllib2.urlopen(req)
                finalurl = res.geturl()
                #xbmc.log(finalurl)
                api_call = finalurl

            return True, api_call
            
        return False, False
