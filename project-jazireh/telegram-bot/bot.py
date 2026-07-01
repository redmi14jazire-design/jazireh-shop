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
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ═══════════════════════════════════════
#  تنظیمات - این بخش رو تغییر بده
# ═══════════════════════════════════════

# توکن ربات تلگرام (از BotFather بگیر)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

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
    # {
    #     "code": "PRD-001",
    #     "name": "محصول نمونه ۱",
    #     "price": 250000,
    #     "stock": 15,
    #     "category": "دسته‌بندی",
    #     "description": "توضیح کامل و سئو شده",
    #     "image_url": "https://example.com/image.jpg"
    # },
]

# ═══════════════════════════════════════
#  پیام‌های ثابت
# ═══════════════════════════════════════

ABOUT_TEXT = """
🏪 *فروشگاه جزیره*

محصولات باکیفیت با بهترین قیمت بازار
📍 ارسال سریع به سراسر ایران
📦 بسته‌بندی حرفه‌ای و ایمن
🔄 ضمانت ۷ روز بازگشت کالا
📞 پشتیبانی ۲۴ ساعته

آدرس: (اینجا آدرس فروشگاه رو بنویس)
ساعت کاری: همه روزه ۹ صبح تا ۹ شب
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

    # ساخت اپلیکیشن
    app = Application.builder().token(BOT_TOKEN).build()

    # ثبت هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(?!confirm_order).*"))
    app.add_handler(CallbackQueryHandler(confirm_order_handler, pattern="^confirm_order$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # شروع
    print("🚀 ربات فروشگاه جزیره شروع به کار کرد...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
