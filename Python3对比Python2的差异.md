# Python3对比Python2的差异

## 语法差异

- print

​	在Python3中print变成了函数，在python2中是关键字。目的是可以做更灵活的事情，例如可以用函数名替换的方式，找到某个输出。

- iterable

​	dict.items（）在Python3中返回的是一个迭代器，在Python2中是返回的一个列表。原因：避免便利keys的时候产生内存展开。然后map/zip/filter也有类似。在Python3中，用range取代xrange。

- Super简化

​	super(Foo,self).func(1,2)-->super().func(1,2)

- 对象比较

​	Python3默认两个不同类型的对象是不可以进行比较的，会发生报错。然后如果有些接口底层可能涉及到对象显示比较的在Python3中都被禁止了。相同类型的对象比较方式如下：

```python
_eq_(self,other): 定义相等比较(=)
_ne_(self,other): 定义不相等比较(!=)
_It_(self,other): 定义小于比较(<)
_le_(self,other): 定义小于等于比较（<=）
_gt_(self,other)：定义大于比较(>)
_ge_(self,other): 定义大于等于比较(>=)
```

在Python3中cmp()不再支持，实在要用可以自己实现。实现的具体可以借鉴引用到six库，然后用Compare。另外在Python3中“_nonzero__"换成了 "_bool_",这是为了保证语义的统一

- 整型

​	Python3中去掉了long类型，long类型改名为int类型。/：除法返回float，//：返回int类型

​	round：python2和python3底层算法不一样了，python2采用的是四舍五入的方式。python3采用的是银行家舍入法（四舍六入，五奇进偶退）。

![](C:\Users\wb.liutao18\Desktop\1.png)

除法可能会带来的问题：比如113除以100，在python2中除完后会得到1，python3中除完后会得到1.13，这个时候如果有匹配项的话，那么python2会匹配到1，python3得到的结果由于不等于1，所以会按默认的结果走，会匹配到0。

- function、

​	python3中unbound method去掉了，代替成function，同时boundmethod.im_func/im_self等变成了_func_/_self_

- metaclass

​	metaclass是python中元类的概念，目的是可以动态的创建一个类。举个例子：

​	不使用metaclass：

```python
class A:
    NAME = "AA"
    def func(self):
        pass
```

​	使用metaclass：

```python
class MetaA(type):
    def _new_(cls,name,bases,d):
        d['NAME'] = "AA"
        d['func'] = func
        return type._new_(cls,name,bases,d)
class A(metaclass = MetaA):
    pass
```

上面这两种写法是完全等价的，但是代码2会更灵活和可控

python3和python2语法上存在差别，在Python 3中，`__metaclass__`属性不再支持，必须使用`metaclass`关键字参数来指定元类。

- hasattr异常处理

​	hasattr:用于检查对象是否包含指定的属性或方法。在Python3中如果尝试访问的属性与异常情况相关，`hasattr()`会抛出异常，而不会像Python 2那样忽略这些异常并返回`False`。

- str与unicode

 	unicode虽然全且兼容性好，但是占空间，于是有了utf-8变长方案，unicode与bytes转换关系如下：bytes通过decode转成unicode，unicode通过encode转成bytes。 这样其实服务器和客户端交互传输数据的时候也方便。

- import&meta_path

  相对import和绝对import：python3搜索不会自动下一层级，而是只是搜索当前层级，这个时候通过一个参数来解决这个问题。

  meta_path：在兼容原本python2的情况下，增加ModuleSpec类，存储module的位置等信息，create_module与exec_modules分开，保证在exec的时候，module已经存在与sys.modules（exec的时候可能访问自己）

- pyo/pyc

​	Python3将pyc文件同意放到`_pycache_`目录下，取消了pyo后缀

## 新的语法

- fstring

​	字符串格式化。

- str.removeprefix、str.removesuffix
- Python3.8引入了一套特殊参数，通过显式的’/‘与'*'两符号标明位置或关键字参数。具体用途就是后续如果函数需要加入传入参数个数会导致出现问题从而在源头上解决这一问题。
- 海象运算符
- 函数标注
- enum
- match语句类似于其他语法中的switch
- BreakPoint。

## 新的库

- importlib代替imp()
- dataclass，python2中要实现简单的数据类可能会用到`_slots_`,`property`等，python采用dataclass
- asyncio
- pickle&marshal
- pathlib
- concurrent.futures



