from newsapi import NewsApiClient
from newspaper import Article
import json
import urllib.request
import PyPDF2
import io
import requests
from tika import parser

url = 'https://newsapi.org/v2/everything?'

newsapi_key = '333dcb27683b46cf99b482ca64e32bca'

response_json_body = {}

def get_json_tittles(topic):

    titles = []
    global response_json_body

    parameters = {
        'q': topic, # query phrase
        'pageSize': 20,  # maximum is 100
        'apiKey': newsapi_key # your own API key
    }

    # Make the request
    response = requests.get(url, params=parameters)

    # Convert the response to JSON format
    response_json = response.json()
    response_json_body = response_json

    for i in range(len(response_json['articles'])):
        titles.append(response_json['articles'][i]['title'])

    return titles


def get_info_new(title):

    global response_json_body

    for i in range(len(response_json_body['articles'])):
        if response_json_body['articles'][i]['title'] == title:
            #pprint.pprint(response_json_body['articles'][i])
            return response_json_body['articles'][i]



def obtain_full_content(url):
    # Crear un objeto de artículo con la URL proporcionada
    article = Article(url)
    
    # Descargar y analizar el artículo
    article.download()
    article.parse()

    return article.text



def obtain_information_of_url(url):
    
    # Crear un objeto de artículo con la URL proporcionada
    article = Article(url)
    
    # Descargar y analizar el artículo
    article.download()
    article.parse()

    article_json = {
        "Article's Author" : article.authors,
        "Article Publication Date" : article.publish_date,
        "Article's Title" : article.title,
        "Article's Text" : article.text
    }

    return article_json



def add_url_content_to_json(title):
    json_without_full_content = get_info_new(title)
    url = json_without_full_content['url']
    content_text = obtain_full_content(url)
    print(type(content_text))

    data = json_without_full_content


    # Añadir el nuevo ítem "Explicit content" al diccionario
    data["ExplicitContent"] = content_text
    

    # Convertir el diccionario actualizado a JSON nuevamente
    json_data_actualizado = json.dumps(data, indent=2)

    return json_data_actualizado


# Function for upload url document
def get_url_doc_info(url):

    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes)

    text = ''

    for i in range(pdfdoc_remote.numPages):
        current_page = pdfdoc_remote.getPage(i)  

        text += "Content on page:" + str(i + 1) + "\n"

        text += current_page.extractText()

    return text
