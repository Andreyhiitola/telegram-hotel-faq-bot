#!/bin/bash

# Загружаем переменные из .env
if [ -f .env ]; then
  export $(cat .env | xargs)
else
  echo "Ошибка: файл .env не найден"
  exit 1
fi

# Переменные из .env
REPO_PATH=/root/telegram-hotel-faq-bot


cd "$REPO_PATH" || exit 1

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

# Отправляем изменения на сервер с переменными из .env
git push https://$GIT_USERNAME:$GIT_PASSWORD@github.com/Andreyhiitola/telegram-hotel-faq-bot

echo "Изменения отправлены."
