import bs4 as bs
import urllib.request
from time import time
from articles.objects import *
from datetime import date as sys_date


db = Database()
langs = ("en", "fr", "ar")
months = {
    'janvier' : "01", 'january' : "01", 'يناير' : "01",
    'fevrier' : "02", 'february' : "02", 'فبراير' : "02", "février": "02",
    'mars' : "03", 'march' : "03", 'مارس' : "03",
    'avril' : "04", 'april' : "04", 'أبريل' : "04",
    'mai' : "05", 'may' : "05", 'ماي' : "05",
    'juin' : "06", 'june' : "06", 'يونيو' : "06",
    'juillet' : "07", 'july' : "07", 'يوليوز' : "07",
    'aout' : "08", 'august' : "08", 'غشت' : "08", "août": "08",
    'septembre' : "09", 'septembre' : "09", 'شتنبر' : "09",
    'octobre' : "10", 'october' : "10", 'أكتوبر' : "10",
    'novembre' : "11", 'november' : "11", 'نونبر' : "11",
    'decembre' : "12", 'december' : "12", 'دجنبر' : "12", "décembre": "12"
}


class Euronews:

    def __init__(self) -> None:
        self.url = "https://www.euronews.com/"
        self.source = "euronews"
        self.language = "en"
    
    def changeLanguage(self, language):
        if language in langs:
            if language == "fr":
                self.url = "https://fr.euronews.com/"
            elif language == "ar":
                self.url = "https://arabic.euronews.com/"
            else:
                self.url = "https://www.euronews.com/"
            self.language = language
        else:
            print("Unrecognized language!")
    
    def scrapData(self, query):
        # timing scraping operation
        start_time = time()

        # source of query page
        query_url = self.url if query == '' else self.url + "search?query=" + query
        try:
            page_source = urllib.request.urlopen(query_url)
        except:
            return Result(self.language, self.source)
        soup = bs.BeautifulSoup(page_source,'html.parser')

        
        result = Result(self.language, self.source)
        
        # scraping all articles
        for article in soup.find_all('article'):
            # getting article title
            article_title = " ".join(article.text.split())
            if article_title.lower() in ("games", "widgets & services", "follow us", "jeux", "suivez-nous"):
                continue

            # getting article 'a' element
            try:
                link = article.div.figure.a
            except AttributeError:
                continue
            
            # getting article link
            article_link = ""
            try:
                article_link = self.url + link['href']
            except KeyError:
                pass
        
            # getting article date
            date_element = article.find(class_='m-object__date')
            article_date = ""
            try:
                article_date = " ".join(date_element.text.split())
            except AttributeError:
                article_date = "/".join(str(sys_date.today()).split('-')[::-1])

            # getting article image
            # some articles don't return an image, in which case a default image will be loaded
            image_element = link.img
            article_image = ""
            try:
                article_image = image_element['data-src']
            except KeyError:
                pass
            
            # add scraped article to list
            result.addArticle(Article(article_title, article_link, article_image, article_date, self.language, self.source))
        end_time = time()

        # compute and set search time  
        result.setTime(end_time - start_time)

        return result


class France24:

    def __init__(self) -> None:
        self.url = "https://www.france24.com/en/"
        self.source = "france24"
        self.language = "en"
    
    def changeLanguage(self, language):
        if language in langs:
            if language == "fr":
                self.url = "https://www.france24.com/fr/"
            elif language == "ar":
                self.url = "https://www.france24.com/ar/"
            else:
                self.url = "https://www.france24.com/en/"
            self.language = language
        else:
            print("Unrecognized language!")
    
    def scrapData(self, query):
        
        # france24 doesn't support queries, so only articles on front page are scrapped
        result = Result(self.language, self.source)
        if query != '': return result

        # timing scraping operation
        start_time = time()

        # source of query page
        query_url = self.url
        page_source = urllib.request.urlopen(query_url)
        try:
            soup = bs.BeautifulSoup(page_source,'html.parser')
        except:
            return Result(self.language, self.source)
        
        for article in soup.find_all(class_="m-item-list-article"):

            # extract article title
            article_title = article.find(class_="article__title").text
            article_title = " ".join(article_title.split())

            # extract article image
            try:
                article_image = article.find('picture').img['srcset'].split()[0]
            except:
                continue

            # extract article link
            article_link = self.url + article.a['href'][4:]
            if "/s://" in article_link: continue

            # setting date to system's date
            article_date = "/".join(str(sys_date.today()).split('-')[::-1])

            # add scraped article to list
            result.addArticle(Article(article_title, article_link, article_image, article_date, self.language, self.source))


        end_time = time()

        # compute and set search time  
        result.setTime(end_time - start_time)

        return result


class Map:

    def __init__(self) -> None:
        self.url = "https://www.mapnews.ma/en/"
        self.source = "map"
        self.language = "en"
    
    def changeLanguage(self, language):
        if language in langs:
            if language == "fr":
                self.url = "https://www.mapnews.ma/fr/"
            elif language == "ar":
                self.url = "https://www.mapnews.ma/ar/"
            else:
                self.url = "https://www.mapnews.ma/en/"
            self.language = language
        else:
            print("Unrecognized language!")
    
    def scrapData(self, query):
        # timing scraping operation
        start_time = time()

        # source of query page
        query_url = self.url if query == '' else self.url + "search/node/" + query
        try:
            page_source = urllib.request.urlopen(query_url)
        except:
            return Result(self.language, self.source)
        soup = bs.BeautifulSoup(page_source,'html.parser')

        
        result = Result(self.language, self.source)
        
        # if no query passed, scrap landing page
        if query == "":
            for article in soup.find_all(class_="block-1"):
                # getting article header
                article_header = article.find(class_="title_article").a

                # extracting title
                article_title = article_header.text
                
                # extracting article link
                article_link = self.url + article_header['href'][4:]

                # setting date to system's date
                article_date = "/".join(str(sys_date.today()).split('-')[::-1])

                # getting article image
                article_image = article.find('img')['src']

                # add scraped article to list
                result.addArticle(Article(article_title, article_link, article_image, article_date, self.language, self.source))
            
            for article, date in zip(soup.find_all(class_="width-actualites"), soup.find_all(class_="date-actualites")):
                # getting article header
                article_header = article.a

                # extracting title
                article_title = article_header.text
                
                # extracting article link
                article_link = self.url + article_header['href'][4:]

                # extracting article date
                article_date_list = date.text.split()
                try:
                    article_date = article_date_list[0] + "/" + months[article_date_list[1].lower()] + "/" + article_date_list[2]
                except:
                    article_date = "/".join(str(sys_date.today()).split('-')[::-1])

                # no article image
                article_image = ""

                # add scraped article to list
                result.addArticle(Article(article_title, article_link, article_image, article_date, self.language, self.source))
        
        # if query is not empty
        else :
            for article in soup.find(class_="search-results node-results").find_all('li'):
                
                # article header
                article_header = article.find(class_="title").a 

                # extracting article title
                article_title = article_header.text

                # extracting article link
                article_link = article_header['href']

                # extracting article date
                article_date_list = article.find(class_="field-content node-date").text.split()
                try:
                    article_date = article_date_list[0] + "/" + months[article_date_list[1].lower()] + "/" + article_date_list[2]
                except:
                    article_date = "/".join(str(sys_date.today()).split('-')[::-1])

                # map offers no images for search queries
                article_image = ""

                # add scraped article to list
                result.addArticle(Article(article_title, article_link, article_image, article_date, self.language, self.source))


        end_time = time()

        # compute and set search time  
        result.setTime(end_time - start_time)

        return result


class Hespress:

    def __init__(self) -> None:
        self.url = "https://en.hespress.com/"
        self.source = "hespress"
        self.language = "en"
    
    def changeLanguage(self, language):
        if language in langs:
            if language == "fr":
                self.url = "https://fr.hespress.com/"
            elif language == "ar":
                self.url = "https://hespress.com/"
            else:
                self.url = "https://en.hespress.com/"
            self.language = language
        else:
            print("Unrecognized language!")
    
    def scrapData(self, query):
        # timing scraping operation
        start_time = time()

        # source of query page
        query_url = self.url if query == '' else self.url + "?s=" + query

        # using a user-agent to avoid error 403
        request_site = urllib.request.Request(query_url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            page_source = urllib.request.urlopen(request_site)
        except:
            return Result(self.language, self.source)
        soup = bs.BeautifulSoup(page_source,'html.parser')

        
        result = Result(self.language, self.source)
        # scraping all articles
        for card in soup.find_all(class_='overlay card'):

            # article header
            article = card.find(class_="stretched-link")

            # extracting article link
            article_link = " ".join(article['href'].split())

            # exracting article title
            article_title = " ".join(article['title'].split())

            # exracting article image
            try:
                article_image = "".join(article.find('img')['src'])
            except:
                article_image = ""

            # extracting article date
            try:
                article_date_list = card.find(class_="time").text.split()
                article_date = article_date_list[1] + "/" + months[article_date_list[2].lower()] + "/" + article_date_list[3]
            except:
                article_date = "/".join(str(sys_date.today()).split('-')[::-1])
            

            # add scraped article to list
            result.addArticle(Article(article_title, article_link, article_image, article_date, self.language, self.source))
        
        end_time = time()

        # compute and set search time  
        result.setTime(end_time - start_time)

        return result