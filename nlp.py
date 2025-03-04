import stanza
import stanza.models
import stanza.models.common
import stanza.models.common.doc
nlp = stanza.Pipeline("cs", download_method=stanza.DownloadMethod.REUSE_RESOURCES) # load czech language model

upos_convertion = {
    "NOUN": "Podstatné jméno",
    "VERB": "Sloveso",
    "ADJ": "Přídavné jméno",
    "ADV": "Příslovce",
    "PRON": "Zájmeno",
    "DET": "Determinátor",
    "ADP": "Předložka",
    "NUM": "Číslovka",
    "CONJ": "Spojka",
    "PART": "Částice",
    "INTJ": "Citoslovce",
    "SCONJ": "Podřadící spojka",
    "AUX": "Pomocné sloveso",
    "SYM": "Symbol",
    "X": "Neznámé",
    # "PUNCT": "Interpunkce",
    # "SPACE": "Mezera",
    "PROPN": "Vlastní jméno",
    "CCONJ": "Souřadící spojka"     
}

xpos_conversion = { # hypotéza
    "N": "Podstatné jméno",
    "A": "Přídavné jméno",
    "V": "Sloveso",
    "D": "Příslovce",
    "R": "Předložka",
    "P": "Zájmeno",
    "J": "Spojka",
    "C": "Číslovka",
    "T": "Částice"
}

# input_text = "Příliš žluťoučký kůň úpěl ďábelské ódy."
def get_upos_sentence(input_text):
    doc = nlp(input_text)
    print(doc.sentences)

    for sentence in doc.sentences:
        result = {}
        for word in sentence.words:
            try:
                result[word.text] = upos_convertion[word.upos]
            except KeyError:
                pass
        return result
    
def get_xpos_sentence(input_text):
    doc = nlp(input_text)
    print(doc.sentences)
# Udělal to moc rychle, a proto jej nevzali na naši školu.
    for sentence in doc.sentences:
        result = {}
        for word in sentence.words:
            try:
                result[word.text] = xpos_conversion[word.xpos[0]]
            except KeyError:
                pass
        return result
    
if __name__ == "__main__":
    # print(get_upos_sentence(input("Enter a sentence: ")))
    print(get_xpos_sentence(input("Enter a sentence: ")))