
import json
import os

from datetime import datetime


# based on code found in ghost forum https://forum.ghost.org/t/api-db-access-point/22250


cwd = os.getcwd()

# AMEND THESE VALUES

# where is the extract file? i.e. the file written by admin-extract.py
importFilePath = cwd + '/myblog_ghost_io_2022-06-22-15-27-41.json'

# what is the post id to recover?
postId = '62b31eb2e72cab003d2f80b0'


def write_json(f_path, nameprefix, data):
    now = datetime.now().utcnow()
    f_name = now.strftime(
        '{}/{}.json'.format(
            f_path, nameprefix))
    with open(f_name, 'w') as f:
        json.dump(data, f)


def write_file(f_path, nameprefix, data):
    now = datetime.now().utcnow()
    f_name = now.strftime(
        '{}/{}.txt'.format(
            f_path, nameprefix))
    with open(f_name, 'w') as f:
        f.write(data)



data = {}
with open(importFilePath) as f:
    data = json.load(f) 

revisions = data['db'][0]['data']['mobiledoc_revisions']
print(len(revisions))



for revision in revisions:
    if revision['post_id'] == postId:
        mobileDoc = json.loads(revision['mobiledoc'])

        rawcards = ""
        output = ""
        for card in mobileDoc['cards']:
            rawcards = rawcards + repr(card) + "\n"
            try:
                markdownContent = card[1]['markdown']
                markdownContent = markdownContent.replace("\\n","\n")
                output = output + markdownContent + "\n"
            except:
                print("Error processing card outputing raw card")
                output = output + repr(card) + "\n"
        
        write_json(cwd, revision['post_id'] + "-" + str(revision['created_at_ts']), revision)
        write_file(cwd, revision['post_id'] + "-" + str(revision['created_at_ts']), output)
        write_file(cwd, revision['post_id'] + "-" + str(revision['created_at_ts']) + "-rawcards", rawcards)