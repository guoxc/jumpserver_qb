# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals
from django import forms
from django.shortcuts import reverse, redirect
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin

from common.utils import get_logger
from perms.models import AssetPermission
from ..models import User, UserGroup
from ..utils import AdminUserRequiredMixin
from .. import forms

__all__ = ['UserGroupListView', 'UserGroupCreateView', 'UserGroupDetailView',
           'UserGroupUpdateView', 'UserGroupGrantedAssetView']
logger = get_logger(__name__)


class UserGroupListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_group_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User group list')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = UserGroup
    form_class = forms.UserGroupForm
    template_name = 'users/user_group_create_update.html'
    success_url = reverse_lazy('users:user-group-list')
    success_message = _(
        'User group <a href={url}> {name} </a> was created successfully'
    )

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('Create user group'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_message(self, cleaned_data):
        url = reverse_lazy(
            'users:user-group-detail',
            kwargs={'pk': self.object.id}
        )
        return self.success_message.format(
            url=url, name=self.object.name
        )


class UserGroupUpdateView(AdminUserRequiredMixin, UpdateView):
    model = UserGroup
    form_class = forms.UserGroupForm
    template_name = 'users/user_group_create_update.html'
    success_url = reverse_lazy('users:user-group-list')

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        group_users = [user.id for user in self.object.users.all()]
        context = {
            'app': _('Users'),
            'action': _('Update user group'),
            'users': users,
            'group_users': group_users
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupDetailView(AdminUserRequiredMixin, DetailView):
    model = UserGroup
    context_object_name = 'user_group'
    template_name = 'users/user_group_detail.html'

    def get_context_data(self, **kwargs):
        users = User.objects.exclude(id__in=self.object.users.all())
        context = {
            'app': _('Users'),
            'action': _('User group detail'),
            'users': users,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupGrantedAssetView(AdminUserRequiredMixin, DetailView):
    model = UserGroup
    template_name = 'users/user_group_granted_asset.html'
    context_object_name = 'user_group'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': 'User',
            'action': 'User group granted asset',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
