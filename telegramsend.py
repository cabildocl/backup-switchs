def telegramsend(token_id,group_id,message):
    import requests
    send_text = 'https://api.telegram.org/bot' + token_id + '/sendMessage?chat_id=' + group_id + '&parse_mode=Markdown&text=' + message 
    response = requests.get(send_text)
    return response.json()
def telegramsendfile(token_id,group_id,bot_file):
    import requests
    send_text = 'https://api.telegram.org/bot' + token_id + '/sendDocument?chat_id=' + group_id
    files = {'document': (bot_file, open(bot_file, 'rb')),}
    response = requests.get(send_text, files=files)
    return response.json()
