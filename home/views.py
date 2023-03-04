from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,RedirectView
from .forms import PasswordChangeForm,UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.db.models import Sum

checkbox = {
    "on":True,
    "off":False
}
FaviconView = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class DonateView(TemplateView):
    template_name = "donate.html"

class LogoutView(RedirectView):
    permanent = True
    pattern_name = 'home:login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class ProfileView(TemplateView):
    template_name = "upload.html"

    def post(self, request, *args, **kwargs):
        pass
        
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

class SignupView(TemplateView):
    template_name = "authentication/signup.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        about = request.POST.get("about","")
        password1 = request.POST.get("password1","")
        password2 = request.POST.get("password2","")
        website = request.POST.get("website","")
        address = request.POST.get("address","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        postalcode = request.POST.get("postalcode","")
        activemembers = request.POST.get("activemembers","")
        alerts = request.POST.get("alerts","")
        country = request.POST.get("country","")
        newsletter = request.POST.get("newsletter","")
        verificationfile = request.FILES.get("verificationfile","")
        if name != "" and verificationfile != "" and email != "" and phone != "" and about != "" and password1 != "" and password2 != "" and website != "" and address != "" and city != "" and state != "" and postalcode != "" and alerts != "" and country != "" and newsletter != "" and password1 != "" and password1 == password2:
            address = address +", "+ city +" "+ postalcode+", " + state +", "+ country
            user = User(name=name,email=email,phone=phone,verification_file=verificationfile,about=about,active_members=activemembers,website="https://"+website,address=address,alerts=checkbox[alerts],newsletters=checkbox[newsletter])
            user.set_password(password1)
            user.save()
            login(request,user)
            return redirect("/dashboard")
        else:
            return self.render_to_response({"error":True})

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

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get("id","")
        status = request.POST.get("status","")
        if ticket_id != "" and status != "":
            animal = get_object_or_404(Animal,pk=ticket_id)
            if animal.status == "Allotted" and animal in request.user.ticket:
                animal.status = STATUS[status]
                animal.save()
                return self.render_to_response({"submitted":True})
        return self.render_to_response({"submitted":False})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = self.request.user.tickets.all()
        return context

class RecommendedView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get("id","")
        status = request.POST.get("status","")
        if ticket_id != "" and status != "":
            animal = get_object_or_404(Animal,pk=ticket_id)
            if animal.status == "Allotted" and animal in request.user.ticket:
                animal.status = STATUS[status]
                animal.save()
                return self.render_to_response({"submitted":True})
        return self.render_to_response({"submitted":False})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = self.request.user.tickets.all()
        return context


@login_required(login_url='/login/')
def APIView(request):
    offset_lat = 360 * SEARCH_RADIUS / 40075016.686
    offset_long = 360 * SEARCH_RADIUS / 40075017
    up = request.user.latitude + offset_lat
    down = request.user.latitude - offset_lat
    left = request.user.longitude - offset_long
    right = request.user.longitude + offset_long
    valid = Animal.objects.filter(latitude__lte=up,latitude__gte=down,longitude__lte=right,longitude__gte=left,status="Pending")
    if request.method == "POST":
        id = request.POST.get("id",None)
        animal = get_object_or_404(valid,pk=id)
        user = User.objects.get(pk=request.user.id)
        animal.status = STATUS["ALLOTTED"]
        animal.save()
        user.tickets.add(animal)
        return JsonResponse(data={"submitted":True})
    data = AnimalSerializer(valid,many=True)
    return JsonResponse(data=data.data,safe=False)

def send_email(animal):
    """
    Send email to NGO with animal details.
    """
    message = get_template("email.html").render(Context({
        'animal': animal
    }))
    offset_lat = 360 * SEARCH_RADIUS / 40075016.686
    offset_long = 360 * SEARCH_RADIUS / 40075017
    up = animal.latitude + offset_lat
    down = animal.latitude - offset_lat
    left = animal.longitude - offset_long
    right = animal.longitude + offset_long
    valid = [ a.email  for a in User.objects.filter(latitude__lte=up,latitude__gte=down,longitude__lte=right,longitude__gte=left) if a.alerts ]
    mail = EmailMessage(
        subject="Injured Animal reported near you.",
        body=message,
        from_email="emergency@pawsforacause.com",
        to=valid,
        reply_to=["emergency@pawsforacause.com"],
    )
    mail.content_subtype = "html"
    return mail.send()