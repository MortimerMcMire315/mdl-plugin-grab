from bs4 import BeautifulSoup
import os, sys, re

def list_plugins(f):
    plugin_names = []
    with open(f, 'r') as html_file:
        text = html_file.read()
        soup = BeautifulSoup(text, "html.parser")
        plugin_table = soup.find(id="plugins-control-panel")
        for row in plugin_table.find_all('tr'):
            row_classes = row.get('class')
            if not row_classes:
                continue
            if 'disabled' in row_classes:
                continue
            for row_class in row_classes:
                if re.match(r'name-',row_class):
                    plugin_names.append(re.sub(r'name-(.+)',r'\1',row_class))
    return(plugin_names)

def sanity():
    if len(sys.argv) is not 2:
        print("Usage: " + sys.argv[0] + " HTML")
        print("   where:")
        print("       HTML is a dump of the /admin/plugins.php page,")
        exit(1)

    html_file=sys.argv[1]
    if not os.path.isfile(html_file):
        print("File not found: " + html_file)
        exit(1)

    for i in list_plugins(html_file):
        print(i)

if __name__ == "__main__":
    sanity()
