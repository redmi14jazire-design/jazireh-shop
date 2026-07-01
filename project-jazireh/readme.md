# راهنمای دیپلوی — فروشگاه جزیره

## ۱. دیپلوی سایت روی Netlify (رایگان)

### روش A: Drag & Drop (ساده‌ترین)
1. برو به <https://app.netlify.com>
2. با گیت‌هاب یا ایمیل ثبت‌نام کن
3. پوشه `website` رو بکش و رها کن توی Netlify
4. یه دامنه رایگان می‌گیری مثل `jazireh.netlify.app`

### روش B: اتصال به گیت‌هاب (پیشنهادی — آپدیت خودکار)
1. پروژه رو روی گیت‌هاب push کن
2. توی Netlify: **Add new site → Import an existing project → GitHub**
3. مخزن رو انتخاب کن
4. توی تنظیمات:
   - Base directory: `project-jazireh/website`
   - Build command: (خالی بذار — سایت استاتیکه)
   - Publish directory: `project-jazireh/website`
5. **Deploy site**

### سفارشی‌سازی دامنه
- توی Netlify برو به **Domain settings**
- می‌تونی دامنه `.ir` خودت رو وصل کنی
- یا از Subdomain رایگان Netlify استفاده کنی

---

## ۲. دیپلوی ربات تلگرام

### ۲.۱ ساختن ربات در BotFather
1. توی تلگرام برو به [@BotFather](https://t.me/BotFather)
2. دستور `/newbot` رو بفرست
3. اسم ربات رو انتخاب کن (مثلاً "فروشگاه جزیره")
4. username ربات رو انتخاب کن (مثلاً `JazirehShopBot`)
5. توکن رو دریافت می‌کنی — توی فایل `bot.py` در خط `BOT_TOKEN` جایگزین کن

### ۲.۲ تنظیم منوی ربات
توی BotFather دستور `/setcommands` رو بفرست و اینا رو paste کن:
```
start - 🏠 منوی اصلی
help - ❓ راهنما
```

### ۲.۳ اجرای ربات (سرور)

#### گزینه ۱: Railway (رایگان — ۵۰۰ ساعت در ماه)
1. برو به <https://railway.app>
2. با گیت‌هاب ثبت‌نام کن
3. **New Project → Deploy from GitHub repo**
4. فایل‌های مورد نیاز توی مخزن:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`: `worker: python bot.py`
5. محیط متغیرها رو تنظیم کن:
   - `BOT_TOKEN` = توکن ربات
   - `ADMIN_CHAT_ID` = آیدی عددی خودت
6. Deploy

#### گزینه ۲: PythonAnywhere (رایگان)
1. ثبت‌نام در <https://pythonanywhere.com>
2. تب **Files** → آپلود `bot.py` و `requirements.txt`
3. تب **Consoles** → Bash → اجرا:
   ```
   pip install -r requirements.txt
   python bot.py
   ```

#### گزینه ۳: سرور شخصی / VPS
```bash
# نصب پکیج‌ها
pip install -r requirements.txt

# اجرا با nohup (پس‌زمینه)
nohup python bot.py > bot.log 2>&1 &

# یا با systemd (پیشنهادی)
sudo nano /etc/systemd/system/jazireh-bot.service
```

---

## ۳. اتصال ربات به Google Sheets

### روش: Google Apps Script

1. شیت گوگل رو باز کن
2. منوی **Extensions → Apps Script**
3. کد `google-sheets-template.md` (بخش پایینی) رو paste کن
4. **Deploy → New deployment → Web app**
5. تنظیمات:
   - Execute as: **Me**
   - Who has access: **Anyone**
6. آدرس Web App رو کپی کن
7. توی `bot.py` متغیر `SHEET_WEBAPP_URL` رو با این آدرس جایگزین کن

### روش: Google Sheets API (پیشرفته‌تر)

1. [Google Cloud Console](https://console.cloud.google.com)
2. پروژه جدید → Enable **Google Sheets API**
3. **Credentials → Create Service Account**
4. کلید JSON رو دانلود کن
5. فایل JSON رو کنار `bot.py` بذار
6. آدرس ایمیل service account رو توی شیت Share کن (با دسترسی Editor)

```python
# جایگزینی توی bot.py:
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('YOUR_SHEET_ID').sheet1
```

---

## ۴. تنظیم عکس‌ها

۱. عکس‌ها رو در پوشه `project-jazireh/website/images/` بذار
۲. نام‌گذاری: `product-001.jpg`, `product-002.jpg`, ...
۳. حذف پس‌زمینه با [Remove.bg](https://remove.bg) (رایگان برای ۵۰ عکس)
۴. داخل `index.html` ، لیست `products` رو پر کن
