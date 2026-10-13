# build index.html from tools/template.html reusing DATA + SHEET_URL + head from current index.html (no image work)
import re, sys
R = sys.argv[1]
idx = open(f'{R}/index.html').read(); t = open(f'{R}/tools/template.html').read()
head = idx[:idx.index('<title>')]
data = re.search(r'const DATA = (.*?);\nconst BOOKS', idx, re.S).group(1)
url = re.search(r"const SHEET_URL = '([^']*)'", idx).group(1)
body = t.replace('/*DATA*/', data, 1).replace('/*SHEET_URL*/', url)
body = body.replace('</style>\n\n', '</style>\n<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n\n\n', 1)
gen = head + body + '\n</body>\n</html>\n'
if len(sys.argv) > 2 and sys.argv[2] == 'check': print('identical' if gen == idx else 'DIFFERENT'); sys.exit()
open(f'{R}/index.html', 'w').write(gen); print('wrote', len(gen))
