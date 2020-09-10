import re 
def clean_text_english(x):

    x = x.lower()

    x = re.compile('htt\S+').sub(' enlace ',x)
    x = re.compile('@\S+').sub(' mencion ',x)
    x = re.compile('#\S+').sub(' hashtag ',x)
    
    x = re.sub(r"[^a-zA-Z.]", ' ', x)      #A exepción de ' para las contraciones
    x = re.sub(r" +", ' ', x)
    return x

def clean_text_spanish(x):

    x = x.lower()

    x = re.compile('htt\S+').sub(' enlace ',x)
    x = re.compile('@\S+').sub(' mencion ',x)
    x = re.compile('#\S+').sub(' hashtag ',x)
    
    x = re.sub(r"[^a-zA-Z.áéíóúñ]", ' ', x)
    x = re.sub(r" +", ' ', x)
    return x