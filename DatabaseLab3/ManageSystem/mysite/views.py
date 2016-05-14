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
    # 嵌套查询
    cur.execute('select c_no, c_name from course where c_no  in (select c_no from selection where student_no = %s)', username)
    courses = cur.fetchall()
    selected = []
    for course in courses:
        info = {'c_no': course[0], 'c_name': course[1]}
        selected.append(info)
    return render_to_response('student_index.html', locals())


def teacher_homepage(request):
    """
    显示教师看到的主页
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from teacher where t_no = %s', username)
    teacher = cur.fetchone()
    teacher_no = teacher[0]
    id = teacher[1]
    name = teacher[2]
    i_name = teacher[3]
    telephone = teacher[4]
    email = teacher[5]
    location = teacher[6]
    cur.execute('select c_no, c_name from course where t_no = %s', username)
    courses = cur.fetchall()
    sectioned = []
    for course in courses:
        info = {'c_no': course[0], 'c_name': course[1]}
        sectioned.append(info)
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


def manager_homepage(request):
    """
    显示教学主管看到的主页
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from manager where m_no = %s', username)
    manager = cur.fetchone()
    m_no = manager[0]
    id = manager[1]
    name = manager[2]
    i_name = manager[3]
    telephone = manager[4]
    email = manager[5]
    location = manager[6]
    return render_to_response('manager_index.html', locals())


def manager_teacher(request):
    """
    教学主管查看学院的教师
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from manager where m_no = %s', username)
    manager = cur.fetchone()
    m_no = manager[0]
    id = manager[1]
    name = manager[2]
    i_name = manager[3]
    telephone = manager[4]
    email = manager[5]
    location = manager[6]
    cur.execute('select t_no, teacher_name from teacher where i_name = %s', i_name)
    teachers = cur.fetchall()
    info_ = []
    for teacher in teachers:
        info = {'t_no': teacher[0], 'teacher_name': teacher[1]}
        info_.append(info)
    return render_to_response('manager_teacher.html', locals())


def manager_student(request):
    """
    教学主管查看学院的学生
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    cur = connection.cursor()
    cur.execute('select * from manager where m_no = %s', username)
    manager = cur.fetchone()
    m_no = manager[0]
    id = manager[1]
    name = manager[2]
    i_name = manager[3]
    telephone = manager[4]
    email = manager[5]
    location = manager[6]
    # 嵌套查询
    cur.execute('select student_no, student_name from student where d_name in (select d_name from discipline where '
                'i_name = %s)', i_name)
    students = cur.fetchall()
    info_ = []
    for student in students:
        info = {'student_no': student[0], 'student_name': student[1]}
        info_.append(info)
    return render_to_response('manager_student.html', locals())


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
            if Name != "账号" and Password != "Password" and Class != "身份":
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
                        elif Class == 'manager':
                            response = HttpResponseRedirect('/manager_home', locals())
                        response.set_cookie('username', Name, 3600*3)  # 写入cookie 登录时间是3个小时
                        return response
                else:
                    return render_to_response('login_failed.html')
            else:
                return render_to_response('login_failed.html')
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
            if no == '证件号' or password == '密码' or class_ == '身份':
                return render_to_response('register_failed.html')
            if class_ == 'student':
                cur = connection.cursor()
                cur.execute('select * from student where student_no = %s', no)
                user = cur.fetchone()
                if user:
                    cur.execute('select * from login where username = %s', no)
                    user = cur.fetchone()
                    if user:
                        return render_to_response('register_failed.html')
                    cur.execute('insert into login values(%s, %s, %s)', (no, class_, password))
                    response = HttpResponseRedirect('/student_home', locals())
                    response.set_cookie('username', no, 3600*3)
                    return response
                else:
                    return render_to_response('register_failed.html')
            elif class_ == 'teacher':
                cur = connection.cursor()
                cur.execute('select * from teacher where t_no = %s', no)
                user = cur.fetchone()
                if user:
                    cur.execute('select * from login where username = %s', no)
                    user = cur.fetchone()
                    if user:
                        return render_to_response('register_failed.html')
                    cur.execute('insert into login values(%s, %s, %s)', (no, class_, password))
                    response = HttpResponseRedirect('/teacher_home', locals())
                    response.set_cookie('username', no, 3600*3)
                    return response
                else:
                    return render_to_response('register_failed.html')
            elif class_ == 'stuff':
                cur = connection.cursor()
                cur.execute('select * from stuff where stuff_no = %s', no)
                user = cur.fetchone()
                if user:
                    cur.execute('select * from login where username = %s', no)
                    user = cur.fetchone()
                    if user:
                        return render_to_response('register_failed.html')
                    cur.execute('insert into login values(%s, %s, %s)', (no, class_, password))
                    response = HttpResponseRedirect('/stuff_home', locals())
                    response.set_cookie('username', no, 3600*3)
                    return response
                else:
                    return render_to_response('register_failed.html')
            elif class_ == 'manager':
                cur = connection.cursor()
                cur.execute('select * from manager where m_no = %s', no)
                user = cur.fetchone()
                if user:
                    cur.execute('select * from login where username = %s', no)
                    user = cur.fetchone()
                    if user:
                        return render_to_response('register_failed.html')
                    cur.execute('insert into login values(%s, %s, %s)', (no, class_, password))
                    response = HttpResponseRedirect('/manager_home', locals())
                    response.set_cookie('username', no, 3600*3)
                    return response
                else:
                    return render_to_response('register_failed.html')
            else:
                return render_to_response('register_failed.html')
    return render_to_response('register.html')


def section(request):
    """
    教师开课
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
    if request.method == 'POST':
        post = request.POST
        if post:
            course = post['c_name']
            c_no = post['c_no']
            if course == u'课程名' or c_no == u'课程号':  # 有没有填写的表项
                return render_to_response('section_failed.html', locals())
            cur = connection.cursor()
            cur.execute('select * from course where c_no = %s', c_no)
            course_ = cur.fetchone()
            if course_:  # 课程已经存在
                return render_to_response('section_failed.html', locals())
            cur.execute('insert into course values(%s, %s, %s)', (c_no, username, course))
            return HttpResponseRedirect('/teacher_home', locals())  # 转到课程的设置
    return render_to_response('section.html', locals())


def teacher_course(request):
    """
    教师查看开课信息
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
    cur.execute('select c_no, c_name from course NATURAL join teacher where t_no = %s', username.encode('utf-8'))
    courses = cur.fetchall()
    # 分组查询
    cur.execute('select count(*) from selection group by c_no')
    number = cur.fetchall()
    info_ = []
    for i in range(len(courses)):
        info = {'c_no': courses[i][0], 'c_name': courses[i][1], 'number': number[i][0]}
        info_.append(info)
    n = len(courses)
    if n > 0:
        return render_to_response('teacher_course.html', locals())
    else:
        return render_to_response('section_failed.html')


def teacher_delete(request):
    """
    教室删除开设的课程
    :param request:
    :return:
    """
    if request.GET:
        delete_c_no = request.GET["id"]
        cur = connection.cursor()
        # 删除选了这门课程的学生
        cur.execute('delete from selection where c_no = %s', delete_c_no)
        # 删除这门课程
        cur.execute('delete from course where c_no = %s', delete_c_no)
        return HttpResponseRedirect('/teacher_course')
    return HttpResponseRedirect('/teacher_course')


def student_course(request):
    """
    学生选课
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
    # 嵌套查询
    cur.execute('select c_no, c_name from course where c_no not in (select c_no from selection where student_no = %s)',
                username)
    courses = cur.fetchall()
    selecting = []
    for course in courses:
        info = {'c_no': course[0], 'c_name': course[1]}
        selecting.append(info)
    cur.execute('select c_no, c_name from course where c_no  in (select c_no from selection where student_no = %s)',
                username)
    courses = cur.fetchall()
    selected = []
    for course in courses:
        info = {'c_no': course[0], 'c_name': course[1]}
        selected.append(info)
    return render_to_response('student_course.html', locals())


def student_select(request):
    """
    学生选课
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    if request.GET:
        select_c_no = request.GET["id"]
        cur = connection.cursor()
        cur.execute('insert into selection values(%s, %s)', (select_c_no, username))
        return HttpResponseRedirect('/student_course')
    return HttpResponseRedirect('/student_course')


def student_delete(request):
    """
    学生退课
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    if request.GET:
        delete_c_no = request.GET["id"]
        cur = connection.cursor()
        cur.execute('delete from selection where c_no = %s and student_no = %s', (delete_c_no, username))
        return HttpResponseRedirect('/student_course')
    return HttpResponseRedirect('/student_course')


def stuff_course(request):
    """
    教务处职员查看选课信息
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
    # 连接查询
    cur.execute('select c_no, c_name, teacher_name from course NATURAL join teacher ')
    courses = cur.fetchall()
    info_ = []
    for course in courses:
        info = {'c_no': course[0], 'c_name': course[1], 't_name': course[2]}
        info_.append(info)

    return render_to_response('stuff_course.html', locals())


def stuff_look(request):
    """
    教务处职员查看选课名单
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
    if request.GET:
        c_no = request.GET["id"]
        cur.execute('select student_no, student_name from selection NATURAL JOIN student where c_no = %s', c_no)
        students = cur.fetchall()
        info_ = []
        for student in students:
            info = {'student_no': student[0], 'student_name': student[1]}
            info_.append(info)
    return render_to_response('stuff_look.html', locals())
