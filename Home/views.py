from ast import Not
from asyncio import subprocess
from distutils import extension
import email
from time import time
from unicodedata import name
from django.shortcuts import render, HttpResponse
from Home.models import Problem, Submission, TestCases, User
from django.contrib import messages
from datetime import datetime
import os
import subprocess
from difflib import Differ

def start(request):
    return render(request,'startpage.html')

def home(request,user_name):
    user = User.objects.get(username=str(user_name))
    types = Problem.objects.values('type').distinct()
    return render(request,'homepage.html',{'user':user,'types':types})

def signin(request):
    if request.method == "GET":
        email = request.GET.get('email')
        password = request.GET.get('password')

        user_list = User.objects.filter(email=str(email),password=str(password))
        if len(user_list) > 0:
            user = user_list[0]
            return render(request,'homepage.html',{'user':user})
        if password is not None:
            messages.error(request,'Incorrect Email or Password') 
    
    return render(request,'startpage.html')

def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2 and password1 is not None:
            messages.success(request,'Passwords don\'t match.')
        else:
            user = User(name=name,email=email,password=password1)
            user.save()
            messages.success(request,'Your Account has been created.')

    return render(request,'signup.html')

def problems(request,user_name):
    user = User.objects.get(username=str(user_name))
    problems = Problem.objects.all()
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    types = Problem.objects.values('type').distinct()
    return render(request,'problems.html',{'user':user,'problems':problems,'types':types,'rank':rank})

def problem_search(request,user_name):
    if request.method == "POST":
        search_string = request.POST.get('search')
        problems = Problem.objects.filter(name__icontains=search_string)
    else:
        problems = Problem.objects.all()
    user = User.objects.get(username=str(user_name))
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    types = Problem.objects.values('type').distinct()
    return render(request,'problems.html',{'user':user,'problems':problems,'types':types,'rank':rank})

def problems_typeSpecific(request,user_name,type):
    user = User.objects.get(username=str(user_name))
    problems = Problem.objects.filter(type=str(type))
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    types = Problem.objects.values('type').distinct()
    return render(request,'problems.html',{'user':user,'problems':problems,'types':types,'rank':rank})

def problems_difficuiltySpecific(request,user_name,difficuilty):
    user = User.objects.get(username=str(user_name))
    problems = Problem.objects.filter(difficuilty=str(difficuilty))
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    types = Problem.objects.values('type').distinct()
    return render(request,'problems.html',{'user':user,'problems':problems,'types':types,'rank':rank})

def problem_description(request,user_name,id):
    user = User.objects.get(username=str(user_name))
    problem = Problem.objects.get(id=id)
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    return render(request,'problem_desc.html',{'user':user,'problem':problem,'rank':rank})

def submit(request,user_name,id):
    user = User.objects.get(username=str(user_name))
    problem = Problem.objects.get(id=id)
    curr_testcase = TestCases.objects.get(problem=problem)
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    if request.method == 'POST':
        code = request.POST.get('textarea')
        language = request.POST.get('language')
        ext = {1:"cpp",2:"java",3:"py"}
        filename = "problem_"+str(id)+"_"+user_name
        filepath = "static/code/"+filename+"."+ext[int(language)]
        out_file = curr_testcase.output.split('/')[-1]
        in_file = curr_testcase.input.split('/')[-1]
        verdict = ""

        with open(filepath,'w') as f:
            f.write(code)
        
        command = {  1 : "g++ "+filename+".cpp -o "+filename+".exe",
                     2 : "",
                     3 : "python "+filepath }
        cmd = ["python",filepath]
        input_testcases = open(curr_testcase.input,'r')
        testcases = input_testcases.readlines()
        with open("static/execution/"+out_file,'w') as f:
            pass
        my_output = open("static/execution/"+out_file,'a')
        
        count = 1
        for testcase in testcases:
            input = testcase.split(' ')
            print(input)
            print()
            my_input = open("static/execution/"+in_file,'w')
            for i in input:
                my_input.write(i+"\n")
            try:
                p = subprocess.run(cmd,timeout=5.5,stdin=my_input,stdout=my_output)
                if p.returncode == 0:
                    print("Testcase "+ count + " passed.")
                    count += 1
                else:
                    print("Error")
            except subprocess.TimeoutExpired:
                print("TLE")
                messages.error(request,'Time limit exceeded.')
                verdict = "Time Limit Exceeded"
            my_input.close()

        out_testcase = curr_testcase.output
        compiled_testcase = "static/execution/"+out_file
        ans = 0
        ans = match_testcases(out_testcase,compiled_testcase,ans)
        if ans==1:
            messages.success(request,'Your code has passed all the testcases.')
            verdict = "Correct Answer"
        else:
            messages.error(request,"Wrong answer.")
            verdict = "Wrong Answer"

        submission = Submission(user=user,problem=problem,code=code,verdict=verdict,time=datetime.now())
        submission.save()
        
    return render(request,'problem_desc.html',{'user':user,'problem':problem,'rank':rank})

def match_testcases(output_path,compile_path,ans):

    with open(output_path) as file_1, open(compile_path) as file_2:
        differ = Differ()
  
        for line in differ.compare(file_1.readlines(), file_2.readlines()):
            if line.startswith('-') or line.startswith('+') or line.startswith('?'):
                ans = 0
                return ans
        
    ans = 1
    return ans

def submissions(request,user_name):
    user = User.objects.get(username=str(user_name))
    submissions = Submission.objects.filter(user=user)
    rank = User.objects.all().filter(problems_solved__gt=user.problems_solved).count() + 1
    return render(request,'submissions.html',{'user':user,'submissions':submissions,'rank':rank})

def leaderboard(request):
    user = User.objects.order_by('-problems_solved')
    return render(request,'leaderboard.html',{'user':user})