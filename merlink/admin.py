from django.contrib import admin
from .models import Server, Software, Version

admin.site.register(Server)
admin.site.register(Software)
admin.site.register(Version)

# class ServerAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "name",
#         "ip_address",	
#         "fqdn",	
#         "status",	
# 				]
#     list_display_links = [
#         'id', 
#         'name'
#         ]
#     readonly_fields = ["slug"]

#     class Meta:
#         model = Server

# admin.site.register(Server, ServerAdmin)


# class SoftwareAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "name",
#         "version",	
#         "install_date",	
#         "status",	
# 				]
#     list_display_links = [
#         'id', 
#         'name'
#         ]
#     readonly_fields = ["slug"]

#     class Meta:
#         model = Software

# admin.site.register(Software, SoftwareAdmin)