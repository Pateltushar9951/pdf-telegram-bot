# 🤖 PDF Telegram Bot

A simple Telegram bot that converts images into a single PDF file within seconds.
Users can send one or multiple images, and the bot automatically processes and returns a downloadable PDF.

---

## 🚀 Features

* 🖼️ Convert images to PDF instantly
* ⚡ Fast and automated processing
* 📂 Supports multiple images in one PDF
* 🤖 Easy interaction via Telegram
* 🔄 Efficient media handling

---

## 🛠️ Tech Stack

* Python
* Telegram Bot API
* Pillow (Image Processing)
* PyPDF / ReportLab (PDF Generation)

---

## 📁 Project Structure

```bash
pdf-telegram-bot/
│
├── bot.py              # Main bot logic
├── requirements.txt    # Dependencies
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Pateltushar9951/pdf-telegram-bot.git
cd pdf-telegram-bot
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure Bot Token

Create a `.env` file or add directly in code:

```env
BOT_TOKEN=your_telegram_bot_token
```

---

### 4️⃣ Run the Bot

```bash
python bot.py
```

---

## 🤖 How It Works

1. User sends images to the bot
2. Bot receives and processes images
3. Images are converted into a single PDF
4. PDF is sent back to the user

---

## 📦 Requirements

* Python 3.x
* Telegram Bot Token (via BotFather)

---

## 📌 Future Improvements

* Add file size optimization
* Support for document formats (DOCX → PDF)
* User session handling for better grouping
* Cloud storage integration

---

## 👨‍💻 Author

**Tushar Patel**
Backend Developer
