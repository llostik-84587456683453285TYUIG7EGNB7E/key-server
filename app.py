from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import threading
import telebot
from telebot import types
import requests
import random
import string
import urllib.parse
import base64
import time
import json
from datetime import datetime, timedelta

BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOOMONEY_TOKEN = os.environ.get("YOOMONEY_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "llostik-84587456683453285TYUIG7EGNB7E/key-server"
WALLET = "4100119480343964"
SUPPORT_1 = "@llostikKJ00"
SUPPORT_2 = "@cha7ok"

UPDATE_LINKS = [
    "https://github.com/llostiktt/GGshop-llostik-Cha7ok — версия 1.0",
]

PLANS = {
    "base": {
        "5d":   {"days": 5,   "usd": 2,   "name_ru": "5 дней",   "name_en": "5 days"},
        "30d":  {"days": 30,  "usd": 10,  "name_ru": "30 дней",  "name_en": "30 days"},
        "365d": {"days": 365, "usd": 40,  "name_ru": "365 дней", "name_en": "365 days"},
        "inf":  {"days": -1,  "usd": 60,  "name_ru": "Навсегда", "name_en": "Forever"},
    },
    "premium": {
        "5d":   {"days": 5,   "usd": 4,   "name_ru": "5 дней",   "name_en": "5 days"},
        "30d":  {"days": 30,  "usd": 14,  "name_ru": "30 дней",  "name_en": "30 days"},
        "365d": {"days": 365, "usd": 44,  "name_ru": "365 дней", "name_en": "365 days"},
        "inf":  {"days": -1,  "usd": 130, "name_ru": "Навсегда", "name_en": "Forever"},
    }
}

SUBS_FILE = "subscriptions.json"
PREMIUM_SUBS_FILE = "premium_subscriptions.json"

T = {
    "ru": {
        "welcome": "👋 *Добро пожаловать в GGShop|Dark Side!*\n\n🎮 Продаём скрипты для Project Delta\n\nВыбери раздел ниже 👇",
        "buy_btn": "🛒 Купить подписку",
        "help_btn": "❓ Помощь",
        "updates_btn": "🔄 Обновления",
        "choose_product": "🛍️ *Что хочешь купить?*\n\nВыбери продукт:",
        "base_btn": "🔵 Base — база для спокойно легитной игры",
        "premium_btn": "🟣 Ultimate — можно играть вообще без легита",
        "base_wip": (
            "🔵 *Base — база для спокойно легитной игры*\n\n"
            "📝 Описание:\n\n"
            "_(обычный скрипт если хочешь играть легитно но с легкостью)_\n\n"
            "💳 *Тарифы:*\n\n"
            "• 5 дней — $2 (~{p5}₽)\n"
            "• 30 дней — $10 (~{p30}₽)\n"
            "• 365 дней — $40 (~{p365}₽)\n"
            "• Навсегда — $60 (~{pinf}₽)\n\n"
            "👤 {s1}\n👤 {s2}"
        ),
        "premium_wip": (
            "🟣 *Ultimate — можно играть вообще без легита*\n\n"
            "📝 Описание:\n\n"
            "_(есть все функции за каторые не банят в том числе и speedhack и анти отдача и разброс и еще не мал функций)_\n\n"
            "💳 *Тарифы:*\n\n"
            "• 5 дней — $4 (~{p5}₽)\n"
            "• 30 дней — $14 (~{p30}₽)\n"
            "• 365 дней — $44 (~{p365}₽)\n"
            "• Навсегда — $130 (~{pinf}₽)\n\n"
            "👤 {s1}\n👤 {s2}"
        ),
        "confirm_base": "✅ Понял, выбрать тариф Base",
        "confirm_premium": "✅ Понял, выбрать тариф Ultimate",
        "choose_plan": "💳 *Выбери тариф:*",
        "help_text": "❓ *Помощь*\n\nЕсли возникли проблемы — пиши в поддержку:\n\n👤 {s1}\n👤 {s2}\n\nПроверить подписку: /mysub",
        "updates_locked": "🔒 *Раздел обновлений*\n\nДоступен только для тарифов *365 дней* и *Навсегда*.\n\nКупи подходящий тариф через 🛒 Купить подписку",
        "updates_empty": "📭 Обновлений пока нет.",
        "updates_title": "🔄 *Доступные обновления:*\n\n",
        "no_sub": "❌ Подписка не найдена. Купи через 🛒 Купить подписку",
        "sub_expired": "❌ Подписка истекла. Купи новую через 🛒 Купить подписку",
        "sub_active": "✅ *Активная подписка*\n\n👤 Ник: `{u}`\n📦 Тариф: {p}\n⏳ Действует: {e}",
        "sub_forever": "навсегда ♾️",
        "sub_until": "до {d} ({n} дн.)",
        "payment_msg": "💳 *Тариф: {plan}*\n\n💰 Сумма: *{rub}₽* (${usd})\n\nОплати по ссылке:\n{link}\n\nПринимаем: Сбер, Тинькофф, любые карты 🏦\n\nПосле оплаты нажми /check\n\nПроблемы с оплатой? {s1} или {s2}",
        "checking": "🔍 Проверяю оплату...",
        "paid_ok": "✅ *Оплата найдена!*\n\nНапиши свой ник в Roblox:",
        "paid_fail": "❌ Оплата не найдена.\n\nПодожди пару минут и попробуй /check снова.\n\nПроблемы? {s1} или {s2}",
        "no_plan": "❌ Сначала выбери тариф через 🛒 Купить подписку",
        "activated_base": "🎉 *Подписка Base активирована! Подождите пока сервер вас обновит — от 1 до 5-6 минут 🥰*\n\n👤 Ник: `{u}`\n📦 Тариф: {p}\n⏳ Действует: {e}\n\nЗапускай скрипт в Xeno:\n`loadstring(game:HttpGet('https://raw.githubusercontent.com/llostik-84587456683453285TYUIG7EGNB7E/by.llostikxCha7ok/refs/heads/main/Final.best'))()`",
        "activated_premium": "🎉 *Подписка Ultimate активирована! Подождите пока сервер вас обновит — от 1 до 5-6 минут 🥰*\n\n👤 Ник: `{u}`\n📦 Тариф: {p}\n⏳ Действует: {e}\n\nЗапускай скрипт в Xeno:\n`loadstring(game:HttpGet('https://raw.githubusercontent.com/llostik-84587456683453285TYUIG7EGNB7E/by.llostikxCha7ok/refs/heads/main/PREMIUM_SCRIPT'))()`",
        "updates_hint": "\n\n🔄 Обновления доступны в разделе *Обновления*",
        "error_activate": "⚠️ Ошибка при активации.\n{s1} или {s2}",
        "error_sub": "⚠️ Ошибка при проверке подписки.",
        "plan_name": "name_ru",
        "lang_choose": "🌍 Выбери язык / Choose language:",
    },
    "en": {
        "welcome": "👋 *Welcome to GGShop|Dark Side!*\n\n🎮 We sell scripts for Project Delta\n\nChoose a section below 👇",
        "buy_btn": "🛒 Buy subscription",
        "help_btn": "❓ Help",
        "updates_btn": "🔄 Updates",
        "choose_product": "🛍️ *What do you want to buy?*\n\nChoose a product:",
        "base_btn": "🔵 Base — a base for a quietly legal game",
        "premium_btn": "🟣 Ultimate — you can play without any limit at all",
        "base_wip": (
            "🔵 *Base — a base for a quietly legal game*\n\n"
            "📝 Description:\n\n"
            "_(a regular script if you want to play legitimately but easily)_\n\n"
            "💳 *Plans:*\n\n"
            "• 5 days — $2 (~{p5}₽)\n"
            "• 30 days — $10 (~{p30}₽)\n"
            "• 365 days — $40 (~{p365}₽)\n"
            "• Forever — $60 (~{pinf}₽)\n\n"
            "👤 {s1}\n👤 {s2}"
        ),
        "premium_wip": (
            "🟣 *Ultimate — you can play without any limit at all*\n\n"
            "📝 Description:\n\n"
            "_(there are all the functions that don't get banned, including speedhack, NoRecoil, spread, and more. Unfortunately, we know that the script is written in Russian, so there will be prompts.1.speedhack if the value is higher than 21 = ban if it starts to teleport too much, lower it to 19this and everything else is intuitive.)_\n\n"
            "💳 *Plans:*\n\n"
            "• 5 days — $4 (~{p5}₽)\n"
            "• 30 days — $14 (~{p30}₽)\n"
            "• 365 days — $44 (~{p365}₽)\n"
            "• Forever — $130 (~{pinf}₽)\n\n"
            "👤 {s1}\n👤 {s2}"
        ),
        "confirm_base": "✅ Got it, choose Base plan",
        "confirm_premium": "✅ Got it, choose Ultimate plan",
        "choose_plan": "💳 *Choose a plan:*",
        "help_text": "❓ *Help*\n\nIf you have any issues — contact support:\n\n👤 {s1}\n👤 {s2}\n\nCheck your subscription: /mysub",
        "updates_locked": "🔒 *Updates section*\n\nOnly available for *365 days* and *Forever* plans.\n\nBuy the right plan via 🛒 Buy subscription",
        "updates_empty": "📭 No updates yet.",
        "updates_title": "🔄 *Available updates:*\n\n",
        "no_sub": "❌ Subscription not found. Buy via 🛒 Buy subscription",
        "sub_expired": "❌ Your subscription has expired. Buy a new one via 🛒 Buy subscription",
        "sub_active": "✅ *Active subscription*\n\n👤 Username: `{u}`\n📦 Plan: {p}\n⏳ Valid: {e}",
        "sub_forever": "forever ♾️",
        "sub_until": "until {d} ({n} days left)",
        "payment_msg": "💳 *Plan: {plan}*\n\n💰 Amount: *{rub}₽* (${usd})\n\nPay via link:\n{link}\n\nWe accept: any card 🏦\n\nAfter payment press /check\n\nPayment issues? {s1} or {s2}",
        "checking": "🔍 Checking payment...",
        "paid_ok": "✅ *Payment found!*\n\nEnter your Roblox username:",
        "paid_fail": "❌ Payment not found.\n\nWait a few minutes and try /check again.\n\nIssues? {s1} or {s2}",
        "no_plan": "❌ First choose a plan via 🛒 Buy subscription",
        "activated_base": "🎉 *Base subscription activated! Please wait for the server to update you — 1 to 5-6 minutes 🥰*\n\n👤 Username: `{u}`\n📦 Plan: {p}\n⏳ Valid: {e}\n\nRun the script in Xeno:\n`loadstring(game:HttpGet('https://raw.githubusercontent.com/llostik-84587456683453285TYUIG7EGNB7E/by.llostikxCha7ok/refs/heads/main/Final.best'))()`",
        "activated_premium": "🎉 *Ultimate subscription activated! Please wait for the server to update you — 1 to 5-6 minutes 🥰*\n\n👤 Username: `{u}`\n📦 Plan: {p}\n⏳ Valid: {e}\n\nRun the script in Xeno:\n`loadstring(game:HttpGet('https://raw.githubusercontent.com/llostik-84587456683453285TYUIG7EGNB7E/by.llostikxCha7ok/refs/heads/main/PREMIUM_SCRIPT'))()`",
        "updates_hint": "\n\n🔄 Updates are available in the *Updates* section",
        "error_activate": "⚠️ Activation error.\n{s1} or {s2}",
        "error_sub": "⚠️ Error checking subscription.",
        "plan_name": "name_en",
        "lang_choose": "🌍 Выбери язык / Choose language:",
    }
}

def t(lang, key, **kwargs):
    text = T.get(lang, T["ru"]).get(key, "")
    return text.format(s1=SUPPORT_1, s2=SUPPORT_2, **kwargs)

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Память вместо GitHub для pending и lang
pending_memory = {}
lang_memory = {}

def pending_get(chat_id):
    return pending_memory.get(str(chat_id))

def pending_set(chat_id, value):
    pending_memory[str(chat_id)] = value

def pending_del(chat_id):
    pending_memory.pop(str(chat_id), None)

def lang_get(chat_id):
    return lang_memory.get(str(chat_id), "ru")

def lang_set(chat_id, lang):
    lang_memory[str(chat_id)] = lang

def get_usd_rub():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        return r.json()["rates"]["RUB"]
    except:
        return 90

def usd_to_rub(usd):
    return round(usd * get_usd_rub())

def github_read(filename):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code == 404:
        return {}, None
    data = r.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return json.loads(content), data["sha"]

def github_write(filename, data, sha=None, message="update"):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
    encoded = base64.b64encode(json.dumps(data, ensure_ascii=False, indent=2).encode()).decode()
    payload = {"message": message, "content": encoded}
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload, timeout=10)
    return r.status_code in (200, 201)

def is_active(sub_data):
    if sub_data["expires"] is None:
        return True
    expires = datetime.fromisoformat(sub_data["expires"])
    return datetime.utcnow() < expires

def update_users_txt(subs, filename="users.txt"):
    active = [u.lower() for u, d in subs.items() if is_active(d)]
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
    r = requests.get(url, headers=headers, timeout=10)
    sha = r.json().get("sha") if r.status_code == 200 else None
    content = "\n".join(active) + "\n"
    encoded = base64.b64encode(content.encode()).decode()
    payload = {"message": f"Sync {filename}", "content": encoded}
    if sha:
        payload["sha"] = sha
    requests.put(url, headers=headers, json=payload, timeout=10)

def add_subscription(username, plan_key, tg_id, product):
    plans = PLANS[product]
    plan = plans[plan_key]
    subs_file = PREMIUM_SUBS_FILE if product == "premium" else SUBS_FILE
    users_file = "premium_users.txt" if product == "premium" else "users.txt"

    subs, sha = github_read(subs_file)
    now = datetime.utcnow()
    expires = None if plan["days"] == -1 else (now + timedelta(days=plan["days"])).isoformat()
    subs[username.lower()] = {
        "plan": plan_key,
        "plan_name_ru": plan["name_ru"],
        "plan_name_en": plan["name_en"],
        "expires": expires,
        "bought_at": now.isoformat(),
        "tg_id": tg_id,
        "product": product
    }
    ok = github_write(subs_file, subs, sha, f"Added {username}")
    if ok:
        update_users_txt(subs, users_file)
    return ok

def cleanup_expired():
    while True:
        try:
            print("Проверка истёкших подписок...")
            for subs_file, users_file in [
                (SUBS_FILE, "users.txt"),
                (PREMIUM_SUBS_FILE, "premium_users.txt")
            ]:
                subs, sha = github_read(subs_file)
                changed = False
                for username in list(subs.keys()):
                    if not is_active(subs[username]):
                        print(f"Удаляем: {username}")
                        del subs[username]
                        changed = True
                if changed:
                    github_write(subs_file, subs, sha, "Cleanup expired")
                    update_users_txt(subs, users_file)
        except Exception as e:
            print(f"cleanup error: {e}")
        time.sleep(3600)

def lang_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    return kb

def main_menu(lang):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(t(lang, "buy_btn"))
    kb.row(t(lang, "help_btn"), t(lang, "updates_btn"))
    return kb

def product_keyboard(lang):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(t(lang, "base_btn"), callback_data="product_base"))
    kb.add(types.InlineKeyboardButton(t(lang, "premium_btn"), callback_data="product_premium"))
    return kb

def plans_keyboard(lang, product):
    kb = types.InlineKeyboardMarkup()
    for key, plan in PLANS[product].items():
        rub = usd_to_rub(plan["usd"])
        name = plan[T[lang]["plan_name"]]
        kb.add(types.InlineKeyboardButton(
            f"{name} — ${plan['usd']} (~{rub}₽)",
            callback_data=f"buy_{product}_{key}"
        ))
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        t("ru", "lang_choose"),
        reply_markup=lang_keyboard())

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def handle_lang(call):
    lang = call.data.replace("lang_", "")
    lang_set(call.message.chat.id, lang)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
        t(lang, "welcome"),
        parse_mode="Markdown",
        reply_markup=main_menu(lang))

@bot.message_handler(func=lambda m: m.text in [t("ru", "buy_btn"), t("en", "buy_btn")])
def buy_menu(message):
    lang = lang_get(message.chat.id)
    bot.send_message(message.chat.id,
        t(lang, "choose_product"),
        parse_mode="Markdown",
        reply_markup=product_keyboard(lang))

@bot.callback_query_handler(func=lambda c: c.data.startswith("product_"))
def handle_product(call):
    lang = lang_get(call.message.chat.id)
    product = call.data.replace("product_", "")
    bot.answer_callback_query(call.id)
    rate = get_usd_rub()

    if product == "base":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(t(lang, "confirm_base"), callback_data="confirm_base"))
        bot.send_message(call.message.chat.id,
            t(lang, "base_wip",
              p5=round(2*rate),
              p30=round(10*rate),
              p365=round(40*rate),
              pinf=round(60*rate)),
            parse_mode="Markdown",
            reply_markup=kb)
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(t(lang, "confirm_premium"), callback_data="confirm_premium"))
        bot.send_message(call.message.chat.id,
            t(lang, "premium_wip",
              p5=round(4*rate),
              p30=round(14*rate),
              p365=round(44*rate),
              pinf=round(130*rate)),
            parse_mode="Markdown",
            reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data in ("confirm_base", "confirm_premium"))
def handle_confirm(call):
    lang = lang_get(call.message.chat.id)
    product = "base" if call.data == "confirm_base" else "premium"
    bot.answer_callback_query(call.id)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(call.message.chat.id,
        t(lang, "choose_plan"),
        parse_mode="Markdown",
        reply_markup=plans_keyboard(lang, product))

@bot.message_handler(func=lambda m: m.text in [t("ru", "help_btn"), t("en", "help_btn")])
def help_menu(message):
    lang = lang_get(message.chat.id)
    bot.send_message(message.chat.id,
        t(lang, "help_text"),
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in [t("ru", "updates_btn"), t("en", "updates_btn")])
def updates_menu(message):
    lang = lang_get(message.chat.id)
    has_access = False
    try:
        for subs_file in [SUBS_FILE, PREMIUM_SUBS_FILE]:
            subs, _ = github_read(subs_file)
            for uname, data in subs.items():
                if data.get("tg_id") == message.chat.id and data["plan"] in ("365d", "inf"):
                    if is_active(data):
                        has_access = True
                        break
    except:
        pass

    if not has_access:
        bot.send_message(message.chat.id, t(lang, "updates_locked"), parse_mode="Markdown")
        return

    if not UPDATE_LINKS:
        bot.send_message(message.chat.id, t(lang, "updates_empty"))
        return

    text = t(lang, "updates_title")
    for i, link in enumerate(UPDATE_LINKS, 1):
        text += f"{i}. {link}\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['mysub'])
def my_sub(message):
    lang = lang_get(message.chat.id)
    try:
        for subs_file in [SUBS_FILE, PREMIUM_SUBS_FILE]:
            subs, _ = github_read(subs_file)
            for uname, data in subs.items():
                if data.get("tg_id") == message.chat.id:
                    if is_active(data):
                        plan_name = data.get(f"plan_name_{lang}", data.get("plan_name_ru", ""))
                        if data["expires"]:
                            expires = datetime.fromisoformat(data["expires"])
                            days_left = (expires - datetime.utcnow()).days
                            exp_str = t(lang, "sub_until", d=expires.strftime('%d.%m.%Y'), n=days_left)
                        else:
                            exp_str = t(lang, "sub_forever")
                        bot.send_message(message.chat.id,
                            t(lang, "sub_active", u=uname, p=plan_name, e=exp_str),
                            parse_mode="Markdown")
                    else:
                        bot.send_message(message.chat.id, t(lang, "sub_expired"))
                    return
        bot.send_message(message.chat.id, t(lang, "no_sub"))
    except Exception as e:
        print(f"mysub error: {e}")
        bot.send_message(message.chat.id, t(lang, "error_sub"))

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def handle_plan_choice(call):
    lang = lang_get(call.message.chat.id)
    parts = call.data.split("_")
    product = parts[1]
    plan_key = parts[2]
    plan = PLANS[product][plan_key]
    rub = usd_to_rub(plan["usd"])
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    pending_set(call.message.chat.id, {
        "code": code,
        "plan": plan_key,
        "product": product,
        "rub": rub,
        "step": "pay"
    })

    params = {
        "receiver": WALLET,
        "quickpay-form": "shop",
        "targets": f"GGshop {product} {plan['name_ru']}",
        "paymentType": "AC",
        "sum": rub,
        "label": code,
    }
    link = "https://yoomoney.ru/quickpay/confirm?" + urllib.parse.urlencode(params)
    plan_name = plan[T[lang]["plan_name"]]

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
        t(lang, "payment_msg", plan=plan_name, rub=rub, usd=plan["usd"], link=link),
        parse_mode="Markdown")

def check_payment(code):
    try:
        headers = {"Authorization": f"Bearer {YOOMONEY_TOKEN}"}
        r = requests.post(
            "https://yoomoney.ru/api/operation-history",
            headers=headers,
            data={"records": 10},
            timeout=10
        )
        for op in r.json().get("operations", []):
            if op.get("status") == "success" and op.get("label") == code:
                return True
    except Exception as e:
        print(f"check_payment error: {e}")
    return False

@bot.message_handler(commands=['check'])
def check(message):
    lang = lang_get(message.chat.id)
    data = pending_get(message.chat.id)
    if not data or data.get("step") != "pay":
        bot.send_message(message.chat.id, t(lang, "no_plan"))
        return

    bot.send_message(message.chat.id, t(lang, "checking"))

    if check_payment(data["code"]):
        data["step"] = "username"
        pending_set(message.chat.id, data)
        bot.send_message(message.chat.id, t(lang, "paid_ok"), parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, t(lang, "paid_fail"), parse_mode="Markdown")

@bot.message_handler(func=lambda m: (pending_get(m.chat.id) or {}).get("step") == "username")
def get_username(message):
    lang = lang_get(message.chat.id)
    username = message.text.strip()
    data = pending_get(message.chat.id)
    if not data:
        return
    plan_key = data["plan"]
    product = data.get("product", "base")
    plan = PLANS[product][plan_key]

    success = add_subscription(username, plan_key, message.chat.id, product)
    pending_del(message.chat.id)

    if success:
        if plan["days"] == -1:
            exp_str = t(lang, "sub_forever")
        else:
            exp_date = (datetime.utcnow() + timedelta(days=plan["days"])).strftime('%d.%m.%Y')
            exp_str = t(lang, "sub_until", d=exp_date, n=plan["days"])

        plan_name = plan[T[lang]["plan_name"]]
        activated_key = "activated_premium" if product == "premium" else "activated_base"
        text = t(lang, activated_key, u=username, p=plan_name, e=exp_str)
        if plan_key in ("365d", "inf"):
            text += t(lang, "updates_hint")
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu(lang))
    else:
        bot.send_message(message.chat.id, t(lang, "error_activate"), parse_mode="Markdown")

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == f"/{BOT_TOKEN}":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                update = telebot.types.Update.de_json(json.loads(body.decode("utf-8")))
                bot.process_new_updates([update])
            except Exception as e:
                print(f"Webhook error: {e}")
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        user = params.get('user', [''])[0]

        if not user:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
            return

        try:
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            found = False
            for filename in ["users.txt", "premium_users.txt"]:
                url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    content = base64.b64decode(r.json()["content"]).decode("utf-8")
                    users = [u.strip().lower() for u in content.splitlines() if u.strip()]
                    if user.lower() in users:
                        found = True
                        break
            response = b'valid' if found else b'invalid'
        except Exception as e:
            print(f"Handler error: {e}")
            response = b'error'

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        pass

RAILWAY_URL = os.environ.get("RAILWAY_PUBLIC_DOMAIN")

if not RAILWAY_URL:
    print("ОШИБКА: RAILWAY_PUBLIC_DOMAIN не задан!")
else:
    WEBHOOK_URL = f"https://{RAILWAY_URL}/{BOT_TOKEN}"
    print("Удаляем старый webhook...")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true")
    time.sleep(2)
    print(f"Ставим webhook: {WEBHOOK_URL}")
    r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")
    print(f"Webhook результат: {r.json()}")

cleanup_thread = threading.Thread(target=cleanup_expired, daemon=True)
cleanup_thread.start()

port = int(os.environ.get('PORT', 8080))
print(f"Сервер на порту {port}")
print(f"GITHUB_TOKEN: {bool(GITHUB_TOKEN)}")
print(f"BOT_TOKEN: {bool(BOT_TOKEN)}")
print(f"YOOMONEY_TOKEN: {bool(YOOMONEY_TOKEN)}")

server = HTTPServer(('0.0.0.0', port), Handler)
server.serve_forever()
