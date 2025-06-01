import stanza
import requests

# if isnt downloaded, uncomment the next line to download the Czech language model
#stanza.download("cs", model_dir="stanza_resources") # download Czech language model
nlp = stanza.Pipeline("cs", download_method=stanza.DownloadMethod.REUSE_RESOURCES) # load czech language model

mphDita = lambda sentence: f"https://lindat.mff.cuni.cz/services/morphodita/api/tag?data={sentence}&output=json&convert_tagset=strip_lemma_id" # použití Morphodita API
genDita = lambda lemma: f"https://lindat.mff.cuni.cz/services/morphodita/api/generate?data={lemma}&convert_tagset=pdt_to_conll2009&output=json" # použití Morphodita API pro genitiv

xpos_to_upos = {
    "N": "NOUN",
    "A": "ADJ",
    "V": "VERB",
    "D": "ADV",
    "R": "ADP",
    "P": "PRON",
    "J": "CCONJ",
    "C": "NUM",
    "T": "PART",
    "I": "INTJ",
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



def xpos_to_feats(xpos):
    feats = []
    # 3rd - Gender
    if xpos[2] == "M":
        feats.append("Gender=Masc")
        feats.append("Animacy=Anim") # pokud je mužský rod, tak je životný
    elif xpos[2] == "I":
        feats.append("Gender=Masc")
        feats.append("Animacy=Inan")
    elif xpos[2] == "F":
        feats.append("Gender=Fem")
    elif xpos[2] == "N":
        feats.append("Gender=Neut")
    # 4th - Number
    if xpos[3] == "S":
        feats.append("Number=Sing")
    elif xpos[3] == "P":
        feats.append("Number=Plur")
    # 5th - Case
    try:
        feats.append("Case=" + ("", "Nom", "Gen", "Dat", "Acc", "Voc", "Loc", "Ins")[int(xpos[4])]) # 2 možné exceptions: indexError (když není case) nebo ValueError (když není číslo)
    except (IndexError, ValueError):
        pass
    # 8th - Person
    try:
        feats.append("Person=" + ("", "1", "2", "3")[int(xpos[7])])
    except (IndexError, ValueError):
        pass
    # 9th - Tense
    if xpos[8] == "P":
        feats.append("Tense=Pres")
    elif xpos[8] == "F":
        feats.append("Tense=Fut")
    elif xpos[8] == "R":
        feats.append("Tense=Past")
    # 12th - Voice
    if xpos[11] == "A":
        feats.append("Voice=Act")
    elif xpos[11] == "P":
        feats.append("Voice=Pass")
    # 13th - Aspect
    if xpos[12] == "P":
        feats.append("Aspect=Perf")
    elif xpos[12] == "I":
        feats.append("Aspect=Imp")
    
    return "|".join(feats) if len(feats) > 0 else "_"
    

    
def get_xpos_sentence(input_text):
    doc = requests.get(mphDita(input_text)).json()["result"]
    # print(doc)
    print(doc[0],file=open("nlp_log.txt", "w"))
    for sentence in doc:
        result = {}
        for word in sentence:
            try:
                """# pokud se rád pojí na slovo, které není v rámci přísudku, tak musíme ručně 2->6
                if word.lemma == "rád" and doc.sentences[0].words[word.head-1].lemma != "být" and word.head != 0: # au
                    word.xpos = "D" + word.xpos[1:] # aby se to neukazovalo jako příd. jm., ale jako příslovce
                elif word.lemma == "rád" and (doc.sentences[0].words[word.head-1].lemma == "být" or word.head == 0): # au^2
                    word.xpos = "A" + word.xpos[1:]"""
                result[word["token"]] = xpos_num_conversion[word["tag"][0]] #xpos_conversion[word["tag"][0]], chceme-li slovy
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
    "Vzor": "Vzor",
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
    "Vzor": { # pro účely kódu
    "pán": "pán",
    "hrad": "hrad",
    "muž": "muž",
    "stroj": "stroj",
    "předseda": "předseda",
    "soudce": "soudce",
    "žena": "žena",
    "růže": "růže",
    "píseň": "píseň",
    "kost": "kost",
    "město": "město",
    "moře": "moře",
    "kuře": "kuře",
    "stavení": "stavení",
    }
}



def get_morphology_sentence(input_text):
    # getting pos tags from morphodita
    morphodita_result = requests.get(mphDita(input_text)).json()["result"]
    doc = nlp(input_text)
    # musíme přepsat upos tagy na xpos to upos konvertovaný morphodita result
    for i, sentence in enumerate(morphodita_result):
        for j, word in enumerate(sentence):
            try:
                if doc.sentences[i].words[j].upos != xpos_to_upos[word["tag"][0]] and doc.sentences[i].words[j].lemma != "být":# is not "být"
                    doc.sentences[i].words[j].upos = xpos_to_upos[word["tag"][0]]
                    # musíme také opravit feats, protože morphodita dává jiný tag než nlp
                    doc.sentences[i].words[j].feats = xpos_to_feats(word["tag"])
            except KeyError:
                pass

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
            if word.upos == "NOUN" or word.upos == "PROPN":
                vzor = get_vzor(word.feats, word.lemma)
                result[word.text] += "|Vzor=" + vzor
    future_pop = [] # seznam slov, které se mají vymazat z result (pomocná slovesa)
    result_copy = result.copy() # uděláme kopii, abychom mohli upravit result a předešli změnám během iterace
    for word in result_copy.keys(): # převedení stringu v AJ na dict v ČJ
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
                        for key in result_copy.keys():
                            if my_head.text in key: # hledá, kdy klíč co sedí na head, aby mohl pracovat
                                # 2 možnosti: už je zpracované (a je type dict) nebo není (a je type str)
                                for feat in result[word].split("|"):
                                    try:
                                        real_result[morphology_key_conversion[feat.split("=")[0]]] = morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]
                                    except KeyError: # keyerror, když jde o něco, co nás nezajímá
                                        pass
                                if type(result[key]) == dict: # pokud už je zpracované, tak ho nebudeme znovu zpracovávat
                                    # result[word] = real_result
                                    # nyní dodáme do významového
                                    for category, value in real_result.items():
                                        if category == "Osoba" or (category == "Způsob" and value == "oznamovací") or category == "Slovesná forma":
                                            result[key][category] = value
                                        elif category == "Způsob" and value == "podmiňovací":
                                            result[key][category] = value
                                            result[key]["Čas"] = "přítomný"
                                    result[f"{key} ({word})"] = result[key]
                                    # a vymažeme původní key
                                    result.pop(key)
                                    future_pop.append(word) # vymažeme původní pomocné sloveso
                                elif type(result[key]) == str: # pokud není zpracované, tak ho zpracujeme
                                    if word == "jsem": # debug
                                        print("jsem: ", result[word])
                                        print(f"{key}: ", result[key])
                                    # odděláme čas, protože pomocné sloveso neurčuje čas významového
                                    if not "Mood=Ind" in result[word]:
                                        result[key] = result[key].replace("Tense=Past", "Tense=Pres") # podmiňovací způsob je v přítomném čase
                                        result[f"{key} ({word})"] = result[key] + "|" + result[word]
                                    else:
                                        result[f"{key} ({word})"] = result[key] + "|" + result[word].replace("Tense=Pres", "").replace("Aspect=Imp", "").replace("Voice=Act", "")
                                        
                                    # a vymažeme původní key
                                    result.pop(key)
                                    future_pop.append(word) # vymažeme původní pomocné sloveso
                                elif type(result[key]) == tuple: # pokud je to tuple, tak ho zpracujeme jako sloveso mít rád
                                    # odděláme čas, protože pomocné sloveso neurčuje čas významového
                                    result[key][0].replace("Tense=Past", "Tense=Pres")
                                    result[f"{key} ({word})"] = [result[key][0] + "|" + result[word], result[key][1]]

                                    mitrad_form = f"{key} ({word})" # aby se spustila výjimka v kódu výše
                                    # a vymažeme původní key
                                    result.pop(key)
                                    future_pop.append(word) # vymažeme původní pomocné sloveso

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
    secondary_result = {} # pro slovesa, která se ještě nezpracovala
    for word in result.keys():
        secondary_result[word] = {} # vytvoříme prázdný slovník pro každé slovo
        if type(result[word]) == str:
            for feat in result[word].split("|"):
                try:
                    secondary_result[word][morphology_key_conversion[feat.split("=")[0]]] = morphology_value_conversion[feat.split("=")[0]][feat.split("=")[1]]
                except KeyError:
                    pass
        else: # it is dict
            secondary_result[word] = result[word]

    result = secondary_result # přepíšeme result na secondary_result, aby bylo vše v jednom slovníku

    
    for word in future_pop: # vymažeme pomocná slovesa
        try:
            result.pop(word)
        except KeyError:
            pass

    return result

def get_vzor(feats, nominative: str, first_run: bool = True):
    nominative = nominative.lower() if first_run else nominative # pokud je to první běh, tak převedeme na malá písmena, jinak necháme velká
    vzory = {
    "Masc": [
        ("pán", "", "a"),
        ("hrad", "", "u"),
        ("muž", "", "e"),
        ("stroj", "", "e"),
        ("předseda", "a", "y"),
        ("soudce", "e", "e")
    ],
    "Fem": [
        ("žena", "a", "y"),
        ("růže", "e", "e"),
        ("píseň", "", "e"),
        ("kost", "", "i")
    ],
    "Neut": [
        ("město", "o", "a"),
        ("moře", "e", "e"),
        ("kuře", "e", "ete"),
        ("stavení", "í", "í")
    ]
    }
    if "Gender=Masc" in feats:
        relevant_vzory = vzory["Masc"]
        # kontrola životnosti
        if "Animacy=Inan" in feats:
            relevant_vzory.remove(("pán", "", "a"))
            relevant_vzory.remove(("předseda", "a", "y"))
            relevant_vzory.remove(("soudce", "e", "e"))
            relevant_vzory.remove(("muž", "", "e"))
        elif "Animacy=Anim" in feats:
            relevant_vzory.remove(("hrad", "", "u"))
            relevant_vzory.remove(("stroj", "", "e"))
    elif "Gender=Fem" in feats:
        relevant_vzory = vzory["Fem"]
        if nominative == "dítě" and "Number=Plur" in feats:
            return "kost"
    elif "Gender=Neut" in feats:
        relevant_vzory = vzory["Neut"]
    else:
        return "N/A"
    genitive = ""
    for generated in requests.get(genDita(nominative)).json()["result"][0]:
        if "Cas=2" in generated["tag"] and "Num=S" in generated["tag"]:
            genitive = generated["form"]
            break
    nom_ending = nominative[-1] if nominative[-1] in ("a", "e", "í", "o", "ě") else ""
    if nom_ending == "ě": nom_ending = "e"
    relevant_vzory = list(filter(lambda x: x[1] == nom_ending, relevant_vzory))

    if genitive == "":
        if first_run: # pokud nenajde genitiv, zkusí vlastní jméno s velkým písmenem
            print(nominative)
            try:
                return get_vzor(feats, nominative.capitalize(), False) # pokud nenajde genitiv, zkusí vlastní jméno s velkým písmenem
            except RuntimeError:
                raise RuntimeError("Non-existent word.")
        else:
            raise RuntimeError("Non-existent word.")
    if genitive[-3:] == "ete" or genitive[-3:] == "ěte":
        gen_ending = genitive[-3:]
    elif genitive[-1] in ("a", "e", "y", "í", "i", "ě", "u"):
        gen_ending = genitive[-1]
    else:
        gen_ending = ""

    if gen_ending == "ě": gen_ending = "e"
    elif gen_ending == "ěte": gen_ending = "ete"
    if "Gender=Neut" not in feats and gen_ending == "ete": gen_ending = "e"
    print(relevant_vzory)
    relevant_vzory = list(filter(lambda x: x[2] == gen_ending, relevant_vzory))
    #print(f"Nom_ending: {nom_ending}, Gen_ending: {gen_ending}")
    return list(relevant_vzory)[0][0] if len(list(relevant_vzory)) > 0 else "N/A"


if __name__ == "__main__":
    print(get_morphology_sentence("Včera jsem umyl nádobí."))
    print(get_morphology_sentence("Včera umyl jsem nádobí."))
    # print(get_xpos_sentence(input("Enter a sentence: ")))
    #print(get_vzor("Gender=Masc", "čas"))