from django.shortcuts import render, redirect

def my_groups(request):
    # View to list student's groups
    student_id = request.session.get('student_id')
    if student_id:
        return render(request, 'index.html')
    return redirect('login')
