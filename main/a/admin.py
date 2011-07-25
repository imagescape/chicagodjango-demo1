from django.contrib import admin 
from django.contrib.auth.models import User 
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.forms.models import fields_for_model
from a import models, utils

class PostAdminForm(forms.ModelForm):


    class Meta:
        model =  models.Post

    def clean(self):
        cleaned_data = self.cleaned_data
        message = cleaned_data.get("message", False)

        if len(message) < 20:
            raise forms.ValidationError("Message must be 20+ chars long.")

        return cleaned_data


class PostAdmin(admin.ModelAdmin):

    list_display = ['title','type','preformed_by',]
    readonly_fields=['created', 'modified', 'preformed_by', 'ipaddress', ]
    form = PostAdminForm

    fieldsets = []
  
    def __init__(self, model, admin_site):
        
        post_fields = ['title','type','featured']
        meta_fields = ['created','modified',]
        client_fields = ['preformed_by','ipaddress']
        message_fields = ['message',]       
 
        ex_fields = post_fields +  meta_fields + client_fields + message_fields
        all_fields = fields_for_model(model)

        base_fields = [tuple(post_fields), tuple(meta_fields), tuple(message_fields)]

        rest_fields = list(set(all_fields) - set(ex_fields))
    
        self.fieldsets.append(('Post Info', { 'fields': tuple(base_fields), }))
        self.fieldsets.append(('Client Info', { 'fields': tuple(client_fields), }))
        
        if rest_fields:
            self.fieldsets.append(('Other', { 'fields': tuple(rest_fields), }))
        self.fieldsets = tuple(self.fieldsets)

        super(PostAdmin, self).__init__(model, admin_site)


    def get_readonly_fields(self, request, obj = None):
        if obj: 
            if not (request.user.is_staff or request.user.is_superuser):
                return ['featured',] + self.readonly_fields
            return self.readonly_fields
        else:
            return self.readonly_fields

    admin_actions = None

    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        try:
            del actions['delete_selected']
        except KeyError:
            pass 
        return actions

    def has_delete_permission(self, request, obj=None):
        return_value = False
        user = request.user
        if user.is_authenticated() and user.is_staff:
            return_value = True
        return return_value 

    def has_add_permission(self, request):
        return_value = False
        user = request.user
        if user.is_authenticated() and user.is_superuser:
            return_value = True
        return return_value 


    def save_model(self, request, obj, form, change):
        obj.preformed_by = request.user
        obj.ipaddress = utils.get_client_ip(request)
        obj.save()

    filter_horizontal = ('category',)

    raw_id_fields = ("tags",)


admin.site.register(models.Post, PostAdmin)



##################################################################################

class PostInline(admin.TabularInline):
    model = models.Post
    extra = 0
    readonly_fields = ['created', 'modified', 'preformed_by', 'ipaddress']
    exclude = ['tags','category',]


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('date_joined','last_login')
    list_filter = UserAdmin.list_filter + ('is_active',)
    inlines = [PostInline,]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(models.PostCategory)
admin.site.register(models.PostTag)


