# tutorial実行に際して
 
## world.draw()
ubuntu（WSL）でGUI表示ができないので[設定](https://qiita.com/nishiys/items/3b8c1670891f745c5a81)  
```
sudo apt install libxkbcommon-x11-0

sudo apt install python-tk python3-tk tk-dev

export DISPLAY=localhost:0.0
```  

pyenv使ってて[tkinterが認識されない](http://dragstar.hatenablog.com/entry/2016/09/23/110714)  
```
pip freeze > pip.txt
pyenv versions
pyenv uninstall 3.7.4
sudo apt install python-tk tk-dev
pyenv install 3.7.4
pip install -r pip.txt
```  
