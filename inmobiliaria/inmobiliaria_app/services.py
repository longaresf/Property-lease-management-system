from django.contrib.auth.models import Group, User
from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble, Comuna, Provincia, Region, Image
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib import messages

def crear_usuario(form, form_2):
    user = User.objects.create(username=form_2['username'].value(), first_name=form['nombres'].value(), last_name=form['apellidos'].value(), email=form['email'].value(), password=make_password(form_2['password1'].value()))

    user_id = User.objects.get(id=user.id)
    group = Group.objects.get(name=form['tipo_user'].value())
    user.groups.add(group)
        
    usuario = Usuario.objects.create(rut=form['rut'].value(), nombres=form['nombres'].value(), apellidos=form['apellidos'].value(), direccion=form['direccion'].value(), telefono=form['telefono'].value(), email=form['email'].value(), tipo_user=form['tipo_user'].value(), activo=form['activo'].value(), usuario=user_id, creado_por=form['creado_por'].value())

    return user_id

def update_usuario(form):
    id = form['usuario'].value()
    user = User.objects.filter(pk=id).update(first_name=form['nombres'].value(), last_name=form['apellidos'].value(), email=form['email'].value())

    group = Group.objects.get(name=form['tipo_user'].value())
    group.user_set.add(user)
    
    usuario = Usuario.objects.filter(usuario=id).update(nombres=form['nombres'].value(), apellidos=form['apellidos'].value(), direccion=form['direccion'].value(), telefono=form['telefono'].value(), email=form['email'].value(), tipo_user=form['tipo_user'].value())
    
    return usuario

def crear_inmueble(form, files, user):
    comuna = Comuna.objects.get(id=form['comuna'].value())

    inm = Inmueble.objects.create(nombre=form['nombre'].value(), descripcion=form['descripcion'].value(), construido=form['construido'].value(), totales=form['totales'].value(), estacionamiento=form['estacionamiento'].value(), habitaciones=form['habitaciones'].value(), banios=form['banios'].value(), direccion=form['direccion'].value(), comuna=comuna, inmueble_tipo=form['inmueble_tipo'].value(), arriendo_mes=form['arriendo_mes'].value(), activo=True, creado_por=user)

    user_id = User.objects.filter(id=user.id)
    inm.usuario.set(user_id)
    
    for f in files:
        Image.objects.create(inmueble = inm, image = f)
    return inm

def del_image(img_id):
    delete_img = Image.objects.get(id=img_id)
    delete_img.delete()
    return delete_img

def image_inm(images, inm_id):
    inm = Inmueble.objects.get(id=inm_id)
    for i in images:
        img = Image.objects.create(inmueble = inm, image = i)
    return img

def update_inmueble(form, inm_id):
    comuna = Comuna.objects.get(id=form['comuna'].value())
    inm = Inmueble.objects.filter(pk=inm_id).update(nombre=form['nombre'].value(), descripcion=form['descripcion'].value(), construido=form['construido'].value(), totales=form['totales'].value(), estacionamiento=form['estacionamiento'].value(), habitaciones=form['habitaciones'].value(), banios=form['banios'].value(), direccion=form['direccion'].value(), comuna=comuna, inmueble_tipo=form['inmueble_tipo'].value(), arriendo_mes=form['arriendo_mes'].value())
    return inm

def search_page(form):
    if Comuna.objects.filter(Q(nombre__istartswith=form['search'].value()) | Q(nombre__icontains=form['search'].value())):
        comuna = Comuna.objects.filter(Q(nombre__istartswith=form['search'].value()) | Q(nombre__icontains=form['search'].value()))
        for c in comuna:
            inm = Inmueble.objects.filter(comuna=c.id)
        return  inm
    
    elif Provincia.objects.filter(Q(nombre__istartswith=form['search'].value()) | Q(nombre__icontains=form['search'].value())):
        ciudad = Provincia.objects.filter(Q(nombre__istartswith=form['search'].value()) | Q(nombre__icontains=form['search'].value()))
        comuna = Comuna.objects.filter(provincia_id=ciudad.values_list('id')[0])
        for c in comuna:
            inm = Inmueble.objects.filter(comuna=c.id)
        return  inm
    
    elif Region.objects.filter(Q(nombre__istartswith=form['search'].value()) | Q(nombre__icontains=form['search'].value())):
        region = Region.objects.filter(Q(nombre__istartswith=form['search'].value()) | Q(nombre__icontains=form['search'].value()))
        ciudad = Provincia.objects.filter(region_id=region.values_list('id')[0])
        for c in ciudad:
            comuna = Comuna.objects.filter(provincia_id=c.id)
        for com in comuna:
            inm = Inmueble.objects.filter(comuna=com.id)
        return  inm
    
def solicitud_arriendo(user_id, inm_id):
    arrendador = Usuario.objects.get(usuario_id=user_id.id)
    arr = Usuario_Inmueble.objects.filter(inmueble_id=inm_id).update(arrendador=arrendador)
    return arr

def listar_prop_arriendo(user_id):
    arriendos = Usuario_Inmueble.objects.filter(arrendatario=user_id)
    return arriendos

def estado_arriendo(inm_id, form, request):
    try:
        arriendo = Usuario_Inmueble.objects.filter(inmueble=inm_id).update(estado=form['estado'].value())
        messages.success(request, f"Actualizado correctamente estado de arriendo a {form['estado'].value()}.")
    except:
        messages.warning(request, "Algo falló, favor intentar nuevamente")   

