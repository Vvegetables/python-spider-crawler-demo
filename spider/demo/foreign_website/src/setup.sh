#!/usr/bin/env bash

# 如何使用
# sudo -E bash -x setup_development.sh

# ${source_root} 是代码所在目录
source_root='/root/web'



sudo rm -f /etc/nginx/sites-enabled/*
sudo rm -f /etc/nginx/sites-available/*

# 建立一个软连接
sudo ln -s -f ${source_root}/web.conf /etc/supervisor/conf.d/web.conf
# 不要再 sites-available 里面放任何东西
sudo ln -s -f ${source_root}/web.nginx /etc/nginx/sites-enabled/web

# 设置文件夹权限给 nginx 用
sudo chmod o+xr /root
sudo chmod -R o+xr ${source_root}

sudo service supervisor restart
sudo service nginx restart

echo "setup development environemtn success"
