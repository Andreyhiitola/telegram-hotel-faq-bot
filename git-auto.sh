#!/bin/bash

# Поднимаемся в корень репозитория (если нужно)
cd /root/telegram-hotel-faq-bot || exit 1

# Обновить локальную ветку с origin
git pull origin main

# Добавить изменения
git add .

# Запрашиваем комментарий
read -p "Введите сообщение для коммита: " commit_message

# Проверяем, что сообщение не пустое
if [ -z "$commit_message" ]; then
  echo "Сообщение коммита не может быть пустым. Отмена."
  exit 1
fi

# Выполняем коммит с введённым сообщением
git commit -m "$commit_message"

# Отправляем изменения на сервер
git push origin main

echo "Изменения отправлены."
