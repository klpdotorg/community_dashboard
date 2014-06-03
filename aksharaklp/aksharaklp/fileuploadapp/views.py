# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from aksharaklp import settings
from aksharaklp.fileuploadapp.models import Document
from aksharaklp.fileuploadapp.forms import DocumentForm
from aksharaklp.fileuploadapp.filereader import read_file

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
       
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            read_file(settings.PROJECT_ROOT+newdoc.docfile.url)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('aksharaklp.fileuploadapp.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'fileuploadapp/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
