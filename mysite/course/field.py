from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    # 自定义的字段属性在本质上就是一个类。定义了类的名称，并且继承models.PositiveIntegerField
    # 这里定义的OrderField是要得到对象排序的序号，其值为整数u，所以继承PositiveIntegerField
    def __init__(self,for_fields=None,*args,**kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args,**kwargs)

    def pre_save(self, model_instance, add):
        """pre_save()方法的作用是在保存之前对数值进行预处理，在具体的某个字段属性中，因为特殊需要，常常将Field类中的这个方法重写
        通过重写pre_save()方法，最终将实例的序号记录下来
        """
        if getattr(model_instance,self.attname) is None:
            # getattr()是Python的內建函数，它能够返回一个对象属性的值，getattr(model_instance,self.attname) 中的self.attname
            # 也是在Fields类里面规定的一个参数。
            # 使用 self.attname参数，判断当前对象（实例）中是否有某个属性（字段），如果有，就执行else分支，调用父类的
            # pre_save()方法，当不会在数据库中增加记录；否则就执行try语句，在try中主要计算新增一条数据后的序号
            try:
                qs = self.model.objects.all()   # 6 得到当前实例的所有记录
                if self.for_fields:
                    query = {field:getattr(model_instance,field) for field in self.for_fields}  #
                    #  得到字段列表中的属性名称（字段名称）在本实例中是否存在字典
                    qs = qs.filter(**query) # 根据 if语句中的数据对 结果进行筛选
                last_item = qs.latest(self.attname) # 根据self.attname 得到经过语句6筛选之后的记录中的最后一条
                value = last_item.order + 1   # 对当前实例进行序号的编排
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)      # 在相应的字段上记录本实例的序号，返回该序号值并通过pre_save()自动保存
            return value
        else:
            return super(OrderField, self).pre_save(model_instance,add)
