# obj, created = sfs_upcs.objects.update_or_create(
#     # filter on the unique value of `upc`
#     upc=upc,
#     # update these fields, or create a new object with these values
#     defaults={
#         'product_title': product_title, 'is_buyable': is_buyable,  'price': price, 
#         'image_url': image_url, 'breadcrumb': breadcrumb, 'product_url': product_url,
#     }
# )
    # def create(self, validated_data):
    #     # server_name = validated_data['name']
    #     # if Server.objects.filter(name=server_name).values_list('id', flat=True).exists() == True:
    #     #     print(f'SERVER EXISTS IN DATABASE:')
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={'name': validated_data.get('name', None)})
    #     return server
    # def create(self, validated_data):
    #     # server_name = validated_data['name']
    #     # if Server.objects.filter(name=server_name).values_list('id', flat=True).exists() == True:
    #     #     print(f'SERVER EXISTS IN DATABASE:')
    #     server, created = Server.objects.update_or_create(
    #         # slug = validated_data.get('name', None).lower(),
    #         name = validated_data.get('name', None),
    #         status = validated_data.get('status', None),
    #         ip_address = validated_data.get('ip_address', None),
    #         fqdn = validated_data.get('fqdn', None),
    #         defaults={
    #             'name': validated_data.get('name', None),
    #             # 'slug': validated_data.get('slug', None),
    #             'status': validated_data.get('status', None),
    #             'ip_address': validated_data.get('ip_address', None),
    #             'fqdn': validated_data.get('slug', None),

    #             })
    #     return server
    # def update(self, validated_data):
    #     server_name = validated_data['name']
    #     if Server.objects.filter(name=server_name).values_list('id', flat=True).exists() == False:
    #         print("Entry contained in queryset")
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={'name': validated_data.get('name', None)})
    #     return server
    # def create(self, validated_data):
    #     server_name = validated_data['name']
    #     print(f'THIS IS VALIDATED DATA: \n ********** \n{validated_data}\n **********')
    #     # Check if server exists in database - and return true/false
    #     server_exists = Server.objects.filter(name=server_name).values_list('id', flat=True).exists()
    #     print(f'SERVER EXISTS IN DATABASE: \n ********** \n{server_exists}\n **********')
    #     if server_exists == False:
    #         print(f'CREATING NEW SERVER: \n{server_exists} with {server_name}')
    #         return Server.objects.create(**validated_data)
    #     else:
    #         print('WTF')