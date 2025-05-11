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
    "Z": "Interpunkce",
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
    "Z": 0
}



def get_upos_sentence(input_text): #určený pouze pro testování
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
                # pokud se rád pojí na slovo, které není v rámci přísudku, tak musíme ručně 2->6
                if word.lemma == "rád" and doc.sentences[0].words[word.head-1].lemma != "být" and word.head != 0: # au
                    word.xpos = "D" + word.xpos[1:] # aby se to neukazovalo jako příd. jm., ale jako příslovce
                elif word.lemma == "rád" and (doc.sentences[0].words[word.head-1].lemma == "být" or word.head == 0): # au^2
                    word.xpos = "A" + word.xpos[1:]
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
                if (doc.sentences[0].words[word.head-1].upos != "VERB" and doc.sentences[0].words[word.head-1].upos != "AUX") or word.head == 0:
                    # hledáme "mít"
                    for word2 in sentence.words:
                        if word2.lemma == "mít":
                            word.head = word2.id # nastavíme head na mít, aby se to zpracovalo jako mít rád
                if doc.sentences[0].words[word.head-1].lemma == "mít":
                    result[word.text + " " + doc.sentences[0].words[word.head-1].text] = (word.feats, doc.sentences[0].words[word.head-1].feats)
                    mitrad_form = word.text + " " + doc.sentences[0].words[word.head-1].text
                    if doc.sentences[0].words[word.head-1].text in result.keys(): # pokud jsme na mít narazili dříve, tak ho vymažeme
                        try:
                            result.pop(doc.sentences[0].words[word.head-1].text)
                        except KeyError:
                            pass
                    used_words.append(word.head) # přidáme mít do seznamu zpracovaných slov, aby se nezpracovávalo znovu
                    used_words.append(word.id) # přidáme rád:
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
            elif word.id not in used_words: # pokud není už zpracováno
                result[word.text] = "" # pokud je to jiný slovní druh (nebo interpunkce), tak vrátíme prázdný string
    for word in result.keys(): # převedení stringu v AJ na dict v ČJ
        try:
            real_result = {} # unikátní výsledek pro každé slovo, pak se přidá do result
            if word == mitrad_form: # sloveso mít + rád, které je zpracováno jako jedno slovo
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
                # zkontrolovat, jestli má minulý čas a pokud ano, tak jestli má osobu. Pokud ne -> přidat osobu 3.
                if "Tense=Past" in result[word][1] and "Person" not in result[word][1]:
                    real_result["Osoba"] = 3
                result[word] = real_result
                continue
            # první zjistíme, jestli není pomocné - najdeme ho v nlp výstupu a najdeme jeho head, jeho head pak hledáme v real_result, pokud tam není, tak upravíme result
            for NLPword in sentence.words:
                if NLPword.text == word and NLPword.upos == "AUX":
                    my_head = sentence.words[NLPword.head-1] # head je 1...n, takže musíme odečíst 1
                    # podmínky: je sloveso, má ve feats "Tense=Past"; MŮŽE být mít rád a zvratné, protože stále může mít pomocné být
                    if my_head.upos == "VERB" and my_head.feats != "_" and "Tense=Past" in my_head.feats:
                        #   hledáme v resultech sloveso, které obsahuje pomocné sloveso (ale může tam toho být víc (např. *měl* rád))
                        result_copy = result.copy() # uděláme kopii, abychom mohli upravit result a předešli změnám během iterace
                        for key in result_copy.keys():
                            if my_head.text in key:
                                # 2 možnosti: už je zpracované (a je type dict) nebo není (a je type str)
                                for feat in result[word].split("|"):
                                    try:
                                        real_result[morphology_key_conversion[feat.split("=")[0]]] = morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]
                                    except KeyError:
                                        pass
                                if type(result[key]) == dict: # pokud už je zpracované, tak ho nebudeme znovu zpracovávat
                                    result[word] = real_result
                                    # nyní dodáme do významového
                                    for category, value in result[word].items():
                                        if category == "Osoba":
                                            result[key][category] = value
                                        elif category == "Způsob" and value == "podmiňovací":
                                            result[key][category] = value
                                            result[key]["Čas"] = "přítomný"
                                elif type(result[key]) == str: # pokud není zpracované, tak ho zpracujeme
                                    # odděláme čas, protože pomocné sloveso neurčuje čas významového
                                    if not "Mood=Ind" in result[word]:
                                        result[key] = result[key].replace("Tense=Past", "Tense=Pres") # podmiňovací způsob je v přítomném čase
                                        result[f"{key} ({word})"] = result[key] + "|" + result[word]
                                    else:
                                        result[f"{key} ({word})"] = result[key] + "|" + result[word].replace("Tense=Pres", "")
                                    # a vymažeme původní key
                                    result.pop(key)
                                    result[word] = real_result
                                elif type(result[key]) == tuple: # pokud je to tuple, tak ho zpracujeme jako sloveso mít rád
                                    # odděláme čas, protože pomocné sloveso neurčuje čas významového
                                    result[key][0].replace("Tense=Past", "Tense=Pres")
                                    result[f"{key} ({word})"] = [result[key][0] + "|" + result[word], result[key][1]]

                                    mitrad_form = f"{key} ({word})" # aby se spustila výjimka v kódu výše
                                    # a vymažeme původní key
                                    result.pop(key)
                                    result[word] = real_result
            try:
                result[word] = result[word].split("|") # pokud je to pomocné sloveso, pak je zpracováno výše -> AttributeError
                # result[word] = {feat.split("=")[0]: feat.split("=")[1] for feat in result[word]}
                for feat in result[word]:
                    try:
                        # result[word] = {morphology_key_conversion[feat.split("=")[0]]: morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]}
                        real_result[morphology_key_conversion[feat.split("=")[0]]] = morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]
                    except KeyError:
                        pass
                # zkontrolovat, jestli má minulý čas a pokud ano, tak jestli má osobu. Pokud ne -> přidat osobu 3.
                if "Tense=Past" in result[word] and "Person" not in result[word]:
                    real_result["Osoba"] = 3
                result[word] = real_result
            except AttributeError:
                pass
        except KeyError:
            pass


    return result



if __name__ == "__main__":
    print(get_morphology_sentence(input("Enter a sentence: ")))
    # print(get_xpos_sentence(input("Enter a sentence: ")))