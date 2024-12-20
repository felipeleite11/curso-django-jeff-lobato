from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

def index(request):
	"""Página inicial do projeto"""
	return render(request, 'learning_logs/index.html')

@login_required
def auth_index(request):
	"""Página inicial do usuário autenticado"""
	return render(request, 'learning_logs/auth_index.html')

@login_required
def topics(request):
	"""Página de tópicos"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')

	context = {'topics': topics}

	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""Mostra um tópico único"""
	topic = Topic.objects.get(id=topic_id)

	if topic.owner != request.user:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')

	context = {
		'topic': topic, 
		'entries': entries
	}

	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	"""Adiciona um novo tópico"""
	if request.method != 'POST':
		# Gera formulário em branco
		form = TopicForm()
	else:
		# Formulário submetido
		form = TopicForm(request.POST)

		if form.is_valid():
			new_topic = form.save(commit=False)

			new_topic.owner = request.user

			new_topic.save()

			return HttpResponseRedirect(reverse('topics'))
	
	context = {'form': form}

	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Adiciona uma nova entrada"""
	topic = Topic.objects.get(id=topic_id)

	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# Gera formulário em branco
		form = EntryForm()
	else:
		# Formulário submetido
		form = EntryForm(data=request.POST)

		if form.is_valid():
			new_entry = form.save(commit=False)

			new_entry.topic = topic

			new_entry. save()

			return HttpResponseRedirect(reverse('topic', args=[topic_id]))
	
	context = {'form': form, 'topic': topic}

	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Edita uma entrada"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# Gera formulário em branco
		form = EntryForm(instance=entry)
	else:
		# Formulário submetido
		form = EntryForm(instance=entry, data=request.POST)

		if form.is_valid():
			form.save()

			return HttpResponseRedirect(reverse('topic', args=[topic.id]))
	
	context = {'form': form, 'topic': topic, 'entry': entry}

	return render(request, 'learning_logs/edit_entry.html', context)