from django.shortcuts import render,redirect
from .models import User,Contact,Product,Wishlist,Cart,Shipping_Address,Billing_Address,Transaction
import random
from django.conf import settings
from django.core.mail import send_mail
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    amount = int(request.POST['amount'])
    transaction = Transaction.objects.create(made_by=user, amount=amount)
    
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()
    carts=Cart.objects.filter(user=user,payment_status=False)
    for i in carts:
        i.payment_status=True
        i.save()
    carts=Cart.objects.filter(user=user,payment_status=False)
    request.session['cart_count']=len(carts)
    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

def index(request):
    product=Product.objects.all()
    try:
        user=User.objects.get(email=request.session['email'])
        if user.usertype=="buyer":
            
            return render(request,'index.html',{'product':product})
        else:
            return render(request,'seller-index.html')
    except:
        return render(request,'index.html',{'product':product})
def seller_index(request):
    return render(request,'seller-index.html')
def shop(request):
    product=Product.objects.all()
    return render(request,'shop.html',{'product':product})
def detail(request,pk):
    wishlist_flag=False
    cart_flag=False
    product=Product.objects.get(pk=pk)
    user=User()
    try:
        user=User.objects.get(email=request.session['email'])
    except:
        pass
    try:
        Wishlist.objects.get(user=user,product=product)
        wishlist_flag=True
    except:
        pass
    try :
        Cart.objects.get(user=user,product=product)
        cart_flag=True
    except:
        pass


    return render(request,'detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        msg="Contact Form Submitted Successfully"
        return render(request,'contact.html',{'msg':msg})
    else:
        return render(request,'contact.html')
def seller_contact(request):
    if request.method=="POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],

        )
        msg="Contact Form Submitted Successfully"
        return render(request,'seller-contact.html',{'msg':msg})
    else:
        return render(request,'seller-contact.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                if user.usertype=="buyer":
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile_pic']=user.profile_pic.url
                    wishlist=Wishlist.objects.filter(user=user)
                    cart=Cart.objects.filter(user=user,payment_status=False)
                    request.session['wishlist_count']=len(wishlist)
                    request.session['cart_count']=len(cart)

                    return render(request,'index.html')
                else:
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile_pic']=user.profile_pic.url
                    return render(request,'seller-index.html')
            else:
                msg="Password is Incorrect"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Not Registered"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
def register(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registared"
            return render(request,'register.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password'],
                    profile_pic=request.FILES['profile_pic'],
                    usertype=request.POST['usertype'],
                    address=request.POST['address']
                )
                msg="User Sign Up Sucessfully"
                return render(request,'register.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Does Not Matched"
                return render(request,'register.html',{'msg':msg})
    else:
        return render(request,'register.html')
def logout(request):
    try:
        del request.session['fname']
        del request.session['profile_pic']
        del request.session['email']
        return render(request,'login.html')
    except:
        return render(request,'login.html')
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if user.usertype=="buyer":
        if request.method=="POST":
            user.fname=request.POST['fname']
            user.lname=request.POST['lname']
            user.address=request.POST['address']
            user.mobile=request.POST['mobile']
            try:
                user.profile_pic=request.FILES['profile_pic']
            except:
                pass
            user.save()
            msg="Profile Has been Updated Succesfully"
            request.session['fname']=user.fname
            request.session['profile_pic']=user.profile_pic.url
            return render(request,'seller-profile.html',{'msg':msg,'user':user})
        else:
            return render(request,'profile.html',{'user':user})
    else:
        if request.method=="POST":
            user.fname=request.POST['fname']
            user.lname=request.POST['lname']
            user.address=request.POST['address']
            user.mobile=request.POST['mobile']
            try:
                user.profile_pic=request.FILES['profile_pic']
            except:
                pass
            user.save()
            msg="Profile Has been Updated Succesfully"
            request.session['fname']=user.fname
            request.session['profile_pic']=user.profile_pic.url
            return render(request,'profile.html',{'msg':msg,'user':user})
        else:
            return render(request,'profile.html',{'user':user})
def seller_profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.address=request.POST['address']
        user.mobile=request.POST['mobile']
        try:
            user.profile_pic=request.FILES['profile_pic']
        except:
            pass
        user.save()
        msg="Profile Has been Updated Succesfully"
        request.session['fname']=user.fname
        request.session['profile_pic']=user.profile_pic.url
        return render(request,'seller-profile.html',{'msg':msg,'user':user})
    else:
        return render(request,'seller-profile.html',{'user':user})
def change_password(request):
    user=User.objects.get(email=request.session['email'])

    if request.method=="POST":
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg="New password & Confirm New Password Does not Matched"
                return render(request,'change-password.html',{'msg':msg})
        else:
            msg="Old password & New Password Does not Matched"
            return render(request,'change-password.html',{'msg':msg})
    else:
        return render(request,'change-password.html')
def seller_change_password(request):
    user=User.objects.get(email=request.session['email'])

    if request.method=="POST":
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg="New password & Confirm New Password Does not Matched"
                return render(request,'seller-change-password.html',{'msg':msg})
        else:
            msg="Old password & New Password Does not Matched"
            return render(request,'seller-change-password.html',{'msg':msg})
    else:
        return render(request,'seller-change-password.html')
def forgot_password(request):
    if request.method=="POST":
        try:
            otp=random.randint(1111,9999)
            user=User.objects.get(email=request.POST['email'])
            subject = 'OTP for Forgot Password'
            message = 'OTP for Forgot Password is'+" "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'otp.html', {'otp': otp, 'email': user.email})
        except:
            return render(request,'forgot-password.html')
    else:
        return render(request,'forgot-password.html')
def verify_otp(request):
    email=request.POST['email']
    otp=request.POST['otp']
    uotp=request.POST['uotp']
    if otp==uotp:
        return render(request,'new-password.html',{'email':email})
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'email':email,'msg':msg,'otp':otp})

def new_password(request):
    email=request.POST['email']
    npass=request.POST['new_password']
    cnpass=request.POST['cnew_password']
    if npass==cnpass:
        user=User.objects.get(email=email)
        user.password=npass
        user.save()
        msg="Password Updated Succesfully"
        return render(request,'login.html',{'msg':msg})
    else:
        msg="New Password & Confirm Password Does not Matched"
        return render(request,'new-password.html', {'msg':msg})
def view_product(request):
    product_seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(product_seller=product_seller)

    return render(request,'view-product.html',{'products':products})
def add_product(request):
    if request.method=="POST":
        product_seller=User.objects.get(email=request.session['email'])
        Product.objects.create(
            product_seller=product_seller,
            product_cate=request.POST['product_cate'],
            dressess_cate=request.POST['dressess_cate'],
            product_name=request.POST['product_name'],
            product_price=request.POST['product_price'],
            product_desc=request.POST['product_desc'],
            product_size=request.POST['product_size'],
            product_pic=request.FILES['product_pic']

        )
        msg="Product Added SuccessFully"    
        return render(request,'add-product.html',{'msg':msg})
    else:
        return render(request,'add-product.html')
def seller_detail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'seller-detail.html',{'product':product})
def edit_seller_product(request,pk):
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.product_cate=request.POST['product_cate']
        product.product_desc=request.POST['product_desc']
        product.product_name=request.POST['product_name']
        product.product_price=request.POST['product_price']
        product.product_size=request.POST['product_size']
        product.dressess_cate=request.POST['dressess_cate']
        try:
            product.product_pic.url=request.FILES['product_pic']
        except:
            pass
        product.save()
        msg="Product Updated SuccessFully"
        return render(request,'edit-seller-product.html',{'msg':msg,'product':product})
    else:
        return render(request,'edit-seller-product.html',{'product':product})
def delete_seller_product(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return render(request,'view-prodyct.html')
def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(
        user=user,
        product=product,
        product_price=product.product_price,
        product_qty=1,
        total_price=product.product_price,

    )
    return redirect('cart')
def cart(request):
    net_price=0
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user,payment_status=False)
    for i in carts:
        net_price=net_price+i.total_price+i.total_price_shipping
    request.session['cart_count']=len(carts)

    return render(request,'cart.html',{'carts':carts,'net_price':net_price})
def remove_from_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    cart=Cart.objects.get(user=user,product=product,payment_status=False)
    cart.delete()
    return redirect('cart')
def add_to_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(user=user,product=product)
    wishlist=Wishlist.objects.filter(user=user)
    return redirect('wishlist')
def wishlist(request):
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.filter(user=user)
    request.session['wishlist_count']=len(wishlist)
    return render(request,'wishlist.html',{'wishlist':wishlist})
def remove_from_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.get(user=user,product=product)
    wishlist.delete()
    return redirect('wishlist')
def change_qty(request):
    cart=Cart.objects.get(pk=request.POST['pk'])
    product_qty=int(request.POST['product_qty'])
    product_price=cart.product_price
    total_price=product_qty*product_price
    print(total_price)
    cart.product_qty=product_qty
    cart.total_price=total_price
    cart.save()
    return redirect('cart')


def checkout(request):
    net_price=0
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user,payment_status=False)
    for i in carts:
        net_price=net_price+i.total_price+i.total_price_shipping
    return render(request,'checkout.html',{'carts':carts,'net_price':net_price,'user':user})

def billing(request):
    if request.method=="POST":
        bill_address=Billing_Address.objects.create (
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            address=request.POST['address'],
            mobile=request.POST['mobile'],
            billing_country=request.POST['country'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip_code'],

        )
        Billings=Billing_Address.objects.all().order_by("-id")
        msg="Sucessfully Added"
        return render(request,'billing-address.html',{'Billings':Billings,'msg':msg})


    else:
        Billings=Billing_Address.objects.all().order_by("-id")

        return render(request,'billing-address.html',{'Billings':Billings})
def shipping(request):
    if request.method=="POST":
        shipping_Address=Shipping_Address.objects.create(
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            address=request.POST['address'],
            shipping_country=request.POST['country'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip_code'],

        )
        msg="Sucessfully Added"
        Shippings=Shipping_Address.objects.all().order_by("-id")
        return render(request,'shipping-address.html',{'Shippings':Shippings,'msg':msg})

    else:
        Shippings=Shipping_Address.objects.all().order_by("-id")

        return render(request,'shipping-address.html',{'Shippings':Shippings})

   