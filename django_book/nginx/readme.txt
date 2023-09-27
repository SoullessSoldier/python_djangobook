В обычной консоли
start nginx
или
sudo systemctl start nginx

Статус
tasklist /fi "imagename eq nginx.exe"
или
sudo systemctl status nginx

Перезагрузить
nginx -s reload
или
sudo systemctl reload nginx

Остановить
nginx -s quit
или
sudo systemctl stop nginx