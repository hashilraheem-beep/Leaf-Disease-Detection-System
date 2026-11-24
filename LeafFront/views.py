from django.shortcuts import render, redirect
from .ai_model import predict_leaf_disease
from django.core.files.storage import FileSystemStorage
from .models import LeafImage  
from LeafBack.models import ProductDb,DiseaseDb
from LeafFront.models import CreateAccountDb,cartdb,orderdb
from django.contrib import messages
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


def predictresult(request):
    result = None

    if request.method == "POST" and request.FILES.get("leaf_image"):
        leaf_image_file = request.FILES["leaf_image"]

        # Save file to media folder
        fs = FileSystemStorage()
        filename = fs.save(leaf_image_file.name, leaf_image_file)
        file_path = fs.path(filename)

        # --- Save to database ---
        leaf_image_obj = LeafImage.objects.create(
            image=filename  # This stores the file path relative to MEDIA_ROOT
        )

        # Predict disease using AI model
        prediction = predict_leaf_disease(file_path)  # ← returns dictionary now

        # Prepare result to show in template
        result = {
            'disease': prediction.get('disease'),
            'confidence': prediction.get('confidence'),
            'solution': prediction.get('solution'),
            'image_url': fs.url(filename),
            'image_id': leaf_image_obj.id,
            'upload_date': leaf_image_obj.upload_date
        }

    else:
        # If user directly visits the predict page, redirect to home
        return redirect('home')

    return render(request, 'predictresult.html', {'result': result})

def about(request):
    return render(request, 'about.html')

def indexabout(request):
    return render(request, 'indexabout.html')

def shop(request):
    products=ProductDb.objects.all()
    return render(request, 'shop.html',{'products':products})

def productmore(request, dataid):
    product = ProductDb.objects.get(id=dataid)
    return render(request, 'productmore.html', {'product': product})

def signup(request):
    return render(request, 'signup.html')

def createaccount(req):
    if req.method == "POST":
        un = req.POST.get('username')
        a = req.POST.get('age')
        e = req.POST.get('email')
        pwd = req.POST.get('password')
        obj = CreateAccountDb(username=un,age=a, email=e, password=pwd)
        obj.save()
        return redirect(index)

def login(request):
    return render(request, 'login.html')

def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CreateAccountDb.objects.filter(username=username, password=password).exists():
            request.session['username'] = username
            request.session['password'] = password
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
            return redirect('login')

    return redirect('login')

def logout(req):
    del req.session['username']
    del req.session['password']
    return redirect(index)

def addtocart(request, id):
    if 'username' not in request.session:
        return redirect('login')

    product = ProductDb.objects.get(id=id)

    # Check if the product already exists in cart
    cart_item, created = cartdb.objects.get_or_create(
        username=request.session['username'],
        product=product,
        defaults={
            'productname': product.productname,
            'price': product.price,
            'quantity': 1,
            'totalprice': product.price,
            'image': product.image
        }
    )

    if not created:
        # If already exists, just increase quantity
        cart_item.quantity += 1
        cart_item.totalprice = cart_item.quantity * product.price
        cart_item.save()

    return redirect('cart')

def cart(request):
    if 'username' not in request.session:
        return redirect('login')

    data = cartdb.objects.filter(username=request.session['username'])

    total = sum(item.price * item.quantity for item in data)

    # Shipping only if cart is not empty
    shipping = 50 if total > 0 else 0
    totalprice = total + shipping

    return render(request, 'cart.html', {
        'data': data,
        'total': total,
        'shipping': shipping,
        'totalprice': totalprice,
    })

def update_cart(request, id):
    if request.method == "POST":
        cart_item = get_object_or_404(cartdb, id=id)
        new_qty = int(request.POST.get("quantity", 1))
        if new_qty > 0:
            cart_item.quantity = new_qty
            cart_item.save()
    return redirect('cart')

def remove_cart(request, id):
    item = cartdb.objects.get(id=id)
    item.delete()
    return redirect('cart')

def clear_cart(request):
    username = request.session.get('username')  # get logged-in user's username
    if username:
        cartdb.objects.filter(username=username).delete()
    return redirect('shop')

from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import cartdb, orderdb  # make sure both models are imported

def confirmorder(req):
    if req.method == "POST":
        email = req.POST.get('email')
        address = req.POST.get('address')

        # Get all repeated fields as lists
        usernames     = req.POST.getlist('username[]')
        productnames  = req.POST.getlist('productname[]')
        quantities    = req.POST.getlist('quantity[]')
        prices        = req.POST.getlist('price[]')

        # Safety check: all lists should have same length
        if not (len(usernames) == len(productnames) == len(quantities) == len(prices)):
            return render(req, 'cart.html', {
                'data': cartdb.objects.filter(username=req.session.get('username', '')),
                'total': 0,
                'totalprice': 0,
                'order_success': False,
                'error': 'Cart data mismatch. Please try again.'
            })

        # Save each cart item as a separate order record
        for i in range(len(productnames)):
            try:
                qty = int(quantities[i])
                price = float(prices[i])

                orderdb.objects.create(
                    username=usernames[i],
                    productname=productnames[i],
                    quantity=qty,
                    totalprice=qty * price,      # per item total
                    email=email,
                    address=address,
                    # You can add more fields:
                    # status = 'pending',
                    # created_at = timezone.now(),
                    # payment_method = 'cod',
                )
            except (ValueError, TypeError):
                # Skip invalid rows (bad quantity/price)
                continue

        # Clear the user's cart after successful order
        current_username = req.session.get('username')
        if current_username:
            cartdb.objects.filter(username=current_username).delete()

        # Prepare success context
        context = {
            'order_success': True,
            'email': email,
            'address': address,
            'data': [],               # cart is now empty
            'total': 0,
            'totalprice': 0,
        }

        return render(req, 'cart.html', context)

    return redirect('cart')

def diseaseinfo(request):
    disease=DiseaseDb.objects.all()
    return render(request, 'disease.html',{'disease':disease})