import re

from bs4 import BeautifulSoup

with open('usda_components.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    print(soup)
    
    raw_components = soup.find_all('span', class_= 'mat-option-text')
    
    components = []
    for component in raw_components:
        components.append(re.sub("\\s\\([^)]+\\)$","", component.text.strip()).strip())
        
    print(components)

