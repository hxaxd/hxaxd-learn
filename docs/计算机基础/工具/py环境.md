## python
mac自带python,但是一定要自己安装,否则pip安装的包会因为权限用不了

记得alias python与pip

其它系统正常安装即可,win注意加入环境变量
```shell
brew install python

pip install <package> #下载包

pip install --upgrade <package>  # 升级软件包

pip freeze # 查看已安装的内容

pip uninstall <package>  # 卸载包

export PATH=${PATH}:/opt/homebrew/bin/python3
alias python="/opt/homebrew/bin/python3"
alias pip="/opt/homebrew/bin/pip3"

```
## IDE与虚拟环境
推荐使用PyCharm,教育免费  
在py编程中,虚拟环境无疑是我们要关注的,py原生的虚拟环境工具venv足够使用,但如果目的是使用包进行科学研究,第三方的虚拟环境工具要更加易用

不过pycharm支持虚拟环境的快速切换等操作,因此对我足够使用
```bash
python -m venv dir #建立
source ENV_DIR/bin/activate #激活
.\ENV_DIR\Scripts\activate #win激活
deactivate #退出
# 在虚拟环境当中的pip一切如常,会自动下载本环境
```
以上操作pycharm也都可以图形化

不过觉得还是不够重的话,那么conda就是你的选择
