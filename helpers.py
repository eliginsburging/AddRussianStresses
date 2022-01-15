vowel_dict = {
    'а': 'а́',
    'я': 'я́',
    'э': 'э́',
    'е': 'е́',
    'и': 'и́',
    'ы': 'ы́',
    'у': 'у́',
    'ю': 'ю́',
    'о': 'о́',
    'ё': 'ё'
}
vowels = 'аяэеоуюиыАЯЭЕОУЮИЫ'  # used to check if word needs stress
rusalph = 'аАбБвВгГдДеЕёЁжЖзЗиИйЙкКлЛмМнНоОпПрРсСтТуУфФхХцЦчЧшШщЩъЪыЫьЬэЭюЮяЯ'


def mark_stress(stressed_line):
    """
    takes a string containing a scraped html element with the correct stress
    for the target word (marked with a bold html tag)
    (e.g. '<div class="rule ">\n\t\n\t\t В таком варианте ударение следует
    ставить на слог с буквой О — г<b>О</b>ры. \n\t\t\t</div>')
    returns a list in which each element contains stress options for the target
    word. The options are either marked by a bold tag or replaced by the
    stressed equivalents (with combining acute) based on user input.
    """
    stressed_line = stressed_line.replace('<div class="rule ">', '')
    stressed_line = stressed_line.replace('</div>', '')
    stressed_line = stressed_line.replace('\n', '')
    stressed_line = stressed_line.replace('\t', '')
    stressed_line = stressed_line.replace('.', '')
    stressed_line = stressed_line.replace(',', '')
    stressed_line = stressed_line.lower()
    targets = []
    for word in stressed_line.split():
        if '<b>' in word:
            # target_index = word.find('<b>')
            # target_index += 3
            # target_letter = word[target_index]
            # new_string = word[:target_index] + vowel_dict[target_letter] + word[target_index + 1:]
            # new_string = new_string.replace('<b>', '')
            # new_string = new_string.replace('</b>', '')
            # targets.append(new_string)
            targets.append(word)
    return targets

# test1 = mark_stress("""<div class="rule">
# 		  В данном слове ударение ставят на слог с буквой А — господ<b>А</b>.
# 			</div>""")
# test2 = mark_stress("""<div class="rule">
# 		  В упомянутом выше варианте ударение падает на слог с первой буквой О — г<b>О</b>спода.
# 			</div>""")
# for word in test1:
#     print(word)


def needs_stress(word):
    """
    Takes a string containing a Russian word. Returns True if the word needs
    stress marked (i.e. has more than 1 vowel and does not contain ё). returns
    False otherwise
    """
    if 'ё' in word:
        return False
    vowel_count = 0
    for letter in word:
        if letter in vowels:
            vowel_count += 1
    if vowel_count > 1:
        return True
    return False


def is_russian(word):
    """
    Returns true if a string only contains letters of the Russian
    alphabet; false otherwise
    """
    for letter in word:
        if letter not in rusalph:
            return False
    return True


def remove_punct(word, split=False):
    """
    removes various punctuation marks from a string
    """
    word = word.replace(',', '')
    word = word.replace('.', '')
    word = word.replace('!', '')
    word = word.replace('?', '')
    word = word.replace('/', '')
    word = word.replace('\\', '')
    word = word.replace('—', '')
    word = word.replace('\'', '')
    word = word.replace('"', '')
    word = word.replace('—', '')
    word = word.replace('«', '')
    word = word.replace('»', '')
    word = word.replace(';', '')
    word = word.replace(':', '')
    word = word.replace('(', '')
    word = word.replace(')', '')
    word = word.replace('[', '')
    word = word.replace(']', '')
    word = word.replace('…', '')
    if split:
        return word.split()
    else:
        return word


def replace_tags(word):
    print(f'replaceing {word}')
    if '<b>' in word:
        target_index = word.find('<b>')
        target_index += 3
        target_letter = word[target_index]
        new_string = word[:target_index] + vowel_dict[target_letter] + word[target_index + 1:]
        new_string = new_string.replace('<b>', '')
        new_string = new_string.replace('</b>', '')
    else:
        return word
    return new_string


def gen_replacement_text(stresslst, cap=False):
    """
    Takes a lsit of stress options and returns a string version of those
    options (joined by \\ if there's more than one option); optionally
    capitalizes each option before joining
    """
    print(f'received {stresslst}')
    if cap:
        if len(stresslst) > 1:
            # for w in stresslst:
            #     print(f'replacing {w} with {replace_tags(w)}')
            caplist = [replace_tags(w).capitalize() for w in stresslst]
            replacement = '\\'.join(caplist)
        else:
            replacement = replace_tags(stresslst[0]).capitalize()
    else:
        if len(stresslst) > 1:
            # for w in stresslst:
            #     print(f'replacing {w} with {replace_tags(w)}')
            replacement = '\\'.join([replace_tags(item) for item in stresslst])
        else:
            replacement = replace_tags(stresslst[0])
    # print(f'returning {replacement}')
    return replacement


def remove_vertical(word):
    """
    Takes a string, splits it based on | and returns the first part
    """
    return word.split('|')[0]
