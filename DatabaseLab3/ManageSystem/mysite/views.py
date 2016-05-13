# coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
# Create your views here.


def student_homepage(request):
    """
    显示学生看到的主页
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from student where student_no = %s', username.encode('utf-8'))
    student = cur.fetchone()
    student_no = student[0]
    name = student[1]
    id = student[2]
    d_name = student[3]
    telephone = student[4]
    email = student[5]
    cur.execute('select * from discipline WHERE d_name = %s', d_name)
    i_name = cur.fetchone()[1]

    return render_to_response('student_index.html', locals())


def teacher_homepage(request):
    """
    显示教师看到的主页
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from teacher where t_no = %s', username.encode('utf-8'))
    teacher = cur.fetchone()
    teacher_no = teacher[0]
    id = teacher[1]
    name = teacher[2]
    i_name = teacher[3]
    telephone = teacher[4]
    email = teacher[5]
    location = teacher[6]
    return render_to_response('teacher_index.html', locals())


def stuff_homepage(request):
    """
    显示职工看到的主页
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from stuff where stuff_no = %s', username.encode('utf-8'))
    stuff = cur.fetchone()
    stuff_no = stuff[0]
    id = stuff[1]
    name = stuff[2]
    telephone = stuff[3]
    email = stuff[4]
    return render_to_response('stuff_index.html', locals())


def login(request):
    """
    登录页面
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = request.POST
        if post:
            Name = post['username']
            Password = post['password']
            Class = post['class']
            if Name != "" and Password != "" and Class != "":
                cur = connection.cursor()
                cur.execute('select * from login where username = %s GROUP BY %s', (Name, Class))
                user = cur.fetchone()
                if user:
                    password_ = user[2]
                    if password_ == Password:
                        # 登录成功
                        if Class == 'student':
                            response = HttpResponseRedirect('/student_home', locals())
                        elif Class == 'teacher':
                            response = HttpResponseRedirect('/teacher_home', locals())
                        elif Class == 'stuff':
                            response = HttpResponseRedirect('/stuff_home', locals())
                        response.set_cookie('username', Name, 3600*3)  # 写入cookie 登录时间是3个小时
                        return response
                else:
                    return HttpResponseRedirect('/register')
            else:
                return render_to_response('login.html')
    return render_to_response('login.html', locals())


def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    response = HttpResponseRedirect('/')
    response.delete_cookie('username')  # 删除cookie
    return response


def student_setting(request):
    """
    查看学生个人信息
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from student where student_no = %s', username.encode('utf-8'))
    student = cur.fetchone()
    student_no = student[0]
    name = student[1]
    id = student[2]
    d_name = student[3]
    telephone = student[4]
    email = student[5]
    cur.execute('select * from discipline WHERE d_name = %s', d_name)
    i_name = cur.fetchone()[1]

    return render_to_response('student_info.html', locals())


def student_setting_change(request):
    """
    修改学生个人信息
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from student where student_no = %s', username.encode('utf-8'))
    student = cur.fetchone()
    student_no = student[0]
    name = student[1]
    id = student[2]
    d_name = student[3]
    cur.execute('select * from discipline WHERE d_name = %s', d_name)
    i_name = cur.fetchone()[1]
    if request.method == 'POST':
        post = request.POST
        if post:
            email = post['email']
            telephone = post['telephone']
            cur.execute('update student set telephone = %s WHERE student_no = %s', (telephone, student_no))
            cur.execute('update student set email = %s WHERE student_no = %s', (email, student_no))
            return HttpResponseRedirect('/student_setting', locals())
    return render_to_response('student_setting.html', locals())


def teacher_setting(request):
    """
    教师个人信息
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from teacher where t_no = %s', username.encode('utf-8'))
    teacher = cur.fetchone()
    teacher_no = teacher[0]
    id = teacher[1]
    name = teacher[2]
    i_name = teacher[3]
    telephone = teacher[4]
    email = teacher[5]
    location = teacher[6]
    return render_to_response('teacher_info.html', locals())


def teacher_setting_change(request):
    """
    修改教师个人信息
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from teacher where t_no = %s', username.encode('utf-8'))
    teacher = cur.fetchone()
    teacher_no = teacher[0]
    id = teacher[1]
    name = teacher[2]
    i_name = teacher[3]
    location = teacher[6]
    if request.method == 'POST':
        post = request.POST
        if post:
            email = post['email']
            telephone = post['telephone']
            cur.execute('update teacher set telephone = %s WHERE t_no = %s', (telephone, teacher_no))
            cur.execute('update teacher set email = %s WHERE t_no = %s', (email, teacher_no))
            return HttpResponseRedirect('/teacher_setting', locals())
    return render_to_response('teacher_setting.html', locals())


def stuff_setting(request):
    """
    职员个人信息
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from stuff where stuff_no = %s', username.encode('utf-8'))
    stuff = cur.fetchone()
    stuff_no = stuff[0]
    id = stuff[1]
    name = stuff[2]
    telephone = stuff[3]
    email = stuff[4]
    return render_to_response('stuff_info.html', locals())


def stuff_setting_change(request):
    """
    修改职员个人信息
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from stuff where stuff_no = %s', username.encode('utf-8'))
    stuff = cur.fetchone()
    stuff_no = stuff[0]
    id = stuff[1]
    name = stuff[2]
    if request.method == 'POST':
        post = request.POST
        if post:
            email = post['email']
            telephone = post['telephone']
            cur.execute('update stuff set telephone = %s WHERE stuff_no = %s', (telephone, stuff_no))
            cur.execute('update stuff set email = %s WHERE stuff_no = %s', (email, stuff_no))
            return HttpResponseRedirect('/stuff_setting', locals())
    return render_to_response('stuff_setting.html', locals())


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = request.POST
        if post:
            no = post['no']
            password = post['password']
            class_ = post['class']
            if class_ == 'student':
                cur = connection.cursor()
                cur.execute('select * from student where student_no = %s', no)
                user = cur.fetchone()
                if user:
                    cur.execute('insert into login values(%s, %s, %s)', (no, class_, password))
                    response = HttpResponseRedirect('/student_home', locals())
                    response.set_cookie('username', no, 3600*3)
                    return response
                else:
                    return HttpResponseRedirect('/register')
            elif class_ == 'teacher':
                cur = connection.cursor()
                cur.execute('select * from teacher where t_no = %s', no)
                user = cur.fetchone()
                if user:
                    cur.execute('insert into login values(%s, %s, %s)', (no, class_, password))
                    response = HttpResponseRedirect('/home', locals())
                    response.set_cookie('username', no, 3600*3)
                    return response
                else:
                    return HttpResponseRedirect('/register')
            elif class_ == 'stuff':
                cur = connection.cursor()
                cur.execute('select * from stuff where stuff_no = %s', no)
                user = cur.fetchone()
                if user:
                    cur.execute('insert into login values(%s, %s, %s)', (no, class_, password))
                    response = HttpResponseRedirect('/home', locals())
                    response.set_cookie('username', no, 3600*3)
                    return response
                else:
                    return HttpResponseRedirect('/register')
            else:
                return HttpResponseRedirect('/register')
    return render_to_response('register.html')

