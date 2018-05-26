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

# 安装项目依赖库
pip install -r requirements.txt
```

- 关于deepcopy：
```
在使用selenium做业务处理的时候，遇到selenium的webdirver对象无法deepcopy
```


