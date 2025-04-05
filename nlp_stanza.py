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
    "PROPN": "Vlastní jméno",
    "CCONJ": "Souřadící spojka"     
}

xpos_conversion = {
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
def get_upos_sentence(input_text): #určený pouze pro testování nebo morfologii
    doc = nlp(input_text)
    # print(doc.sentences)

    for sentence in doc.sentences:
        result = {}
        for word in sentence.words:
            try:
                result[word.text] = word.upos
            except KeyError:
                pass
        return result
    
def get_xpos_sentence(input_text):
    doc = nlp(input_text)
    print(doc.sentences,file=open("nlp_log.txt", "w"))
    for sentence in doc.sentences:
        result = {}
        for word in sentence.words:
            try:
                result[word.text] = xpos_conversion[word.xpos[0]]
            except KeyError:
                pass
        return result
    
morphology_key_conversion = {
    "Case": "Pád",
    "Gender": "Rod",
    "Number": "Číslo",
    "Person": "Osoba",
    "Tense": "Čas",
    "Aspect": "Vid",
    "Mood": "Způsob",
    "Voice": "Slovesný rod",
    "VerbForm": "Slovesná forma"
}
morphology_value_conversion = {
    "Case": {
    "Nom": 1,
    "Gen": 2,
    "Dat": 3,
    "Acc": 4,
    "Voc": 5,
    "Loc": 6,
    "Ins": 7},
    "Gender": {
    "Masc": "mužský",
    "Fem": "ženský",
    "Neut": "střední"},
    "Number": {
    "Sing": "jednotné",
    "Plur": "množné"},
    "Person": {
    "1": 1,
    "2": 2,
    "3": 3},
    "Tense": {
    "Pres": "přítomný",
    "Past": "minulý",
    "Fut": "budoucí"},
    "Mood": {
    "Ind": "oznamovací",
    "Imp": "rozkazovací",
    "Sub": "podmiňovací",
    "Cnd": "podmiňovací",},
    "Voice": {
    "Act": "činný",
    "Pass": "trpný"},
    "VerbForm": {
    "Fin": "finitní",
    "Inf": "infinitiv"},
    "Aspect": {
    "Perf": "dokonavý",
    "Imp": "nedokonavý"}
}



def get_morphology_sentence(input_text):
    upos = get_upos_sentence(input_text)
    doc = nlp(input_text)
    mitrad = 0 # pokud je mitrad==1, tak se neprovádí morfologie pro sloveso mít
    ## sloveso mít rád (hledám rád v doc.sentences, pokud je tam, tak mitrad=1)
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.lemma == "rád":
                if doc.sentences[0].words[word.head].lemma == "mít":
                    mitrad = 1
                    break
    ## END
    clened_upos = upos.copy() # copy the dictionary to avoid modifying the original
    for word in upos.keys(): # zajímají nás pouze podst. jm. a slovesa a pomocná slovesa a nesmí být "mít", pokud mitrad==1
        if not (upos[word] == "NOUN" or upos[word] == "VERB" or upos[word] == "PROPN" or upos[word] == "AUX"):
            clened_upos.pop(word)
    print(doc.sentences,file=open("nlp_log.txt", "w", encoding="utf-8")) # pro debugging
    for sentence in doc.sentences:
        result = {}
        for word in sentence.words:
            try:
                if word.text in clened_upos.keys():
                    result[word.text] = word.feats
                #result[word.text] = word.feats
            except KeyError:
                pass
    for word in result.keys():
        try:
            result[word] = result[word].split("|")
            # result[word] = {feat.split("=")[0]: feat.split("=")[1] for feat in result[word]}
            real_result = {}
            for feat in result[word]:
                try:
                    # result[word] = {morphology_key_conversion[feat.split("=")[0]]: morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]}
                    real_result[morphology_key_conversion[feat.split("=")[0]]] = morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]
                except KeyError:
                    pass
            result[word] = real_result
        except KeyError:
            pass


    return result



if __name__ == "__main__":
    # print(get_morphology_sentence(input("Enter a sentence: ")))
    print(get_upos_sentence(input("Enter a sentence: ")))