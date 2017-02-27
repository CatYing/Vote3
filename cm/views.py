# coding=utf8
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from models import *
from django.contrib import auth

import csv


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {'user': user}
    return render(request, 'index.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        user = None
        state = ""
        if request.method == "POST":
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse_lazy('list'))
            else:
                state = 'error'
        content = {
            'user': user,
            'state': state,
        }
        return render(request, 'login.html', content)


@login_required(login_url=reverse_lazy('login'))
def member_list(request):
    if request.method == "GET":
        user = request.user
        state = ""
        member_list = Member.objects.all()
        if Record.objects.filter(voter=user.myuser).count() != 0:
            state = "existed"
        content = {
            'user': user,
            'member_list': member_list,
            'state': state,
        }
        return render(request, 'list.html', content)
    elif request.method == "POST":
        user = request.user
        key_list = [i for i in request.POST.keys() if i != 'csrfmiddlewaretoken']
        if len(key_list) != Member.objects.count():
            return HttpResponse("您有未评分选手！")
        else:
            # 已经评分
            if Record.objects.filter(voter=user.myuser).count() != 0:
                for member_id in key_list:
                    member = Member.objects.get(id=int(member_id))
                    record = Record.objects.get(voter=user.myuser, member=member)
                    record.grade = request.POST.get(member_id)
                    record.save()

            else:
                for member_id in key_list:
                    member = Member.objects.get(id=int(member_id))
                    record = Record(
                        voter=user.myuser,
                        member=member,
                        grade=request.POST.get(member_id),
                    )
                    record.save()

            return HttpResponseRedirect(reverse_lazy('voter_rank'))


# @login_required(login_url=reverse_lazy('login'))
# def member_detail(request, member_id):
#     user = request.user
#     state = ''
#     record_state = ''
#     last_grade = 0
#     member_list = Member.objects.filter(id=member_id)
#     if len(member_list) < 1:
#         return HttpResponseRedirect(reverse_lazy('list'))
#     else:
#         member = member_list[0]
#         # if len(Record.objects.filter(member=member)) >= 1:
#         #     average = 0
#         #     for record in Record.objects.filter(member=member):
#         #         average += float(record.grade)
#         #     average /= Record.objects.filter(member=member).count()
#         # else:
#         #     average = 0
#         if len(Record.objects.filter(voter=request.user.myuser, member=member)) >= 1:
#             record_state = 'existed'
#             last_grade = Record.objects.filter(voter=request.user.myuser, member=member)[0].grade
#             if request.method == "POST":
#                 grade = request.POST.get('grade', '')
#                 try:
#                     a = float(grade)
#                 except:
#                     return HttpResponse("输入不合法，请输入数字")
#                 record = Record.objects.get(voter=request.user.myuser, member=member)
#                 record.grade = grade
#                 record.save()
#                 state = 'success'
#         else:
#             record_state = 'not_existed'
#             if request.method == "POST":
#                 grade = request.POST.get('grade', '')
#                 try:
#                     a = float(grade)
#                 except:
#                     return HttpResponse("输入不合法，请输入数字")
#                 record = Record(
#                     member=member,
#                     voter=request.user.myuser,
#                     grade=grade
#                 )
#                 record.save()
#                 record_state = 'existed'
#                 last_grade = grade
#                 state = 'success'
#         content = {
#             'user': user,
#             'member': member,
#             'state': state,
#             'record_state': record_state,
#             'last_grade': last_grade,
#         }
#         return render(request, 'detail.html', content)


@login_required(login_url=reverse_lazy('login'))
def edit_grade(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        grade = request.POST.get('grade')
        member = Member.objects.get(id=int(member_id))
        record = Record.objects.get(voter=request.user.myuser, member=member)
        record.grade = grade
        record.save()
        return HttpResponse('success!')


@login_required(login_url=reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required(login_url=reverse_lazy('login'))
def voter_rank(request):
    user = request.user
    record_list = Record.objects.filter(voter=user.myuser)
    content = {
        'user': user,
        'record_list': record_list,
    }
    return render(request, 'voter-rank.html', content)


@login_required(login_url=reverse_lazy('login'))
def all_rank(request):
    user = request.user
    myuser = user.myuser
    if not myuser.permission:
        return HttpResponse('您无权查看选手总榜')
    else:
        member_list = Member.objects.all()
        voter_list = MyUser.objects.all()
        contentDisposition = u'attachment; filename=\"' + u'选手总榜.csv\"'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = contentDisposition.encode('gbk')
        writer = csv.writer(response)
        first_line = [" "]
        for voter in voter_list:
            first_line.append(voter.name.encode('gbk'))
        writer.writerow(first_line)
        for member in member_list:
            temp_list = [member.name.encode('gbk')]
            for voter in voter_list:
                record = Record.objects.filter(member=member, voter=voter)
                if record:
                    temp_list.append(record[0].grade.encode('gbk'))
                else:
                    temp_list.append(" ")
            writer.writerow(temp_list)
        return response
