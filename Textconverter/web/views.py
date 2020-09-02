from django.shortcuts import render
from . import models
from web.forms import NewLink

import bs4 as bs
import urllib.request
import re
import pandas as pd
import heapq
import nltk
from web.models import Link
import lxml.etree
import lxml
import requests




# Create your views here.




def users(request):
    form = NewLink()



    if request.method == "POST":
        form = NewLink(request.POST)



        if form.is_valid() :
            form.save(commit=True)




            return index(request)
        else:
            print("Error Form Invalid")
    return render(request,'link_name.html', {'form':form})







def index(request):
    field_name = 'Number_of_Lines'
    obj = Link.objects.last()
    field_object = Link._meta.get_field(field_name)
    ho = field_object.value_from_object(obj)




    so = Link.objects.all().last()
    # so = ho.objects.all()





    url_list = [so]
    for url in url_list:#this means go to each url
        response = requests.get(url)#this is where we are accessing programatically the url, this is basiclly scrapping
        xml_page = response.text#get the text inside it



    #source =urllib.request.urlopen(ho).read()
    soup = bs.BeautifulSoup(xml_page,'lxml')
    text = ""
    for paragraph in soup.find_all('p'):#soup is object which contain all html, here we are telling find all p tag
        print(paragraph.text)#paragraph is actually a tag , so we cannot concat it with string that's why we are using .text to convert it into string
        text += paragraph.text
        text += '\n\n'
    text = re.sub(r'\[[0-9]*\]',' ',text)
    text = re.sub(r'\s+',' ',text)
    clean_text = text.lower()
    clean_text = re.sub(r'\W',' ',clean_text)#if any word character is there (-- _ -+) replace it with space
    clean_text = re.sub(r'\d',' ',clean_text)#if there is single digit replace it with space
    clean_text = re.sub(r'\s+',' ',clean_text)
    sentences = nltk.sent_tokenize(text)#ham sentence ko tokenize kr rahe hai
    stop_words = nltk.corpus.stopwords.words('english')
    word2count = {}#create a dictionary object
    for word in nltk.word_tokenize(clean_text):#we go to the text which we have clean
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
    for key in word2count.keys():
        word2count[key] = word2count[key]/max(word2count.values())
    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 25:#IF sentence has more than 25 words you don't considered it
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]

# Gettings best 5 lines
    best_sentences = heapq.nlargest(ho, sent2score, key=sent2score.get)
    text =""

    for sentence in best_sentences:
        text=text+sentence


    my_dict = {'insert_me':text}
    return render(request,'index.html',context=my_dict)



def about(request):
    return render(request,'about.html')





#
# class LinkDetailView(DetailView):
#     context_object_name= 'link_detail'
#     model=models.Link
#
#
#     template_name = 'web/index.html'
#     def get_context_data(self,**kwargs):
#         context  = super(LinkDetailView,self).get_context_data(**kwargs)
#
#         return context
