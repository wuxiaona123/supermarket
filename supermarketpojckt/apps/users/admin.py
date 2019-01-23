from django.contrib import admin
# 引用模块
from users.models import UserModels


# Register your models here.





# 用户表
@admin.register(UserModels)
class StudentAdmin(admin.ModelAdmin):
    list_per_page = 4  #: 每页显示条数

    actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
    actions_on_bottom: True  # 操作是否在下面显示, 默认   False

    # 自定义显示列，在models类中对字段有方法的就填方法名
    list_display = ['id', 'phone', 'nickname', 'password', 'gender', 'head', 'school', 'hometown', 'address',
                    'birthday', 'add_time', 'up_time', 'is_delete']

    # 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
    list_display_links = ['id', 'phone', 'nickname', 'password', 'gender', 'head', 'school', 'hometown', 'address',
                          'birthday', 'add_time', 'up_time', 'is_delete']

    # 列表右侧栏过滤器,只能写一个
    list_filter = ['phone']

    # 搜索框,搜索字段 也只能写一个
    search_fields = ['phone']

    # 对可编辑区域分组,列表里面的字段填写模型的属性，


fieldsets = (
    ('电话', {"fields": ['phone']}),
    ('昵称', {"fields": ['nickname']}),
    ('密码', {"fields": ['password']}),
    ('性别', {"fields": ['gender']}),
    ('头像', {"fields": ['head']}),
    ('学校', {"fields": ['school']}),
    ('老家', {"fields": ['hometown']}),
    ('地址', {"fields": ['address']}),
    ('出生日期', {"fields": ['birthday']}),
)

# 例子：
# 学生表 关联对象
# class StudentAdminInline(admin.TabularInline):
#     model = StudentInfo    #关联子对象，学生详情表
#     extra = 2    # 额外编辑2个子对象

# 学生表   (配值了学生详情表，就不单独写显示详细信息表了。)
# 注册模型类方式二
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
# list_per_page = 4  #: 每页显示条数

# 没效果
# actions_on_top: True  # 操作是否在上面显示, 默认  True  ,反正两个相反
# actions_on_bottom: True  # 操作是否在下面显示, 默认   False

# 自定义显示列，在models类中对字段有方法的就填方法名
# list_display = ['id', 'stu_name', 'stu_age', 'stu_sex', 'cla']

# 设置在列表页字段上添加一个 a标签, 从而进入到编辑页面,在models类中对字段有方法的就填方法名
# list_display_links = ['id', 'stu_name', 'stu_age', 'stu_sex', 'cla']

# 列表右侧栏过滤器,只能写一个
# list_filter = ['stu_name']

# 搜索框,搜索字段 也只能写一个
# search_fields = ['stu_name']

# fields = []: 定义在添加或者编辑的时候操作哪些字段，一般不设

# 对可编辑区域分组,列表里面的字段填写模型的属性，
# fieldsets = (
#     ('姓名', {"fields": ['stu_name']}),
#     ('年龄', {"fields": ['stu_age']}),
#     ('性别', {"fields": ['stu_sex']}),
#     ('所在班级', {"fields": ['cla']}),
# )

# 关联子对象,可以关联多个子对象，现在只关联自定义的StudentAdminInline类
# inlines = [StudentAdminInline]
