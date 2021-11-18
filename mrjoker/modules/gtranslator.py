from gpytranslate import SyncTranslator
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from mrjoker import dispatcher
from mrjoker.modules.disable import DisableAbleCommandHandler

trans = SyncTranslator()

def translate(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    message = update.effective_message
    reply_msg = message.reply_to_message
    if not reply_msg:
        message.reply_text("Reply to a message to translate it!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate,
                        sourcelang=source, targetlang=dest)
    reply = f"<b>Translated from {source} to {dest}</b>:\n" \
        f"<code>{translation.text}</code>"

    bot.send_message(text=reply, chat_id=message.chat.id, parse_mode=ParseMode.HTML)


def languages(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    bot = context.bot
    bot.send_message(
        text="Click [here](https://t.me/Tele_united_bots/3559) to see the list of supported language codes!",
        chat_id=message.chat.id, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

__help__ = """ 
Use this module to translate stuff!

*Commands:*

🔹 `/tl` (or `/tr`): as a reply to a message, translates it to English.

🔹 `/tl <lang>`: translates to <lang>
        eg: `/tl si`: translates to Sinhala.
        
🔹 `/tl <source>//<dest>`: translates from <source> to <lang>.
        eg: `/tl si//en`: translates from Sinhala to English.
        
• *Language Codes*
`af,am,ar,az,be,bg,bn,bs,ca,ceb,co,cs,cy,da,de,el,en,eo,es,
et,eu,fa,fi,fr,fy,ga,gd,gl,gu,ha,haw,hi,hmn,hr,ht,hu,hy,
id,ig,is,it,iw,ja,jw,ka,kk,km,kn,ko,ku,ky,la,lb,lo,lt,lv,mg,mi,mk,
ml,mn,mr,ms,mt,my,ne,nl,no,ny,pa,pl,ps,pt,ro,ru,sd,si,sk,sl,
sm,sn,so,sq,sr,st,su,sv,sw,ta,te,tg,th,tl,tr,uk,ur,uz,
vi,xh,yi,yo,zh,zh_CN,zh_TW,zu`
"""

TRANSLATE_HANDLER = DisableAbleCommandHandler(["tr", "tl"], translate)
TRANSLATE_LANG_HANDLER = DisableAbleCommandHandler(["lang", "languages"], languages)

dispatcher.add_handler(TRANSLATE_HANDLER)
dispatcher.add_handler(TRANSLATE_LANG_HANDLER)

__mod_name__ = "G-Translator"
__command_list__ = ["tr", "tl", "lang", "languages"]
__handlers__ = [TRANSLATE_HANDLER, TRANSLATE_LANG_HANDLER]
