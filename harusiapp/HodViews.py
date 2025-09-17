from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from harusiapp.forms import AddMwanaharusiForm, EditMwanaharusiForm
from harusiapp.models import CustomUser, Staffs, Courses, Subjects, Mwanaharusis, FeedBackMwanaharusi, FeedBackStaffs, \
    LeaveReportMwanaharusi, LeaveReportStaff

def admin_home(request):
    mwanaharusi_count=Mwanaharusis.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    mwanaharusi_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        mwanaharusi=Mwanaharusis.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        mwanaharusi_count_list_in_course.append(mwanaharusis)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    mwanaharusi_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        mwanaharusi_count=Mwanaharusis.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        mwanaharusi_count_list_in_subject.append(mwanaharusi_count)

    staffs=Staffs.objects.all()
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        staff_name_list.append(staff.admin.username)

    mwanaharusis_all=Mwanaharusis.objects.all()
    mwanaharusi_name_list=[]
    for mwanaharusi in mwanaharusis_all:
        leaves=LeaveReportMwanaharusi.objects.filter(mwanaharusi_id=mwanaharusi.id,leave_status=1).count()
        mwanaharusi_name_list.append(mwanaharusi.admin.username)


    return render(request,"hod_template/home_content.html",{"mwanaharusi_count":mwanaharusi_count,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"mwanaharusi_count_list_in_course":mwanaharusi_count_list_in_course,"mwanaharusi_count_list_in_subject":mwanaharusi_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list})

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_mwanaharusi(request):
    form=AddMwanaharusiForm()
    return render(request,"hod_template/add_mwanaharusi_template.html",{"form":form})

def add_mwanaharusi_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddMwanaharusiForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_start=form.cleaned_data["session_start"]
            session_end=form.cleaned_data["session_end"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.mwanaharusis.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.mwanaharusis.course_id=course_obj
                user.mwanaharusis.session_start_year=session_start
                user.mwanaharusis.session_end_year=session_end
                user.mwanaharusis.gender=sex
                user.mwanaharusis.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Mwanaharusi")
                return HttpResponseRedirect(reverse("add_mwanaharusi"))
            except:
                messages.error(request,"Failed to Add Mwanaharusi")
                return HttpResponseRedirect(reverse("add_mwanaharusi"))
        else:
            form=AddMwanaharusiForm(request.POST)
            return render(request, "hod_template/add_mwanaharusi_template.html", {"form": form})

def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_mwanaharusi(request):
    mwanaharusis=Mwanaharusis.objects.all()
    return render(request,"hod_template/manage_mwananaharusi_template.html",{"mwanaharusis":mwanaharusis})

def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_mwanaharusi(request,mwanaharusi_id):
    request.session['mwanaharusi_id']=mwanaharusi_id
    mwanaharusi=Mwanaharusis.objects.get(admin=mwanaharusi_id)
    form=EditMwanaharusiForm()
    form.fields['email'].initial=mwanaharusi.admin.email
    form.fields['first_name'].initial=mwanaharusi.admin.first_name
    form.fields['last_name'].initial=mwanaharusi.admin.last_name
    form.fields['username'].initial=mwanaharusi.admin.username
    form.fields['address'].initial=mwanaharusi.address
    form.fields['course'].initial=mwanaharusi.course_id.id
    form.fields['sex'].initial=mwanaharusi.gender
    form.fields['session_start'].initial=mwanaharusi.session_start_year
    form.fields['session_end'].initial=mwanaharusi.session_end_year
    return render(request,"hod_template/edit_mwanaharusi_template.html",{"form":form,"id":mwanaharusi_id,"username":mwanaharusi.admin.username})

def edit_mwanaharusi_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        mwanaharusi_id=request.session.get("mwanaharusi_id")
        if mwanaharusi_id==None:
            return HttpResponseRedirect(reverse("manage_mwanaharusi"))

        form=EditMwanaharusiForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_start = form.cleaned_data["session_start"]
            session_end = form.cleaned_data["session_end"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=mwanaharusi_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                mwanaharusi=Mwanaharusis.objects.get(admin=mwanaharusi_id)
                mwanaharusi.address=address
                mwanaharusi.session_start_year=session_start
                mwanaharusi.session_end_year=session_end
                mwanaharusi.gender=sex
                course=Courses.objects.get(id=course_id)
                mwanaharusi.course_id=course
                if profile_pic_url!=None:
                    mwanaharusi.profile_pic=profile_pic_url
                mwanaharusi.save()
                del request.session['mwanaharusi_id']
                messages.success(request,"Successfully Edited Mwanaharusi")
                return HttpResponseRedirect(reverse("edit_mwanaharusi",kwargs={"mwanaharusi_id":mwanaharusi_id}))
            except:
                messages.error(request,"Failed to Edit Mwanaharusi")
                return HttpResponseRedirect(reverse("edit_mwanaharusi",kwargs={"mwanaharusi_id":mwanaharusi_id}))
        else:
            form=EditMwanaharusiForm(request.POST)
            mwanaharusi=Mwanaharusis.objects.get(admin=mwanaharusi_id)
            return render(request,"hod_template/edit_mwanaharusi_template.html",{"form":form,"id":mwanaharusi_id,"username":mwanaharusi.admin.username})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")
        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":feedbacks})

def mwanaharusi_feedback_message(request):
    feedbacks=FeedBackMwanaharusi.objects.all()
    return render(request,"hod_template/mwanaharusi_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def mwanaharusi_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackMwanaharusi.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

def mwanaharusi_leave_view(request):
    leaves=LeaveReportMwanaharusi.objects.all()
    return render(request,"hod_template/mwanaharusi_leave_view.html",{"leaves":leaves})

def mwanaharusi_approve_leave(request,leave_id):
    leave=LeaveReportMwanaharusi.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("mwanaharusi_leave_view"))

def mwanaharusi_disapprove_leave(request,leave_id):
    leave=LeaveReportMwanaharusi.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("mwanaharusi_leave_view"))


def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_send_notification_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/staff_notification.html",{"staffs":staffs})

@csrf_exempt
def send_staff_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    staff=Staffs.objects.get(admin=id)
    token=staff.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Mwanaharusi Management System",
            "body":message,
            "click_action":"https://mwanaharusimanagementsystem22.herokuapp.com/staff_all_notification",
            "icon":"http://mwanaharusimanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStaffs(staff_id=staff,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
