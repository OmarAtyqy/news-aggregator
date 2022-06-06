from django.shortcuts import render
from articles.forms import QueryForm 
from . import objects, scrapers
from articles.models import Headline
import mimetypes
import os
from django.http.response import HttpResponse

scrapers_list = [scrapers.Euronews(), scrapers.France24(), scrapers.Hespress(), scrapers.Map()]

# database object to communicate with database
db = objects.Database()

def clear(request):
    Headline.objects.all().delete()
    return render(request, "index.html", {})

def welcome_view(request):
    return render(request, 'welcome_page.html', {})

# Create your views here.
def main_view(request):

    # clear current articles
    Headline.objects.all().delete()

    # scrap new articles
    # for scr in scrapers_list:
    #     for lang in ('fr', 'en', 'ar'):
    #         scr.changeLanguage(lang)
    #         result = scr.scrapData("")
    #         db.insertResults(result)
    #         print(f'Completed {scr.source} - {scr.language}')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # collect query keywords
            keywords = form.cleaned_data['keywords']

            # collect query languages
            languages = []
            if form.cleaned_data['fr']: languages.append("fr")
            if form.cleaned_data['en']: languages.append("en")
            if form.cleaned_data['ar']: languages.append("ar")

            # collect query sources
            sources = []
            if form.cleaned_data['france24']: sources.append("france24")
            if form.cleaned_data['hespress']: sources.append("hespress")
            if form.cleaned_data['map']: sources.append("map")
            if form.cleaned_data['euronews']: sources.append("euronews")

            # query the database
            result = db.query(keywords, languages, sources)

        else:
            result = db.query("", "", "")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = QueryForm()
        result = db.query("", "", "")

    # loop over articles found in query and add then objet list
    for article in result.articles_list[::-1]:
        new_headline = Headline()

        new_headline.image = article.document['image']
        new_headline.lang = article.document['lang']
        new_headline.source = article.document['source']
        new_headline.date = article.document['date']
        new_headline.link = article.document['link']

        title = article.document['title']
        new_headline.title = title if len(title) >= 50 else title + " " * (50 - len(title))

        new_headline.save()
    
    result.countArticlesPerSite()
    result.saveToCsv()
    return render(request, 'index.html', {'form': form, 'object_list':Headline.objects.all(), 'result':result, 'file':'../data.csv'})


def save_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'data.csv'
    # Define the full file path
    filepath = BASE_DIR + "\\" + filename
    print(filepath)
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response
