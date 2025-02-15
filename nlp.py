import stanza
import stanza.models
import stanza.models.common
import stanza.models.common.doc
nlp = stanza.Pipeline("cs") # load czech language model

convertion = {
    "NOUN": "Podstatné jméno",
    "VERB": "Sloveso",
    "ADJ": "Přídavné jméno",
    "ADV": "Příslovce",
    "PRON": "Zájmeno",
    # "DET": "Člen",
    "ADP": "Předložka",
    "NUM": "Číslovka",
    "CONJ": "Spojka",
    "PART": "Částice",
    "INTJ": "Citoslovce"
}

# input_text = "Příliš žluťoučký kůň úpěl ďábelské ódy."
def get_pos_sentence(input_text):
    doc = nlp(input_text)

    for sentence in doc.sentences:
        result = {}
        for word in sentence.words:
            try:
                result[word.text] = convertion[word.upos]
            except KeyError:
                pass
        return result