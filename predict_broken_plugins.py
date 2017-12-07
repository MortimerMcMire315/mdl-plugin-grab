#!/usr/bin/python3

from bs4 import BeautifulSoup
from get_installed_plugins import list_plugins
from grab_plugin import find_plugin_zip_url
import requests, os, sys, re

IGNORE = [ 'theme_bootstrap'
         , 'theme_bootstrapbase'
         ]

def main(html_file, old_version, new_version, human_readable):
    plugin_ls = list_plugins(html_file)
    for plugin in plugin_ls:
        if plugin not in IGNORE:
            print_if_not_exists(plugin, new_version, human_readable)

def print_if_not_exists(plugin, desired_version, human_readable):
    r = requests.get("https://moodle.org/plugins/pluginversions.php?plugin=" + plugin)
    if r.status_code != 200:
        #print("Plugin download page could not be found for plugin: " + plugin)
        #print(plugin)
        return
    if not find_plugin_zip_url(r.text, desired_version):
        #print("A version of %s supporting Moodle %s could not be found." % (plugin, desired_version))
        if human_readable:
            soup = BeautifulSoup(r.text, "html.parser")
            human_name = soup.find(id="region-main").find_all('h2', class_="title")[0].find_all('a')[0].text
            print(plugin + " (" + human_name + ")")
        else:
            print(plugin)

def sanity():
    if len(sys.argv) < 4:
        print("Usage: " + sys.argv[0] + " HTML OLDVERSION NEWVERSION [-h]")
        print("   where:")
        print("       HTML is a dump of the /admin/plugins.php page,")
        print("       OLDVERSION is the old Moodle version (e.g. 3.2)")
        print("       NEWVERSION is the new Moodle version (e.g. 3.3)")
        print("")
        print("   -h  Human-readable output (titles of plugins rather than technical names)")
        exit(1)

    html_file=sys.argv[1]
    old_version=sys.argv[2]
    new_version=sys.argv[3]
    if not re.match(r'^[0-9]\.[0-9]$', str(old_version)) or not re.match(r'^[0-9]\.[0-9]$', str(new_version)):
        print("Version numbers must be of the format X.Y, "
               "where X and Y are integers between 0 and 9.")
        exit(1)

    if not os.path.isfile(html_file):
        print("File not found: " + html_file)
        exit(1)

    human_readable = False

    if len(sys.argv) == 5:
        if sys.argv[4] == '-h':
            human_readable = True

    main(html_file, old_version, new_version, human_readable)

if __name__ == "__main__":
    sanity()
