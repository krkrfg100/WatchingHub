from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError 
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .models import *
import json


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
         

    # Get user settings
        user_settings, created  = Settings.objects.get_or_create(user=request.user)

        # Start the query based on the shows owner
        shows_query = Show.objects.filter(Show_Owner=request.user)

        # Apply classification filter
        if user_settings.Filter_By_Classification and user_settings.Filter_By_Classification != 'all':
            shows_query = shows_query.filter(Show_Owner=request.user,Show_Classification=user_settings.Filter_By_Classification)
        else:
            shows_query = shows_query.filter(Show_Owner=request.user)

        # Apply sorting based on Sort_Shows_By
        sort_by = user_settings.Sort_Shows_By
        if sort_by == "Random":
            shows_query = shows_query.order_by('?')
        elif sort_by == "Show_title":
            shows_query = shows_query.order_by('Show_title')
        elif sort_by == "Date_added_latest":
            shows_query = shows_query.order_by('-id')
        elif sort_by == "Date_added_oldest":
            shows_query = shows_query.order_by('id')
        elif sort_by == "Newest_in_release":
            shows_query = shows_query.order_by('-Publication_year')
        elif sort_by == "Oldest_in_release":
            shows_query = shows_query.order_by('Publication_year')
        elif sort_by == "Highest_rating":
            shows_query = shows_query.order_by('-Show_raring')
        elif sort_by == "Lowest_rating":
            shows_query = shows_query.order_by('Show_raring')
        elif sort_by == "Date_finished_watching_latest":
            shows_query = shows_query.order_by('-Date_finished_watching')
        elif sort_by == "Date_finished_watching_oldest":
            shows_query = shows_query.order_by('Date_finished_watching')
        elif sort_by == "Longest_duration":
            shows_query = shows_query.order_by('-duration')
        elif sort_by == "Shortest_duration":
            shows_query = shows_query.order_by('duration')

        # Display the results with the template
        




        classification = Classification.objects.filter(Classification_Owner=request.user).all()


        return render(request, "WatchingHub/index.html",{
            "Shows": shows_query,
            "Classification": classification,
        })



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:   
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request , "WatchingHub/login.html",{
                "message": "أسم المستخدم او كلمة المرور خاطئة"
            })

    return render(request , "WatchingHub/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "WatchingHub/register.html", {
                "message": "تأكيد كلمة المرور وكلمة المرور غير متطابقة"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username,password=password)
            user.save()
            
    
        except IntegrityError:
             return render(request, "WatchingHub/register.html",{
                "message": "يوجد أسم مستخدم بهذا الاسم بالفعل"
            })
        login(request,user)

        # add a defult Classification for evray new user 
        for classification in ['مسلسل', "فيلم"]:
            defult_ShowClassification = Classification(Classification_Owner=request.user,Classification=classification)
            defult_ShowClassification.save()

        defult_user_settings = Settings(user=request.user, Sort_Shows_By="Random")
        defult_user_settings.save()
        return HttpResponseRedirect(reverse("index"))
    else:     
        return render(request, "WatchingHub/register.html")


def addshow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        showOwner = request.user
        showtitle = data['showtitle']
        showimg = data['showimg']
        ShowClassification = [data['ShowClassification']]
        ShowDiscription = data['ShowDiscription'] or None
        ShowRaring = data['ShowRaring'] or None
        PublicationYear = data['PublicationYear'] or None
        DateFinishedWatching = data['DateFinishedWatching']  or None
        Duration = data['Duration'] or None
        


        newShow = Show(
            Show_Owner=showOwner,
            Show_title=showtitle,
            Show_img=showimg,
            Show_discription=ShowDiscription,
            Show_raring=ShowRaring,
            Publication_year=PublicationYear,
            Date_finished_watching = DateFinishedWatching,
            duration=Duration,
        )
        newShow.save()
        if len(ShowClassification) == 1 and  not isinstance(ShowClassification[0], list):
            for classification in ShowClassification:
                # if ShowClassification have onlay 1 component
                newShow.Show_Classification.add(Classification.objects.filter(Classification_Owner = request.user, Classification=classification).values('id')[0]['id'])
             
        else:
             for classification in ShowClassification[0]:
                # if ShowClassification have t more then 1 componen
                newShow.Show_Classification.add(Classification.objects.filter(Classification_Owner = request.user, Classification=classification).values('id')[0]['id'])
        return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))


def show_info(request, show_id):

    show = Show.objects.filter(pk=show_id).first()
    
    
    # Check if show_id its belongs to user
    if show.Show_Owner.id == request.user.id:
        data = {"Show_discription": show.Show_discription}
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "You don't have access to this show"}, status=403)


def edit_show(request, show_id):
    if request.method == "POST":

        # Search for the show using the provided show_id
        show = Show.objects.filter(pk=show_id).first()

        # Check if the show belongs to the current user
        if show.Show_Owner.id == request.user.id:
            # Get variables from the POST request
            show_title = request.POST.get('showtitle',)
            show_img = request.POST.get('showimg',)
            show_classification = request.POST.getlist('ShowClassification')
            show_description = request.POST.get('ShowDiscription', None)
            show_rating = request.POST.get('ShowRaring', None)
            date_finished_watching = request.POST.get('DateFinishedWatching', None)
            publication_year = request.POST.get('PublicationYear', None)
            duration = request.POST.get('Duration', None)

            # Update show fields
            if show_title:
                show.Show_title = show_title
            if show_img:
                show.Show_img = show_img

            if show_description:
                show.Show_discription = show_description

            if show_rating:
                show.Show_raring = show_rating

            if date_finished_watching:
                show.Date_finished_watching = date_finished_watching

            if publication_year:
                show.Publication_year = publication_year

            if duration:
                show.duration = duration


            
            if show_classification:
                    # if Show_Classification have onlay 1 component
                    classifications = Classification.objects.filter(
                        Classification_Owner=request.user,
                        Classification__in=show_classification
                    )
                    show.Show_Classification.set(classifications)

            # Save the updated show
            show.save()
            
            return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))


def DateFinishedWatching(request, show_id):

    show = Show.objects.filter(pk=show_id).first()
    
    # Check if show_id its belongs to user
    if show.Show_Owner.id == request.user.id:
        data = {"DateFinishedWatching": show.Date_finished_watching}
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "You don't have access to this show"}, status=403)    

def delete_show(request):
    if request.method == "POST":
        data = json.loads(request.body)
        show_id = data['show_id']
        show = Show.objects.filter(pk=show_id).first()

        # Check if the show belongs to the current user
        if show.Show_Owner.id == request.user.id:
            show.delete()
    else:
        return HttpResponseRedirect(reverse("index"))
    

def shorted_by(request):
    if request.method == "POST":
        sort_by = request.POST.get("sort_by", "Random") 
        user_settings, created = Settings.objects.get_or_create(user=request.user) 
        user_settings.Sort_Shows_By = sort_by  
        user_settings.save()  
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

def edit_filter(request):
        
        if request.method == "POST":
            if request.POST.get('filter_by_classification', '') != "":
                filter_by_classification = request.POST.get('filter_by_classification', '')
                new_setting = Settings.objects.get(user=request.user)
                new_setting.Filter_By_Classification=Classification.objects.filter(pk=filter_by_classification)[0]
                new_setting.save()
            else:
                print(request.POST.get('filter_by_classification', ''))
                new_setting = Settings.objects.get(user=request.user)
                new_setting.Filter_By_Classification_id = None
                new_setting.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))

def add_Classification(request):
    Classification_name = None

    if request.method == "POST":
        Classification_name = request.POST['Classification_name']
        print(Classification_name)
        new_Classification = Classification(Classification_Owner = request.user,Classification=Classification_name)
        new_Classification.save()
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return HttpResponseRedirect(reverse("index"))