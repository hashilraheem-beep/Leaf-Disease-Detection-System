from django.shortcuts import render,redirect
from LeafBack.models import DiseaseDb,ProductDb
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from LeafFront.models import CreateAccountDb,orderdb

def adminLogin(req):
    return render(req, "adminLogin.html")

def Login(req):
    if req.method == "POST":
        un = req.POST.get('user_name')
        pwd = req.POST.get('pass_word')
        if User.objects.filter(username__contains=un).exists():
            user = authenticate(username=un, password=pwd)
            if user is not None:
                login(req, user)
                req.session['username'] = un
                req.session['password'] = pwd
                return redirect(adminhome)
            else:
                return redirect(adminLogin)
        else:
            return redirect(adminLogin)

def adminhome(request):
    total_users = CreateAccountDb.objects.count()
    new_users = CreateAccountDb.objects.order_by('-id').first()
    pendingorders = orderdb.objects.count()
    last_order = orderdb.objects.order_by('-id').first()
    all_orders = orderdb.objects.order_by('-id')[:5]

    context = {
        'total_users': total_users,
        'pendingorders':pendingorders,
        'last_order':last_order,
        'new_users':new_users,
        'all_orders':all_orders,
    }

    return render(request, 'adminhome.html', context)


def addDisease(request):
    return render(request, 'addDisease.html')

def DiseaseSave(request):
    if request.method == "POST":
        dn = request.POST.get('diseasename')
        p = request.POST.get('plant')
        d = request.POST.get('description')
        s = request.POST.get('symptoms')
        t = request.POST.get('treatment')
        img = request.FILES['image']
        obj = DiseaseDb(diseasename=dn,plant=p,description=d,symptoms=s,treatment=t,image=img)
        obj.save()
        messages.success(request, "Disease saved successfully!")
        return redirect('addDisease')
    
def viewdisease(request):
    info=DiseaseDb.objects.all()
    return render(request, 'viewdisease.html',{'info':info})
       
def AdminLogout(request):
    del request.session['username']
    del request.session['password']
    return redirect('index')

def editdisease(request):
    data=DiseaseDb.objects.all()
    return render(request, 'editdisease.html',{'data':data})

def updatedisease(req, dataid):
    info = DiseaseDb.objects.get(id=dataid)
    return render(req, "updatedisease.html", {'info': info})

def UpdateDiseaseButton(req, dataid):
    if req.method == "POST":
        dn = req.POST.get('diseasename')
        p = req.POST.get('plant')
        d = req.POST.get('description')
        s = req.POST.get('symptoms')
        t = req.POST.get('treatment')
        try:
            img = req.FILES['image']
            fs=FileSystemStorage()
            file=fs.save(img.name,img)
        except MultiValueDictKeyError:
            file=DiseaseDb.objects.get(id=dataid).image
        DiseaseDb.objects.filter(id=dataid).update(diseasename=dn,plant=p,description=d,symptoms=s,treatment=t,image=file)
        return redirect(editdisease)
    
def deletedisease(request, dataid):
    dell = DiseaseDb.objects.filter(id=dataid)
    dell.delete()
    return redirect('editdisease')

def addproduct(req):
    return render(req,"addproduct.html")

def productsave(request):
    if request.method == "POST":
        pn = request.POST.get('productname')
        d = request.POST.get('description')
        mrp = request.POST.get('mrp')
        p = request.POST.get('price')
        img = request.FILES['image']
        obj = ProductDb(productname=pn,description=d,mrp=mrp,price=p,image=img)
        obj.save()
        messages.success(request, "Product saved successfully!")
        return redirect('addproduct')
    
def viewproduct(request):
    products=ProductDb.objects.all()
    return render(request, 'viewproduct.html',{'products':products})

def editproduct(request):
    products=ProductDb.objects.all()
    return render(request, 'editproduct.html',{'products':products})

def updateproduct(req, dataid):
    products = ProductDb.objects.get(id=dataid)
    return render(req, "updateproduct.html", {'products': products})

def UpdateProductButton(req, dataid):
    if req.method == "POST":
        pn = req.POST.get('productname')
        d = req.POST.get('description')
        mrp = req.POST.get('mrp')
        p = req.POST.get('price')
        try:
            img = req.FILES['image']
            fs=FileSystemStorage()
            file=fs.save(img.name,img)
        except MultiValueDictKeyError:
            file=ProductDb.objects.get(id=dataid).image
        ProductDb.objects.filter(id=dataid).update(productname=pn,description=d,mrp=mrp,price=p,image=file)
        return redirect(editproduct)
    
def deleteproduct(request, dataid):
    dell = ProductDb.objects.filter(id=dataid)
    dell.delete()
    return redirect('editproduct')

def users(request):
    user=CreateAccountDb.objects.all()
    return render(request, 'users.html',{'user':user})

def deleteuser(request, dataid):
    dell = CreateAccountDb.objects.filter(id=dataid)
    dell.delete()
    return redirect('users')

def adduser(req):
    if req.method == "POST":
        un = req.POST.get('username')
        a = req.POST.get('age')
        e = req.POST.get('email')
        pwd = req.POST.get('password')
        obj = CreateAccountDb(username=un,age=a, email=e, password=pwd)
        obj.save()
        return redirect(users)
    
def order(request):
    orders=orderdb.objects.all()
    return render(request,'order.html',{'orders':orders})
    
from django.shortcuts import render, get_object_or_404

def user_orders_detail(request, username):
    # Get all orders for this specific user
    orders = orderdb.objects.filter(username=username)
    
    if not orders.exists():
        return render(request, 'user_orders_detail.html', {
            'username': username,
            'error': 'No orders found for this user.'
        })

    # Calculate grand total
    grand_total = sum(order.totalprice for order in orders)

    # Get email & address (assuming they are the same for all orders of a user)
    email = orders.first().email if orders else 'N/A'
    address = orders.first().address if orders else 'N/A'

    context = {
        'username': username,
        'orders': orders,
        'grand_total': grand_total,
        'email': email,
        'address': address,
    }
    
    return render(request, 'user_orders_detail.html', context)

def deleteorder(request, dataid):
    dell = orderdb.objects.filter(id=dataid)
    dell.delete()
    return redirect('order')

# views.py
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Only for testing - better to use proper CSRF in production
def send_order_confirmation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')

            if not username or not email:
                return JsonResponse({'success': False, 'message': 'Missing username or email'})

            subject = f'Your Leafix Order is Confirmed - {username}'
            message = f"""
Dear {username},

Your order(s) have been confirmed and processed.

The delivery partner will notify you once product reached near by you.

Thank you for shopping with Leafix!

Best regards,
Leafix Team
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def delete_all_user_orders(request, username):
    if request.method == 'POST':
        try:
            deleted_count, _ = orderdb.objects.filter(username=username).delete()
            return JsonResponse({'success': True, 'deleted': deleted_count})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})