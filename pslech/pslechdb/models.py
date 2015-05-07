# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from redactor.widgets import RedactorEditor
import re
def removeHTML(text):
    text=re.sub('<[^>]*>','',text)
    text=re.sub('</[^>]*>','',text)
    return text

# Create your models here.
class Paper(models.Model):
    year = models.DateField()
    def __unicode__(self):
        return year

class Part(models.Model):
    P1='P1'
    P2='P2'
    TYPE_CHOICES=(
            (P1,u'阅读理解一'),
            (P2,u'阅读理解二'),
            )
    type = models.CharField(max_length=2,choices=TYPE_CHOICES)
    def __unicode__(self):
        return self.get_type_display()

class Section(models.Model):
    TYPE_CHOICES=(
            ('SA',u'A组'),
            ('SB',u'B组'),
            )
    type = models.CharField (max_length=2,choices=TYPE_CHOICES)
    def __unicode__(self):
        return self.get_type_display()

class Topic(models.Model):
    name = models.CharField(max_length=30)
    part = models.ForeignKey(Part)

    def __unicode__(self):
        return self.name

class QTag(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Passage(models.Model):
    content = models.TextField(max_length=4000)
    part = models.ForeignKey(Part)
    section = models.ForeignKey(Section)
    #topic = models.ForeignKey(Topic)
    topic=ChainedForeignKey(
            Topic,
            chained_field="part",
            chained_model_field="part",
            show_all=False,
            auto_choose=True
            )
    paper = models.ForeignKey(Paper,blank=True,null=True) # a passage can belong to no paper
    def preview(self):
        return removeHTML(self.content[0:130])[0:100]+"......"
    def __unicode__(self):
        return self.preview()

class Question(models.Model):
    content     = models.TextField(max_length=1000)
    tag        = models.ForeignKey(QTag,blank=True,null=True)
    passage     = models.ForeignKey(Passage)
    mark        = models.IntegerField()
    difficulty = models.IntegerField()
    isTable = models.NullBooleanField()

    def get_question(self):
        #Get text of the question (without choices)
        if (self.content.find('<table>')!=-1):
            self.isTable=True
            return removeHTML(self.content[:self.content.find('<table>')])

        #part 2 questions are not MCQ questions
        if (self.passage.part.type=="P2"):
            return removeHTML(self.content)

        index = self.content.find('A.')
        return removeHTML(self.content[0:index])
    def __unicode__(self):
        return self.get_question()
    def get_table_presentation(self):
        if not self.isTable:
            return
        l=re.findall('\s*\(\s*[a-z]\s*\)\s*',self.content)
        res=self.content[self.content.find('<table>'):]
        for s in l:
            i=res.find(s)+len(s)
            res=res[:i]+'<textarea></textarea>'+res[i:]
        i=res.find('<table')+len('<table');
        res=res[:i]+' class="table-qn" id="q-'+str(self.id)+'"'+res[i:];
        return res
    def get_table_filled_presentation(self,response):
        r=response.split('\n')
        l=re.findall('\s*\(\s*[a-z]\s*\)\s*',self.content)
        res=self.content[self.content.find('<table>'):]
        c=0
        for s in l:
            i=res.find(s)+len(s)
            res=res[:i]+'<textarea onfocus="blur()">'+r[c]+'</textarea>'+res[i:]
            c+=1
        i=res.find('<table')+len('<table');
        res=res[:i]+' class="table-qn" id="q-'+str(self.id)+'"'+res[i:];
        return res


    def get_choices(self):
        #Get a tuple of possible choices for the MCQ question

        #part 2 questions are not MCQ questions
        if (self.passage.part.type=="P2"):
            return None

        # Current code uses simple search and string cutting, TODO: Upgrade to Regex
        indexA = self.content.find('A.')
        indexB = self.content.find('B.')
        indexC = self.content.find('C.')
        indexD = self.content.find('D.')

        indexC = len(self.content) if indexC == -1 else indexC
        indexD = len(self.content) if indexD == -1 else indexD

        # Added +2 to remove the choice lettering (A/B/C/D)
        ans_a = self.content[indexA+2:indexB].strip()
        ans_b = self.content[indexB+2:indexC].strip()
        ans_c = self.content[indexC+2:indexD].strip()
        ans_d = removeHTML(self.content[indexD+2:].strip())

        ans_dict = {}

        if ans_a:
            ans_dict['a'] = ans_a
        if ans_b:
            ans_dict['b'] = ans_b
        if ans_c:
            ans_dict['c'] = ans_c
        if ans_d:
            ans_dict['d'] = ans_d

        return ans_dict


class Solution(models.Model):
    content     = models.TextField(max_length=1000)
    question    = models.OneToOneField(Question)
    def __unicode__(self):
        return removeHTML(self.content)[0:20]

class Assessment(models.Model):
    "Assessment model to represent different assessment engines"

    PRACTICE = 'P'
    TEST = 'T'
    ASSESSMENT_MODE_CHOICES = (
        (PRACTICE, 'Practice'),
        (TEST, 'Test'),
    )

    name        = models.CharField(max_length=30)
    type        = models.CharField(max_length=1, choices=ASSESSMENT_MODE_CHOICES)
    active      = models.BooleanField()
    engine      = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Response(models.Model):
    content     = models.TextField(max_length=1000)
    question    = models.ForeignKey(Question)
    user        = models.ForeignKey(User)
    mark        = models.IntegerField()
    date        = models.DateTimeField(auto_now=True)
    correctness = models.DecimalField(max_digits=3, decimal_places=2, null=True) # Percent correct in dec (0-1)
    criterion   = models.DecimalField(max_digits=3, decimal_places=1) # Max marks for random practice/test, diff for CAT
    ability     = models.DecimalField(max_digits=5, decimal_places=2, null=True) # Current ability score for practices
    assessment  = models.ForeignKey(Assessment)

class Tip(models.Model):
    title   = models.CharField(max_length=100)
    content   = models.TextField()

    def __unicode__(self):
        return self.title

