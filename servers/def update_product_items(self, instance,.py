    def update_product_items(self, instance, validated_data):
        # get the nested objects list
        software_product_items = validated_data.pop('products')
        # get all nested objects related with this instance and make a dict(id, object)
        software_product_items_dict = dict((i.id, i) for i in instance.products.all())

        for software_item_data in software_product_items:
            if 'id' in software_item_data:
                # if exists id remove from the dict and update
                software_product_item = software_product_items_dict.pop(software_item_data['id'])
                # remove id from validated data as we don't require it.
                software_item_data.pop('id')
                # loop through the rest of keys in validated data to assign it to its respective field
                for key in software_item_data.keys():
                    setattr(software_product_item,key,software_item_data[key])

                software_product_item.save()
            else:
                # else create a new object
                Software.objects.create(software=instance, **software_item_data)

        # delete remaining elements because they're not present in my update call
        if len(software_product_items_dict) > 0:
            for item in software_product_items_dict.values():
                item.delete()


class Invoice(models.Model):
    nr = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

class InvoiceItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    invoice = models.ForeignKey(Invoice, related_name='items')
class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), required=False)
    class Meta:
        model = InvoiceItem


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice

    def create(self, validated_data):
        items = validated_data.pop('items', None)
        invoice = Invoice(**validated_data)
        invoice.save()
        for item in items:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice

    def update(self, instance, validated_data):
        instance.nr = validated_data.get('nr', instance.nr)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        items = validated_data.get('items')

        for item in items:
            item_id = item.get('id', None)
            if item_id:
                inv_item = InvoiceItem.objects.get(id=item_id, invoice=instance)
                inv_item.name = item.get('name', inv_item.name)
                inv_item.price = item.get('price', inv_item.price)
                inv_item.save()
            else:
                InvoiceItem.objects.create(account=instance, **item)

        return instance



        from rest_framework.utils import model_meta

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_item=InvoiceItemSerializer(many=True,required=False)

    field_map={"invoice_item" : { "model":  models.InvoiceItem
                                   "pk_field" : "id"}}    



    class Meta:
        model = models.Invoice
        fields = '__all__'

    def create(self, validated_data):
        extra_data={}
        for key in self.field_map.keys():
            extra_data[key]=validated_data.pop(key,[])

        # create invoice
        invoice = models.Invoice.objects.create(**validated_data)

        for key in extra_data.keys():
            for data in extra_data[key]:
                self.field_map[key]["model"].objects.create(invoice=invoice,**data)

        return invoice

    def _update(self,instance,validated_data):
        #drf default implementation
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def update(self,instance,validated_data):

        extra_data={}
        for key in self.field_map.keys():
            extra_data[key]=validated_data.pop(key,[])

        instance=self._update(instance,validated_data)

        for key in extra_data.keys():
            for data in extra_data[key]:

                id=data.get(self.field_map[key]["pk_field"],None)
                if id:
                    try:
                        related_instance=self.field_map[key]["model"].objects.get(id=id)
                    except:
                        raise
                    self._update(related_instance,data)
                else:
                    self.field_map[key]["model"].objects.create(**data)

        return instance    