from django.contrib import admin

from .models import Product, Order, Category


# 产品类型
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'update_time')
    list_per_page = 10

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {'fields':
                        (
                            'name', 'desc',
                        )}),
        )


# 产品信息
@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'desc', 'price', 'model', 'size', 'object_id',
                    'create_time', 'update_time')
    list_per_page = 20

    def get_fieldsets(self, request, obj=None):
        return ( (None, {'fields': (
            'category', 'name', 'desc', 'model', 'size', 'object_id', 'price', 'image',
        )}),
                 )


# 订单信息管理
@admin.register(Order)
class BookingsAdmin(admin.ModelAdmin):

    def post_item(self, obj):
        return [it.product for it in obj.item.all()]

    post_item.short_description = "订单内产品"

    list_display = ('order_id',
                    'create_by',
                    'to_user',
                    'post_item',
                    'total_price',
                    'order_status',
                    'create_time',
                    'update_time'
                    )
    list_per_page = 20
    # search_fields = ('order_id',
    #                  'create_by',
    #                  'to_user',
    #                  'total_price',
    #                  'order_status',
    #                  )
    list_filter = ('order_id',
                   'create_by',
                   'to_user',
                   'total_price',
                   'order_status',
                   )

    # 自定义功能
    actions = ('custom_button',)

    def custom_button(self, request, queryset):
        pass

    custom_button.short_description = "测试按钮"
    custom_button.icon = 'fas fa-audio-description'

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g)
        return group_names

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or '管理员' in group_names:
            return 'to_user', 'order_status'
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(BookingsAdmin, self).get_changelist_instance(request)

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {'fields':
                        (
                            'order_id', 'create_by', 'to_user', 'total_price', 'total_quantity',
                            'order_status', 'order_pay', 'order_send_status', 'order_send_way', 'order_send_nu'
                        )}),
        )
