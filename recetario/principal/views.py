from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from principal.forms import ComentarioForm, ContactoForm, RecetaForm
from principal.models import Comentario, Receta

def sobre(request):
	html = "<html><body>Proyecto de ejemplo en MDW</body></html>"
	return HttpResponse(html)

def inicio(request):
	recetas = Receta.objects.all()
	return render_to_response('inicio.html',
		{'recetas':recetas},
		context_instance=RequestContext(request))

def usuarios(request):
	usuarios = User.objects.all()
	recetas = Receta.objects.all()
	return render_to_response('usuarios.html',
		{'usuarios': usuarios, 'recetas': recetas},
		context_instance=RequestContext(request))

def lista_recetas(request):
	recetas = Receta.objects.all()
	return render_to_response('lista_recetas.html',
		{'datos': recetas},
		context_instance = RequestContext(request))

def detalle_receta(request, id_receta):
	dato = get_object_or_404(Receta, pk=id_receta)
	comentarios = Comentario.objects.filter(receta=dato)
	return render_to_response('receta.html',
		{'receta': dato, 'comentarios': comentarios},
		context_instance = RequestContext(request))

def contacto(request):
	if request.method=='POST':
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mensaje desde el recetario'
			contenido = formulario.cleaned_data['mensaje'] + "\n"
			contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['norberto@utdelacosta.edu.mx'])
			correo.send()
			return HttpResponseRedirect('/')
	else:
			formulario = ContactoForm()
	return render_to_response('contactoForm.html',
			{'formulario': formulario},
			context_instance=RequestContext(request))

def nueva_receta(request):
    if request.method=='POST':
        formulario = RecetaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/recetas')
    else:
        formulario = RecetaForm()
    return render_to_response('recetaform.html',{'formulario':formulario}, context_instance=RequestContext(request))

def nuevo_comentario(request):
	if request.method=='POST':
		formulario = ComentarioForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/recetas')
	else:
		formulario = ComentarioForm()
	return render_to_response('comentarioForm.html',
		{'formulario': formulario},
		context_instance=RequestContext(request))

def nuevo_usuario(request):
	if request.method=='POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = UserCreationForm()
	return render_to_response('nuevo_usuario.html',
		{'formulario': formulario},
		context_instance=RequestContext(request))

def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	if request.method=='POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html',
						context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html',
					context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html',
		{'formulario': formulario},
		context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	return render_to_response('privado.html',
		{'usuario': usuario},
		context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')