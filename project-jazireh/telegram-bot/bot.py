#!/usr/bin/env python3
"""
ربات تلگرام فروشگاه جزیره
- منوی اصلی با دکمه‌های شیشه‌ای
- دریافت قیمت و موجودی از Google Sheets
- ثبت سفارش در Google Sheets
- پشتیبانی ۲۴ ساعته خودکار

نیازمندی‌ها:
pip install python-telegram-bot gspread oauth2client
"""

import os
import json
import logging
import subprocess
import httpx
from pathlib import Path
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ═══════════════════════════════════════
#  تنظیمات - این بخش رو تغییر بده
# ═══════════════════════════════════════

# توکن ربات تلگرام (از BotFather بگیر)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8702077052:AAHX9uqfkYViH3OdhsdDlN1QFpuqTO1lq84")

# پروکسی برای ایران (در صورت نیاز)
# مثال: http://127.0.0.1:10808 یا socks5://127.0.0.1:10808
PROXY_URL = os.getenv("PROXY_URL", "")

# مسیر workspace (برای آپلود عکس و push به گیت)
WORKSPACE_DIR = Path(__file__).resolve().parents[2]
WEBSITE_IMAGES = WORKSPACE_DIR / "project-jazireh" / "website" / "images"
DOCS_IMAGES = WORKSPACE_DIR / "docs" / "images"

# آیدی عددی ادمین (برای دریافت نوتیفیکیشن سفارش‌ها)
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "123456789")

# آدرس Web App برای Google Apps Script (بعد از Deploy می‌گیری)
# یا می‌تونی مستقیم از Google Sheets API استفاده کنی
SHEET_WEBAPP_URL = os.getenv("SHEET_WEBAPP_URL", "")

# ═══════════════════════════════════════
#  اطلاعات محصولات (کَش محلی)
#  در نسخه نهایی از Google Sheets می‌خونه
# ═══════════════════════════════════════

PRODUCTS = [
    {"code": "PRD-001", "name": "ساعت مردانه — مشکی کلاسیک بند استیل نقره‌ای", "price": 2000000, "stock": 15, "category": "ساعت مردانه", "description": "صفحه مشکی کلاسیک، بند استیل نقره‌ای باکیفیت، شیشه Mineral Crystal، قطر ۴۰mm. جعبه اصلی باکیفیت + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-002", "name": "ساعت مردانه — صفحه آبی بند استیل نقره‌ای", "price": 2000000, "stock": 12, "category": "ساعت مردانه", "description": "صفحه آبی جذاب، بند استیل نقره‌ای براق، تاریخ‌شمار، قطر ۴۰mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-003", "name": "ساعت مردانه — سفید مینیمال بند استیل نقره‌ای", "price": 2000000, "stock": 18, "category": "ساعت مردانه", "description": "صفحه سفید مینیمال، بند استیل نقره‌ای شیک، قطر ۴۰mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-004", "name": "ساعت مردانه کرونوگراف — مشکی بند استیل نقره‌ای", "price": 2000000, "stock": 8, "category": "ساعت مردانه", "description": "سه شمارنده فرعی، بند استیل نقره‌ای، کرنومتر، قطر ۴۲mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-005", "name": "ساعت مردانه — صفحه سبز بند استیل نقره‌ای", "price": 2000000, "stock": 10, "category": "ساعت مردانه", "description": "صفحه سبز منحصربه‌فرد، بند استیل نقره‌ای، تاریخ‌شمار، قطر ۴۰mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-006", "name": "ساعت مردانه — صفحه طوسی بند استیل نقره‌ای", "price": 2000000, "stock": 14, "category": "ساعت مردانه", "description": "صفحه طوسی مدرن، بند استیل نقره‌ای، طراحی امروزی، قطر ۴۰mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-007", "name": "ساعت مردانه — صفحه قهوه‌ای بند استیل نقره‌ای", "price": 2000000, "stock": 11, "category": "ساعت مردانه", "description": "صفحه قهوه‌ایی گرم، بند استیل نقره‌ای، تاریخ‌شمار، قطر ۴۰mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-008", "name": "ساعت مردانه اسکلتون — صفحه باز بند استیل نقره‌ای", "price": 2000000, "stock": 7, "category": "ساعت مردانه", "description": "صفحه Skeleton باز با چرخ‌دنده‌های نمایان، بند استیل نقره‌ای، قطر ۴۲mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-009", "name": "ساعت مردانه نگین‌دار — مشکی بند استیل نقره‌ای", "price": 2000000, "stock": 9, "category": "ساعت مردانه", "description": "شاخص‌های نگین‌دار، صفحه مشکی لوکس، بند استیل نقره‌ای، قطر ۴۰mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
    {"code": "PRD-010", "name": "ساعت مردانه روز-تاریخ — مشکی بند استیل نقره‌ای", "price": 2000000, "stock": 20, "category": "ساعت مردانه", "description": "نمایش روز و تاریخ کامل، صفحه مشکی، بند استیل نقره‌ای، قطر ۴۰mm. جعبه اصلی + گارانتی باتری ۱۲ ماهه"},
]

# ═══════════════════════════════════════
#  پیام‌های ثابت
# ═══════════════════════════════════════

ABOUT_TEXT = """
⌚ *فروشگاه ساعت جزیره*

ساعت مچی مردانه با بهترین کیفیت
💎 تمام مدل‌ها فقط ۲ میلیون تومان
🔩 بند استیل نقره‌ای باکیفیت
🎁 جعبه اصلی شکیل + گارانتی باتری ۱۲ ماهه
📍 ارسال فوری به سراسر ایران
🔄 ضمانت ۷ روز بازگشت
📞 پشتیبانی همه روزه ۹ صبح تا ۹ شب
"""

HELP_TEXT = """
🤖 *راهنمای ربات*

• 📋 *لیست قیمت* — مشاهده همه محصولات با قیمت
• 🔍 *استعلام قیمت* — قیمت لحظه‌ای هر محصول
• 🛒 *ثبت سفارش* — سفارش مستقیم از طریق ربات
• 📞 *تماس با ما* — ارتباط با پشتیبانی
• ℹ️ *درباره ما* — اطلاعات فروشگاه

برای شروع از منوی زیر استفاده کنید 👇
"""

# ═══════════════════════════════════════
#  توابع Google Sheets
# ═══════════════════════════════════════

def get_products_from_sheet():
    """
    خواندن محصولات از Google Sheets
    اگر SHEET_WEBAPP_URL تنظیم نشده، از کش محلی PRODUCTS استفاده می‌کنه
    """
    if not SHEET_WEBAPP_URL:
        return PRODUCTS
    
    try:
        import requests
        resp = requests.get(SHEET_WEBAPP_URL, params={"action": "getProducts"}, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        logging.error(f"Sheet read error: {e}")
    
    return PRODUCTS


def get_product(product_code):
    """دریافت اطلاعات یک محصول با کد"""
    products = get_products_from_sheet()
    for p in products:
        if p.get("code") == product_code:
            return p
    return None


def register_sale(customer_info, product_code, quantity):
    """ثبت فروش در Google Sheets"""
    if not SHEET_WEBAPP_URL:
        logging.warning("SHEET_WEBAPP_URL not set — sale not recorded")
        return False
    
    try:
        import requests
        data = {
            "action": "addSale",
            "customer": customer_info,
            "productCode": product_code,
            "quantity": quantity
        }
        resp = requests.post(SHEET_WEBAPP_URL, json=data, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        logging.error(f"Sheet write error: {e}")
        return False


# ═══════════════════════════════════════
#  توابع کمکی
# ═══════════════════════════════════════

def format_price(price):
    """فرمت قیمت به صورت ۱,۲۵۰,۰۰۰"""
    return f"{int(price):,}"


def build_main_menu():
    """ساخت منوی اصلی"""
    keyboard = [
        [InlineKeyboardButton("📋 لیست قیمت", callback_data="price_list")],
        [
            InlineKeyboardButton("🛒 ثبت سفارش", callback_data="order"),
            InlineKeyboardButton("🔍 استعلام قیمت", callback_data="check_price"),
        ],
        [
            InlineKeyboardButton("ℹ️ درباره ما", callback_data="about"),
            InlineKeyboardButton("📞 تماس با ما", callback_data="contact"),
        ],
        [InlineKeyboardButton("📸 آپلود عکس محصول", callback_data="upload_info")],
        [InlineKeyboardButton("❓ راهنما", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_category_menu(products):
    """ساخت منوی دسته‌بندی محصولات"""
    categories = {}
    for p in products:
        cat = p.get("category", "عمومی")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    keyboard = []
    for cat_name, cat_products in categories.items():
        keyboard.append([InlineKeyboardButton(
            f"📂 {cat_name} ({len(cat_products)} محصول)",
            callback_data=f"cat_{cat_name}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


def build_product_list_keyboard(products):
    """ساخت لیست محصولات به صورت دکمه‌ای"""
    keyboard = []
    for p in products[:20]:  # حداکثر ۲۰ محصول در یک صفحه
        stock_status = "✅" if p.get("stock", 0) > 0 else "❌"
        keyboard.append([InlineKeyboardButton(
            f"{stock_status} {p['name']} — {format_price(p['price'])} تومان",
            callback_data=f"prod_{p['code']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


def build_product_detail_keyboard(product_code):
    """ساخت دکمه‌های جزئیات محصول"""
    keyboard = [
        [InlineKeyboardButton("🛒 سفارش این محصول", callback_data=f"buy_{product_code}")],
        [InlineKeyboardButton("🔙 لیست محصولات", callback_data="price_list")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ═══════════════════════════════════════
#  هندلرهای ربات
# ═══════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user = update.effective_user
    welcome = f"""
👋 سلام {user.first_name} عزیز!

به ربات *فروشگاه جزیره* خوش اومدی 🏪

اینجا می‌تونی:
• 📋 لیست محصولات رو ببینی
• 💰 قیمت‌ها رو استعلام کنی
• 🛒 سفارش ثبت کنی
• 📞 با پشتیبانی در ارتباط باشی
"""
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=build_main_menu()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش دکمه‌های شیشه‌ای"""
    query = update.callback_query
    await query.answer()
    data = query.data

    products = get_products_from_sheet()

    # ── منوی اصلی ──
    if data == "main_menu":
        await query.edit_message_text(
            "🏪 *منوی اصلی*\nلطفاً یکی از گزینه‌ها رو انتخاب کن:",
            parse_mode="Markdown",
            reply_markup=build_main_menu()
        )

    # ── لیست قیمت (دسته‌بندی) ──
    elif data == "price_list":
        if not products:
            await query.edit_message_text(
                "⚠️ هنوز محصولی ثبت نشده.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
                ]])
            )
            return
        
        await query.edit_message_text(
            "📂 *دسته‌بندی محصولات:*",
            parse_mode="Markdown",
            reply_markup=build_category_menu(products)
        )

    # ── نمایش محصولات یک دسته ──
    elif data.startswith("cat_"):
        cat_name = data[4:]
        cat_products = [p for p in products if p.get("category", "عمومی") == cat_name]
        await query.edit_message_text(
            f"📂 *{cat_name}*\n\nبرای مشاهده جزئیات روی محصول کلیک کن:",
            parse_mode="Markdown",
            reply_markup=build_product_list_keyboard(cat_products)
        )

    # ── جزئیات محصول ──
    elif data.startswith("prod_"):
        code = data[5:]
        product = get_product(code)
        if not product:
            await query.answer("محصول یافت نشد ❌")
            return

        stock_text = f"✅ موجود ({product.get('stock', 0)} عدد)" if product.get('stock', 0) > 0 else "❌ ناموجود"
        
        text = f"""
🛍️ *{product['name']}*

📂 دسته: {product.get('category', 'عمومی')}
💰 قیمت: *{format_price(product['price'])}* تومان
📦 وضعیت: {stock_text}

📝 *توضیحات:*
{product.get('description', 'توضیحی ثبت نشده')}

🆔 کد محصول: `{product['code']}`
"""
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=build_product_detail_keyboard(code)
        )

    # ── شروع فرآیند خرید ──
    elif data.startswith("buy_"):
        code = data[4:]
        product = get_product(code)
        if not product:
            await query.answer("محصول یافت نشد ❌")
            return

        if product.get("stock", 0) <= 0:
            await query.answer("این محصول ناموجود است ⚠️")
            return

        context.user_data["buying_product"] = code
        context.user_data["buying_step"] = "quantity"

        await query.edit_message_text(
            f"🛒 *سفارش محصول*\n\n"
            f"محصول: *{product['name']}*\n"
            f"قیمت هر عدد: *{format_price(product['price'])}* تومان\n\n"
            f"📝 لطفاً *تعداد مورد نظر* رو به صورت عدد وارد کن:\n"
            f"(مثال: 2)",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 انصراف", callback_data="main_menu")
            ]])
        )

    # ── استعلام قیمت ──
    elif data == "check_price":
        await query.edit_message_text(
            "🔍 *استعلام قیمت*\n\n"
            "لطفاً *کد محصول* یا *نام محصول* رو وارد کن:\n"
            "(مثال: PRD-001 یا نام محصول)",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
            ]])
        )
        context.user_data["checking_price"] = True

    # ── ثبت سفارش (عمومی) ──
    elif data == "order":
        if not products:
            await query.edit_message_text(
                "⚠️ محصولی برای سفارش موجود نیست.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
                ]])
            )
            return

        await query.edit_message_text(
            "🛒 *ثبت سفارش*\n\n"
            "لطفاً *کد محصول* مورد نظر رو وارد کن:\n"
            "می‌تونی از لیست قیمت کد محصول رو پیدا کنی 📋",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📋 مشاهده لیست قیمت", callback_data="price_list"),
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu"),
            ]])
        )
        context.user_data["ordering"] = True

    # ── درباره ما ──
    elif data == "about":
        await query.edit_message_text(
            ABOUT_TEXT,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
            ]])
        )

    # ── تماس با ما ──
    elif data == "contact":
        await query.edit_message_text(
            "📞 *راه‌های ارتباطی*\n\n"
            "👤 پشتیبانی: @YOUR_SUPPORT_USERNAME\n"
            "📱 تلفن: ۰۹XX-XXX-XXXX\n"
            "📷 اینستاگرام: @YOUR_INSTAGRAM\n\n"
            "⏰ ساعت پاسخگویی: ۹ صبح تا ۹ شب",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
            ]])
        )

    # ── راهنمای آپلود ──
    elif data == "upload_info":
        products_list = "\n".join([f"`{p['code']}` — {p['name']}" for p in products])
        await query.edit_message_text(
            f"📸 *آپلود عکس محصول*\n\n"
            f"برای آپلود عکس، مراحل زیر رو انجام بده:\n\n"
            f"۱. عکس رو با دوربین یا گالری انتخاب کن\n"
            f"۲. توی Caption عکس، *کد محصول* رو بنویس\n"
            f"۳. دکمه ارسال رو بزن\n\n"
            f"🎯 *لیست کد محصولات:*\n{products_list}\n\n"
            f"⚠️ عکس باید مربع (۱:۱) باشه و پس‌زمینه حذف شده باشه.\n"
            f"📏 سایز پیشنهادی: ۸۰۰×۸۰۰ پیکسل",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
            ]])
        )

    # ── راهنما ──
    elif data == "help":
        await query.edit_message_text(
            HELP_TEXT,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
            ]])
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام‌های متنی (ثبت سفارش، استعلام قیمت)"""
    text = update.message.text.strip()
    products = get_products_from_sheet()

    # ── مرحله تعداد در خرید ──
    if context.user_data.get("buying_step") == "quantity":
        try:
            qty = int(text)
            if qty <= 0:
                raise ValueError
        except ValueError:
            await update.message.reply_text(
                "⚠️ لطفاً یک *عدد صحیح مثبت* وارد کن.",
                parse_mode="Markdown"
            )
            return

        product_code = context.user_data["buying_product"]
        product = get_product(product_code)

        if not product or product.get("stock", 0) < qty:
            await update.message.reply_text(
                f"⚠️ موجودی کافی نیست. موجودی فعلی: {product.get('stock', 0)} عدد",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
                ]])
            )
            context.user_data.clear()
            return

        context.user_data["buying_qty"] = qty
        context.user_data["buying_step"] = "confirm"

        total = product["price"] * qty

        await update.message.reply_text(
            f"📋 *تأیید سفارش*\n\n"
            f"محصول: *{product['name']}*\n"
            f"تعداد: *{qty}* عدد\n"
            f"قیمت واحد: *{format_price(product['price'])}* تومان\n"
            f"💰 *مبلغ کل: {format_price(total)}* تومان\n\n"
            f"آیا سفارش رو تأیید می‌کنی؟",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ تأیید و ثبت", callback_data="confirm_order"),
                    InlineKeyboardButton("❌ انصراف", callback_data="main_menu"),
                ]
            ])
        )

    # ── استعلام قیمت ──
    elif context.user_data.get("checking_price"):
        # جستجو بر اساس کد یا نام
        found = None
        for p in products:
            if p["code"].upper() == text.upper() or text in p["name"]:
                found = p
                break

        if found:
            stock_status = "✅ موجود" if found.get("stock", 0) > 0 else "❌ ناموجود"
            await update.message.reply_text(
                f"🔍 *نتیجه استعلام*\n\n"
                f"🛍️ {found['name']}\n"
                f"💰 قیمت: *{format_price(found['price'])}* تومان\n"
                f"📦 موجودی: {stock_status} ({found.get('stock', 0)} عدد)\n"
                f"🆔 کد: `{found['code']}`",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🛒 سفارش", callback_data=f"buy_{found['code']}"),
                    InlineKeyboardButton("🔙 منو", callback_data="main_menu"),
                ]])
            )
        else:
            await update.message.reply_text(
                "❌ محصولی با این مشخصات پیدا نشد.\n"
                "لطفاً دوباره تلاش کن یا از لیست قیمت استفاده کن 📋",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📋 لیست قیمت", callback_data="price_list"),
                    InlineKeyboardButton("🔙 منو", callback_data="main_menu"),
                ]])
            )

        context.user_data.pop("checking_price", None)

    # ── ثبت سفارش (دریافت کد محصول) ──
    elif context.user_data.get("ordering"):
        product = None
        for p in products:
            if p["code"].upper() == text.upper() or p["name"] == text:
                product = p
                break

        if not product:
            await update.message.reply_text(
                "❌ کد محصول نامعتبره. دوباره تلاش کن.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📋 لیست قیمت", callback_data="price_list"),
                    InlineKeyboardButton("🔙 منو", callback_data="main_menu"),
                ]])
            )
            return

        if product.get("stock", 0) <= 0:
            await update.message.reply_text(
                "⚠️ این محصول در حال حاضر ناموجود است.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")
                ]])
            )
            context.user_data.clear()
            return

        context.user_data["buying_product"] = product["code"]
        context.user_data["buying_step"] = "quantity"
        context.user_data.pop("ordering", None)

        await update.message.reply_text(
            f"محصول *{product['name']}* انتخاب شد ✅\n"
            f"قیمت: *{format_price(product['price'])}* تومان\n\n"
            f"📝 حالا *تعداد* مورد نظر رو وارد کن:",
            parse_mode="Markdown"
        )

    # ── پیام عادی (بدون state) ──
    else:
        await update.message.reply_text(
            "👋 برای استفاده از ربات، از منوی زیر استفاده کن:",
            reply_markup=build_main_menu()
        )


async def confirm_order_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تأیید نهایی سفارش"""
    query = update.callback_query
    await query.answer()

    if context.user_data.get("buying_step") != "confirm":
        await query.edit_message_text(
            "⚠️ سفارش منقضی شده. لطفاً دوباره شروع کن.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")
            ]])
        )
        context.user_data.clear()
        return

    product_code = context.user_data["buying_product"]
    qty = context.user_data["buying_qty"]
    product = get_product(product_code)
    total = product["price"] * qty
    user = query.from_user

    # اطلاعات مشتری
    customer_info = {
        "username": user.username or "",
        "first_name": user.first_name,
        "last_name": user.last_name or "",
        "chat_id": user.id,
    }

    # ثبت در Google Sheets
    success = register_sale(customer_info, product_code, qty)

    # پاک کردن state
    context.user_data.clear()

    if success:
        await query.edit_message_text(
            f"✅ *سفارش با موفقیت ثبت شد!*\n\n"
            f"🛍️ {product['name']} × {qty}\n"
            f"💰 مبلغ: *{format_price(total)}* تومان\n\n"
            f"📞 همکاران ما به‌زودی برای هماهنگی ارسال باهات تماس می‌گیرن.\n\n"
            f"🙏 از اعتمادت ممنونیم!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")
            ]])
        )
    else:
        await query.edit_message_text(
            f"✅ *سفارش ثبت شد!*\n\n"
            f"🛍️ {product['name']} × {qty}\n"
            f"💰 مبلغ: *{format_price(total)}* تومان\n\n"
            f"⚠️ توجه: ثبت در سیستم با تأخیر انجام می‌شه.\n"
            f"📞 لطفاً برای قطعی کردن سفارش با پشتیبانی تماس بگیر:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📞 تماس با پشتیبانی", callback_data="contact"),
                InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu"),
            ]])
        )

    # اطلاع به ادمین
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"🔔 *سفارش جدید*\n\n"
                 f"👤 مشتری: {user.first_name} (@{user.username or 'بدون نام کاربری'})\n"
                 f"🛍️ محصول: {product['name']} ({product_code})\n"
                 f"📦 تعداد: {qty}\n"
                 f"💰 مبلغ: {format_price(total)} تومان\n"
                 f"📅 تاریخ: {datetime.now().strftime('%Y/%m/%d %H:%M')}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Admin notification failed: {e}")


# ═══════════════════════════════════════
#  هندلر آپلود عکس
# ═══════════════════════════════════════

async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /upload"""
    products = get_products_from_sheet()
    products_list = "\n".join([f"`{p['code']}` — {p['name']}" for p in products])
    await update.message.reply_text(
        f"📸 *آپلود عکس محصول*\n\n"
        f"حالا عکس رو بفرس و توی کپشن، *کد محصول* رو بنویس.\n\n"
        f"🎯 کد محصولات:\n{products_list}",
        parse_mode="Markdown"
    )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت عکس و آپلود در سایت"""
    caption = update.message.caption or ""
    caption = caption.strip().upper()
    
    # اعتبارسنجی کد محصول
    products = get_products_from_sheet()
    valid_codes = [p["code"] for p in products]
    
    if caption not in valid_codes:
        codes_list = ", ".join(valid_codes)
        await update.message.reply_text(
            f"⚠️ کد محصول نامعتبره!\n\n"
            f"کد وارد شده: `{caption or 'خالی'}`\n"
            f"کدهای معتبر: {codes_list}\n\n"
            f"لطفاً دوباره عکس رو با کد محصول درست بفرس.",
            parse_mode="Markdown"
        )
        return
    
    product = get_product(caption)
    product_name = product["name"] if product else caption
    
    await update.message.reply_text(f"⏳ در حال آپلود عکس {product_name}...")
    
    try:
        # دانلود عکس از تلگرام
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        
        # تعیین نام فایل بر اساس کد محصول
        file_num = caption.replace("PRD-", "")
        filename = f"product-{file_num}.jpg"
        
        # ایجاد پوشه‌ها در صورت نیاز
        WEBSITE_IMAGES.mkdir(parents=True, exist_ok=True)
        DOCS_IMAGES.mkdir(parents=True, exist_ok=True)
        
        # ذخیره در هر دو مسیر
        web_path = WEBSITE_IMAGES / filename
        docs_path = DOCS_IMAGES / filename
        
        web_path.write_bytes(photo_bytes)
        docs_path.write_bytes(photo_bytes)
        
        # Push به گیت‌هاب
        os.chdir(WORKSPACE_DIR)
        subprocess.run(["git", "add", str(web_path.relative_to(WORKSPACE_DIR)), str(docs_path.relative_to(WORKSPACE_DIR))], capture_output=True, timeout=30)
        subprocess.run(["git", "commit", "-m", f"📸 آپلود عکس {caption} — {product_name}"], capture_output=True, timeout=30)
        result = subprocess.run(["git", "push"], capture_output=True, timeout=60, text=True)
        
        if result.returncode == 0:
            await update.message.reply_text(
                f"✅ *عکس با موفقیت آپلود شد!*\n\n"
                f"🛍️ {product_name}\n"
                f"🆔 {caption}\n"
                f"📁 {filename}\n\n"
                f"🔗 تا ۳۰ ثانیه دیگه توی سایت آپدیت میشه\n"
                f"<https://redmi14jazire-design.github.io/jazireh-shop/>",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"✅ *عکس ذخیره شد* اما push به گیت‌هاب خطا داد.\n\n"
                f"خطا: {result.stderr[:200]}\n\n"
                f"عکس لوکال ذخیره شده — دفعه بعد push میشه.",
                parse_mode="Markdown"
            )
    
    except Exception as e:
        logging.error(f"Photo upload error: {e}")
        await update.message.reply_text(
            f"❌ خطا در آپلود عکس:\n{str(e)[:300]}\n\nلطفاً دوباره تلاش کن."
        )


# ═══════════════════════════════════════
#  اجرای ربات
# ═══════════════════════════════════════

def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ لطفاً BOT_TOKEN رو تنظیم کن!")
        print("از @BotFather توی تلگرام ربات بساز و توکن رو اینجا بذار.")
        return

    # ساخت اپلیکیشن با پشتیبانی از پروکسی
    builder = Application.builder().token(BOT_TOKEN)
    if PROXY_URL:
        print(f"🔌 استفاده از پروکسی: {PROXY_URL}")
        builder.proxy(PROXY_URL).get_updates_proxy(PROXY_URL)
    app = builder.build()

    # ثبت هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("upload", upload_command))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(?!confirm_order).*"))
    app.add_handler(CallbackQueryHandler(confirm_order_handler, pattern="^confirm_order$"))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # شروع
    print("🚀 ربات فروشگاه جزیره شروع به کار کرد...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
