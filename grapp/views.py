from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, HttpResponse
from .sender import send_otp_to_phone
from .models import CustomUser,  Branch, Zone, HeadOffice
from django.contrib.auth import login, authenticate, logout
from .forms import OTPForm, loginform, HZBForm


def home(request):
    if request.user.is_authenticated:
        ulogin = True
    else:
        ulogin = False
    context = {"login": ulogin}
    return render(request, "grsolapp/home.html", context)


def User_register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":

            HZBform = HZBForm(request.POST)

            if HZBform.is_valid():
                branch = HZBform.cleaned_data['branch']
                zone = HZBform.cleaned_data['zone']
                head_office = HZBform.cleaned_data['head_office']
                access_level = HZBform.cleaned_data['access_level']
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            Password = request.POST.get("Password")
            username = request.POST.get("username")

            check_email = CustomUser.objects.filter(email=email).first()
            check_phone = CustomUser.objects.filter(Phone_number=phone).first()
            check_username = CustomUser.objects.filter(
                username=username).first()
            if check_email or check_phone or check_username:
                if check_email:
                    msg = "Email is Already registered"
                elif check_phone:
                    msg = "Phone Number is Already registered"
                elif check_username:
                    msg = "Username Already Exist!"
                hzbform = HZBForm()
                context = {"message": msg,
                           "class": "danger", "myform": hzbform}
                return render(request, "grsolapp/register.html", context)
            else:
                user_data = CustomUser.objects.create(
                    username=username, email=email, Phone_number=phone, branch=str(branch), zone=str(zone), head_office=str(head_office), access_level=str(access_level))
                user_data.set_password(Password)

                user_data.save()
                request.session["mobile"] = phone
                return redirect("/login/")
        else:
            hzbform = HZBForm()

            return render(request, "grsolapp/register.html", {"myform": hzbform})
    else:
        return redirect("/profile/")


# login form


def User_login(request):
    if not request.user.is_authenticated:

        if request.method == "POST":

            formdata = loginform(request.POST)
            if formdata.is_valid():
                phone = formdata.cleaned_data["Phone"]

            try:
                registered_phone = request.session['mobile']
            except Exception as e:
                try:
                    registered_phone = CustomUser.objects.get(
                        Phone_number=phone).Phone_number
                except CustomUser.DoesNotExist:
                    hzbform = HZBForm()
                    context = {
                        "message": "your number is not registered please register it", "class": "warning", "myform": hzbform}
                    return render(request, "grsolapp/register.html", context)

            if phone == registered_phone:
                otp = send_otp_to_phone(registered_phone)
                CustomUser.objects.filter(Phone_number=phone).update(
                    otp=otp, Phone_is_verified=True)
                request.session["otp"] = otp
                return redirect("/enterOtp/")
            else:
                hzbform = HZBForm()
                context = {
                    "message": "your number is not registered please register it", "class": "warning", "myform": hzbform}
                return render(request, "grsolapp/register.html", context)
        else:
            formdata = loginform()
            return render(request, "grsolapp/login.html", {"form": formdata})

    else:
        return redirect("/profile/")


def Enter_otp(request):

    if not request.user.is_authenticated:
        if request.method == "POST":
            formdata = OTPForm(request.POST)
            if formdata.is_valid():
                otp = formdata.cleaned_data['otp']
                user = authenticate(request=request, otp=otp)
                if user is not None:
                    login(request, user)
                    return redirect("/profile/")
                else:
                    context = {"message": "invalid otp ",
                               "class": "warning", "form": formdata}
                    return render(request, "grsolapp/otp.html", context)

            else:
                context = {"message": "invalid otp ",
                           "class": "warning", "form": formdata}

                return render(request, "grsolapp/otp.html", context)
        else:
            formdata = OTPForm()
            context = {"message": "We have sent an otp to your Registered Mobile Number ",
                       "class": "success", "form": formdata}
            return render(request, "grsolapp/otp.html",  context)

    else:
        return redirect("/profile/")


# get the content type for the Branch model
content_type = ContentType.objects.get_for_model(Branch)


def User_profile(request):
    if request.user.is_authenticated:
        headofficename = request.user.head_office
        zonename = request.user.zone
        branchname = request.user.branch

        mycontext = generate_report(request)

        return render(request, "grsolapp/profile.html", mycontext)
    else:
        return redirect("/login/")


def generate_report(request):
    Position = request.user.access_level
    if Position == "admin":
        report = generate_headoffice_report(request)
        headofficename = request.user.head_office
        context = {"message": "Hey Admin(head-office) show all zones Under this Head-office",
                   "class": "success", "report": report, "fieldname": "Zones", "Name_field": f'Head-office = {headofficename}'}
    elif Position == 'manager':
        report = generate_zones_report(request)
        zonename = request.user.zone
        context = {"message": "Hey Manager(zone) you will show all branches report",
                   "class": "success", "report": report, "fieldname": "Branches", "Name_field": f'Zone = {zonename}'}

    elif Position == "employee":
        report = generate_branch_report(request)
        branchname = request.user.branch
        context = {"message": "Hey Employee (Branch) you will show only branch level report",
                   "class": "success", "report": report, "fieldname": "Branch User Data", "Name_field": f'Branch = {branchname}'}
    return context


def generate_headoffice_report(request):
    headofficename = request.user.head_office
    headofficeId = HeadOffice.objects.get(
        HeadOffice_name=headofficename).HeadOffice_id
    allzonesname = Zone.objects.filter(head_office=headofficeId)
    list = [str(zones) for zones in allzonesname]
    return list


def generate_branch_report(request):
    branchname = request.user.branch
    allbranchuser = CustomUser.objects.filter(branch=branchname)
    UsersLIst = [users.username for users in allbranchuser]
    return UsersLIst


def generate_zones_report(request):
    zonename = request.user.zone
    ZoneId = Zone.objects.get(
        Zone_name=zonename).Zone_id
    Allbranchname = Branch.objects.filter(zone=ZoneId)
    branchlist = [str(branches) for branches in Allbranchname]
    return branchlist


def User_logout(request):
    logout(request)
    return redirect("/login/")
