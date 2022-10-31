import time
import urllib.request
import telegram
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import (
    TelegramError,
    Unauthorized,
    BadRequest,
    TimedOut,
    ChatMigrated,
    NetworkError,
)

"""
AU PREALABLE A AVOIR :
- LE TOKEN DE VOTRE BOT TELEGRAM
- CONNAITRE LA VERSION DE VOTRE GOOGLE CHROME ET INSTALLER LE CHROMEDRIVER ADEQUAT
- SI VOUS ETES SUR UN VPS DECOMMENTER DIRECTEMENT LES OPTIONS ET CHANGER LE TEXTE
DE L'ELEMENT BUTTON ET DIV EN ANGLAIS SI LA CONNECTION ECHOUE DES LE DEBUT.
- UN COMPTE INSTAGRAM POUR LE BOT
- UN TOKEN API SUR PICWISH (25 Photos Gratuite)
"""


# Decommenter les options ci-dessous si la connection instagram se passe bien.
options = Options()
#options.add_argument("start-maximized")
#options.add_argument("--lang=fr-FR");
#options.add_argument("--headless")
#options.add_argument("--no-sandbox")

user_agent = "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
options.add_argument(f"user-agent={user_agent}")

# Version de Google Chrome utilisé pour ma part : Google Chrome 106.0.5249.119
# Installer la bonne version sur la racine de ce répertoire la bonne version de votre chromedriver.
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)

# Connection a un compte instagram obligatoire pour pouvoir grab les photo de profiles.
driver.get("https://www.instagram.com")
time.sleep(3)

login_link = driver.find_element_by_xpath("//button[contains(text(),'Uniquement autoriser les cookies essentiels')]")
login_link.click()
print("✅ BOT : BOUTON COOKIE ✅")
time.sleep(3)
driver.find_element_by_name("username").send_keys("VOTRE-PSEUDO-INSTAGRAM")
print("✅ BOT : USERNAME ✅")
time.sleep(1)
driver.find_element_by_name("password").send_keys("VOTRE-MOTDEPASSE-INSTAGRAM")
print("✅ BOT : PASSWORD ✅")
time.sleep(2)
login_link = driver.find_element_by_xpath("//div[contains(text(),'Se connecter')]")
login_link.click()
time.sleep(3)
print("✅ BOT : CONNECTION  ✅");
time.sleep(8)
print("✅ BOT : MONITORING TELEGRAM ✅")


def start(update, context):
    pseudo = update.message.from_user.first_name
    msg = (
        "Salut "
        + pseudo
        + " 👋🏴\nContent de te voir ici 😉\n🤖 Bot github.com/mousliiim 🤖\nVoir commande disponible avec /help 😁"
    )
    update.message.reply_text(msg)
    context.bot.send_video(chat_id = update.effective_chat.id, video = "https://sparksight.com/wp-content/uploads/2019/12/insta-mobile.gif")

def help(update, context):
    msg = "📋 Commande Disponible 📋\n/insta [PSEUDO]\nRecupere la photo de profil Instagram"
    update.message.reply_text(msg)


def version(update, context):
    msg ="🤖 Bot en développement 🤖\n🤖 Prochaine feature bientôt 🤖"
    update.message.reply_text(msg)


def insta(update, context):
    try:
        InstaProfil = " ".join(context.args)

        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id,
            action=telegram.ChatAction.UPLOAD_PHOTO,
        )
        
        # Lien complet avec le nom d'utilisateur donné en argument sur Telegram ci dessus.
        urlcomplet = "https://www.instagram.com/" + InstaProfil + "/?__a=1&__d=dis"
        update.message.reply_text("Chargement de ta photo..⌛")
        
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id,
            action=telegram.ChatAction.UPLOAD_PHOTO,
        )
        
        # Photo de profil récuperer grace au format JSON.
        driver.get(urlcomplet)
        time.sleep(2)
        source = driver.find_element_by_tag_name("pre").text
        data = json.loads(source)
        data2 = data["graphql"]
        data3 = data2["user"]
        PicUrl = data3["profile_pic_url_hd"]
       
       # API PicWish pour optimisé la qualité de la photo instagram.
        response = requests.request(
        "POST", 
        "https://techhk.aoscdn.com/api/tasks/visual/scale", 
        headers= {'X-API-KEY': 'VOTRE-TOKEN-API-PICWISH'}, 
        data={'sync': '1','type':'clean','image_url' : PicUrl},
        )
        
        data = response.text
        json_data = json.loads(data)
        img_url = json_data['data']['image']

       # Envoit de la photo aprés passage de l'API.
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_url)
    
    except Exception as error:
        update.message.reply_text(str(error))


def main():
    # Mettre Token de ton Bot Telegram (Disponible sur BotFather)
    token = "TOKEN-BOT-TELEGRAM"
    
    # Note: The use_context=True is a special argument only needed for version 12 of the library. The default value is False. It allows for better backwards compatibility with older versions of the library, and to give users some time to upgrade. From version 13 use_context=True it is the default.
    updater = Updater(token, use_context=True)
    botcmd = updater.dispatcher

    # Commande /start
    start_command_handler = CommandHandler("start", start)
    botcmd.add_handler(start_command_handler)

    # Commande /help
    help_command_handler = CommandHandler("help", help)
    botcmd.add_handler(help_command_handler)
    
    # Commande /version
    version_command_handler = CommandHandler("version", version)
    botcmd.add_handler(version_command_handler)

    # Commande /insta
    insta_handler = CommandHandler("insta", insta)
    botcmd.add_handler(insta_handler)

    # Start BOT #
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
