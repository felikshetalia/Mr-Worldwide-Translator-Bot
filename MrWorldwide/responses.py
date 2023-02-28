import random
def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'sup':
        return 'Wazzup'
    
    if p_message == 'roll':
        return str(random.randint(1, 6))
    
    if p_message == 'bot is ready':
        return 'yay!'

    if p_message == '!help':
        return "`This is a help message that you can modify.`"
    
    return 'I did not understand bruh try typing !help'
