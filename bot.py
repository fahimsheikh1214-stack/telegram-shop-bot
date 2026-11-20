import logging
from telegram import WebAppInfo
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# --- আপনার তথ্য এখানে বসান ---
BOT_TOKEN = "8686258762:AAHjfRugTypJZ0IyDHIU-Ca7XLDcRZjMXUY"
ADMIN_CHAT_ID = 7464736224  # আপনার টেলিগ্রাম আইডি

# --- আপনার পণ্যের তালিকা (এখানে আপনি নতুন পণ্য যোগ করতে পারবেন) ---
PRODUCTS = {
    "P101": {"name": "স্মার্ট ওয়াচ", "price": 850, "desc": "দারুণ মানের স্মার্ট ওয়াচ।"},
    "P102": {"name": "ব্লুটুথ ইয়ারবাড", "price": 550, "desc": "নয়েজ ক্যানসেলিং ইয়ারবাড।"},
    "P103": {"name": "পাওয়ার ব্যাংক", "price": 1200, "desc": "২০০০০mAh ফাস্ট চার্জিং।"}
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = f"স্বাগতম {user_name}! 🛍️\n\nআমাদের শপে আপনাকে স্বাগতম। নিচের বাটনে ক্লিক করে আমাদের ওয়েবসাইট থেকে পণ্য অর্ডার করতে পারেন।"
    
    # এখানে আপনার ওয়েবসাইটের লিংকটি বসাবেন
    website_url = "https://fastbazar71.blogspot.com/?m=1" # <--- এখানে আপনার লিংক দিন
    
    # Open Site / Open App বাটন তৈরি
    keyboard = [
        [InlineKeyboardButton("🌐 Open Site", web_app=WebAppInfo(url=website_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = []
    for pid, info in PRODUCTS.items():
        keyboard.append([InlineKeyboardButton(f"{info['name']} - ৳{info['price']}", callback_data=f"prod_{pid}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("আমাদের পণ্যসমূহ:", reply_markup=reply_markup)

async def product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pid = query.data.split("_")[1]
    prod = PRODUCTS[pid]
    text = f"📦 *{prod['name']}*\n\n💰 মূল্য: ৳{prod['price']}\n📝 বিবরণ: {prod['desc']}"
    keyboard = [
        [InlineKeyboardButton("✅ অর্ডার করুন", callback_data=f"order_{pid}")],
        [InlineKeyboardButton("⬅️ পেছনে যান", callback_data="show_products")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pid = query.data.split("_")[1]
    user_id = query.from_user.id
    user_data[user_id] = {"pid": pid, "step": "ask_name"}
    await query.edit_message_text("অর্ডার করতে আপনার *নাম* লিখে পাঠান:", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if user_id not in user_data or "step" not in user_data[user_id]:
        return
    state = user_data[user_id]
    if state["step"] == "ask_name":
        state["name"] = text
        state["step"] = "ask_phone"
        await update.message.reply_text(f"ধন্যবাদ {text}। এবার আপনার *ফোন নম্বর* দিন:", parse_mode='Markdown')
    elif state["step"] == "ask_phone":
        state["phone"] = text
        state["step"] = "done"
        pid = state["pid"]
        prod = PRODUCTS[pid]
        admin_msg = (
            f"🚨 *নতুন অর্ডার এসেছে!*\n\n"
            f"📦 পণ্য: {prod['name']} (ID: {pid})\n"
            f"💰 মূল্য: ৳{prod['price']}\n"
            f"👤 কাস্টমার: {state['name']}\n"
            f"📞 ফোন: {state['phone']}\n"
            f"🆔 কাস্টমার Telegram ID: {user_id}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode='Markdown')
        await update.message.reply_text("✅ আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে! আমরা শীঘ্রই আপনার সাথে যোগাযোগ করব।")
        del user_data[user_id]

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_products, pattern="^show_products$"))
    application.add_handler(CallbackQueryHandler(product_detail, pattern="^prod_"))
    application.add_handler(CallbackQueryHandler(order_start, pattern="^order_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("বট চালু হয়েছে...")
    import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Render-এর জন্য ডামি ওয়েব সার্ভার
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), BaseHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    # ডামি সার্ভার চালু করা
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    # বট চালু করা
    print("বট চালু হয়েছে...")
    application.run_polling()
