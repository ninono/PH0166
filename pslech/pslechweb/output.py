# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from pslechdb.models import *
import csv, codecs, cStringIO
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = UnicodeWriter(response)
    passages=Passage.objects.all()
    for pas in passages:
        writer.writerow([pas.part.get_type_display()])
        writer.writerow([pas.section.get_type_display()])
        writer.writerow([pas.topic.name])
        writer.writerow([pas.content])

        questions=Question.objects.filter(passage=pas)
        print pas
        for q in questions:
            if q.tag:
                writer.writerow([q.tag.name,q.content])
            else:
                writer.writerow(["NULL",q.content])
            print q
            sol=Solution.objects.get(question=q)
            writer.writerow([sol.content])
    return response
