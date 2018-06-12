## FAQ

这里记录一下常见的一些问题

- 导出导入依赖库
```
# 导出当前环境的所有库
pip freeze > requirements.txt

# 导出项目依赖库
# 相关链接：https://github.com/bndr/pipreqs
pip install pipreqs
pipreqs --encoding utf-8 project-path
# 更新依赖库
pipreqs --force --encoding utf-8 project-path

# 安装项目依赖库
pip install -r requirements.txt
```

- whl文件是神？如何安装whl文件？
```
# whl格式本质上是一个压缩包，里面包含了py文件，以及经过编译的pyd文件
# 使得可以在不具备编译环境的情况下，选择合适自己的python环境进行安装
# 安装方法很简单，进入命令行输入
pip install xxxx.whl
# 或者如果是升级
pip install -U xxxx.whl
```

- 关于deepcopy：
```
在使用selenium做业务处理的时候，遇到selenium的webdirver对象无法deepcopy
```

- 生成list
```
[x for x in range(1, 1000)]
```

- list拆分
```
a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

a[x:y:z]

# x: 开始索引,默认0.可以省略,即a[:y:z]
# y: 结束索引,默认最后一个.可以省略,即啊a[x::z]
# z: 步长,如果z<0,逆向拆分
```

- 拆开dict传递参数: 在sqlachemy中add很有用
```
a = {
    'b': 'b',
    'c': 'c'
}
def d(b, c):
    pass

print(d(**a))
```

- 将字典字符串转为字典
```
可以使用json来转：字典字符串的键值必须是双引号;
可以使用eval：存在安全性问题,可能将输入的字符串作为系统命令执行;
ast.literal_eval()
```
