from django.shortcuts import render
from .models import Chats, Messages
from .forms import MessageForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from social.models import Notification
from django.shortcuts import redirect
from django.db.models import Q
# Create your views here.



def index(request):
    user = request.user
    chats = Chats.objects.filter(users=request.user)

    notifcations = Notification.objects.filter(to_user=request.user)


    context = {
        'chats': chats,
        'notifcations': notifcations
    }
    return render(request, 'chats/index.html', context)


class ChatView(View, LoginRequiredMixin, UserPassesTestMixin):
    def get(self, request, pk, *args, **kwargs):
        chat = get_object_or_404(Chats, pk=pk)

        messages = Messages.objects.filter(
            chat=chat).order_by('created_on')


        notification = Notification.objects.filter(to_user=request.user)


        for n in notification:
            if n.chat == chat:
                n.delete()


        authorized = False

        for user in chat.users.all():
            if user == request.user:
                authorized = True


        form = MessageForm()

        context = {
            'messages': messages,
            'form': form
        }

        if authorized:
            return render(request, 'chats/chat.html', context)

        else:
            return render(request, 'chats/forbidden.html')

    def post(self, request, pk, *args, **kwargs):
        chat = get_object_or_404(Chats, pk=pk)
        messages = Messages.objects.filter(
            chat=chat).order_by('created_on')

        user = 'hahahahahaha'


        authorized = False

        for user in chat.users.all():
            if user == request.user:
                authorized = True

        for user in chat.users.all():
            if user != request.user:
                to_user = user

        form = MessageForm(request.POST, request.FILES)


        if authorized:
            if form.is_valid():
                new_message = form.save(commit=False)
                new_message.author = request.user
                new_message.chat = chat
                new_message.save()
                Notification.objects.create(notification_type=4, from_user=request.user, to_user=user, chat=chat)


            form = MessageForm()

            context = {
                'messages': messages,
                'form': form
            }

            return render(request, 'chats/chat.html', context)

        else:
            return render(request, 'chats/forbidden.html')






class MessageEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Messages
    fields = ['message']
    template_name = 'chats/message_update.html'

    def get_success_url(self):
        return reverse_lazy('chats_list')

    def test_func(self):
        message = self.get_object()
        return self.request.user == message.author


class MessageDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Messages
    template_name = 'chats/message_delete.html'

    def get_success_url(self):
        return reverse_lazy('chats_list')

    def test_func(self):
        message = self.get_object()
        return self.request.user == message.author



class MessageCreate(View):
    def post(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=request.user.pk)
        user2 = User.objects.filter(pk=pk)
        chats = Chats.objects.all()

        go = True
        chat = None

        for chat in chats:
            if chat.users.first() == user or chat.users.first() == user2 and chat.users.last == user or chat.users.last() == user2:
                go = False

        if go:
            chat = Chats.objects.create()
            chat.users.add(request.user.id)
            chat.users.add(pk)
            chat.save()
            return redirect('chats_list')

        else:

            messages = Messages.objects.filter(chat=chat)

            form = MessageForm()

            context = {
                'messages': messages,
                'form': form
            }


            return render(request, 'chats/chat.html', context)
