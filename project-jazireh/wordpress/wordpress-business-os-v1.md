# فروشگاه جزیره — WordPress Business OS v1.0

> مستند جامع معماری، توسعه و دیپلوی فروشگاه وردپرسی  
> ۱۰ مدل ساعت مچی مردانه • بند استیل نقره‌ای • ۲ میلیون تومان  
> آماده اجرا روی هاست

---

## 📋 فهرست

1. [System Role — تیم مجازی](#1-system-role)
2. [معماری کلی سایت](#2-معماری-کلی-سایت)
3. [Tech Stack — فناوری‌ها](#3-tech-stack)
4. [طراحی UI/UX](#4-طراحی-uiux)
5. [ساختار محصولات و WooCommerce](#5-ساختار-محصولات)
6. [صفحه اصلی — Homepage](#6-صفحه-اصلی)
7. [صفحه محصول — Single Product](#7-صفحه-محصول)
8. [صفحات فرعی](#8-صفحات-فرعی)
9. [SEO & Schema](#9-seo--schema)
10. [Performance Optimization](#10-performance)
11. [امنیت](#11-امنیت)
12. [اتوماسیون و اتصالات خارجی](#12-اتوماسیون)
13. [چک‌لیست راه‌اندازی](#13-چکلیست-راهاندازی)
14. [پرامپت‌های تخصصی برای AI](#14-پرامپتهای-تخصصی)

---

## 1. System Role

```text
You are a Senior WordPress Architect + WooCommerce Expert + UI/UX Designer +
SEO Manager + CRO Specialist + Performance Engineer + Security Engineer +
Python Automation Engineer.

Your mission: Build a production-ready WooCommerce store for "فروشگاه جزیره"
that outperforms competitors in speed, design, and conversion rate.

Rules:
- Never use lorem ipsum — use real Persian content
- Mobile-first RTL design
- No unnecessary plugins
- Every decision must increase conversion rate
- All output must be implementation-ready
```

---

## 2. معماری کلی سایت

### ۲.۱ نقشه سایت

```
🌐 فروشگاه جزیره
├── 🏠 صفحه اصلی
│   ├── Hero (بنر اصلی + CTA)
│   ├── مزایای خرید
│   ├── محصولات پرفروش (۶ تایی)
│   ├── محصولات جدید (۴ تایی)
│   ├── تخفیف ویژه / Flash Sale
│   ├── دسته‌بندی‌ها (Grid 3 تایی)
│   ├── نظرات مشتریان
│   ├── اینستاگرام (Embed)
│   ├── سوالات متداول (Accordion)
│   └── Newsletter
├── 🛍️ فروشگاه (Shop)
│   ├── فیلترها (Sidebar)
│   ├── Grid محصولات (۳ ستونه)
│   ├── مرتب‌سازی
│   └── Pagination
├── 📦 محصول (Single Product)
│   ├── گالری تصاویر (Zoom + Lightbox)
│   ├── توضیحات + مشخصات
│   ├── Add to Cart (Sticky)
│   ├── محصولات مرتبط
│   └── سوالات و نظرات
├── 📂 دسته‌بندی‌ها
│   ├── ساعت مردانه
│   ├── ساعت زنانه
│   ├── ست ساعت
│   └── پک کادویی
├── ℹ️ درباره ما
├── ❓ سوالات متداول
├── 🛡️ گارانتی و بازگشت
├── 🚚 ارسال و پرداخت
├── 📞 تماس با ما
├── 📝 وبلاگ
├── 🔐 حساب کاربری
│   ├── ورود / ثبت‌نام
│   ├── سفارش‌های من
│   ├── آدرس‌ها
│   └── علاقه‌مندی‌ها
├── 🛒 سبد خرید
├── 💳 تسویه حساب
├── 📋 قوانین و حریم خصوصی
└── 📦 پیگیری سفارش
```

### ۲.۲ ساختار URL

```
/                         صفحه اصلی
/shop/                    فروشگاه
/product/sample-product/  محصول
/product-category/men/    دسته‌بندی
/about/                   درباره ما
/faq/                     سوالات متداول
/warranty/                گارانتی
/shipping/                ارسال
/contact/                 تماس
/blog/                    وبلاگ
/cart/                    سبد خرید
/checkout/                پرداخت
/my-account/              حساب کاربری
/tracking/                پیگیری سفارش
```

---

## 3. Tech Stack

| لایه | انتخاب اصلی | جایگزین |
|-------|-----------|---------|
| CMS | WordPress 6.x | — |
| Commerce | WooCommerce 9.x | — |
| قالب | GeneratePress Premium | Astra Pro |
| صفحه‌ساز | Elementor Pro | Bricks Builder |
| SEO | RankMath Pro | Yoast SEO |
| کش | LiteSpeed Cache | WP Rocket |
| CDN | Cloudflare Free | — |
| فرم‌ها | Fluent Forms | Gravity Forms |
| امنیت | Wordfence | Solid Security |
| SMTP | FluentSMTP | Post SMTP |
| پشتیبان | UpdraftPlus | — |
| بهینه‌سازی تصویر | Imagify | ShortPixel |

### افزونه‌های پیشنهادی (فقط ضروری)

```yaml
core:
  - WooCommerce
  - Elementor Pro
  - RankMath Pro
  - LiteSpeed Cache

enhancement:
  - WooCommerce Smart Coupons
  - Variation Swatches for WooCommerce
  - YITH Wishlist
  - YITH WooCommerce Compare
  - WooCommerce PDF Invoices

persian:
  - Persian WooCommerce (شمسی + تومان + درگاه)
  - ParsPal (درگاه پرداخت)
  - WP-Persian (تقویم شمسی)

optional:
  - Fluent Forms Pro
  - Wordfence Premium
  - UpdraftPlus Premium
  - Imagify
  - FluentCRM (ایمیل مارکتینگ)
```

> ⚠️ **قانون طلایی:** هرگز بیش از ۱۵ افزونه فعال نداشته باش.

---

## 4. طراحی UI/UX

### ۴.۱ رنگ‌ها

```css
:root {
  --color-white:       #FFFFFF;
  --color-off-white:   #F8F9FA;
  --color-light-gray:  #E9ECEF;
  --color-gray:        #6C757D;
  --color-dark-gray:   #212529;
  --color-black:       #000000;
  --color-gold:        #C9A84C;
  --color-gold-light:  #E8D5A3;
  --color-silver:      #A8B2B8;
  --color-purple:      #6C5CE7;
  --color-green:       #00B894;
  --color-red:         #FF4757;
}
```

### ۴.۲ تایپوگرافی

```css
/* فونت اصلی: Vazirmatn */
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

body {
  font-family: 'Vazirmatn', 'Vazir', Tahoma, sans-serif;
  font-size: 16px;
  line-height: 2;
  direction: rtl;
  color: var(--color-dark-gray);
}

h1 { font-size: 2.5rem; font-weight: 900; }
h2 { font-size: 2rem; font-weight: 800; }
h3 { font-size: 1.5rem; font-weight: 700; }
h4 { font-size: 1.25rem; font-weight: 600; }

.price { font-weight: 900; color: var(--color-purple); }
.discount { color: var(--color-red); text-decoration: line-through; }
```

### ۴.۳ اصول طراحی

| اصل | اجرا |
|-----|-------|
| Mobile-First | طراحی از ۳۶۰px شروع می‌شه |
| RTL کامل | تمام المان‌ها راست‌چین |
| Dark Mode | پشتیبانی با CSS variables |
| Accessibility | WCAG 2.1 AA |
| فاصله‌ها | ۸px grid system |
| گوشه‌های گرد | border-radius: 12px |
| سایه‌ها | ملایم، فقط برای elevate |
| انیمیشن | فقط hover و transition (زیر ۲۰۰ms) |
| دکمه‌ها | ارتفاع minimum ۴۸px (قانون انگشت) |
| کنتراست | متن: پس‌زمینه = ۴.۵:۱ |

### ۴.۴ Breakpoints

```
Mobile:     360-767px
Tablet:     768-1023px  
Desktop:    1024-1439px
Wide:       1440px+
```

---

## 5. ساختار محصولات

### ۵.۱ Attributes (ویژگی‌ها)

```php
// در ووکامرس ایجاد کن:
pa_color        → مشکی, آبی, سفید, سبز, طوسی, قهوه‌ای
pa_strap        → استیل نقره‌ای
pa_dial_size    → ۴۰mm, ۴۲mm
pa_movement     → کوارتز
pa_glass        → Mineral Crystal
```

### ۵.۲ Custom Fields (با ACF Pro)

```php
Field Group: product_extra_info

garanti_battery       // گارانتی باتری: Text (۱۲ ماهه)
box_type              // نوع جعبه: Select (جعبه اصلی باکیفیت)
water_resistant       // مقاومت آب: Text
shipping_time         // زمان ارسال: Text
weight_grams          // وزن: Number
```

### ۵.۳ ۱۰ محصول — داده کامل

| SKU | نام | رنگ صفحه | قطر | قیمت | موجودی |
|-----|-----|---------|-----|------|--------|
| PRD-001 | ساعت مردانه — مشکی کلاسیک | مشکی | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۱۵ |
| PRD-002 | ساعت مردانه — آبی | آبی | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۱۲ |
| PRD-003 | ساعت مردانه — سفید مینیمال | سفید | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۱۸ |
| PRD-004 | ساعت مردانه کرونوگراف — مشکی | مشکی | ۴۲mm | ۲,۰۰۰,۰۰۰ | ۸ |
| PRD-005 | ساعت مردانه — سبز | سبز | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۱۰ |
| PRD-006 | ساعت مردانه — طوسی | طوسی | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۱۴ |
| PRD-007 | ساعت مردانه — قهوه‌ای | قهوه‌ای | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۱۱ |
| PRD-008 | ساعت مردانه اسکلتون | — | ۴۲mm | ۲,۰۰۰,۰۰۰ | ۷ |
| PRD-009 | ساعت مردانه نگین‌دار — مشکی | مشکی | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۹ |
| PRD-010 | ساعت مردانه روز-تاریخ — مشکی | مشکی | ۴۰mm | ۲,۰۰۰,۰۰۰ | ۲۰ |

### ۵.۴ دسته‌بندی‌ها (Categories)

```
ساعت مردانه (parent)
├── کلاسیک
├── کرونوگراف
├── اسکلتون
├── نگین‌دار
└── روز-تاریخ
```

### ۵.۵ قیمت‌گذاری

```
قیمت پایه: ۲,۰۰۰,۰۰۰ تومان
قیمت ویژه: — (نداریم فعلاً)
قیمت عمده: ۱,۸۰۰,۰۰۰ تومان (حداقل ۵ عدد)

نحوه نمایش:
<span class="price">۲,۰۰۰,۰۰۰ <span class="currency">تومان</span></span>
```

---

## 6. صفحه اصلی

### ۶.۱ سکشن‌های Elementor

```yaml
section_1_hero:
  type: Full Width
  content:
    - Heading: "ساعت مچی مردانه — کیفیت بالا، قیمت استثنایی"
    - Subtitle: "۱۰ مدل ساعت مردانه با بند استیل نقره‌ای • فقط ۲ میلیون تومان"
    - CTA Button: "🛍️ مشاهده محصولات" → /shop
    - CTA Secondary: "🤖 سفارش با ربات تلگرام" → https://t.me/JazirehWatchBot
  bg: Gradient (dark gray to black)
  motion: Fade-in on scroll

section_2_benefits:
  type: 4 Column Grid
  items:
    - icon: 🚚 | title: ارسال فوری | desc: تهران ۳ ساعته، شهرستان ۲۴ ساعته
    - icon: 🔄 | title: ضمانت بازگشت | desc: ۷ روز بازگشت بی‌قید و شرط
    - icon: 🛡️ | title: گارانتی باتری | desc: ۱۲ ماه گارانتی تعویض
    - icon: 🎁 | title: جعبه اصلی | desc: بسته‌بندی شکیل و آماده هدیه

section_3_popular:
  type: Product Grid (6 columns → 3 on tablet → 2 on mobile)
  source: WooCommerce — Best Selling — Limit 6
  template: Custom Product Card (طراحی اختصاصی)

section_4_new:
  type: Product Grid (4 columns)
  source: WooCommerce — Newest — Limit 4
  template: Custom Product Card

section_5_banner:
  type: Full Width CTA
  bg: Image (ساعت روی زمینه تیره)
  content: "همه مدل‌ها فقط ۲ میلیون تومان — با جعبه اصلی و گارانتی"
  button: "همین حالا خرید کن"

section_6_categories:
  type: 3 Column Grid
  items:
    - image: men-classic.jpg → /product-category/classic
    - image: chronograph.jpg → /product-category/chronograph
    - image: special.jpg → /product-category/skeleton

section_7_testimonials:
  type: Carousel (3 items visible)
  source: Reviews Plugin or Manual
  style: Card with avatar, stars, text

section_8_instagram:
  type: Smash Balloon Instagram Feed
  shortcode: [instagram-feed cols=6 num=6]

section_9_faq:
  type: Accordion
  items:
    - Q: چطور سفارش بدم؟
    - Q: ارسال چقدر طول میکشه؟
    - Q: گارانتی داره؟
    - Q: اگه پشیمون شدم چی؟
    - Q: پرداخت چطوریه؟
    - Q: ساعت‌ها ضد آب هستن؟

section_10_newsletter:
  type: CTA Banner
  content: "برای تخفیف‌های ویژه عضو شوید"
  form: Fluent Forms — Email Only
```

### ۶.۲ Header

```yaml
layout: Sticky Top Bar + Main Header + Mega Menu

top_bar:
  - متن: "🚚 ارسال رایگان تهران | 💎 گارانتی ۱۲ ماهه | 🔄 ۷ روز بازگشت"
  - لینک: ورود / ثبت‌نام | پیگیری سفارش

main_header:
  - logo: لوگوی فروشگاه جزیره (SVG)
  - search: Ajax Search (FiboSearch)
  - icons: Wishlist | Cart (با تعداد) | Account

mega_menu:
  - فروشگاه (Mega Menu با تصاویر دسته‌بندی)
  - دسته‌بندی‌ها (Dropdown)
  - درباره ما
  - وبلاگ
  - تماس با ما
```

### ۶.۳ Footer

```yaml
layout: 4 Column + Bottom Bar

column_1:
  - لوگو
  - توضیح کوتاه
  - شبکه‌های اجتماعی

column_2:
  heading: "دسترسی سریع"
  links: [فروشگاه, محصولات پرفروش, محصولات جدید, تخفیف‌ها]

column_3:
  heading: "خدمات مشتریان"
  links: [سوالات متداول, گارانتی, ارسال, بازگشت کالا, پیگیری سفارش]

column_4:
  heading: "تماس با ما"
  content: "📞 ۰۹XX-XXX-XXXX\n📱 @JazirehWatchBot\n📷 Instagram: @jazire1400"

bottom_bar:
  - "© ۱۴۰۴ فروشگاه جزیره"
  - "قوانین و مقررات | حریم خصوصی"
```

---

## 7. صفحه محصول

### ۷.۱ Layout (Elementor Single Product Template)

```yaml
section_gallery:
  type: 2 Column (60% image | 40% info) → 1 Column on mobile

  column_left:
    - WooCommerce Product Gallery (Zoom + Lightbox)
    - Thumbnails: Vertical Left
    - Badge: "پرفروش" / "جدید" / "خاص"

  column_right:
    - Category + Breadcrumb
    - Product Title (H1)
    - Star Rating (اختیاری)
    - Price: "۲,۰۰۰,۰۰۰ تومان"
    - Short Description
    - Benefits Icons (۴ تایی: ارسال، گارانتی، جعبه، بازگشت)
    - Quantity + Add to Cart Button (Full Width)
    - Wishlist + Compare Icons
    - Trust Badge: "پرداخت امن • ارسال فوری • گارانتی"

section_details:
  type: Tabs
  tabs:
    - توضیحات کامل
    - مشخصات فنی (Attribute Table)
    - گارانتی و خدمات پس از فروش
    - نظرات کاربران (Reviews)
    - سوالات متداول

section_related:
  type: Product Carousel (4 items)
  title: "محصولات مرتبط"
  source: Related Products (WooCommerce)

section_recently_viewed:
  type: Product Carousel
  title: "بازدیدهای اخیر"
```

### ۷.۲ Sticky Add to Cart (Mobile)

```yaml
trigger: Scroll past gallery section
position: Fixed bottom
content: Product thumbnail + Price + Add to Cart button
background: White with shadow
```

### ۷.۳ Product Badges

```css
.badge-special { background: #C9A84C; } /* طلایی — پرفروش */
.badge-new     { background: #00B894; } /* سبز — جدید */
.badge-unique  { background: #6C5CE7; } /* بنفش — خاص */
```

---

## 8. صفحات فرعی

### ۸.۱ درباره ما

```yaml
section_hero:
  title: "داستان فروشگاه جزیره"
  subtitle: "از عشق به ساعت تا فروشگاه آنلاین"

section_story:
  text: |
    فروشگاه جزیره از سال ۱۴۰۴ با هدف ارائه ساعت‌های مچی باکیفیت
    و قیمت منصفانه شروع به کار کرد. ما معتقدیم یک ساعت خوب نباید
    گران باشد. تمام محصولات ما با دقت انتخاب می‌شوند و قبل از
    ارسال تست کیفیت می‌شوند.

section_values:
  grid: 3 Column
  items:
    - title: "کیفیت" | icon: 💎
    - title: "صداقت" | icon: 🤝
    - title: "سرعت" | icon: ⚡

section_team:
  (اختیاری — عکس + نام + سمت)
```

### ۸.۲ سوالات متداول (FAQ)

```yaml
type: Accordion with Search

categories:
  - ارسال و تحویل (۴ سوال)
  - پرداخت و قیمت (۳ سوال)
  - گارانتی و بازگشت (۴ سوال)
  - محصولات (۴ سوال)
  - سفارش و پشتیبانی (۳ سوال)

schema: FAQPage Schema
```

### ۸.۳ تماس با ما

```yaml
section_contact:
  type: 2 Column
  column_left:
    - Form: Fluent Forms
    - Fields: نام, ایمیل, تلفن, موضوع, پیام
  column_right:
    - Map: Google Maps (آدرس فروشگاه)
    - Info: تلفن, ایمیل, آدرس, ساعت کاری
    - Social Links
```

### ۸.۴ وبلاگ

```yaml
layout: Sidebar Right
categories:
  - راهنمای خرید ساعت
  - نگهداری از ساعت
  - استایل و مد
  - اخبار فروشگاه

post_template:
  - Featured Image
  - Title + Meta
  - Content
  - Related Posts (3)
  - Comments
```

---

## 9. SEO & Schema

### ۹.۱ تنظیمات RankMath

```yaml
global:
  separator: "|"
  homepage_title: "فروشگاه ساعت جزیره | خرید ساعت مچی مردانه با بهترین قیمت"
  homepage_desc: "۱۰ مدل ساعت مردانه با بند استیل نقره‌ای. قیمت یکسان ۲ میلیون تومان. ارسال فوری، گارانتی ۱۲ ماهه"
  rtl: true

post_types:
  product:
    title_template: "%title% | قیمت %price% | فروشگاه جزیره"
    desc_template: "%excerpt% — ارسال فوری ✓ گارانتی باتری ۱۲ ماهه ✓ قیمت %price% ✓"
  
  product_cat:
    title_template: "خرید %term_title% | فروشگاه جزیره"
    desc_template: "انواع %term_title% با بهترین قیمت و کیفیت. ارسال فوری به سراسر ایران ✓"

social:
  og_image: default_product_image.jpg
  twitter_card: summary_large_image
  facebook: jazire1400
  instagram: jazire1400

sitemap:
  include_images: true
  priority: product > category > page > post

local_seo:
  (در صورت داشتن فروشگاه فیزیکی)
```

### ۹.۲ Schema Markup

```json
// Product Schema (خودکار توسط RankMath)
{
  "@type": "Product",
  "name": "ساعت مردانه — مشکی کلاسیک بند استیل نقره‌ای",
  "sku": "PRD-001",
  "offers": {
    "@type": "Offer",
    "price": "2000000",
    "priceCurrency": "IRR",
    "availability": "https://schema.org/InStock"
  }
}

// FAQ Schema
{
  "@type": "FAQPage",
  "mainEntity": [...]
}

// Organization Schema
{
  "@type": "Organization",
  "name": "فروشگاه جزیره",
  "url": "https://jazireh-shop.ir",
  "logo": "https://jazireh-shop.ir/logo.png"
}
```

### ۹.۳ Internal Linking Strategy

```yaml
rules:
  - هر پست وبلاگ → لینک به ۲-۳ محصول مرتبط
  - صفحه محصول → لینک به دسته‌بندی + محصولات مرتبط
  - دسته‌بندی → توضیح + لینک به محصولات آن دسته
  - FAQ → لینک به صفحات محصول و ارسال
```

---

## 10. Performance

### ۱۰.۱ تنظیمات LiteSpeed Cache

```yaml
cache:
  - Enable Cache: ON
  - Cache Mobile: ON
  - Cache Logged-in: OFF
  - TTL: 604800 (۱ هفته)

optimize:
  - CSS Minify: ON
  - CSS Combine: OFF (باعث مشکل RTL میشه)
  - JS Minify: ON
  - JS Combine: OFF
  - JS Defer: ON
  - HTML Minify: ON

media:
  - Lazy Load Images: ON
  - Lazy Load Iframes: ON
  - WebP Replacement: ON
  - Missing Image Sizes: ON

page_optimization:
  - DNS Prefetch: ON (fonts.googleapis.com, cdn.jsdelivr.net)
  - Remove CSS: render-blocking (فقط فایل‌های غیرضروری)
  - Remove Google Fonts: OFF (نیاز به Vazirmatn داریم)
  - Critical CSS: ON (Generate با Elementor)
```

### ۱۰.۲ Cloudflare

```yaml
ssl: Full (Strict)
cache_level: Standard
browser_cache_ttl: 1 month
always_online: ON
auto_minify: OFF (LiteSpeed انجام میده)
http2: ON
http3: ON
0rtt: ON
```

### ۱۰.۳ اهداف Performance

| معیار | هدف |
|-------|-----|
| Google PSI Mobile | ۸۵+ |
| Google PSI Desktop | ۹۵+ |
| LCP | < ۲.۵s |
| FID | < ۱۰۰ms |
| CLS | < ۰.۱ |
| TTFB | < ۵۰۰ms |
| GTMetrix | A |

---

## 11. امنیت

### ۱۱.۱ Wordfence

```yaml
firewall: Enabled (Learning Mode → Enabled)
login_security:
  - 2FA: ON (for admins)
  - reCAPTCHA v3: ON (login + register)
  - Login attempts: 3 → lockout 15 min
  - Password strength: Strong

scan:
  - Schedule: Daily at 3:00 AM
  - Scan plugins/themes: ON
  - Scan files outside WP: ON
  - Email alerts: ON

rate_limiting:
  - Crawler: 120/min
  - Human: 120/min
  - 404: 60/min
```

### ۱۱.۲ قوانین Cloudflare WAF

```
Rule 1: Block Iran threat score > 50
Rule 2: Rate limit /wp-login.php — 5 req/min per IP
Rule 3: Rate limit /xmlrpc.php — 0 req/min (block completely)
Rule 4: Block IPs with ASN: OVH, DigitalOcean (if not using)
```

### ۱۱.۳ اقدامات سرور

```bash
# htaccess
<Files wp-config.php>
    order allow,deny
    deny from all
</Files>

# Disable XML-RPC
add_filter('xmlrpc_enabled', '__return_false');

# Limit login attempts
# Use Wordfence instead

# Auto-update
add_filter('auto_update_plugin', '__return_true');
add_filter('auto_update_theme', '__return_true');
```

---

## 12. اتوماسیون

### ۱۲.۱ ربات تلگرام ← Google Sheets ← WooCommerce

```python
# python-telegram-bot + gspread + woocommerce API

# Flow:
# 1. مشتری در ربات سفارش میده
# 2. سفارش در Google Sheets ثبت میشه
# 3. Webhook یا Cron job هر ۵ دقیقه Google Sheets رو میخونه
# 4. سفارش‌های جدید رو در WooCommerce ثبت میکنه
# 5. موجودی رو آپدیت میکنه
# 6. SMS/Telegram notification به مشتری
```

### ۱۲.۲ اتصال به کانال‌ها

```yaml
telegram_channel: "@jazire1400"
# هر محصول جدید → پست در کانال

instagram: "@jazire1400"
# استفاده از Meta Business Suite برای انتشار

bale: "TOKEN_HERE"
# API مشابه تلگرام

eitaa: "TOKEN_HERE"
# API مشابه تلگرام
```

### ۱۲.۳ Google Sheets Sync

```javascript
// Google Apps Script — Web App
// URL: https://script.google.com/macros/s/xxx/exec

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  
  if (data.action === 'addSale') {
    // ثبت فروش در Google Sheets
    const sheet = SpreadsheetApp.getActive().getSheetByName('Sales');
    sheet.appendRow([
      data.invoiceCode,
      new Date(),
      data.customerName,
      data.productCode,
      data.quantity,
      data.totalPrice,
      'در انتظار'
    ]);
  }
  
  return ContentService.createTextOutput(JSON.stringify({status: 'ok'}));
}
```

---

## 13. چک‌لیست راه‌اندازی

### Phase 1: Foundation (روز ۱-۲)
- [ ] خرید هاست (پیشنهاد: lite.host یا hostiran)
- [ ] خرید دامنه .ir
- [ ] نصب WordPress
- [ ] نصب GeneratePress Premium
- [ ] نصب افزونه‌های Core
- [ ] تنظیم SSL (اجباری)
- [ ] تنظیم permalink: /%postname%/
- [ ] تنظیم زبان فارسی + تقویم شمسی

### Phase 2: WooCommerce (روز ۳-۴)
- [ ] تنظیمات WooCommerce Wizard
- [ ] واحد پول: تومان (IRT)
- [ ] تنظیم درگاه پرداخت (ParsPal یا زرین‌پال)
- [ ] ایجاد Attributes
- [ ] ایجاد Categories
- [ ] ایجاد ۱۰ محصول با داده کامل
- [ ] تنظیم SKU و موجودی
- [ ] آپلود تصاویر محصول (WebP)
- [ ] تنظیم shipping zones و methods
- [ ] تنظیم مالیات (صفر برای ایران)

### Phase 3: Design (روز ۵-۷)
- [ ] تنظیم Global Colors/Fonts
- [ ] ساخت Header Template (Elementor)
- [ ] ساخت Footer Template
- [ ] ساخت Single Product Template
- [ ] ساخت Archive/Shop Template
- [ ] ساخت ۱۰ سکشن Homepage
- [ ] طراحی Mobile Menu
- [ ] تنظیم Dark Mode
- [ ] تست همه صفحات روی mobile/tablet/desktop

### Phase 4: Content & SEO (روز ۸-۹)
- [ ] صفحه درباره ما
- [ ] صفحه FAQ
- [ ] صفحه ارسال و پرداخت
- [ ] صفحه گارانتی
- [ ] صفحه تماس
- [ ] ۵ پست وبلاگ اولیه
- [ ] تنظیمات RankMath
- [ ] تولید Meta همه صفحات
- [ ] تنظیم Sitemap
- [ ] تنظیم Schema
- [ ] Submit به Google Search Console

### Phase 5: Optimization (روز ۱۰-۱۱)
- [ ] تنظیم LiteSpeed Cache
- [ ] تنظیم Cloudflare
- [ ] بهینه‌سازی تصاویر (Imagify → WebP)
- [ ] Google PSI → رفع مشکلات
- [ ] Core Web Vitals → بررسی
- [ ] Minify CSS/JS
- [ ] تنظیم Lazy Loading
- [ ] تست سرعت (GTmetrix, Pingdom)

### Phase 6: Security (روز ۱۲)
- [ ] تنظیم Wordfence
- [ ] تنظیم Cloudflare WAF
- [ ] reCAPTCHA روی فرم‌ها
- [ ] 2FA برای ادمین
- [ ] تغییر wp-admin URL
- [ ] تنظیم htaccess
- [ ] اولین Backup

### Phase 7: Automation (روز ۱۳-۱۴)
- [ ] اتصال ربات تلگرام
- [ ] اتصال Google Sheets
- [ ] تنظیم Webhook/Cron برای sync
- [ ] اتصال کانال تلگرام
- [ ] اتصال بله و ایتا (در صورت نیاز)
- [ ] تنظیم ایمیل مارکتینگ (FluentCRM)

### Phase 8: Launch (روز ۱۵)
- [ ] خرید نهایی
- [ ] انتقال دامنه
- [ ] فعال‌سازی درگاه پرداخت واقعی
- [ ] آخرین Backup
- [ ] تست checkout کامل
- [ ] بررسی Mobile کامل
- [ ] اعلام به Google (Request Indexing)
- [ ] پست اول در شبکه‌های اجتماعی
- [ ] 🚀 **LAUNCH**

---

## 14. پرامپت‌های تخصصی

### ۱۴.۱ پرامپت Elementor — صفحه اصلی

```
Build the homepage of "فروشگاه جزیره" in Elementor:

Theme: GeneratePress Premium RTL Persian
Font: Vazirmatn
Colors: White BG, Dark Gray text, Purple (#6C5CE7) accent, Gold (#C9A84C) highlights

Sections (in order):
1. Hero: Full-width dark gradient, headline "ساعت مچی مردانه با بهترین قیمت",
   subtitle "۱۰ مدل • استیل نقره‌ای • ۲ میلیون تومان • جعبه اصلی • گارانتی باتری"
2. 4-column benefits bar under hero: ارسال فوری, گارانتی, جعبه اصلی, بازگشت ۷ روزه
3. Product grid: 6 best-sellers, custom card design with hover effect
4. Banner CTA: "همه مدل‌ها فقط ۲ میلیون تومان" full-width with gold accent
5. Category grid: 3 cards linking to product categories
6. FAQ accordion: 6 questions about shipping, payment, warranty
7. Newsletter CTA: "برای تخفیف‌های ویژه عضو شوید"

Every section: smooth scroll reveal, RTL, mobile-responsive, GSC-compliant.
```

### ۱۴.۲ پرامپت Single Product Template

```
Create a WooCommerce Single Product template in Elementor for a Persian RTL watch store.

Layout:
- Left (60%): Full gallery with zoom, thumbnail slider vertical left
- Right (40%): Breadcrumb → Title → Price → Short description →
  4 benefit icons (truck, shield, gift, refresh) →
  Quantity + Full-width Add to Cart → Wishlist icon →
  Trust badge

Below:
- Tabs: Full description | Specifications table | Warranty info | Reviews
- Related products carousel (4 items)
- Sticky Add to Cart on mobile scroll

Design: Apple-like minimalism, generous whitespace, large typography,
subtle shadows, rounded corners (12px), gold/purple accent colors.
```

### ۱۴.۳ پرامپت SEO — محصول

```
Write RankMath-optimized SEO meta for this product:

Title: [Product Name] | قیمت ۲ میلیون تومان | فروشگاه جزیره
Description: [Product Name] با بند استیل نقره‌ای. ۲ میلیون تومان.
ارسال فوری ✓ جعبه اصلی ✓ گارانتی باتری ۱۲ ماهه ✓

Include:
- Focus keyphrase: [main product keyword in Persian]
- Open Graph title + description
- Twitter card
- Product Schema with price, availability, SKU
- Breadcrumb Schema
```

### ۱۴.۴ پرامپت اتوماسیون — Python

```python
"""
Connect Telegram bot to WooCommerce via REST API.

Flow:
1. User sends order to @JazirehWatchBot
2. Bot records in Google Sheets
3. Cron job (every 5 min) reads Google Sheets
4. Creates WooCommerce order via API
5. Updates stock in WooCommerce
6. Sends confirmation to user via Telegram

Requirements:
- python-telegram-bot
- gspread
- woocommerce (python library)
- requests
"""

# WooCommerce API config
WC_URL = "https://jazireh-shop.ir"
WC_CONSUMER_KEY = "ck_xxx"
WC_CONSUMER_SECRET = "cs_xxx"

from woocommerce import API

wcapi = API(
    url=WC_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3"
)

def create_order(customer_name, phone, product_id, quantity):
    data = {
        "payment_method": "bacs",
        "billing": {
            "first_name": customer_name,
            "phone": phone
        },
        "line_items": [{
            "product_id": product_id,
            "quantity": quantity
        }]
    }
    return wcapi.post("orders", data).json()
```

---

## 📊 خلاصه زمان‌بندی اجرا

| فاز | شرح | زمان |
|-----|------|------|
| ۱ | Foundation (هاست، وردپرس، افزونه‌ها) | ۲ روز |
| ۲ | WooCommerce (محصولات، پرداخت) | ۲ روز |
| ۳ | Design (Elementor، قالب‌ها) | ۳ روز |
| ۴ | Content & SEO | ۲ روز |
| ۵ | Performance Optimization | ۲ روز |
| ۶ | Security | ۱ روز |
| ۷ | Automation (ربات + sync) | ۲ روز |
| ۸ | Launch | ۱ روز |
| **کل** | | **۱۵ روز** |

---

> 📄 این مستند آماده است تا به هر توسعه‌دهنده یا AI داده شود و به‌صورت کامل اجرا گردد.  
> تمام جزئیات، کدها، تنظیمات و پرامپت‌ها در این سند موجود است.
