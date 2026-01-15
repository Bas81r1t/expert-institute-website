from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from django.db.models import Q # Complex search ke liye

# ==========================================
# HELPER FUNCTION (DRY Principle)
# ==========================================
def get_student_session(request):
    """Check karta hai ki session me student ID hai ya nahi"""
    if 'student_id' in request.session:
        try:
            return Student.objects.get(id=request.session['student_id'])
        except Student.DoesNotExist:
            return None
    return None

# ==========================================
# 1. HOME PAGE
# ==========================================
def home(request):
    student_data = get_student_session(request)
    return render(request, 'home.html', {'student_data': student_data})

# ==========================================
# 2. STUDENT LOGIN (DUPLICATE FIX LOGIC)
# ==========================================
def student_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        # CHECK: Kya is Email ya Mobile se koi student pehle se hai?
        existing_student = Student.objects.filter(Q(email=email) | Q(mobile=mobile)).first()

        if existing_student:
            # PURANA USER MIL GAYA -> UPDATE KARO
            student = existing_student
            student.is_online = True  # Status Green karo
            
            # Details update karo (agar user ne change ki hain)
            student.name = name
            student.address = address
            student.save() # Save karte hi 'last_active' update hoga
            
            messages.success(request, f'Welcome back, {student.name}! You are logged in again.')
        
        else:
            # NAYA USER HAI -> CREATE KARO
            student = Student(name=name, mobile=mobile, email=email, address=address)
            student.is_online = True
            student.save()
            messages.success(request, f'Welcome, {name}! Registration Successful.')

        # Session me ID save karo
        request.session['student_id'] = student.id
        return redirect('home')

    return render(request, 'student_login.html')

# ==========================================
# 3. STUDENT PROFILE
# ==========================================
def student_profile(request):
    if 'student_id' in request.session:
        student = get_object_or_404(Student, id=request.session['student_id'])
        return render(request, 'student_profile.html', {'student': student})
    else:
        return redirect('student_login')

# ==========================================
# 4. STUDENT LOGOUT
# ==========================================
def student_logout(request):
    if 'student_id' in request.session:
        try:
            student = Student.objects.get(id=request.session['student_id'])
            student.is_online = False # Status Red (Offline)
            student.save()
        except Student.DoesNotExist:
            pass

        del request.session['student_id']
        messages.info(request, "You have been logged out.")
        
    return redirect('home')

# ==========================================
# 5. ADMIN DASHBOARD (Secure & Sorted)
# ==========================================
@login_required(login_url='login') 
def dashboard(request):
    # Admin panel par bhi Navbar ke liye student data chahiye
    student_data = get_student_session(request)
    
    # Sort by 'last_active' (Jo abhi login hua wo sabse upar)
    all_students = Student.objects.all().order_by('-last_active') 
    
    return render(request, 'dashboard.html', {
        'students': all_students, 
        'student_data': student_data
    })

# ==========================================
# 6. ADMIN AUTHENTICATION
# ==========================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Admin Username or Password')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# ==========================================
# 7. NEW PAGES (Courses, Donate, etc.)
# ==========================================
# In sabhi me 'student_data' pass kiya hai taaki Navbar sahi dikhe

def courses(request):
    student_data = get_student_session(request)
    return render(request, 'courses.html', {'student_data': student_data})

def donate(request):
    student_data = get_student_session(request)
    return render(request, 'donate.html', {'student_data': student_data})

def admission(request):
    # अगर स्टूडेंट लॉग इन है तो उसका डेटा नेविगेशन बार के लिए चाहिए होगा
    student_data = None
    if 'student_id' in request.session:
        try:
            student_data = Student.objects.get(id=request.session['student_id'])
        except Student.DoesNotExist:
            pass
            
    return render(request, 'admission.html', {'student_data': student_data})