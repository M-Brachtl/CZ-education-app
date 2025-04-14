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
    "T": "Částice",
    "I": "Citoslovce",
}
xpos_num_conversion = {
    "N": 1,
    "A": 2,
    "P": 3,
    "C": 4,
    "V": 5,
    "D": 6,
    "R": 7,
    "J": 8,
    "T": 9,
    "I": 10,
}



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
                result[word.text] = xpos_num_conversion[word.xpos[0]] #xpos_conversion[word.xpos[0]], chceme-li slovy
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
    "VerbForm": "Slovesná forma",
    "Animacy": "Životnost",
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
    "Imp": "nedokonavý"},
    "Animacy": {
    "Anim": "životný",
    "Inan": "neživotný"},

}



def get_morphology_sentence(input_text):
    # upos = get_upos_sentence(input_text)
    doc = nlp(input_text)
    print(doc.sentences,file=open("nlp_log.txt", "w", encoding="utf-8")) # pro debugging
    result = {}
    used_words: list[int] = [] # indexy slov, které už byly zpracovány, aby se nezpracovávaly znovu ("mít rád" a zvratná slovesa)
    mitrad_form = "" # zde bude forma "mít rád", až se bude zpracovávat feats
    # normal morphology as lower in the original code
    # reflexives = []
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.lemma == "rád":
                if doc.sentences[0].words[word.head-1].lemma == "mít":
                    result[word.text + " " + doc.sentences[0].words[word.head-1].text] = (word.feats, doc.sentences[0].words[word.head-1].feats)
                    mitrad_form = word.text + " " + doc.sentences[0].words[word.head-1].text
                    if doc.sentences[0].words[word.head-1].text in result.keys(): # pokud jsme na mít narazili dříve, tak ho vymažeme
                        try:
                            result.pop(doc.sentences[0].words[word.head-1].text)
                        except KeyError:
                            pass
                    used_words.append(word.head) # přidáme mít do seznamu zpracovaných slov, aby se nezpracovávalo znovu
                    used_words.append(word.id) # přidáme rád
            elif word.lemma == "se": # pro zvratné sloveso
                result[doc.sentences[0].words[word.head-1].text + " " + word.text] = doc.sentences[0].words[word.head-1].feats # mluv. kategorie zvratného zájmena nepotřebujeme
                # reflexives.append(doc.sentences[0].words[word.head-1].text + " " + word.text)
                if doc.sentences[0].words[word.head-1].text in result.keys(): # pokud jsme na mít narazili dříve, tak ho vymažeme
                    try:
                        result.pop(doc.sentences[0].words[word.head-1].text)
                    except KeyError:
                        pass
                used_words.append(word.head) # přidáme významové sloveso do seznamu zpracovaných slov, aby se nezpracovávalo znovu
                used_words.append(word.id) # přidáme zvratné zájmeno
            elif word.upos == "NOUN" or word.upos == "VERB" or word.upos == "PROPN" or word.upos == "AUX":# zajímají nás pouze podst. jm. a slovesa a pomocná slovesa a nesmí být "mít", pokud mitrad==1
                if word.lemma != "mít" and word.id not in used_words: # pokud není mít a není už zpracováno
                    result[word.text] = word.feats
                    # možná přidat do used_words?
    for word in result.keys():
        try:
            real_result = {}
            if word == mitrad_form:
                for feat in result[word][0].split("|"):
                    try:
                        real_result[morphology_key_conversion[feat.split("=")[0]]] = morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]
                    except KeyError:# as e:
                        # print(e)
                        pass
                for feat in result[word][1].split("|"):
                    try:
                        real_result[morphology_key_conversion[feat.split("=")[0]]] = morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]
                    except KeyError:# as e:
                        # print(e)
                        pass
                result[word] = real_result
                continue

            result[word] = result[word].split("|")
            # result[word] = {feat.split("=")[0]: feat.split("=")[1] for feat in result[word]}
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
    print(get_xpos_sentence(input("Enter a sentence: ")))