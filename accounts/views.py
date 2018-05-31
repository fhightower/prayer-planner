from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import RegistrationForm


class RegistrationView(generic.View):
    form_class = RegistrationForm
    template_name = "registration/registration.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')

        return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, generic.View):
    template_name = "registration/profile.html"

    def get(self, request):
        return render(request, self.template_name)
