# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.loader import render_to_string

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Avg,Q

from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment

from pslechdb.models import *
#from itemrtproject import assessment_engine, formatter_engine
import assessment_engine
from pslechweb import forms

from datetime import datetime, timedelta

import math, re, random, sys
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from grading.grade import grade

from django_ajax.decorators import ajax

def welcome(request):
    "Main page of the site, redirects if logged in"
    # Redirect to respective home portals
    if request.user.is_authenticated():
        # Redirect user to user portal
        return redirect('/home/')

    # Home page for non authenticated users
    return render(request, 'pslechweb/welcome.html')

@login_required
def home(request):
    return render(request, 'pslechweb/home.html')

@login_required
def practice_home(request):
    return render(request, 'pslechweb/practice.home.html')

@login_required
def practice_select_section(request,part,section,topicId=None):
    part_choice= [x for x in Part.TYPE_CHOICES if x[0]==part][0]
    section_choice=[x for x in Section.TYPE_CHOICES if x[0]==section][0]
    topics=Topic.objects.filter(part__type=part)
    qtags={}
    if part=="P2":
        qtags=QTag.objects.all()
    #if request.method=="GET":
    #    required_qtag=request.GET['qtag']
    #print request.GET

    passage_list=Passage.objects.filter(section__type=section,part__type=part)
    if "topic" in request.POST:
        topicId=request.POST["topic"]
    if(topicId):
        passage_list=passage_list.filter(topic__pk=topicId)
    paginator=Paginator(passage_list,10)
    page=request.GET.get('page')
    try:
        passages=paginator.page(page)
    except PageNotAnInteger:
        passages=paginator.page(1)
    except EmptyPage:
        passages=paginator.page(paginator.num_pages)
    if 'qtag' in request.GET:
        required_qtag=request.GET['qtag']
        questions=list(Question.objects.filter(tag=required_qtag))

        return render(request, 'pslechweb/practice.select.section.html',{'question_based':True,'part_choice':part_choice,'section_choice':section_choice,'topics':topics,'questions':questions,'qtags':qtags})

    return render(request, 'pslechweb/practice.select.section.html',{'part_choice':part_choice,'section_choice':section_choice,'topics':topics,'topic_choice':topicId,'passages':passages,'qtags':qtags,'count':paginator.count})

@login_required
def practice_passage(request,part,section,passage_id):
    topics=Topic.objects.filter(part__type=part)
    passage=Passage.objects.get(pk=passage_id)
    questions=Question.objects.filter(passage__pk=passage_id)
    return render(request, 'pslechweb/practice.passage.html',{'topics':topics,'passage':passage,'questions':questions})

@login_required
@ajax
def mark(request):
    i=request.POST["qid"]
    response=request.POST.get("response",None)
    q=Question.objects.get(pk=i)
    solution=q.solution.content
    #print q.id,"\tr=",response,"\ttype=",type(response)
    #print q.id,"\ts=",solution,"\ttype=",type(solution)
    if q.passage.part.type=="P1":
        grade_res=grade("mcq",solution,response,q.mark)
    else:
        grade_res=grade("ensemble",solution,response,q.mark)

    score=grade_res["score"]
    print q.content,score
    feedback_pos=None
    feedback_neg=None
    if 'sematic' in grade_res:
        feedback_pos=grade_res['sematic']['pos']
        feedback_neg=grade_res['sematic']['neg']
    feedback_syn=None
    if 'syntactic' in grade_res:
        feedback_syn=grade_res['syntactic']

    #print q.id,"\tm=",mark
    return {'score':score,'feedback_pos':feedback_pos,'feedback_neg':feedback_neg,'feedback_syn':feedback_syn}

@login_required
def select_cat_qTag(request):

    "Home view to display topics to choose from for practice"
    # Record usage for stats purpose
    #page = "practice"
    # Never accessed this page before, or last access was more than 10 mins ago
    #if 'user_usage_'+page not in request.session or datetime.now() > datetime.strptime(request.session['user_usage_'+page], "%a %b %d %H:%M:%S %Y") + timedelta(minutes=10):
    #    usage = UserUsage(user=request.user, page=page)
    #    usage.save()
    #    request.session['user_usage_'+page] = usage.datetime.strftime("%a %b %d %H:%M:%S %Y")
    # End usage recording

    qTags=QTag.objects.all()

    active_engine = Assessment.objects.all().filter(active=True).get(type=Assessment.PRACTICE)
    engine = getattr(assessment_engine, active_engine.engine)()

    qTag_ability = {}
    for qTag in qTags:
        ability = engine.get_user_ability(user=request.user, qTag=qTag)
        if ability is not None:
            qTag_ability[qTag] = int(ability)
        else:
            qTag_ability[qTag] = None

    return render(request,'pslechweb/select.cat.topic.html',{'qTags':qTags,'qTag_ability':qTag_ability})



@login_required
def cat_practice(request,qTag):
    # Selected qTag
    qTag=QTag.objects.all().get(id=qTag)

    # Init session variable for question
    if 'practice_current_qn' not in request.session:
        request.session['practice_current_qn'] = None

    # Debug data
    debug = {}

    # Error data
    error = {}

    # GET Request or POST w/o session data >> Load Question
    # POST Request >> Answer Question
    if request.method == 'GET' or request.session['practice_current_qn'] is None:
        # Check if existing loaded question is from same topic, otherwise clear it
        if request.session['practice_current_qn'] != None:
            question_qTag = Question.objects.all().get(id=request.session['practice_current_qn']).tag
            if question_qTag != qTag:
                # New practice qTag, clear session variable
                request.session['practice_current_qn'] = None

        # Generate new question if not resuming
        if request.session['practice_current_qn'] == None:
            # Retrieve pool of questions with this qTag
            question_pool = Question.objects.all().filter(tag=qTag)

            # Get active assessment engine (practice) and dynamically load engine
            active_engine = Assessment.objects.all().filter(active=True).get(type=Assessment.PRACTICE)
            engine = getattr(assessment_engine, active_engine.engine)()

            # Initialise session storage for assessment engine
            if 'engine_store' not in request.session:
                request.session['engine_store'] = None

            # Request a new question from the assessment engine
            question = engine.get_next_question(user=request.user, qTag=qTag, question_pool=question_pool, session_store=request.session['engine_store'])

            # Get current ability for debug purposes
            debug['ability'] = engine.get_user_ability(user=request.user, qTag=qTag)

            #debug['answer'] = question.choices[question.answers.all()[0].content.lower()]

            # Woops, we ran out of suitable questions, give error and direct to reset
            # TODO: Proper RESET (Currently when it runs out of questions it will just go back to home!)
            if not question:
                return redirect('/CATPractice/')

            # Update the question to session (for persistance if user refresh page/relogin)
            request.session['practice_current_qn'] = question.id
        else:
            # Reload question from session data if resuming practice or page refresh
            question = Question.objects.all().get(id=request.session['practice_current_qn'])

        # Rendering at end of page
    else:
        # Submitting a practice question
        if 'answered' in request.POST and request.POST['answered']:
            qnid_post=request.POST['answered']
        else:
            qnid_post = None

        qnid_session = request.session['practice_current_qn']

        if qnid_post != qnid_session:
            # Something strange is happening, missing qid from form or mismatch between form and session, TODO: Handle this PROPERLY
            debug['qnid_post'] = qnid_post
            debug['qnid_session'] = qnid_session

        # Reload question from session data
        question = Question.objects.all().get(id=qnid_session)

        # Check if answer was submitted
        if 'answered' in request.POST and request.POST['answered']:
            ans = request.POST['answered']
            response=request.POST['q-'+ans]

            # Get active assessment engine (practice) and dynamically load engine
            active_engine = Assessment.objects.all().filter(active=True).get(type=Assessment.PRACTICE)
            engine = getattr(assessment_engine, active_engine.engine)()

            # Initialise session storage for assessment engine
            if 'engine_store' not in request.session:
                request.session['engine_store'] = None

            # Match answer using assessment engine
            result = engine.match_answers(user=request.user, response=response, question=question, session_store=request.session['engine_store'])

            # Restore updated engine store
            # request.session['engine_store'] = result['session_store']

            # Answer is correct if full points is awarded
            if result['correctness'] == 1.0:
                correct = True
            else:
                correct = False

            # Get correct answer
            question.solution = question.solution

            # Ability score for debug purposes
            debug['ability'] = result['ability']

            # Reset current practice qn to None
            request.session['practice_current_qn'] = None

            # Format question for web mode
            # formatter = formatter_engine.WebQuestionFormatter()
            # question = formatter.format(question)

            # Temp variable to allow ajax through https
            host = request.get_host()
            is_secure = not "localhost" in host

            # Kill debug for non test users
            #if request.user.get_profile().debug is False:
            #    debug = {}

            #return render(request, 'itemrtweb/practice.submit.html', {'question': question, 'qTag': qTag, 'choice': choice, 'correct': correct, 'debug': debug, 'host': host, 'is_secure': is_secure})
            return render(request, 'pslechweb/CATPractice.html', {'marked':True,'q': question,'score':{qnid_post:{'response':response,'mark':result['mark']}}, 'qTag': qTag, 'error': error, 'debug': debug})
        else:
            # Option not selected, prompt error
            error['unselected'] = True

    # Format question for web mode
    # formatter = formatter_engine.WebQuestionFormatter()
    # question = formatter.format(question)

    # Kill debug for non test users
    #if request.user.get_profile().debug is False:
    #    debug = {}

    # Render question page
    return render(request, 'pslechweb/CATPractice.html', {'marked':False,'q': question, 'qTag': qTag, 'error': error, 'debug': debug})

@login_required
def display_tip(request):
    tips=Tip.objects.all()
    return render(request,'pslechweb/tip.html',{'tips':tips})


