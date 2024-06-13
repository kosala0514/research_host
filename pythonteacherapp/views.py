from django.shortcuts import render, redirect
from django.http import HttpResponse
from pythonteacherapp.forms import UserForm
from pythonteacherapp.forms import LoginForm
from pythonteacherapp.models import User
from pythonteacherapp.models import PreTest
from .models import Assignment
from django.http import HttpResponse
from django.template.loader import render_to_string
import subprocess
import os
from django.views.decorators.csrf import csrf_exempt
from difflib import SequenceMatcher
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from django.conf import settings
import ast
import tempfile
from django.contrib.auth.hashers import check_password
import json
from django.contrib.auth import logout
# from django.contrib.auth import authenticate, login

loging_user = {}

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = UserForm()
    return render(request,'register.html',{'form':form})

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                global loging_user
                loging_user= user
                password_match = check_password(password, user.password)
                if password_match:
                    request.session['name'] = user.name
                    request.session['email'] = user.email
                    request.session['user_id'] = user.id
                    # request.session['custom_data'] = user
                    if user.test_marks == 0:
                        questions = PreTest.objects.all()
                        return render(request, 'index.html', {'questions': questions})
                    elif user.test_marks < 40:
                        return render(request, 'low_level/index.html', {'user': user})
                    elif user.test_marks < 75:
                        return render(request, 'medium_level/index.html', {'user': user})
                    else:
                        return render(request, 'high_level/index.html', {'user': user})
                else:
                    form = LoginForm()
                    return render(request, 'login.html', {'error_message': 'Invalid login credentials.', 'form': form})
            except User.DoesNotExist:
                form = LoginForm()
                return render(request, 'login.html', {'error_message': 'Invalid login credentials.', 'form': form})  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def addnew(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = UserForm()
    return render(request, 'index.html',{'form':form})

def edit(request, id):
    user = User.objects.get(id=id)
    return render(request, 'edit.html', {'user': user})

def updatetestmark(request):
    if request.method == 'POST':
        questions = PreTest.objects.all()
        total_marks = 20
        obtained_marks = 0
        for question in questions:
            selected_option = request.POST.get(f'question{question.id}')
            print(question.correct_answer)
            if question.correct_answer == selected_option:
                obtained_marks += 1
        # calculate percentage
        percentage = obtained_marks / total_marks * 100
        user_id = request.session.get('user_id')
        if user_id:
        # retrieve user object
            user = User.objects.get(id=user_id)
            user.test_marks = percentage
            user.save()
            if user.test_marks < 40:
                return render(request, 'low_level/index.html')
            elif user.test_marks < 75:
                return render(request, 'medium_level/index.html')
            else:
                return render(request, 'high_level/index.html')
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
    else:
        questions = PreTest.objects.all()
        return render(request, 'index.html', {'questions': questions})
    # user = User.objects.get(id=id)
    # form = UserForm(request.POST, instance = user)
    # if form.is_valid():
    #     form.save()
    #     return redirect("/")
    # return render(request, 'edit.html', {'user': user})

def delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('/')

# All Level chapters
def chapter(request):
    number = request.GET.get('lesson')
    number = int(number) if number else None
    global loging_user
    # user = request.session.get('custom_data')
    if loging_user.test_marks < 40 :
        if number == 1:
            content = render_to_string('low_level/chapter_01/index.html')
        elif number == 2:
            content = render_to_string('low_level/lesson_02/index.html')
        elif number == 3:
            content = render_to_string('low_level/lesson_03/index.html')
        elif number == 4:
            content = render_to_string('low_level/lesson_04/index.html')
        elif number == 5:
            content = render_to_string('low_level/lesson_05/index.html')
        elif number == 6:
            content = render_to_string('low_level/lesson_06/index.html')
        elif number == 7:
            content = render_to_string('low_level/lesson_07/index.html')
        elif number == 8:
            content = render_to_string('low_level/lesson_08/index.html')
        elif number == 9:
            content = render_to_string('low_level/lesson_09/index.html')
        elif number == 10:
            content = render_to_string('low_level/lesson_10/index.html')
        elif number == 11:
            content = render_to_string('low_level/lesson_11/index.html')
        elif number == 12:
            content = render_to_string('low_level/lesson_12/index.html')
        elif number == 13:
            content = render_to_string('low_level/lesson_13/index.html')
        elif number == 14:
            content = render_to_string('low_level/lesson_14/index.html')
        elif number == None:
            content = render_to_string('low_level/welcome.html')
        else:
            content = render_to_string('low_level/welcome.html')

    elif loging_user.test_marks < 75 :
        if number == 1:
            content = render_to_string('medium_level/chapter_01/index.html')
        elif number == 2:
            content = render_to_string('medium_level/lesson_02/index.html')
        elif number == 3:
            content = render_to_string('medium_level/lesson_03/index.html')
        elif number == 4:
            content = render_to_string('medium_level/lesson_04/index.html')
        elif number == 5:
            content = render_to_string('medium_level/lesson_05/index.html')
        elif number == 6:
            content = render_to_string('medium_level/lesson_06/index.html')
        elif number == 7:
            content = render_to_string('medium_level/lesson_07/index.html')
        elif number == 8:
            content = render_to_string('medium_level/lesson_08/index.html')
        elif number == 9:
            content = render_to_string('medium_level/lesson_09/index.html')
        elif number == 10:
            content = render_to_string('medium_level/lesson_10/index.html')
        elif number == 11:
            content = render_to_string('medium_level/lesson_11/index.html')
        elif number == 12:
            content = render_to_string('medium_level/lesson_12/index.html')
        elif number == 13:
            content = render_to_string('medium_level/lesson_13/index.html')
        elif number == 14:
            content = render_to_string('medium_level/lesson_14/index.html')
        elif number == None:
            content = render_to_string('medium_level/welcome.html')
        else:
            content = render_to_string('medium_level/welcome.html')

    else:
        if number == 1:
            content = render_to_string('high_level/chapter_01/index.html')
        elif number == 2:
            content = render_to_string('high_level/lesson_02/index.html')
        elif number == 3:
            content = render_to_string('high_level/lesson_03/index.html')
        elif number == 4:
            content = render_to_string('high_level/lesson_04/index.html')
        elif number == 5:
            content = render_to_string('high_level/lesson_05/index.html')
        elif number == 6:
            content = render_to_string('high_level/lesson_06/index.html')
        elif number == 7:
            content = render_to_string('high_level/lesson_07/index.html')
        elif number == 8:
            content = render_to_string('high_level/lesson_08/index.html')
        elif number == 9:
            content = render_to_string('high_level/lesson_09/index.html')
        elif number == 10:
            content = render_to_string('high_level/lesson_10/index.html')
        elif number == 11:
            content = render_to_string('high_level/lesson_11/index.html')
        elif number == 12:
            content = render_to_string('high_level/lesson_12/index.html')
        elif number == 13:
            content = render_to_string('high_level/lesson_13/index.html')
        elif number == 14:
            content = render_to_string('high_level/lesson_14/index.html')
        elif number == None:
            content = render_to_string('high_level/welcome.html')
        else:
            content = render_to_string('high_level/welcome.html')
    return HttpResponse(content)

def execute_code(request):
    if request.method == 'POST':
        # Get the code from the request
        code = request.POST.get('code', '')
        # print(code)
        try:
            # Save the code to a temporary file
            filename = 'temp.py'
            with open(filename, 'w') as f:
                f.write(code)
            # Execute the Python code
            result = subprocess.run(['python', filename], capture_output=True, text=True)
            # print(result)
        finally:
            # Delete the temporary file
            os.remove(filename)
            # subprocess.run(['rm', filename])
        if result.stderr:
            return HttpResponse(result.stderr)
        else:
            return HttpResponse(result.stdout)

def assignment(request):
    number = request.GET.get('lesson')
    number = int(number) if number else None
    global loging_user    
    assignments = get_assignments_by_user(loging_user.id)
    print(assignments)
    # user = request.session.get('custom_data')
    if loging_user.test_marks < 40 :
        if number == 1:
            content = render_to_string('low_level/assignments/lesson_1/assignment_1.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 2:
            content = render_to_string('low_level/assignments/lesson_2/assignment_2.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 3:
            content = render_to_string('low_level/assignments/lesson_3/assignment_3.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 4:
            content = render_to_string('low_level/assignments/lesson_4/assignment_4.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 5:
            content = render_to_string('low_level/assignments/lesson_5/assignment_5.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 6:
            content = render_to_string('low_level/assignments/lesson_6/assignment_6.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 7:
            content = render_to_string('low_level/assignments/lesson_7/assignment_7.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 8:
            content = render_to_string('low_level/assignments/lesson_8/assignment_8.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 9:
            content = render_to_string('low_level/assignments/lesson_9/assignment_9.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 10:
            content = render_to_string('low_level/assignments/lesson_10/assignment_10.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 11:
            content = render_to_string('low_level/assignments/lesson_11/assignment_11.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 12:
            content = render_to_string('low_level/assignments/lesson_12/assignment_12.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 13:
            content = render_to_string('low_level/assignments/lesson_13/assignment_13.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 14:
            content = render_to_string('low_level/assignments/lesson_14/assignment_14.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == None:
            content = render_to_string('low_level/welcome.html')
        else:
            content = render_to_string('low_level/welcome.html')

    elif loging_user.test_marks < 75 :
        if number == 1:
            content = render_to_string('medium_level/assignments/lesson_1/assignment_1.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 2:
            content = render_to_string('medium_level/assignments/lesson_2/assignment_2.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 3:
            content = render_to_string('medium_level/assignments/lesson_3/assignment_3.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 4:
            content = render_to_string('medium_level/assignments/lesson_4/assignment_4.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 5:
            content = render_to_string('medium_level/assignments/lesson_5/assignment_5.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 6:
            content = render_to_string('medium_level/assignments/lesson_6/assignment_6.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 7:
            content = render_to_string('medium_level/assignments/lesson_7/assignment_7.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 8:
            content = render_to_string('medium_level/assignments/lesson_8/assignment_8.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 9:
            content = render_to_string('medium_level/assignments/lesson_9/assignment_9.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 10:
            content = render_to_string('medium_level/assignments/lesson_10/assignment_10.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 11:
            content = render_to_string('medium_level/assignments/lesson_11/assignment_11.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 12:
            content = render_to_string('medium_level/assignments/lesson_12/assignment_12.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 13:
            content = render_to_string('medium_level/assignments/lesson_13/assignment_13.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 14:
            content = render_to_string('medium_level/assignments/lesson_14/assignment_14.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == None:
            content = render_to_string('medium_level/welcome.html')
        else:
            content = render_to_string('medium_level/welcome.html')

    else :
        if number == 1:
            content = render_to_string('high_level/assignments/lesson_1/assignment_1.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 2:
            content = render_to_string('high_level/assignments/lesson_2/assignment_2.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 3:
            content = render_to_string('high_level/assignments/lesson_3/assignment_3.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 4:
            content = render_to_string('high_level/assignments/lesson_4/assignment_4.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 5:
            content = render_to_string('high_level/assignments/lesson_5/assignment_5.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 6:
            content = render_to_string('high_level/assignments/lesson_6/assignment_6.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 7:
            content = render_to_string('high_level/assignments/lesson_7/assignment_7.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 8:
            content = render_to_string('high_level/assignments/lesson_8/assignment_8.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 9:
            content = render_to_string('high_level/assignments/lesson_9/assignment_9.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 10:
            content = render_to_string('high_level/assignments/lesson_10/assignment_10.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 11:
            content = render_to_string('high_level/assignments/lesson_11/assignment_11.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 12:
            content = render_to_string('high_level/assignments/lesson_12/assignment_12.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 13:
            content = render_to_string('high_level/assignments/lesson_13/assignment_13.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == 14:
            content = render_to_string('high_level/assignments/lesson_14/assignment_14.html', {'level':loging_user.assignment_progress_level, 'assignments':assignments, 'chapter':loging_user.chapter_level})
        elif number == None:
            content = render_to_string('high_level/welcome.html')
        else:
            content = render_to_string('high_level/welcome.html')
    
    return HttpResponse(content)

@csrf_exempt
def upload_file(request):
    content = ''
    global loging_user    
    # user = request.session.get('custom_data')
    lesson_number = loging_user.chapter_level
    file_name = loging_user.assignment_progress_level
    if loging_user.test_marks < 40:
        file_path = os.path.abspath(f'pythonteacherapp/templates/low_level/assignments/lesson_{lesson_number}/{file_name}.py')
    elif loging_user.test_marks < 75:
        file_path = os.path.abspath(f'pythonteacherapp/templates/medium_level/assignments/lesson_{lesson_number}/{file_name}.py')
    else:
        file_path = os.path.abspath(f'pythonteacherapp/templates/high_level/assignments/lesson_{lesson_number}/{file_name}.py')
    # print("File Path ------------>>>>")
    # print(file_path)
    # print(not os.path.exists(file_path))
    code = 0
    if not os.path.exists(file_path):
        return HttpResponse(f"File {file_path} does not exist")
    if request.method == "POST":
        # print("use POST ----------->")
        uploaded_file = request.FILES.get('file')
        # print("content ----------->")
        file_copy = uploaded_file.file # make a copy of the file object
        # print("file copy ----------->")
        #return HttpResponse(file_copy)
        result = run_the_file(file_copy, file_path)
        print("result ----------->")
        print(result)
        #return HttpResponse(result)
        # uploaded_file = request.FILES.get('file')
        # result_similarity_ratio = run_the_file(uploaded_file, file_path)
        # uploaded_file_2 = request.FILES.get('file')
        remaining_time = request.POST.get('remaining_time')
        time = round((float(remaining_time)/60))
        # print(result_similarity_ratio); 
        if uploaded_file:
            with open(file_path, 'rb') as f: 
                stored_file = f.read().decode('utf-8')
            uploaded_content = uploaded_file.file.getvalue().decode('utf-8')
            #return HttpResponse(uploaded_content.getvalue().decode('utf-8'))
            if len(uploaded_content) == 0:
                print("The uploaded file is empty.")
            else:
                print("File content : ")
                print(uploaded_content)
                print(stored_file)
                similarity_ratio = SequenceMatcher(None, stored_file, uploaded_content).ratio()
                result = round(result, 2)
                code = round((similarity_ratio*100), 2)
                print("result +++++++++++++++>")
                print(code)
                if result == 2:
                    response_data  = {'task': 'error', 'message': "Syntax Error - Check again the code !", 'content': ''} 
                    task = "Syntax Error - Check again the code !"
                    # return HttpResponse(content) 
                elif result != 1:
                    response_data  = {'task': 'error', 'message': "Check again the code and make sure that all the keywords are included!", 'content': ''} 
                    task = "Check again the code and make sure that all the keywords are included!"
                    # return HttpResponse(content)
                else:
                    # global loging_user
                    user = User.objects.get(id=loging_user.id)
                    # print(loging_user)
                    task = get_fuzzy_output(code, time)
                    print('Fuzzy output ----------------------- >>>>>> ')
                    print(task)
                    # content = task
                    #return HttpResponse(content)
                    if task =='again':
                        return ''
                    elif task== 'next_level':
                        if user.assignment_progress_level == 3:
                            user.assignment_progress_level = 3
                        else:
                            user.assignment_progress_level += 1
                    elif task =='next_chapter':
                        user.assignment_progress_level = 1
                        user.chapter_level += 1   
                        user.assignment_level += 1 
                    user.save()          
                    response_data = {'task': task, 'message': ''}
                       
                assignment = Assignment(
                    message=task,
                    assignment_progress_level=loging_user.assignment_progress_level,
                    assignment_level=loging_user.assignment_level,
                    answer = uploaded_content,
                    time = time,
                    marks= code,
                    created_by = loging_user,
                )
                assignment.save()   
                if loging_user.test_marks < 40:     
                    response_data['content'] = render_to_string('low_level/welcome.html')
                elif loging_user.test_marks < 75:
                    response_data['content'] = render_to_string('medium_level/welcome.html')
                else:
                    response_data['content'] = render_to_string('high_level/welcome.html')
            # content = f"File uploaded successfully. Similarity ratio: {result}"
        else:
            if loging_user.test_marks < 40:     
                response_data['content'] = render_to_string('low_level/welcome.html')
            elif loging_user.test_marks < 75:
                response_data['content'] = render_to_string('medium_level/welcome.html')
            else:
                response_data['content'] = render_to_string('high_level/welcome.html')
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        # return HttpResponse(content)
    else:
        # print("POST else ------------>>>>")
        content = ''
    # return HttpResponse(content)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def run_the_file(uploaded_file, file_path):
    try:
        # Run a Python file and wait for it to complete
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        result_of_uploaded_file = subprocess.run(['python', temp_file_path], capture_output=True, text=True, input='John\nDoe\n', check=True)
        result_of_stored_file = subprocess.run(['python', file_path], capture_output=True, text=True, input='John\nDoe\n', check=True)
        similarity_ratio_of_output = SequenceMatcher(None, result_of_uploaded_file.stdout, result_of_stored_file.stdout ).ratio()
        return similarity_ratio_of_output
    except subprocess.CalledProcessError as error:
        # Handle any errors that occurred while running the file
        return 2

def run_python_code(code):
    try:
        output = subprocess.check_output(['python', '-c', code])
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

def run_python_file(file_path):
    try:
        output = subprocess.check_output(['python', file_path])
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')
    
def handle_uploaded_file(uploaded_file):
    media_root = settings.MEDIA_ROOT
    filename = uploaded_file.name
    file_path = os.path.join(media_root, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

def get_fuzzy_output(calculated_marks, calculated_time):
    # Define the input a output variables
    # calculated_marks = 60
    # calculated_time = 35
    marks = np.arange(0, 101, 1)
    time = np.arange(0, 101, 1)
    task = np.arange(0, 101, 1)

    # Define the fuzzy membership functions for marks and time
    low_marks = fuzz.trapmf(marks, [0, 0, 40, 50])
    average_marks = fuzz.trapmf(marks, [50, 55, 75, 80])
    high_marks = fuzz.trapmf(marks, [80, 85, 100, 100])

    poor_time = fuzz.trapmf(time, [0, 0, 20, 25])
    average_time = fuzz.trapmf(time, [25, 30, 35, 40])
    excellent_time = fuzz.trapmf(time, [40, 45, 50, 50])

    # Define the fuzzy membership functions for the output variable task
    again_task = fuzz.trimf(task, [0, 0, 50])
    next_level_task = fuzz.trimf(task, [50, 60, 70])
    next_chapter_task = fuzz.trimf(task, [70, 100, 100])

    # Compute the degree of membership of the input variables in their fuzzy sets
    marks_low = fuzz.interp_membership(marks, low_marks, calculated_marks)
    marks_average = fuzz.interp_membership(marks, average_marks, calculated_marks)
    marks_high = fuzz.interp_membership(marks, high_marks, calculated_marks)

    time_poor = fuzz.interp_membership(time, poor_time, calculated_time)
    time_average = fuzz.interp_membership(time, average_time, calculated_time)
    time_excellent = fuzz.interp_membership(time, excellent_time, calculated_time)

    # Apply the fuzzy rules to compute the degree of membership of the output variable in the fuzzy sets
    # based on the combination of the input variable fuzzy sets
    rule1 = np.fmin(marks_low, time_poor)
    again_membership = np.fmin(rule1, again_task)

    rule2 = np.fmin(marks_average, time_average)
    next_level_membership = np.fmin(rule2, next_level_task)

    rule3 = np.fmin(marks_high, time_excellent)
    next_chapter_membership = np.fmin(rule3, next_chapter_task)

    # Combine the membership values of the output variable fuzzy sets to form a single fuzzy set
    aggregated = np.fmax(again_membership, np.fmax(next_level_membership, next_chapter_membership))

    # Compute the crisp output value by defuzzifying the fuzzy set
    task_crisp = fuzz.defuzz(task, aggregated, 'centroid')

    # Print the crisp output value
    print(task_crisp)

    # Determine the label with the highest degree of membership in the output variable fuzzy sets
    again_mem = fuzz.interp_membership(task, again_task, task_crisp)
    next_level_mem = fuzz.interp_membership(task, next_level_task, task_crisp)
    next_chapter_mem = fuzz.interp_membership(task, next_chapter_task, task_crisp)

    result = ""
    if again_mem > next_level_mem and again_mem > next_chapter_mem:
        print('Task: Again')
        result = "again"
    elif next_level_mem > again_mem and next_level_mem > next_chapter_mem:
        print('Task: Next Level')
        result = "next_level"
    else:
        print('Task: Next Chapter')
        result = "next_chapter"

    return result

def get_assignments_by_user(user_id):
    assignments = Assignment.objects.filter(created_by_id=user_id).order_by('-created_at')
    # Iterate over the assignments and access their properties
    # for assignment in assignments:
        # print(f"Assignment ID: {assignment.id}")
        # print(f"Message: {assignment.message}")
        # print(f"Content: {assignment.answer}")
        # print("------------------------------")
    return assignments

def logout(request):
    request.session['name'] = ''
    request.session['email'] = ''
    request.session['user_id'] = ''
    global loging_user
    loging_user = ''
    return redirect('/')

# def get_fuzzy_output(calculated_marks, calculated_time):
#     # Define fuzzy sets for inputs and output
#     # marks = ctrl.Antecedent(np.arange(0, 101, 1), 'marks')
#     # time = ctrl.Antecedent(np.arange(0, 51, 1), 'time')
#     # task = ctrl.Consequent(np.arange(0, 101, 1), 'task')

#     marks = ctrl.Antecedent(np.arange(0, 101, 1), 'marks')
#     time = ctrl.Antecedent(np.arange(0, 51, 1), 'time')
#     task = ctrl.Consequent(np.arange(0, 101, 1), 'task') 

#     # # Define membership functions for marks
#     # marks['low'] = fuzz.trapmf(marks.universe, [0, 0, 40, 40])
#     # marks['average'] = fuzz.trapmf(marks.universe, [35, 35, 75, 75])
#     # marks['high'] = fuzz.trapmf(marks.universe, [70, 70, 100, 100])

#     # # Define membership functions for time
#     # time['poor'] = fuzz.trapmf(time.universe, [0, 0, 20, 20])
#     # time['average'] = fuzz.trapmf(time.universe, [15, 15, 35, 35])
#     # time['excellent'] = fuzz.trapmf(time.universe, [30, 30, 50, 50])

#     # # Define membership functions for output
#     # task['again'] = fuzz.trimf(task.universe, [0, 0, 50])
#     # task['next level'] = fuzz.trimf(task.universe, [50, 75, 100])
#     # task['next chapter'] = fuzz.trimf(task.universe, [75, 100, 100])

#     marks['low'] = fuzz.trapmf(marks.universe, [0, 0, 40, 50])
#     marks['average'] = fuzz.trapmf(marks.universe, [35, 45, 75, 85])
#     marks['high'] = fuzz.trapmf(marks.universe, [70, 80, 100, 100])

#     time['average'] = fuzz.trapmf(time.universe, [15, 20, 35, 40])
#     time['excellent'] = fuzz.trapmf(time.universe, [30, 35, 50, 50])
#     time['poor'] = fuzz.trapmf(time.universe, [0, 0, 20, 25])

#     # task.universe = range(101) 
#     task['again'] = fuzz.trimf(task.universe, [0, 0, 50])
#     task['next_level'] = fuzz.trimf(task.universe, [30, 50, 70])
#     task['next_chapter'] = fuzz.trimf(task.universe, [50, 100, 100])

#     # Visualize membership functions (optional)
#     # marks.view()
#     # time.view()
#     # task.view()

#     # # Define fuzzy rules
#     # rule1 = ctrl.Rule(marks['low'] & time['poor'], task['again'])
#     # rule2 = ctrl.Rule(marks['average'] & time['average'], task['next_level'])
#     # rule3 = ctrl.Rule(marks['high'] & time['excellent'], task['next_chapter'])
    
#     # # Create a control system
#     # task_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

#     # # Create a simulation
#     # task_sim = ctrl.ControlSystemSimulation(task_ctrl)

#     # Create fuzzy rules
#     rule1 = ctrl.Rule(marks['low'] & time['poor'], task['again'])
#     rule2 = ctrl.Rule(marks['average'] & time['average'], task['next_level'])
#     rule3 = ctrl.Rule(marks['high'] & time['excellent'], task['next_chapter'])

#     # Create fuzzy system
#     task_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
#     task_sim = ctrl.ControlSystemSimulation(task_ctrl)

#     # print(calculated_marks)
#     # print(calculated_time)

#     # # Set input values
#     # task_sim.input['marks'] = 60
#     # task_sim.input['time'] =  40

#     # # Compute output
#     # task_sim.compute()

#     # # Print output value
#     # print("Task:", task_sim.output['task'])

#     # # Visualize output (optional)
#     # # task.view(sim=task_sim)

#     # Set input values
#     task_sim.input['marks'] = 35
#     task_sim.input['time'] = 15

#     # Compute output
#     task_sim.compute()

#     # Get fuzzy output set
#     task_output = task_sim.output['task']
#     # task_output =  round(task_output)
#     print(type(task_output));
#     # Defuzzify to obtain crisp output value
#     task_crisp = fuzz.defuzz(task.universe, task_output, 'centroid')
#     print(task_crisp);
#     # Map crisp output to linguistic label
#     task_again_mem = fuzz.interp_membership(task.universe, task_again, task_crisp)
#     task_next_level_mem = fuzz.interp_membership(task.universe, task_next_level, task_crisp)
#     task_next_chapter_mem = fuzz.interp_membership(task.universe, task_next_chapter, task_crisp)

#     # Print the degree of membership for each label
#     print('Again:', task_again_mem)
#     print('Next Level:', task_next_level_mem)
#     print('Next Chapter:', task_next_chapter_mem)

#     # Determine the label with the highest degree of membership
#     if task_again_mem > task_next_level_mem and task_again_mem > task_next_chapter_mem:
#         print('Task: Again')
#     elif task_next_level_mem > task_again_mem and task_next_level_mem > task_next_chapter_mem:
#         print('Task: Next Level')
#     else:
#         print('Task: Next Chapter')

#     #return the output
#     return task_crisp



    # if request.method == 'POST' and request.FILES.get('file'):
    #     file = request.FILES['file']
    #     file_data = file.read()
    #     print(file_data);
    #     response_data = 'success'
    # else:
    #     response_data = 'No file provided'
    # return HttpResponse(response_data)
# import firebase_admin
# import pyrebase
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from firebase_admin import auth

# config = {
#     "apiKey": "AIzaSyDdhydmfc3dKQLHzm9AnY6a7cHjGbr_7pc",
#     "authDomain": "python-teacher-2595a.firebaseapp.com",
#     "projectId": "python-teacher-2595a",
#     "storageBucket": "python-teacher-2595a.appspot.com",
#     "databaseURL": "https://python-teacher-2595a-default-rtdb.firebaseio.com",
#     "messagingSenderId": "585232727948",
#     "appId": "1:585232727948:web:dbde242be498ba124de0a9",
#     "measurementId": "G-B4YNJ7QRQT"
# };
# firebase = pyrebase.initialize_app(config)
# firebase_admin.initialize_app()
# pyrebase_auth = firebase.auth()
# database = firebase.database()

# count = 1
# pre_test_marks = 0
# loging_user = {}
# id_token=""

# @csrf_exempt
# def postsignIn(request):
#     global count
#     global pre_test_marks
#     global loging_user
#     global id_token
#     email = request.POST.get('email')
#     pasw = request.POST.get('password')
#     try:
#         # if there is no error then signin the user with given email and password
#         user = pyrebase_auth.sign_in_with_email_and_password(email, pasw)
#         userId = user['localId']
#         result = database.child("student").get()
#         # print('result')
#         data = result.val()

#         # Filter the data based on the name
#         for key, student in data.items():
#             if student['id'] == userId:
#                 # print(item)
#                 break
#         count = 0
#         pre_test_marks = 0
#         loging_user = student
#         id_token = user['localId']
#     except:
#         message = "Invalid Credentials!!Please Check your Data"
#         return render(request, "login.html", {"message": message})
#     # session_id = user['idToken']
#     # request.session['uid'] = str(session_id)
#     # print(user)
#     if student['pre_test_marks'] == 0:
#         questions = database.child("pre-test").get().val()
#         # print(questions)
#         context = {
#             'student': student,
#             'questions': questions,
#             'count': count,
#         }
#         return render(request, "home.html", context=context)
#     elif student['pre_test_marks'] <= 40:
#         return render(request, "dashboard_01.html", context=student)
#     elif student['pre_test_marks'] <= 70:
#         return render(request, "dashboard_02.html", context=student)
#     else:
#         return render(request, "dashboard_03.html", context=student)


# @csrf_exempt
# def postsignUp(request):
#     global count
#     global pre_test_marks
#     global loging_user
#     email = request.POST.get('email')
#     passs = request.POST.get('password')
#     name = request.POST.get('name')
#     try:
#         # creating a user with the given email and password
#         user = pyrebase_auth.create_user_with_email_and_password(email, passs)
#         uid = user['localId']
#         user['name'] = name
#         user['pre_test_marks'] = 0
#         # print(user)
#         storeStudentData(user)
#         count = 0
#         pre_test_marks = 0
#         loging_user = user
#         id_token = user['localId']
#         # idtoken = request.session['uid']
#         # print(uid)
#     except:
#         return render(request, "register.html")
#     return render(request, "login.html")


# def login(request):
#     return render(request, 'login.html')


# def register(request):
#     return render(request, 'register.html')


# def storeStudentData(request):
#     data = {
#         'name': request['name'],
#         'email': request['email'],
#         'id': request['localId'],
#         'pre_test_marks': request['pre_test_marks']
#     }
#     details = database.child('student').push(data)
#     print(details)


# @csrf_exempt
# def pretest(request):
#     global  loging_user
#     global id_token
#     # user_info = pyrebase_auth.get_account_info(loging_user['idToken'])
#     # print(loging_user)
#     answer = request.POST.get('answer')
#     questions = database.child("pre-test").get().val()
#     # count = global count +1;
#     global count
#     global pre_test_marks
#     # print(answer, ' ', questions[count-1]["correct_answer"]);
#     try:
#         if answer == questions[count - 1]["correct_answer"]:
#             # print(pre_test_marks)
#             pre_test_marks += 1
#         if count == 3:
#             # database.child("student").order_by_child("email").equal_to(loging_user['email']).update({'pre_test_marks': pre_test_marks})
#             # ref = database.child("student").get().val()
#             # students = [student for student in ref.values() if student['email'] == loging_user['email']]
#             # print(id_token)
#             print(id_token)
#             user = auth.update_user(id_token, **{'pre_test_marks': pre_test_marks})
#             print(user)
#             # auth.update_user(user_uid, {"pre_test_marks": pre_test_marks})
#             # database.child("student").child(id_token).update({"pre_test_marks": pre_test_marks})

#             # # store marks -- > redirect to the specific dashboard
#             # print(loging_user['id'])
#             # user_ref = database.child("student").child(loging_user['email']).update({'pre_test_marks': pre_test_marks})
#         else:
#             count += 1
#             context = {
#                 'questions': questions,
#                 'count': count
#             }
#             return render(request, "home.html", context=context)
#     except Exception as e:
#         # return render(request, "register.html")
#         print(e)
#     return render(request, "login.html")
