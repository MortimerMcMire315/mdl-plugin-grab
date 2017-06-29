from bs4 import BeautifulSoup
import requests
import zipfile
import os

'''
Must run this from a directory right under the main moodle dir.
'''

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def main(plugin_ls, desired_version):
    for plugin in plugin_ls:
        r = requests.get("https://moodle.org/plugins/pluginversions.php?plugin=" + plugin)
        if r.status_code != 200:
            print("Plugin download page could not be found for plugin: " + plugin)
            continue

        zip_url = find_plugin_zip_url(r.text, desired_version)
        if zip_url is None:
            print("A version of %s supporting Moodle %s could not be found." % (plugin, desired_version))
        else:
            print("Downloading %s ..." % plugin)
            zipname = download_file(zip_url)

            zip_ref = zipfile.ZipFile(zipname, 'r')
            folder_to_dump_in = '../' + PLUGIN_DIRS[plugin.split('_')[0]]
            print("Moving %s to %s ..." % (plugin, folder_to_dump_in))
            zip_ref.extractall(folder_to_dump_in)
            zip_ref.close()

def find_plugin_zip_url(html, desired_version):
    soup = BeautifulSoup(html, "html.parser")
    versions = soup.find_all(class_="versions-item")

    for version_row in versions:
        version_num_span = version_row.find(class_="moodleversions")

        if version_num_span is None:
            continue

        version_nums = version_num_span.text.replace("Moodle","").replace(" ","").split(',')
        if desired_version in version_nums:
            # do stuff
            download_link = version_row.find('a', class_="download")
            if download_link is None:
                print("Error finding download link.")
                continue
            else:
                naked_link = download_link.get('href')
                return naked_link
    return None

PLUGIN_DIRS = { 'mod' : 'mod'
              , 'antivirus' : 'lib/antivirus'
              , 'assignsubmission' : 'mod/assign/submission'
              , 'assignfeedback' : 'mod/assign/feedback'
              , 'booktool' : 'mod/book/tool'
              , 'datafield' : 'mod/data/field'
              , 'datapreset' : 'mod/data/preset'
              , 'ltisource' : 'mod/lti/source'
              , 'fileconverter' : 'files/converter'
              , 'ltiservice' : 'mod/lti/service'
              , 'quiz' : 'mod/quiz/report'
              , 'quizaccess' : 'mod/quiz/accessrule'
              , 'scormreport' : 'mod/scorm/report'
              , 'workshopform' : 'mod/workshop/form'
              , 'workshopallocation' : 'mod/workshop/allocation'
              , 'workshopeval' : 'mod/workshop/eval'
              , 'block' : 'blocks'
              , 'qtype' : 'question/type'
              , 'qbehaviour' : 'question/behaviour'
              , 'qformat' : 'question/format'
              , 'filter' : 'filter'
              , 'editor' : 'lib/editor'
              , 'atto' : 'lib/editor/atto/plugins'
              , 'tinymce' : 'lib/editor/tinymce/plugins'
              , 'enrol' : 'enrol'
              , 'auth' : 'auth'
              , 'tool' : 'admin/tool'
              , 'logstore' : 'admin/tool/log/store'
              , 'availability' : 'availability/condition'
              , 'calendartype' : 'calendar/type'
              , 'message' : 'message/output'
              , 'format' : 'course/format'
              , 'dataformat' : 'dataformat'
              , 'profilefield' : 'user/profile/field'
              , 'report' : 'report'
              , 'coursereport' : 'course/report'
              , 'gradeexport' : 'grade/export'
              , 'gradeimport' : 'grade/import'
              , 'gradereport' : 'grade/report'
              , 'gradingform' : 'grade/grading/form'
              , 'mnetservice' : 'mnet/service'
              , 'webservice' : 'webservice'
              , 'repository' : 'repository'
              , 'portfolio' : 'portfolio'
              , 'search' : 'search/engine'
              , 'media' : 'media/player'
              , 'plagiarism' : 'plagiarism'
              , 'cachestore' : 'cache/stores'
              , 'cachelock' : 'cache/locks'
              , 'theme' : 'theme'
              , 'local' : 'local'
              , 'assignment' : 'mod/assignment/type'
              , 'report' : 'admin/report'
              }

plugin_ls = [ 'mod_oublog'
            , 'mod_journal'
            , 'block_progress'
            , 'theme_essential'
            , 'mod_attendance'
            , 'mod_checklist'
            , 'mod_dialogue'
            , 'mod_hotpot'
            , 'mod_questionnaire'
            , 'mod_turnitintool'
            , 'mod_turnitintooltwo'
            , 'block_attendance'
            , 'block_checklist'
            , 'block_dedication'
            , 'block_fbcomments'
            , 'block_wikipedia'
            , 'report_overviewstats'
            , 'repository_evernote'
            , 'theme_aardvark'
            ]

#e.g. 3.2, 3.1, 2.9, etc.. Three-part version numbers (e.g. 3.1.7) won't work.
desired_version = "3.2"

main(plugin_ls, desired_version)
