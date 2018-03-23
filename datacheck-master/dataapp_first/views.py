import os
from django.http import HttpResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect, render_to_response
from bigquery import get_client
from datacheck.settings import BASE_DIR
import pandas as pd
import csv
from django.conf import settings

from django.db import connection



from django.template import RequestContext
from django.urls import reverse

from dataapp_first.models import Document
from dataapp_first.forms import DocumentForm, UrlForm

from pathlib import Path

from django.core.files import File
from django.core.files.storage import FileSystemStorage, Storage, default_storage

client = None
def root(request):
    global client
    query_string=None
    if client !=None and request.method=='POST':
        query_string=request.POST.get('query', 'empty')
        print(query_string) #for testing
        print('in post  ',client) #for testing
        #results=compute_query(query_string)

        job_id, _results = client.query(query_string)
        results = client.get_query_rows(job_id)
        

        path = os.path.join(settings.BASE_DIR, 'static', 'dataset.csv')

        with open(path, "w", newline='') as f:
            w = csv.DictWriter(f, results[0].keys())
            w.writerow(dict((fn,fn) for fn in results[0].keys()))
            w.writerows(results)

        return render(request,'index.html')

        #return render(request,'results.html',{'data':results})

    else:
        print('in get  ',client)
        return render(request,'index.html')

def charting(request):
    documents = Document.objects.all()
    # for doc in documents:
    #     destination = settings.MEDIA_ROOT
    #     if not os.path.exists(destination + '/' + doc.docfile.name):
    #         print(destination + '/' + doc.docfile.name)
    #         doc.delete()
    return render(request, 'charting.html', {'documents': documents})

def fileupload(request):
    if request.method == 'POST' :
        myfile = request.FILES['creds']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        request=authenticate(request,filename)
        if request.authenticated and request.client!=None:
            return redirect('root')
        else:
            return render(request,'upload.html',{'status':False})
    else:
        return render(request, 'upload.html')

def authenticate(request,filename):
    try:
        global client
        f_path = os.path.join(BASE_DIR, 'media')
        fin_path=os.path.join(f_path,filename)
        json_key = fin_path
        client = get_client(json_key_file=json_key, readonly=True)
        request.authenticated=True
        request.client=client
        return request
    except Exception as e:
        print(e)
        request.authenticated = False
        request.client=None
        return request

def compute_query(query_string):
    job_id, _results = client.query(query_string)
    results = client.get_query_rows(job_id)
    resultsdf = pd.DataFrame(results)
    return resultsdf.to_html()




def upload_csv(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            documents = Document.objects.all()
            return render(request, 'charting.html', {'documents': documents})
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    return render(request, 'upload_csv.html', {'documents': documents, 'form': form})

def docaccess(request):
    url = ""
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            print (form.cleaned_data['url'])
            url = form.cleaned_data['url']
            file = default_storage.open(url, 'rb')

            print(settings.BASE_DIR)

            path = os.path.join(settings.BASE_DIR, 'static', 'dataset.csv')
            f = open(path, "w+b")
            f.truncate()
            f.write(file.read())
            f.close()

            #print (file.read())
            documents = Document.objects.all()
            return redirect('charting')