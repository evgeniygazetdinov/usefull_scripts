#!/bin/bash

# Проверяем, установлен ли Ruff
if ! command -v ruff &> /dev/null; then
    echo "Ошибка: Ruff не установлен. Установите его через:"
    echo "  pipx install ruff  # Рекомендуемый способ"
    echo "или"
    echo "  sudo apt install ruff  # Через системный пакет"
    exit 1
fi

# Получаем список изменённых .py файлов (staged + unstaged)
CHANGED_FILES=$(git status --porcelain | awk '{print $2}' | grep '\.py$')

if [ -z "$CHANGED_FILES" ]; then
    echo "Нет изменённых .py файлов для проверки"
    exit 0
fi

# Группируем файлы для обработки
echo -e "Файлы для обработки:\n$CHANGED_FILES" | sed 's/^/  - /'

# Временная переменная для хранения файлов
TMP_FILELIST=$(mktemp)
echo "$CHANGED_FILES" > "$TMP_FILELIST"

# Запускаем Ruff на группе файлов
echo -e "\nЗапуск Ruff check --fix..."
xargs -a "$TMP_FILELIST" ruff check --fix --silent

echo -e "\nЗапуск Ruff format..."
xargs -a "$TMP_FILELIST" ruff format --silent

# Удаляем временный файл
rm "$TMP_FILELIST"

echo -e "\nОбработка завершена. Проверьте изменения:"
echo "  git diff"
echo "  git status"
