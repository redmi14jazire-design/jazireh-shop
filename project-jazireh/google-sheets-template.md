# ساختار Google Sheets — فروشگاه جزیره

## برگه‌ها (Sheets)

### 1. محصولات (Products)

| ستون | نوع | توضیح |
|------|-----|-------|
| A: کد محصول | TEXT | کد یکتا، مثال: PRD-001 |
| B: نام محصول | TEXT | نام کامل فارسی |
| C: دسته‌بندی | DROPDOWN | انتخاب از لیست دسته‌ها |
| D: قیمت خرید (تومان) | NUMBER | قیمت تمام‌شده |
| E: قیمت فروش (تومان) | NUMBER | قیمت مصرف‌کننده |
| F: موجودی فعلی | NUMBER | تعداد در انبار |
| G: حداقل موجودی | NUMBER | هشدار اتمام |
| H: سود هر واحد (تومان) | FORMULA | `=E2-D2` |
| I: حاشیه سود % | FORMULA | `=(E2-D2)/E2*100` - فرمت درصد |
| J: ارزش موجودی (تومان) | FORMULA | `=F2*D2` |
| K: لینک عکس | URL | آدرس عکس محصول |
| L: توضیحات SEO | TEXT | متن سئو شده |
| M: وضعیت | DROPDOWN | فعال / غیرفعال / ناموجود |
| N: تاریخ ثبت | DATE | `=TODAY()` |
| O: تعداد فروش کل | NUMBER | جمع کل فروش |

### 2. مشتریان (Customers)

| ستون | نوع | توضیح |
|------|-----|-------|
| A: کد مشتری | TEXT | CST-001 |
| B: نام مشتری | TEXT | |
| C: شماره تماس | TEXT | |
| D: آدرس | TEXT | |
| E: تلگرام | TEXT | @username |
| F: تعداد خرید | FORMULA | از برگه فروش محاسبه می‌شود |
| G: مجموع خرید (تومان) | FORMULA | از برگه فروش محاسبه می‌شود |
| H: تاریخ ثبت | DATE | `=TODAY()` |
| I: یادداشت | TEXT | |

### 3. فروش (Sales)

| ستون | نوع | توضیح |
|------|-----|-------|
| A: کد فاکتور | TEXT | INV-001 |
| B: تاریخ | DATE | |
| C: کد مشتری | DROPDOWN | از برگه مشتریان |
| D: کد محصول | DROPDOWN | از برگه محصولات |
| E: تعداد | NUMBER | |
| F: قیمت واحد (تومان) | FORMULA | `=VLOOKUP(D2,Products!A:E,5,FALSE)` |
| G: قیمت کل (تومان) | FORMULA | `=E2*F2` |
| H: هزینه ارسال (تومان) | NUMBER | |
| I: تخفیف (تومان) | NUMBER | |
| J: مبلغ نهایی (تومان) | FORMULA | `=G2+H2-I2` |
| K: سود خالص (تومان) | FORMULA | `=E2*(VLOOKUP(D2,Products!A:H,5,FALSE)-VLOOKUP(D2,Products!A:H,4,FALSE))+H2-I2` |
| L: وضعیت | DROPDOWN | در انتظار / پردازش / ارسال / تحویل / لغو |
| M: روش پرداخت | DROPDOWN | کارت به کارت / نقدی / اعتباری |
| N: یادداشت | TEXT | |

### 4. داشبورد (Dashboard)

**کارت‌های آماری:**

| شاخص | فرمول |
|-------|-------|
| فروش امروز (تومان) | `=SUMIFS(Sales!J:J, Sales!B:B, TODAY())` |
| فروش این هفته (تومان) | `=SUMIFS(Sales!J:J, Sales!B:B, ">="&TODAY()-WEEKDAY(TODAY(),2)+1, Sales!B:B, "<="&TODAY()-WEEKDAY(TODAY(),2)+7)` |
| فروش این ماه (تومان) | `=SUMIFS(Sales!J:J, Sales!B:B, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1), Sales!B:B, "<="&EOMONTH(TODAY(),0))` |
| تعداد سفارشات امروز | `=COUNTIFS(Sales!B:B, TODAY())` |
| سود این ماه | فرمول سفارشی با SUMIFS |
| محصولات رو به اتمام | کوئری محصولات با F < G (موجودی < حداقل) |
| تعداد مشتریان کل | `=COUNTA(Customers!A:A)-1` |

### 5. محتوای اینستاگرام (Instagram)

| ستون | نوع | توضیح |
|------|-----|-------|
| A: تاریخ انتشار | DATE | |
| B: کپشن | TEXT | |
| C: هشتگ‌ها | TEXT | |
| D: محصول مرتبط | TEXT | کد محصول |
| E: وضعیت | DROPDOWN | برنامه‌ریزی / منتشر شده |
| F: لینک پست | URL | |

---

## راهنمای استفاده

1. این ساختار رو توی Google Sheets کپی کن
2. برگه‌ها رو با همین نام‌ها بساز
3. فرمول‌ها رو در سطر دوم هر برگه وارد کن و به پایین Drag کن
4. برگه Products رو با ۱۰ محصول اول پر کن
5. برای اتصال به ربات تلگرام: از منوی Extensions > Apps Script استفاده کن

## اسکریپت Google Apps Script (برای ربات تلگرام)

```javascript
// در Apps Script قرار بده
function doGet(e) {
  return handleTelegram(e);
}

function doPost(e) {
  return handleTelegram(e);
}

function handleTelegram(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const productsSheet = sheet.getSheetByName('Products');
  const salesSheet = sheet.getSheetByName('Sales');
  
  // کد ربات در فایل جداگانه نوشته می‌شود
  return ContentService.createTextOutput(JSON.stringify({status: 'ok'}))
    .setMimeType(ContentService.MimeType.JSON);
}

function getProductPrice(productCode) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Products');
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === productCode) {
      return {
        name: data[i][1],
        price: data[i][4],
        stock: data[i][5],
        description: data[i][11]
      };
    }
  }
  return null;
}

function getStock(productCode) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Products');
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === productCode) return data[i][5];
  }
  return 0;
}

function addSale(customerCode, productCode, quantity, shipping, discount) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sales');
  const invoiceCode = 'INV-' + (sheet.getLastRow()).toString().padStart(3, '0');
  const today = new Date();
  
  sheet.appendRow([
    invoiceCode,
    today,
    customerCode,
    productCode,
    quantity,
    '', // قیمت واحد با فرمول محاسبه می‌شود
    '', // قیمت کل با فرمول
    shipping || 0,
    discount || 0,
    '', // مبلغ نهایی با فرمول
    '', // سود با فرمول
    'در انتظار',
    'کارت به کارت',
    ''
  ]);
  
  // بروزرسانی موجودی
  const productsSheet = sheet.getParent().getSheetByName('Products');
  const data = productsSheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === productCode) {
      productsSheet.getRange(i + 1, 6).setValue(data[i][5] - quantity); // ستون F = موجودی
      productsSheet.getRange(i + 1, 15).setValue(data[i][14] + quantity); // ستون O = تعداد فروش
      break;
    }
  }
  
  return invoiceCode;
}
```
