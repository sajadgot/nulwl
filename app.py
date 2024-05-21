from pyrubi import Client
from threading import Thread

auth = [{"auth":"iutoukkqpndluighxnojvqefclfjzjiu","key":"MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAJioPoABtgdBjCvqd3iilwkuL6NrQ0V/emcKtwZX1xDA4d543thgohN5r5MRdjcPpCXXajc40R9p2sZGCihj/50N4kD7qefn62C09F73mhj32t/c75B1xAKd71+E3DW+Q0m96lPSU79DCVFhpj2cUqa1XBMTT2Lf9Z17wl0bcXxvAgMBAAECgYAiti7wAHOZlsf+vGPKJH5fcgcXC67SQLhecctIP/UBNDqn0agqX167OvI3aMMOphnXGPJn+B1lHTbH2uk4YfSfMbqUoSXgqmfz6CBkbOLoELrt5CbAWqtfdITcAFnmaUArW1XaslmYPPcANXDY2NTlpBHAcTbAEWp/lnBmo4rkIQJBAMn5Q6UMdV3rtu1ny/zDmAEJMzwmuiQViTlM5y57hzDf9M8QE6do+IgMErx6pxwFKkQ0dB6co1RuT7Oz44HSt0kCQQDBfePiRVKmb7LZPP3ytOKvGOMrcQtX1hYrbGqS0JJ2Uu7C7CaIgLQiHC5RUa+NtOUdF3bGZdVcAIA8qsjUhH33AkEAuXua7cZFOt2v/tJl+Vk/DSR/0uvV4jGM9fx0CrIS84WY81fWVNYH+BjuU/1n3km4CS8KvNoo/O7ZbzTy6FS1UQJAUDX/4i0atiRX3/aIz7RsxGlswvV53k/BoP6wr2wHS0XV9LgwwSWZhwpnqQ5T2ErFL+oqMtTEPf93Ka8i0faawQJACIbB68MBj0XS0MDEHRN1AJRDbZGRjDjkQIGiiedRZM6NfM/YCW4XMAnphVlrvpv7G8sMhkCq8ILxYCuHr/18kg=="}]

for f in auth:
    bot = Client(auth=f["auth"], private=f["key"], platform="android")
    Guid_map = []

    def target_link(m):
        send = m.reply("please waiting . . .")
        Guid_map.clear()
        if "joinc" in m.text:
            Guid = bot.get_chat_preview(m.text.split("/link")[1].strip())["channel"]["channel_guid"]
            Guid_map.append(Guid)
            m.reply("saved channel upload .")
        elif "@" in m.text:
            Guid = bot.get_chat_info_by_username(m.text.split("/link")[1].strip())["channel"]["channel_guid"]
            Guid_map.append(Guid)
            m.reply("saved channel upload .")
        bot.delete_messages(m.author_guid, [send["message_update"]["message_id"]])

    def upload(m):
        if len(Guid_map) == 0:
            m.reply("not map link !")
        else:
            send = m.reply("please waiting . . .")
            if m.reply_message_id != None:
                types = bot.get_messages(m.object_guid, m.reply_message_id)["messages"][0]["file_inline"]["type"]
                dlink = bot.get_download_link(m.author_guid, m.reply_message_id)
                if types == "Music":
                    bot.send_music(Guid_map[0], file=dlink, file_name="music-rubika")
                elif types == "Image":
                    bot.send_image(Guid_map[0], file=dlink)
                elif types == "Video":
                    bot.send_video(Guid_map[0], file=dlink)
                elif types == "File":
                    bot.send_file(Guid_map[0], file=dlink, file_name="File.mp4")
                m.reply(f"{types} Uploaded.")
            bot.delete_messages(m.author_guid, [send["message_update"]["message_id"]])

    for m in bot.on_message():
        try:
            if m.text.startswith("/upload"):
                Thread(target=upload, args=[m]).start()
            elif m.text.startswith("/link"):
                Thread(target=target_link, args=[m]).start()
        except Exception as e:
            m.reply("error:\n\n" + str(e))