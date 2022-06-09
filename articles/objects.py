import hashlib
import pymongo
from time import time
import csv

sources = ("euronews", "map", "hesspress", "france24")
langs = ("en", "fr", "ar")


class Article:

    def __init__(self, title, link, image, date, lang, source) -> None:

        # document form for easier storage with mongodb
        self.document = {
            '_id': str(hashlib.sha256(str(link).encode('utf-8')).hexdigest())[0:3],
            'title': title,
            'link': link,
            'image': image,
            'date': date,
            'lang': lang,
            'source': source
        }


class Result:

    def __init__(self, lang, source) -> None:
        self.articles_list = []
        self.nbrArticles = 0
        self.time = 0
        self.lang = lang
        self.source = source

        self.n_france24 = 0
        self.n_map = 0
        self.n_hespress = 0
        self.n_euronews = 0
    

    def countArticlesPerSite(self):
        for article in self.articles_list:
            if article.document['source'] == 'map':
                self.n_map += 1
            elif article.document['source'] == 'france24':
                self.n_france24 += 1
            elif article.document['source'] == 'euronews':
                self.n_euronews += 1
            else:
                self.n_hespress += 1

    def addArticle(self, article):
        self.articles_list.append(article)
        self.nbrArticles += 1
    
    def setTime(self, time):
        self.time = "{:.2f}".format(time)
    
    def __str__(self) -> str:
        time_str = "{:.2f}".format(self.time)
        res = f"Number of articles: {self.nbrArticles}\n" + f"Search time: {time_str}s\n" + "-------------------------------\n"
        for article in self.articles_list:
            res += f"Title: {article.document['title']}\n" + f"Link: {article.document['link']}\n" + f"Image: {article.document['image']}\n" + f"Date: {article.document['date']}\n" + f"Language: {article.document['lang']}\n" + f"Source: {article.document['source']}\n"
            res += "-------------------------------\n"
        return res
    
    def saveToCsv(self):

        with open("data.csv", "w", newline='') as f:

            writer = csv.writer(f, dialect=csv.excel)

            writer.writerow(["title", "image", "link", "date", "language", "source"])
            
            # write data to csv file
            for article in self.articles_list:
                try:
                    writer.writerow([article.document['title'], article.document['image'], article.document['link'], article.document['date'], article.document['lang'], article.document['source']])
                except:
                    continue


class Database:

    def __init__(self) -> None:
        self.client = pymongo.MongoClient("mongodb+srv://Omar:EOmar4TW@aggregator.2gkpd.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.aggregator
        self.collection = self.db.articles
    
    # create indices to allow for queries (must be called once)
    def createIndices(self):
        self.collection.create_index([('title', pymongo.TEXT), ('link', pymongo.TEXT)])
    
    # remove all indices on this collection
    def dropIndices(self):
        self.collection.drop_indexes()

    # remove all articles
    def deleteAll(self):
        self.collection.delete_many({})
    
    # insert result into database
    def insertResults(self, results):

        for article in results.articles_list:
            try:
                self.collection.insert_one(article.document)

            except pymongo.errors.DuplicateKeyError:
                pass
    
    def query(self, keyword, lang, source, limit=150):
        result = Result(lang, source)
        i = 0

        # constructing query
        query = {}
        if keyword != '':
            query['$text'] = { '$search': keyword }
        if len(lang) != 0:
            query['lang'] = { '$in': lang }
        if len(source) != 0:
            query['source'] = { '$in': source }

        # create a cursor with articles that match query
        start = time()
        cursor = self.collection.find(query)

        for article_doc in cursor:
            article = Article(article_doc['title'], article_doc['link'], article_doc['image'], article_doc['date'], article_doc['lang'], article_doc['source'])
            result.addArticle(article)
        result.setTime(time() - start)

        return result