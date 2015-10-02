# -*- coding: utf-8 -*-
import sys
import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
_open_func_bak = open # Make a back up, just in case
open = codecs.open
import json
import ast
import bs4
import re

''' num records:
{name:'y-1995-m-3-d-27-h-2-sex-1-mode-1.json'}
    1900-2020  -------------- 120
                              365
                              12
                              2
                              3 (2)

亮度：庙、旺、利、得、平、落、陷
四化飞星：忌科禄权
'''

logging = None

class BaselinePan(object):
    '''missing stars: 31, 51,52,61, 博士天伤都是64'''
    STARS_LIST = None
    HTML_LINE_SEPARATOR = '<br>'

    @staticmethod
    def getName(inputs):
        name = '-'.join(['y', str(inputs['y']), 'm', str(inputs['m']), 'd', str(inputs['d']), 'h', str(inputs['h']), 'sex', str(inputs['sex']), 'mode', str(inputs['mode'])]) + '.json'
        return name
    
    def serializeToFile(self):
        jsonFile = open('data/' + self.name, 'w', encoding="utf-8")
        jsonFile.write(json.dumps(self.serialize(), ensure_ascii=False, indent=2))
        return self.name

    def serialize(self):    
        
        # jsonString = json.dumps(self.data, indent=4, ensure_ascii=False)
        jsonObj = {
            'name': self.name,
            'data': self.data
        }
        # jsonString = json.dumps(jsonObj, ensure_ascii=False)
        return jsonObj

    @staticmethod
    def readStarList():
        if (BaselinePan.STARS_LIST == None):
            starListFile = open('starList.json', 'r', encoding="utf-8")
            starList = json.load(starListFile)
            BaselinePan.STARS_LIST = starList

    @staticmethod
    def byteify(input):
        if isinstance(input, dict):
            return {BaselinePan.byteify(key):BaselinePan.byteify(value) for key,value in input.iteritems()}
        elif isinstance(input, list):
            return [BaselinePan.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def __init__(self, inputs, page, passedLogging):
        global logging
        logging = passedLogging
        self.data = dict()
        self.data['inputs'] = inputs
        self.data['twelveGongs'] = list()
        self.data['centerGong'] = dict()
        page = BaselinePan.replaceBRs(page)
        self.page = bs4.BeautifulSoup(page, 'html.parser')
        BaselinePan.readStarList()
        # logging.info(BaselinePan.getName(self.data['inputs']))
        self.name = BaselinePan.getName(self.data['inputs'])
        logging.debug(page)

    def printLines(self):
        lines = ''
        lines += 'COUNT_OF_LINE_SEPARATORS: '
        pageStr = str(self.page)
        count = pageStr.count(BaselinePan.HTML_LINE_SEPARATOR)
        lines += str(count)
        lines += '\n\n'
        for i in range(0, count-1):
            lines += '------- ' + str(i) + ' -------\n'
            lines += BaselinePan.getNthLineFromPage(pageStr, BaselinePan.HTML_LINE_SEPARATOR, i) + '\n'
        logging.info(lines)
        jsonFile = open('data/' + self.name + '-lines', 'w', encoding="utf-8")
        jsonFile.write(lines)
        return lines

    def setHTMLSeparator(self):
        pageStr = str(self.page)
        linkIdx = pageStr.find('<font color="blue">http://www.zhycw.com</font>') + len('<font color="blue">http://www.zhycw.com</font>')
        openBracketIdx = pageStr.find('<', linkIdx)
        closeBracketIdx = pageStr.find('>', linkIdx)
        separator = pageStr[openBracketIdx:closeBracketIdx+1]
        # logging.info('SEPARATOR: ' + separator + '\n')
        BaselinePan.HTML_LINE_SEPARATOR = separator
        if (separator == '<br/>'):
            self.page.br.extract()
            logging.info('NUM br: '+ pageStr.count('<br>'))
            logging.info('NUM br/: '+ pageStr.count('<br/>'))
            newpage = pageStr.replace(separator, '<br>')
            logging.info('new NUM br: '+ newpage.count('<br>'))
            logging.info('new NUM br/: '+ newpage.count('<br/>'))
            self.page = bs4.BeautifulSoup(newpage)
            logging.info('processed NUM br: '+ str(self.page).count('<br>'))
            logging.info('processed NUM br/: '+ str(self.page).count('<br/>'))
            BaselinePan.HTML_LINE_SEPARATOR = '<br>'
        return separator

    def initData(self):
        self.setHTMLSeparator()
        # self.printLines()
        self.setCenterGong()
        self.cleanUpCenterGong()
        self.setTwelveGongs()

    @staticmethod
    def replaceBRs(page):
        logging.debug(type(page))
        page = page.decode('utf-8')
        page = page.replace('<br/>', '<br>')
        return page


 #    0 1  2  3
    # 4       5
    # 6       7
    # 8 9  10 11

    # 0:no star 1:star 2:diamond

    # 1990-01-01
    # male:1, female:0,
    # life:1, decade:2, year:3
    def setTwelveGongs(self):
        horizontalSeparatorOne = self.page.find_all(text='┌───────────────────────────────────────┐')
        twelveGongs = self.data['twelveGongs']
        
        stages = self.page.find_all('font', color='#008000')
        for i in range(0, 12):
            currentGong = dict()
            twelveGongs.append(currentGong)
            currentGong['redStars'] = list()
            currentGong['magentaStars'] = list()
            currentGong['brownStars'] = list()
            currentGong['cyanStars'] = list()
            currentGong['blueStars'] = list()
            currentGong['stage'] = ''
            
            cyanStar = self.page.find('font', color='#009999').parent
            cyanStarId = BaselinePan.getTextFromA(cyanStar) #BaselinePan.getIdFromA(cyanStar)
            currentGong['cyanStars'].append(cyanStarId)
            logging.debug('type of cyanStar: ' + cyanStar.name)
            
            logging.debug('at this point len of stages: ' + str(len(stages)))
            if (cyanStar.name == 'a'):
                cyanStar.extract()
            
            logging.debug('how many 008000: ' + str(len(stages)));
            if (i >= 4):
                stage = stages[i+1]
            else:
                stage = stages[i]
            currentGong['stage'] = stage.string

        self.setMajorStars()
        

        myIter = iter([0,1,2,3,0,1,2,3,4,5,4,5,6,7,6,7,8,9,10,11,8,9,10,11])
        for i in range(24):
            blueStar = self.page.find_all('font', color='#000099')[i]
            index = myIter.next()
            twelveGongs[index]['blueStars'].append(BaselinePan.getIdFromA(blueStar.parent))
        
        myIter = iter([4,5,6,7,10,11,14,15,20,21,22,23])
        for i in range(12):
            index = myIter.next()
            sibs = [sib for sib in self.page.find_all('font', color='#000099')[index].parent.next_siblings]
            gongName = sibs[1].string
            if (gongName.find(u'★') != -1):
                twelveGongs[i]['star'] = True
            if (gongName.find(u'◆') != -1):
                twelveGongs[i]['diamond'] = True
            gongName = gongName.replace(u'◆', '')
            gongName = gongName.replace(u'★', '')
            twelveGongs[i]['gongName'] = gongName
            twelveGongs[i]['yearInLunar'] = sibs[3].string.strip()
            

        myIter = iter([0,1,2,3,8,9,12,13,16,17,18,19])
        for i in range(12):
            twelveGongs[i]['ageRange'] = ''
            index = myIter.next()
            # logging.info(i)
            sibs = [sib for sib in self.page.find_all('font', color='#000099')[index].parent.next_siblings]
            attempt = sibs[0].string.strip() 
            # logging.info(attempt)
            if (len(attempt) > 0 and attempt[0].isnumeric()):
                # logging.info('attempt success!')
                twelveGongs[i]['ageRange'] = attempt
        # for i in range(12):


        # pprint(twelveGongs)

    
    def prepareBarsForGong(self, bars, index):
        if (index == 0):
            bar1 = self.page.find(text=u'│')
            bar2 = self.page.find_all(text=u'│')[1]
            bar3 = self.page.find_all(text=re.compile(u'│'))[12].string
            bar4 = self.page.find_all(text=re.compile(u'│'))[12]
            while (bar4.name != 'br'):
                bar4 = bar4.next_element
            bars.append(bar1)
            bars.append(bar2)
            bars.append(bar3)
            bars.append(bar4)
        elif (index in [1,2,3,7,9,10,11]):

            for el in bars[0].next_siblings:
                if (el.string.find(u'│') != -1):
                    bars[0] = el
                    break

            if (find_nth(bars[0].string, u'│', 2) != -1):
                # this one contains 2 bars. split
                secondIdx = find_nth(bars[0].string, u'│', 2)
                bars[0].insert_after('<span>'+ bars[0].string[secondIdx:] +'</span>')
                bars[0].string = bars[0].string[:secondIdx]
            # for el in bars[1].next_siblings:
            #   if (el.string.find(u'│') != -1):
            #       bars[1] = el
            #       break
        elif (index in [4]):

            # mingSiHua = self.page.find_all(text=re.compile(u'命四化'))
            # if (len(mingSiHua) == 0):
            #     logging.debug('printing mingsihua page: ' + str(self.page))

            mingSiHua = self.mingSiHuaPrevTag
            
            for el in mingSiHua.previous_elements:
                if (u'│' in el):
                    bars[0] = el
                    break
            
            # panLeiTag = self.page.find_all(text=re.compile(u'盘类'))[0]
            # panLeiTag = panLeiTag.previous_element
            # for el in panLeiTag.previous_elements:
            #   if (u'│' in el):
            #       bars[1] = el
            #       break
        elif index in [5]:
            # mingSiHua = self.page.find_all(text=re.compile(u'命四化'))[0]
            # mingSiHua = mingSiHua.next_element
            mingSiHua = self.mingSiHuaPrevTag.next_element
            for el in mingSiHua.next_elements:
                if (u'│' in el):
                    bars[0] = el
                    break
            
            # panLeiTag = self.page.find_all(text=re.compile(u'盘类'))[0]
            # panLeiTag = panLeiTag.next_element
            # for el in panLeiTag.next_elements:
            #   if (u'│' in el):
            #       bars[1] = el
            #       break
        elif index in [6]:
            separator = self.page.find_all(text=re.compile(u'├─────────┤'))[1]
            separator = separator.next_element
            
            for el in separator.next_elements:
                if (u'│' in el):
                    bars[0] = el
                    break
        elif index in [8]:
            separator = self.page.find_all(text=re.compile(u'├─────────┼─────────┬─────────┼─────────┤'))
            separator = separator[len(separator) - 1]
            separator = separator.next_element
            for el in separator.next_elements:
                if (u'│' in el):
                    bars[0] = el
                    break




            # i = 0
            # for el in bars[0].next_elements:
            #   if (u'│' in str(el) and el.next_element.name == 'br' and u'│' in str(el.next_element.next_element)):
            #       logging.info(str(i) + '_____________________________________________________')
            #       logging.info(el.next_element.next_element)
            #       bars[0] = el.next_element.next_element
            #       break
            # i = 0
            # for el in bars[1].next_elements:
            #   if (u'│' in str(el) and el.next_element.name == 'br' and u'│' in str(el.next_element.next_element)):
            #       logging.info(str(i) + '_____________________________________________________')
            #       logging.info(el.next_element.next_element)
            #       bars[1] = el.next_element.next_element
            #       break
        

    def setMajorStars(self):
        bars = list()
        for i in range(12):
            self.prepareBarsForGong(bars, i)
            self.fillMajorStarsToGong(bars, i)
        
        self.fillMajorStarBrightness(bars)



        # TODO the last char        
        #self.page.find_all(text=re.compile(u'│'))[12]
        # for el in bar4.next_elements:

        # bars = self.page.find_all(text=re.compile(u'│'))
        # i = 0
        # for bar in bars:
        #   logging.info(i)
        #   i += 1
        #   logging.info(bar)

        # self.fillMajorStarsToGong(bars, twelveGongs[0])

        # titleText = self.page.find(text='├─────────┬─────────┬─────────┬─────────┤')
        # logging.info(titleText.string)
        # logging.info(titleText.next_element)
        # logging.info(titleText.next_element.name)
        # logging.info(titleText.next_element.next_element)
        # logging.info(titleText.next_element.next_element.string)
        # logging.info(titleText.next_element.next_element.next_element.string)


    def fillMajorStarsToGong(self, bars, gongIndex):
        bar1 = bars[0]
        # bar2 = bars[1]
        gong = self.data['twelveGongs'][gongIndex]

        current = bar1.next_sibling

        while (current.string.find(u'│') == -1):
            
            if (current.font['color'] == '#ff0000'):
                # logging.info('red')
                gong['redStars'].append([BaselinePan.getIdFromA(current), '', ''])
            elif (current.font['color'] == '#ff00ff'):
                # logging.info('magenta')
                gong['magentaStars'].append([BaselinePan.getIdFromA(current), '', ''])
            else:
                gong['brownStars'].append([BaselinePan.getIdFromA(current), '', ''])
                # logging.info('brown')
            current = current.next_sibling
        
        if (gongIndex == 6):
            bars[0] = current
            # current = bar2
            # for i in range(len(gong['redStars'])):
            #   current = current.next_sibling
            #   gong['redStars'][i][0] = gong['redStars'][i][0] + current.string

            # for i in range(len(gong['magentaStars'])):
            #   current = current.next_sibling
            #   gong['magentaStars'][i][0] = gong['magentaStars'][i][0] + current.string

            # for i in range(len(gong['brownStars'])):
            #   current = current.next_sibling
            #   gong['brownStars'][i][0] = gong['brownStars'][i][0] + current.string

    @staticmethod
    def getNthLineFromPage(page, delim, n):
        if (n == 0):
            n = 1
        firstDelim = n - 1
        start = find_nth(page, delim, firstDelim)
        end = find_nth(page, delim, firstDelim + 1)
        return page[start:end + len(delim)]

    @staticmethod
    def getNthLineFromPageDbg(page, delim, n):
        if (n == 0):
            n = 1
        firstDelim = n - 1
        start = find_nth(page, delim, firstDelim)
        logging.info(start)
        end = find_nth(page, delim, firstDelim + 1)
        logging.info(end)
        logging.info(page[start:end + len(delim)])
        return page[start:end + len(delim)]

    ''' n from 0 '''
    @staticmethod
    def setNthStarBrightnessOfGong(n, brightness, gong):
        if (n < len(gong['redStars'])):
            gong['redStars'][n][1] = brightness
        elif (n < len(gong['redStars']) + len(gong['magentaStars'])):
            index = n - len(gong['redStars'])
            gong['magentaStars'][index][1] = brightness
        elif (n < len(gong['redStars']) + len(gong['magentaStars']) + len(gong['brownStars'])):
            index = n - len(gong['redStars']) - len(gong['magentaStars'])
            gong['brownStars'][index][1] = brightness

    @staticmethod
    def setNthStarSecondBrightnessOfGong(n, brightness, gong):
        if (n < len(gong['redStars'])):
            gong['redStars'][n][2] = brightness
        elif (n < len(gong['redStars']) + len(gong['magentaStars'])):
            index = n - len(gong['redStars'])
            gong['magentaStars'][index][2] = brightness
        elif (n < len(gong['redStars']) + len(gong['magentaStars']) + len(gong['brownStars'])):
            index = n - len(gong['redStars']) - len(gong['magentaStars'])
            gong['brownStars'][index][2] = brightness

    @staticmethod
    def printLineChar(line):
        logging.info(len(line))
        for i in range(0, len(line)):
            logging.info(i)
            logging.info(line[i])

    def fillMajorStarBrightness(self, bars):
        twelveGongs = self.data['twelveGongs']

        line6 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 6))
        line7 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 7))
        line14 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 14))
        line15 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 15))
        line22 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 22))
        line23 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 23))
        line30 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 30))
        line31 = str(BaselinePan.getNthLineFromPage(str(self.page), BaselinePan.HTML_LINE_SEPARATOR, 31))

        for i in range(5, 5 + 9):
            if (line6[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line6[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 5, line6[i], twelveGongs[0])
        for i in range(15, 15 + 9):
            if (line6[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line6[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 15, line6[i], twelveGongs[1])
        for i in range(25, 25 + 9):
            if (line6[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line6[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 25, line6[i], twelveGongs[2])
        for i in range(35, 35 + 9):
            if (line6[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line6[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 35, line6[i], twelveGongs[3])

        for i in range(5, 5 + 9):
            if (line14[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line14[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 5, line14[i], twelveGongs[4])
        index = find_nth(line14, u'│', 3)
        index += 1
        for i in range(index, index + 9):
            if (line14[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                BaselinePan.setNthStarBrightnessOfGong(i - index, line14[i], twelveGongs[5])
        
        for i in range(5, 5 + 9):
            if (line22[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line14[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 5, line22[i], twelveGongs[6])
        index = find_nth(line22, u'│', 3)
        index += 1
        for i in range(index, index + 9):
            if (line22[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                BaselinePan.setNthStarBrightnessOfGong(i - index, line22[i], twelveGongs[7])
        

        for i in range(5, 5 + 9):
            if (line30[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line30[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 5, line30[i], twelveGongs[8])
        for i in range(15, 15 + 9):
            if (line30[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line30[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 15, line30[i], twelveGongs[9])
        for i in range(25, 25 + 9):
            if (line30[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line30[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 25, line30[i], twelveGongs[10])
        for i in range(35, 35 + 9):
            if (line30[i] in [u'庙', u'旺', u'利', u'得', u'平', u'落', u'陷']):
                # logging.info(i)
                # logging.info(line30[i])
                BaselinePan.setNthStarBrightnessOfGong(i - 35, line30[i], twelveGongs[11])
        
        line7Cleaned = line7.replace('<font color="#FF0000">', '')
        line7Cleaned = line7Cleaned.replace('</font>', '')
        line15Cleaned = line15.replace('<font color="#FF0000">', '')
        line15Cleaned = line15Cleaned.replace('</font>', '')
        line23Cleaned = line23.replace('<font color="#FF0000">', '')
        line23Cleaned = line23Cleaned.replace('</font>', '')
        line31Cleaned = line31.replace('<font color="#FF0000">', '')
        line31Cleaned = line31Cleaned.replace('</font>', '')

        # BaselinePan.printLineChar(line7Cleaned)
        # BaselinePan.printLineChar(line15Cleaned)
        # BaselinePan.printLineChar(line23Cleaned)
        # BaselinePan.printLineChar(line31Cleaned)
        for i in range(5, 5 + 9):
            if (line7Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line7Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 5, line7Cleaned[i], twelveGongs[0])
        for i in range(15, 15 + 9):
            if (line7Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line7Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 15, line7Cleaned[i], twelveGongs[1])
        for i in range(25, 25 + 9):
            if (line7Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line7Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 25, line7Cleaned[i], twelveGongs[2])
        for i in range(35, 35 + 9):
            if (line7Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line7Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 35, line7Cleaned[i], twelveGongs[3])

        for i in range(5, 5 + 9):
            if (line15Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line15Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 5, line15Cleaned[i], twelveGongs[4])
        index = find_nth(line15Cleaned, u'│', 3)
        index += 1
        for i in range(index, index + 9):
            if (line15Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                BaselinePan.setNthStarSecondBrightnessOfGong(i - index, line15Cleaned[i], twelveGongs[5])


        for i in range(5, 5 + 9):
            if (line23Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line23Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 5, line23Cleaned[i], twelveGongs[6])
        index = find_nth(line23Cleaned, u'│', 3)
        index += 1
        for i in range(index, index + 9):
            if (line23Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                BaselinePan.setNthStarSecondBrightnessOfGong(i - index, line23Cleaned[i], twelveGongs[7])


        for i in range(5, 5 + 9):
            if (line31Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line31Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 5, line31Cleaned[i], twelveGongs[8])
        for i in range(15, 15 + 9):
            if (line31Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line31Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 15, line31Cleaned[i], twelveGongs[9])
        for i in range(25, 25 + 9):
            if (line31Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line31Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 25, line31Cleaned[i], twelveGongs[10])
        for i in range(35, 35 + 9):
            if (line31Cleaned[i] in [u'忌', u'科', u'禄', u'权']):
                # logging.info(i)
                # logging.info(line31Cleaned[i])
                BaselinePan.setNthStarSecondBrightnessOfGong(i - 35, line31Cleaned[i], twelveGongs[11])


        # for i in range(len(gong['redStars'])):
        #   # gong['redStars'][i][2] = bar4[i + 1]
        #   gong['redStars'][i][1] = bar3[i + 1]
            
        # for i in range(len(gong['magentaStars'])):
        #   # gong['magentaStars'][i][2] = bar4[len(gong['redStars']) + i + 1]
        #   gong['magentaStars'][i][1] = bar3[len(gong['redStars']) + i + 1]
            

        # for i in range(len(gong['brownStars'])):
        #   # gong['brownStars'][i][2] = bar4[len(gong['magentaStars']) + len(gong['redStars']) + i + 1]
        #   gong['brownStars'][i][1] = bar3[len(gong['magentaStars']) + len(gong['redStars']) + i + 1]
        
        # curLastChar = bar4.next_element
        # pattern = re.compile(ur'.*[科].*', re.UNICODE)
        
        # while (curLastChar.name != 'br'):
            
        
            # result = re.match(pattern, curLastChar.string)
            # logging.info(result)
            # curLastChar = curLastChar.next_element


    @staticmethod
    def getIdFromA(aTag):
        starId = int(aTag['href'][aTag['href'].find('id=') + 3:])
        if (starId == 64 and (aTag.font['color'] == '#000099' or aTag.font['color'] == '#009999') ):
            starId = 65
        return starId
    @staticmethod
    def getTextFromA(aTag):
        starText = str(aTag.find('font', color='#009999').string)
        return starText

    def cleanUpCenterGong(self):
        self.page.find_all('font', color='#009999')[6].decompose()
        map(bs4.Tag.decompose, self.page.find_all('font', color='#0080ff'))

        # out = open('centerGongCleared.html', 'w')
        # out.write(str(self.page))


    def setCenterGong(self):
        self.setSCBZ()
        self.setMingSiHua()
        self.setAge()
        self.setMingGongZaiShenGongZai()
        self.setMingZhuShenZhu()
        
        self.setZiDouZai()
        self.setJu()
        self.setBirthday()
        self.setPanLei()

    def setSCBZ(self):
        scbz = self.page.find_all(text=re.compile(u'造：'))[0]
        logging.info(scbz.string)
        scbz = scbz.next_sibling
        logging.info(scbz.string)
        self.data['centerGong']['八字'] = str(scbz.string.strip())


    def setJu(self):
        ju = self.page.find_all(text=re.compile(u'局'))
        ju = ju[0]
        ju = ju[ju.find(u'局') - 2 : ju.find(u'局')]
        self.data['centerGong']['局'] = ju

    def setZiDouZai(self):
        ziDouZai = self.page.find_all(text=re.compile(u'子斗在'))
        ziDouZai = ziDouZai[0]
        self.data['centerGong']['子斗在'] = ziDouZai[ziDouZai.find(u'子斗在') + 3]

    def setPanLei(self):
        panLeiDict = {
            1: u'本命',
            2: u'大限',
            3: u'流年'
        }
        self.data['centerGong']['盘类'] = panLeiDict[self.data['inputs']['mode']]
        panLeiTag = self.page.find_all(text=re.compile(u'盘类'))[0]
        # panLeiTag.extract()

    def setMingSiHua(self):
        mingSiHua = self.page.find_all(text=re.compile(u'命四化'))
        
        mingSiHua = mingSiHua[0]
        mingSiHua = mingSiHua.next_sibling
        mingSiHuaTag = mingSiHua
        mingSiHua = mingSiHua.stripped_strings
        for string in mingSiHua:
            mingSiHua = string
        mingSiHua = mingSiHua[1:-1]
        self.data['centerGong']['命四化'] = mingSiHua
        mingSiHuaPrevTag = mingSiHuaTag.previous_sibling
        mingSiHuaTag.extract()
        self.mingSiHuaPrevTag = mingSiHuaPrevTag
        # mingSiHuaPrevTag.extract()

    def setAge(self):
        age =  self.page.find_all(text=re.compile(u"年龄"))
        age = age[0]
        ageTag = age
        age = age.replace(u"年龄", '')
        age = age.replace(u'岁', '')
        age = int(age)
        self.data['centerGong']['年龄'] = age
        ageTag.extract()

    def setMingGongZaiShenGongZai(self):
        mingGongZai = self.page.find_all(text=re.compile(u"命宫在"))
        mingGongZaiTag = mingGongZai[0]
        mingGongZai = mingGongZai[0].replace(u'命宫在', '')
        self.data['centerGong']['命宫在'] = mingGongZai

        shenGongZai = self.page.find_all(text=re.compile(u"身宫在"))
        shenGongZaiTag = shenGongZai[0]
        shenGongZai = shenGongZai[0].replace(u'身宫在', '')
        self.data['centerGong']['身宫在'] = shenGongZai

        mingGongZaiTag.extract()
        shenGongZaiTag.extract()

    def setMingZhuShenZhu(self):
        mingZhu = self.page.find_all(text=re.compile(u"命主"))
        mingZhuTag = mingZhu[0]
        mingZhu = mingZhu[0].replace(u'命主', '')
        self.data['centerGong']['命主'] = mingZhu

        shenZhu = self.page.find_all(text=re.compile(u"身主"))
        shenzhuTag = shenZhu[0]
        shenZhu = shenZhu[0].replace(u'身主', '')
        self.data['centerGong']['身主'] = shenZhu

        mingZhuTag.extract()
        shenzhuTag.extract()

    def setBirthday(self):
        self.setLunarBirthday()
        self.setSolarBirthday()

    def setLunarBirthday(self):
        yinLiTag = self.page.find(text=re.compile(u'│农历：'))
        
        yinLi = '' + yinLiTag.next_sibling.string
        yinLiTag = yinLiTag.next_sibling
        yinLi += '' + yinLiTag.next_sibling.string
        yinLiTag = yinLiTag.next_sibling
        yinLi += '' + yinLiTag.next_sibling.string
        yinLiTag = yinLiTag.next_sibling
        yinLi += '' + yinLiTag.next_sibling.string
        yinLiTag = yinLiTag.next_sibling
        yinLi += '' + yinLiTag.next_sibling.string
        yinLiTag = yinLiTag.next_sibling
        yinLi += '' + yinLiTag.next_sibling.string
        yinLiTag = yinLiTag.next_sibling
        yinLi += '' + yinLiTag.next_sibling.string
        yinLiTag = yinLiTag.next_sibling
        yinLi += '' + yinLiTag.next_sibling.string

        self.data['centerGong']['阴历生日'] = yinLi.strip()

        yinLiTag = self.page.find(text=re.compile(u'│农历：')).next_sibling
        for i in range(8):
            newTag = yinLiTag.next_sibling
            yinLiTag.extract()
            yinLiTag = newTag


    def setSolarBirthday(self):
        # logging.info(self.data['inputs'])
        yangLi = str(self.data['inputs']['y']) + u'年'

        yangLi = yangLi + (str(self.data['inputs']['m']) if self.data['inputs']['m'] >= 10 else '0' + str(self.data['inputs']['m'])) + u'月'
        yangLi = yangLi + (str(self.data['inputs']['d']) if self.data['inputs']['d'] >= 10 else '0' + str(self.data['inputs']['d'])) + u'日'
        yangLi = yangLi + (str(self.data['inputs']['h']) if self.data['inputs']['h'] >= 10 else '0' + str(self.data['inputs']['d'])) + u'时'
        yangLi += u'生'

        self.data['centerGong']['阳历生日'] = yangLi

        yangLiTag = self.page.find(text=re.compile(u'阳历：'))
        newTag = yangLiTag.next_sibling
        yangLiTag.replace_with(yangLiTag.string.replace(u'阳历：', ''))
        yangLiTag = newTag
        for i in range(9):
            newTag = yangLiTag.next_sibling
            yangLiTag.extract()
            yangLiTag = newTag


# try:
#   STARS = BaselinePan.byteify(json.load(open('starList.json')))
# except ValueError:
#   pass
# BaselinePan.STARS = STARS
# pprint(STARS)
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:

        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def find_nth_dbg(haystack, needle, n):
    
    start = haystack.find(needle)
    logging.info(haystack, needle, n)
    logging.info(start)
    while start >= 0 and n > 1:
        logging.info(haystack)
        logging.info(needle)
        start = haystack.find(needle, start+len(needle))
        logging.info(start)
        n -= 1
    return start
