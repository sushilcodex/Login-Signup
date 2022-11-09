class LogOutView(View):
    def get(self,request,*args,**kwargs):
        try:
            user=User.objects.get(id=request.user.id)
            logout(request)
            
        except:
            return render(request,"frontend/index.html")
        return redirect('accounts:web_login')


class LoginView(View):
    def get(self,request,*args,**kwargs):
        next_page = request.GET.get('next_page')
        return render(request,'registration/login.html' , {'change' : "login", "next_page":next_page})
    
    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            agent=request.META['HTTP_USER_AGENT']
            IP=request.META.get("REMOTE_ADDR")
            next_page = request.POST.get('next_page')
            des= request.path
            urls="https://"+IP+des
            email = request.POST.get("email")
            password = request.POST.get("password")
            if not email:
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="Failed",Code=urls)
                return render(request, 'registration/login.html',{"email":email})
            if not password:
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="Failed",Code=urls,user=email)
                return render(request, 'registration/login.html',{"email":email})
            if request.POST.get('remember_me')=='on':    
                request.session.set_expiry(7600) 
            user = authenticate(username=email, password=password)

            if not user:
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="Failed",Code=urls,user=email)
                if User.objects.filter(email=email,state_id=DELETED):
                    messages.add_message(request, messages.INFO, 'Your account has been deleted. Please create a new one.') 
                else:    
                    messages.add_message(request, messages.INFO, 'Incorrect email or password.')     
                return render(request, 'registration/login.html',{"email":email ,"password" : request.POST.get("password"), "bar":'danger','change' : "login"})
            else:
                if not user.customer_id or user.customer_id==None:
                    try:
                        stripe_customer = stripe.Customer.create(
                            description = "Felix & Fiddo User - %s " % user.email,
                            email = user.email
                        )
                        user.customer_id = stripe_customer.id
                        user.save()
                    except Exception as e:
                        pass
            if user.is_superuser and user.role_id == ADMIN :
                login(request, user)
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="success",Code=urls,user=email)
                user.session_id = request.session.session_key
                user.save()
                return redirect('admin:index')
            elif user.is_superuser and user.role_id == SUB_ADMIN and user.is_verify_mail:
                login(request, user)
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="success",Code=urls,user=email)
                user.session_id = request.session.session_key
                user.save()
                return redirect('admin:index')
            elif user.state_id == INACTIVE:
                messages.add_message(request, messages.INFO, 'Your account has been deactivated. Please contact admin (admin@toxsl.in) to activate your account.')
                return render(request, 'registration/login.html',{"email":email ,"password" : request.POST.get("password"), "bar":'danger','change' : "login"})
            elif user.state_id == DELETED:
                messages.add_message(request, messages.INFO, 'Your account has been deleted. Please create a new one.')
                return render(request, 'registration/login.html',{"email":email ,"password" : request.POST.get("password"), "bar":'danger','change' : "login"})
            elif user.role_id == RVT_LVT and user.is_verified == UNVERIFIED:
                messages.add_message(request, messages.INFO, 'Your Application is not accepted by admin , please wait for approval')     
                return render(request, 'registration/login.html',{"email":email ,"password" : request.POST.get("password"), "bar":'danger','change' : "login"})
            elif user.role_id == USERS and user.is_verify_mail:
                login(request, user)
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="success",Code=urls,user=email)
                user.session_id = request.session.session_key
                user.status = True
                user.save()

                if next_page and next_page != "None":
                    return redirect(next_page)
                messages.add_message(request, messages.INFO, 'Your Successfully Logged In to User Dashboard')
                return redirect('enduser:user_dashboard')
            elif user.role_id == RVT_LVT and user.is_verified == DECLINED:
                messages.add_message(request, messages.INFO, 'Your Application has been declined by admin')     
                return render(request, 'registration/login.html',{"email":email ,"password" : request.POST.get("password"), "bar":'danger','change' : "login"})
            elif user.role_id == RVT_LVT and user.is_verified == VERIFIED and user.is_verify_mail: 
                login(request, user)
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="success",Code=urls,user=email)
                user.session_id = request.session.session_key
                user.status = True
                user.save()
                
                if next_page and next_page != "None":
                    return redirect(next_page)
                messages.add_message(request, messages.INFO, 'Your Successfully Logged In to RVT Dashboard')
                return redirect('rvt_lvt:rvt_dashboard') 
            elif not user.is_verify_mail:
                messages.add_message(request, messages.INFO, 'Email has been sent to you. Please verify your account.') 
                return render(request, 'registration/login.html',{"email":email ,"password" : request.POST.get("password"), "bar":'danger','change' : "login"})    
            login(request, user)
            user.session_id = request.session.session_key
            user.save()
            feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="success",Code=urls,user=email)
            return redirect('frontend:index')

