App Engine приложение для кросс-постинга новостей с +Страницы GDG Omsk в другие ресурсы.

На данный момент реализована поддержка кросс-постинга в группу Вконтакте. 

Ключевой скрипт расположен по адресу http://gdgomsk-news-crossposter.appspot.com/cross_post_to_vk. При обращении к нему происходит перепост +Страница GDG Omsk --> группа вконтакте "GDG Omsk News". Каждая запись перепощивается только один раз, независимо от кол-ва вызовов скрипта. Для публикации используется аккаунт Екатерины Любимовой. 

Более подробную информации о работе скрипта можно найти в исходных кодах самого скрипта - cross_post_to_vk.py.

## Важно! ##

Перед deploy на App Engine необходимо задать секретные константы, которые по соображениям безопасности недопустимо хранить в открытом репозитарии. Все необходимые константы можно найти в документе GDG Omsk News Secrets - https://docs.google.com/document/d/11uZelaTm_T-JBwkXQPVRKDPtlQDsqWkyYoXzNBR5kn4/edit, изменить их в файле constants_secret.py и после этого можно делать deploy.

Владельцем App Engine приложения является admin@gdgomsk.org. URL для доступа к статистике и настройкам приложения - https://appengine.google.com/

## Зависимости: ##

* Google API Library for Python - https://developers.google.com/api-client-library/python/start/installation
* Vkontakte Python API Wrapper - https://github.com/kmike/vkontakte

## Полезные ссылки: ##

Google App Engine for Python:
https://developers.google.com/appengine/docs/python/gettingstartedpython27/

Google Plus API:
https://developers.google.com/+/api/

Вконтакте API:
* http://vk.com/dev
* http://vk.com/developers.php?oid=-1&p=Авторизация_сайтов - процесс получения токена (единственный вариант на данный момент)
* http://vk.com/developers.php?oid=-1&p=wall.post - API для публикации записей на стене
