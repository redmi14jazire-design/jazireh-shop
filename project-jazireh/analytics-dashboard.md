# Analytics Dashboard — فروشگاه ساعت جزیره

## راهنمای راه‌اندازی Google Data Studio (Looker Studio)

### گام ۱: آماده‌سازی منبع داده
1. Google Sheets رو باز کن
2. از برگه Dashboard دیتا برداشت می‌کنیم
3. File → Share → Publish to web → برگه Dashboard رو انتخاب کن

### گام ۲: ساخت گزارش در Looker Studio
1. برو به <https://lookerstudio.google.com>
2. Create → Data Source → Google Sheets
3. شیت فروشگاه رو انتخاب کن
4. برگه Sales رو به عنوان منبع اصلی انتخاب کن
5. یک Report جدید بساز

---

## نمودارهای پیشنهادی

### ۱. کارت‌های KPI (بالای صفحه)
| شاخص | منبع |
|-------|------|
| فروش امروز | `SUM(Sales!J:J) WHERE تاریخ = TODAY()` |
| فروش این ماه | `SUM(Sales!J:J) WHERE ماه = این ماه` |
| تعداد سفارشات | `COUNT(Sales!A:A)` |
| میانگین سبد خرید | `AVG(Sales!J:J)` |

### ۲. نمودار فروش روزانه (Line Chart)
- **محور X:** تاریخ (Sales!B)
- **محور Y:** مبلغ نهایی (Sales!J)
- **بازه:** ۳۰ روز اخیر

### ۳. نمودار محصولات پرفروش (Bar Chart)
- **محور X:** نام محصول (VLOOKUP از Products)
- **محور Y:** تعداد فروش (SUM Sales!E)

### ۴. نمودار وضعیت سفارشات (Pie Chart)
- **دسته:** وضعیت (Sales!L)
- **مقدار:** تعداد

### ۵. نمودار فروش هفتگی (Column Chart)
- **محور X:** هفته
- **محور Y:** مجموع فروش
- **روند:** خط میانگین متحرک

---

## فرمول‌های Google Sheets برای برگه Dashboard

```
A1: شاخص
B1: مقدار

A2: 📅 فروش امروز
B2: =SUMIFS(Sales!J:J, Sales!B:B, TODAY())

A3: 📆 فروش دیروز
B3: =SUMIFS(Sales!J:J, Sales!B:B, TODAY()-1)

A4: 📊 فروش این هفته
B4: =SUMIFS(Sales!J:J, Sales!B:B, ">="&TODAY()-WEEKDAY(TODAY(),2)+1, Sales!B:B, "<="&TODAY())

A5: 📅 فروش این ماه
B5: =SUMIFS(Sales!J:J, Sales!B:B, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1), Sales!B:B, "<="&TODAY())

A6: 💰 سود این ماه
B6: =SUMIFS(Sales!K:K, Sales!B:B, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1), Sales!B:B, "<="&TODAY())

A7: 📦 تعداد سفارشات امروز
B7: =COUNTIFS(Sales!B:B, TODAY())

A8: 📦 تعداد سفارشات این ماه
B8: =COUNTIFS(Sales!B:B, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1), Sales!B:B, "<="&TODAY())

A9: 👤 تعداد مشتریان جدید این ماه
B9: =COUNTIFS(Customers!H:H, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1), Customers!H:H, "<="&TODAY())

A10: 👥 کل مشتریان
B10: =COUNTA(Customers!A:A)-1

A11: 💵 میانگین ارزش سفارش
B11: =IF(B8>0, B4/B8, 0)

A12: 🏷️ محصول پرفروش ماه
B12: =INDEX(Products!B:B, MATCH(MAX(Sales!E:E), Sales!E:E, 0))

A13: ⚠️ محصولات رو به اتمام
B13: =COUNTIFS(Products!F:F, ">"&0, Products!F:F, "<="&Products!G:G)
```

---

## هشدارهای خودکار (Conditional Formatting)

### محصولات رو به اتمام
- برگه Products → Format → Conditional formatting
- Range: F2:F100
- Rule: Less than or equal to `=G2`
- Style: Red background

### سفارشات پردازش نشده (> ۲۴ ساعت)
- برگه Sales
- Range: L2:L100
- Rule: Text contains "در انتظار" AND date difference > ۱
- Style: Yellow background

---

## گزارش هفتگی خودکار

برای ارسال خودکار گزارش هفتگی به تلگرام، این کد رو به Google Apps Script اضافه کن:

```javascript
function sendWeeklyReport() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const dashboard = sheet.getSheetByName('Dashboard');
  
  const weeklySales = dashboard.getRange('B4').getValue();
  const monthlySales = dashboard.getRange('B5').getValue();
  const profit = dashboard.getRange('B6').getValue();
  const orderCount = dashboard.getRange('B8').getValue();
  
  const message = `
📊 گزارش هفتگی فروشگاه جزیره
━━━━━━━━━━━━━━━━
💰 فروش این هفته: ${formatPrice(weeklySales)} تومان
📅 فروش این ماه: ${formatPrice(monthlySales)} تومان
💵 سود این ماه: ${formatPrice(profit)} تومان
📦 سفارشات ماه: ${orderCount} عدد
━━━━━━━━━━━━━━━━
  `;
  
  // ارسال به تلگرام
  const botToken = 'YOUR_BOT_TOKEN';
  const chatId = 'ADMIN_CHAT_ID';
  UrlFetchApp.fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
    method: 'post',
    payload: { chat_id: chatId, text: message, parse_mode: 'Markdown' }
  });
}

function formatPrice(price) {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
```

زمان‌بندی: Edit → Current project's triggers → Add trigger → `sendWeeklyReport` → Time-driven → Week timer → Friday 21:00
