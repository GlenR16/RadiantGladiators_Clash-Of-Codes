from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,RedirectView
from .forms import PasswordChangeForm,UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponse
from .models import User,Interest,Swipe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.db.models import Sum
from aiml.verification.verify import verifyImage

checkbox = {
    "on":True,
    "off":False
}
FaviconView = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

class IndexView(TemplateView):
    template_name = "index.html"

class LogoutView(RedirectView):
    permanent = True
    pattern_name = 'home:login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class ProfileView(TemplateView):
    template_name = "profile.html"
    
    def post(self, request, *args, **kwargs):
        bio = request.POST.get("bio","")
        address = request.POST.get("address","")
        profile_image = request.POST.get("profile_image","")
        profile_image = request.POST.get("profile_image","")
        profile_image = request.POST.get("profile_image","")
        
        return self.render_to_response({"form":form})
        
class LoginView(TemplateView):
    template_name = "authentication/login.html"

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request,email=request.POST.get("username",""),password=request.POST.get("password",""))
            if user is not None:
                login(request,user)
                return redirect("/dashboard/")
        return self.render_to_response({"form":form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserLoginForm(self.request.user)
        return context

def get_otp(request):
    name = request.POST.get("name","")
    phone = request.POST.get("phone","")
    email = request.POST.get("email","")
    dob = request.POST.get("dob","")
    gender = request.POST.get("gender","")
    verification_file = request.FILES.get("verification_file","")
    who_to_date = request.POST.get("who_to_date","")
    password1 = request.POST.get("password1","")
    password2 = request.POST.get("password2","")
    if name != "" and verification_file != "" and who_to_date != "" and email != "" and phone != ""  and password1 != "" and password2 != "" and dob != "" and gender != "" and password1 != "" and password2 != "" and password1 == password2:
        user = User(email=email,name=name,verification_file=verification_file,phone=phone,dob=dob,gender=gender)
        user.set_password(password1)
        user.save()
        print("otp==>",user.otp)
        return JsonResponse(data={"id":user.id})
    return HttpResponse(status=500)

def check_otp(request):
    userid = request.POST.get("id","")
    otp = request.POST.get("otp","")
    user = get_object_or_404(User,pk=userid)
    if otp != "" and int(otp)==user.otp:
        user.email_is_verified = True
        user.save()
        return JsonResponse(data={"correct":True})
    return JsonResponse(data={"correct":False})


class SignupView(TemplateView):
    template_name = "authentication/signup.html"

    def post(self, request, *args, **kwargs):
        userid = request.POST.get("id","")
        user = get_object_or_404(User,pk=userid)
        bio = request.POST.get("bio","")
        college = request.POST.get("college","")
        insta_username = request.POST.get("insta_username","")
        height = request.POST.get("height","")
        country = request.POST.get("country","")
        interests = { j.name:request.POST.get(j.name,"") for j in Interest.objects.all() if request.POST.get(j.name,"") != ""}
        is_habit_drink = request.POST.get("is_habit_drink","")
        is_habit_smoke = request.POST.get("is_habit_smoke","")
        profile_image = request.FILES.get("profile_image","")
        if bio != "":
            user.bio = bio
        if college != "":
            user.college = college
        if insta_username != "":
            user.insta_username = insta_username
        if country != "":
            user.country = country
        if len(interests) != 0:
            for k in interests:
                if interests[k] == True:
                    user.interests.add(Interest.objects.get(name=k))
                else:
                    user.interests.remove(Interest.objects.get(name=k))
        if height != "":
            user.height = height
        if is_habit_drink != "":
            user.is_habit_drink = is_habit_drink
        if is_habit_smoke != "":
            user.is_habit_smoke = is_habit_smoke
        if profile_image != "":
            user.profile_image = profile_image
            user.face_detection_probablity = verifyImage(profile_image.file)
        user.save()
        login(request,user)
        return redirect("/dashboard/")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        return super().get(request, *args, **kwargs)

class PasswordChangeView(LoginRequiredMixin,TemplateView):
    template_name = "authentication/passwordchange.html"
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return render(request,"authentication/passworddone.html")
        else:
            return self.render_to_response({"form":form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PasswordChangeForm(self.request.user)
        return context

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = User.objects.order_by('date_joined', 'likes')[:100]
        context["profiles"] = profiles
        return context

class RecommendedView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required(login_url='/login/')
def APIView(request):
    userid = request.POST.get("id","")
    swipe = request.POST.get("swipe","")
    user = get_object_or_404(User,pk=userid)
    if swipe == "RIGHT":
        swipe = Swipe(first_user=request.user,second_user=user,type="LIKE")
        swipe.save()
        user.likes += 1
        user.user_score = min(user.user_score+request.user.user_score *0.01,3000)
        swipes = Swipe.objects.get(first_user=user)
        right = swipes.filter(type="RIGHT")
        left = swipes.filter(type="LEFT")
        if right.count() >= swipes.count() *0.8:
            selfuser = User.objects.get(id=request.user.id)
            selfuser.score -= 50
            selfuser.save()
        user.save() 
        return JsonResponse(data={"submitted":True})
    elif swipe == "LEFT":
        swipe = Swipe(first_user=request.user,second_user=user,type="DISLIKE")
        swipe.save()
        user.dislikes += 1
        swipes = Swipe.objects.get(second_user=user)
        right = swipes.filter(type="RIGHT")
        left = swipes.filter(type="LEFT")
        if left.count() >= swipes.count() *0.8:
            user.user_score += 20
        user.save() 
        return JsonResponse(data={"submitted":True})
    return JsonResponse(data={"submitted":False})

@login_required(login_url='/login/')
def Recommendations(request):
    pass

def send_email(animal):
    """
    Send email to NGO with animal details.
    """
    message = get_template("email.html").render(Context({
        'animal': animal
    }))
    valid = [ ]
    mail = EmailMessage(
        subject="Injured Animal reported near you.",
        body=message,
        from_email="emergency@pawsforacause.com",
        to=valid,
        reply_to=["emergency@pawsforacause.com"],
    )
    mail.content_subtype = "html"
    return mail.send()