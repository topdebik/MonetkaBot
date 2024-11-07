# Monetka Bot
MonetkaBot - a Telegram bot, that implements some fun things  
Interacts with user/users on Russian

## Functions
/help - prints help message  
/monetka - throws a coin  
/horoscope - fetches horoscope from VK wall (https://vk.com/astrogks) and filters only needed pictures using OCR

## Dependencies
Python libraries - `aiohttp`, `pyTelegramBotAPI`, `vk`, `pytesseract`, `pillow`  
Binaries - `tesseract`

## Installation
### Install Python dependencies
```shell
$ pip install aiohttp pyTelegramBotAPI vk pytesseract pillow
```

### Install binaries (Linux, Debian based)
```shell
$ sudo apt install tesseract-ocr tesseract-ocr-rus
```

### Install binaries (Windows)
1. Download installer binary from https://github.com/UB-Mannheim/tesseract/wiki
1. During installation, enable installing Russian recognition model
1. After installation add installation directory to PATH