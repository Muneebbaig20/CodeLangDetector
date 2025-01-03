import re

Token = {

    'C': {
        'comment': r'//.|/\.\/',
        'STRING': r'".?"|\'.?\'',
        'NUMBER': r'\b\d+\b',
        'KEYWORD': r'\b(break|case|char|const|continue|default|do|double|else|enum|float|for|goto|if|int|long|return|signed|sizeof|static|struct|switch|typedef|unsigned|void|while)\b',
        'OPERATOR': r'\+|\-|\|\/|\%|\+\+|\-\-|\=|\+=|\-=|\=|\/=|\%=|\==|\!=|\>|\<|\>=|\<=|\&\&|\|\||\!|\&|\||\^|\~|\<<|\>>|\>>>',
        'IDENTIFIER': r'\b[a-zA-Z_]\w*\b',
        'PUNCTUATION': r'\{|\}|\[|\]|\(|\)|\.|\,|\;|\:',
    },

    'C++': {
        'comment': r'//.|/\.\/',
        'STRING': r'".?"|\'.?\'',
        'NUMBER': r'\b\d+\b',
        'KEYWORD': r'\b(auto|break|case|catch|char|class|const|continue|default|delete|do|double|else|enum|explicit|extern|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|operator|private|protected|public|register|return|short|signed|sizeof|static|struct|switch|template|this|throw|try|typedef|union|unsigned|using|virtual|void|volatile|while)\b',
        'OPERATOR': r'\+|\-|\|\/|\%|\+\+|\-\-|\=|\+=|\-=|\=|\/=|\%=|\==|\!=|\>|\<|\>=|\<=|\&\&|\|\||\!|\&|\||\^|\~|\<<|\>>|\>>>',
        'IDENTIFIER': r'\b[a-zA-Z_]\w*\b',
        'PUNCTUATION': r'\{|\}|\[|\]|\(|\)|\.|\,|\;|\:',
    },
    'Python': {
        'comment': r'\#.*',
        'STRING': r'".?"|\'.?\'',
        'NUMBER': r'\b\d+\b',
        'KEYWORD': r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|not|or|pass|print|raise|return|try|while|with|yield)\b',
        'OPERATOR': r'\+|\-|\|\/|\%|\+\+|\-\-|\=|\+=|\-=|\=|\/=|\%=|\==|\!=|\>|\<|\>=|\<=|\&\&|\|\||\!|\&|\||\^|\~|\<<|\>>|\>>>',
        'IDENTIFIER': r'\b[a-zA-Z_]\w*\b',
        'PUNCTUATION': r'\{|\}|\[|\]|\(|\)|\.|\,|\;|\:',
    },
    'Java': {
        'comment': r'//.|/\.\/',
        'STRING': r'".?"|\'.?\'',
        'NUMBER': r'\b\d+\b',
        'KEYWORD': r'\b(abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while)\b',
        'OPERATOR': r'\+|\-|\|\/|\%|\+\+|\-\-|\=|\+=|\-=|\=|\/=|\%=|\==|\!=|\>|\<|\>=|\<=|\&\&|\|\||\!|\&|\||\^|\~|\<<|\>>|\>>>',
        'IDENTIFIER': r'\b[a-zA-Z_]\w*\b',
        'PUNCTUATION': r'\{|\}|\[|\]|\(|\)|\.|\,|\;|\:',
    },
    'Php': {
        'comment': r'//.|/\.\/',
        'STRING': r'".?"|\'.?\'',
        'NUMBER': r'\b\d+\b',
        'KEYWORD': r'\b(abstract|and|array|as|break|case|catch|cfunction|class|clone|const|continue|declare|default|do|else|elseif|enddeclare|endfor|endforeach|endif|endswitch|endwhile|extends|final|for|foreach|function|global|goto|if|implements|interface|instanceof|namespace|new|old_function|or|private|protected|public|static|switch|throw|try|use|var|while|xor)\b',
        'OPERATOR': r'\+|\-|\|\/|\%|\+\+|\-\-|\=|\+=|\-=|\=|\/=|\%=|\==|\!=|\>|\<|\>=|\<=|\&\&|\|\||\!|\&|\||\^|\~|\<<|\>>|\>>>',
        'IDENTIFIER': r'\b[a-zA-Z_]\w*\b',
        'PUNCTUATION': r'\{|\}|\[|\]|\(|\)|\.|\,|\;|\:',
    }
}

# Function

def lexer(code, language):
    tokens = [] # this is list 
    token_types = Token[language]
    
    code = re.sub(r'\s+', ' ', code)

    for key, value in token_types.items():
        for token in re.finditer(value, code):
            tokens.append((key, token.group(0)))

    return tokens

def detect_language(code):
    languages = ['C++', 'C', 'Python', 'Java', 'Php']
    
    keywords = {
        'C': ['stdio.h', 'int main()', 'printf', 'scanf'],
        'C++': ['iostream', 'int main()', 'class', 'namespace', 'std::', 'cout', 'cin'],
        'Python': ['def', 'import', 'from', 'as', 'print', 'if', 'else', 'for', 'while', 'class', 'return', 'with'],
        'Java': ['public', 'class', 'System.out.println'],
        'Php': ['<?php', 'echo']
    }
    syntax_patterns = {
        'C': [r'\b#include\b\s*<\s*stdio\.h\s*>', r'\bint\s+main\s*\(\s*\)', r'\bprintf\b', r'\bscanf\b'],
        'C++': [r'\b#include\b\s*<\s*iostream\s*>', r'\bint\s+main\s*\(\s*\)', r'\bclass\b', r'\bnamespace\b', r'\bstd::', r'\bcout\b', r'\bcin\b'],
        'Python': [r'\bdef\b\s+\w+\s*\(', r'\bimport\b\s+\w+', r'\bfrom\b\s+\w+\s+\bimport\b', r'\bprint\b\s*\(', r'\bif\b\s+', r'\belse\b', r'\bfor\b\s+', r'\bwhile\b\s+', r'\bclass\b\s+\w+', r'\breturn\b\s+', r'\bwith\b\s+\w+'],
        'Java': [r'\bpublic\b\s+\bclass\b', r'\bSystem\.out\.println\b'],
        'Php': [r'<\?php', r'\becho\b']
    }

    scores = {language: 0 for language in languages}

    for language in languages:
        scores[language] += sum(re.search(pattern, code) is not None for pattern in syntax_patterns.get(language, []))
        scores[language] += sum(keyword in code for keyword in keywords[language])

    return max(scores, key=scores.get) if scores else None

code = input("Enter the code: ")
language = detect_language(code)
if language:
    print(f"Detected language: {language}")
    tokens = lexer(code, language)
    for token in tokens:
        print(token)
else:
    print("Unable to detect language") 