from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout, authenticate, login
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image
from django.contrib import messages
from inmobiliaria_app.forms import LoginForm, CustomUserCreationForm, UserForm, InmForm, ImageForm, SearchForm, EstatusArriendoForm
from django.contrib.auth.models import Group, User
from inmobiliaria_app.services import crear_usuario, update_usuario, crear_inmueble, update_inmueble, del_image, image_inm, search_page, solicitud_arriendo, estado_arriendo, listar_prop_arriendo

# Create your views here.

def home(request):
    inm = Inmueble.objects.filter(activo=True)
    img = Image.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            try:
                inm = search_page(form)
                return render(request, "home.html", { 'form':form, 'inm': inm })
            except TypeError:
                messages.warning(request, "No se encontró ninguna coincidencia")
        else:
            messages.warning(request, "Algo salió mal, favor intentar nuevamente")
    else:
        form = SearchForm()
    return render(request, 'home.html', {'inm':inm, 'form':form, 'img': img})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.warning(request, "Usuario o contraseña errada")
    else:
        form = LoginForm()
    return render(request, "login.html", {'form':form })

def salir(request):
    logout(request)
    return redirect('/')

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form_2 = CustomUserCreationForm(request.POST)
        
        if form_2.is_valid() and form.is_valid():
            crear_usuario(form, form_2)
            user = authenticate(username = form_2.cleaned_data['username'], password = form_2.cleaned_data['password1'])
            login(request,user)

            messages.success(request, "Registro exitoso. Gracias por registrarte a Inmobiliaria Francisco!")
            return redirect('/')
        else:
            messages.warning(request, "Falló registro, favor intentar nuevamente")
    else:
        form_2 = CustomUserCreationForm()
        form = UserForm()
    return render(request, "register_user.html", { 'form_2':form_2, 'form':form  })

@login_required
def update_user(request):
    user = User.objects.get(pk=request.user.id)
    try:
        usuario = Usuario.objects.get(usuario=request.user.id)
    except User.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")
    except Usuario.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=usuario)

        if form.is_valid():
            update_usuario(form)
            messages.success(request, "Registro mofificado exitosamente.")
        else:
            messages.warning(request, "Hubo un problema, favor intentar nuevamente")
    else:
        form = UserForm()
    return render(request, "update_user.html", { 'form':form, 'usuario':usuario })

@login_required
def perfil_user(request):
    user = User.objects.get(pk=request.user.id)
    try:
        usuario = Usuario.objects.get(usuario=request.user.id)
        if usuario.tipo_user == 'Arrendatario':
            inm = Inmueble.objects.filter(usuario=request.user.id)
    except Usuario.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")
    except User.DoesNotExist:
            messages.warning(request, "Usuario no existe, favor intentar con otro usuario")     
    except Inmueble.DoesNotExist:
            messages.warning(request, "Usuario no posee publicaciones")
    form = UserForm()
    return render(request, "perfil_user.html", { 'form':form, 'user':user, 'usuario':usuario })

@login_required
def delete_user(request):
    user = User.objects.get(pk=request.user.id)
    user.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect('/')

@login_required
def create_inm(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = InmForm(request.POST)
        form1 = ImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() & form1.is_valid():
            crear_inmueble(form, files, user)
            messages.success(request, "Registro de inmueble creado correctamente.")
        else:
            messages.warning(request, "Falló registro, favor intentar nuevamente")
    else:
        form = InmForm()
        form1 = ImageForm()
    return render(request, "create_inm.html", { 'form':form, 'form1':form1 })

def perfil_inm(request):
    inm_id = request.COOKIES['inm_id']
    inm = Inmueble.objects.filter(id=inm_id)
    img = Image.objects.filter(inmueble = inm_id)
    return render(request, "perfil_inm.html", { 'inm':inm, 'img': img } )

@login_required
def image_inmueble(request):
    form = ImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        inm_id = request.COOKIES['inm_id']
        inm = Inmueble.objects.filter(id=inm_id)
        images = request.FILES.getlist('image')
        if form.is_valid():
            image_inm(images, inm_id)
            img = Image.objects.filter(inmueble=inm_id)
            messages.success(request, "Imagen agregada correctamente.")
            return render(request, 'perfil_inm.html', { 'inm':inm, 'img': img })
        else:
            messages.warning(request, "Falló registro, favor intentar nuevamente")

    return render(request, "perfil_inm.html")

@login_required
def publication_inm(request):
    user_id = User.objects.get(id=request.user.id)
    inm = Inmueble.objects.filter(usuario=user_id)
    #img = Image.objects.filter(inmueble=inm)

    return render(request, "publication_inm.html", { 'inm':inm } )

@login_required
def delete_img(request):
    img_id = request.COOKIES['img_cook']
    inm_id = request.COOKIES['inm_id']
    del_image(img_id)
    inm = Inmueble.objects.filter(id=inm_id)
    img = Image.objects.filter(inmueble = inm_id)
    messages.success(request, "Imagen eliminada correctamente.")
    return render(request, "perfil_inm.html", { 'inm':inm, 'img': img } )

@login_required
def delete_inm(request):
    inm_id = request.COOKIES['inm_id']
    inm = Inmueble.objects.get(pk=inm_id)
    inm.delete()
    messages.success(request, "Inmueble eliminado correctamente.")
    return redirect('/')

@login_required
def update_inm(request):
    inm_id = request.COOKIES['inm_id']
    inm = Inmueble.objects.get(pk=inm_id)
    if request.method == 'POST':
        form = InmForm(request.POST)
        if form.is_valid():
            update_inmueble(form, inm_id)
            messages.success(request, "Actualizado correctamente.")
        else:
            messages.warning(request, "Algo falló, favor intentar nuevamente")
    else:
        form = InmForm()
    return render(request, "update_inm.html", { 'form':form, 'inm':inm })

@login_required
def arrendar_inm(request):
    user_id = User.objects.get(id=request.user.id)
    inm_id = request.COOKIES['inm_id']
    arr = solicitud_arriendo(user_id, inm_id)
    if arr is not None:
        messages.success(request, "Solicitud de arriendo exitosa.")
    else:
        messages.warning(request, "Algo falló, favor intentar nuevamente")
    return render(request, "perfil_inm.html" )

@login_required
def estado_inmuebles(request):
    user_id = User.objects.get(id=request.user.id)
    arriendos = listar_prop_arriendo(user_id)
    if request.method == 'POST':
        form = EstatusArriendoForm(request.POST)
        if form.is_valid():
            inm_id = request.COOKIES['inm_id']
            estado_arriendo(inm_id, form, request)
        else:
            return render(request, "arriendo.html", { 'arriendos': arriendos } )
    return render(request, "arriendo.html", { 'arriendos': arriendos } )



def bad_request(request, exception=None):
    # return render(request, '400.html')
    return redirect('/')

def permission_denied(request, exception=None):
    # return render(request, '403.html')
    return redirect('/')

def page_not_found(request, exception=None):
    # return render(request, '404.html')
    return redirect('/')

def server_error(request, exception=None):
    # return render(request, '500.html')
    return redirect('/')

