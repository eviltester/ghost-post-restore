# Ghost Post Restore

Just had that panic mode where you accidentally (or it just happened by itself) moment where you are editing a post in Ghost and all text is deleted?

Yup.

Me too.

I cobbled together this set of scripts to restore versions of Ghost blog posts from admin extract.

## How does it work?

Ghost maintains 5 or so versions of posts as it auto-saves. And these are stored in the database.

But... they are not exported when you do an export from labs.

And... there is no way to restore drafts from within Ghost itself.

These scripts use the Ghost API to issue a query on the database, extract the data with versions to a JSON file.

And then parse the file to pull out all the versions of a post ID it can find.

The information on how to do this was pulled from the docs and support forums and I've added links into the script for the sources.

## What to do if you delete a post?

This script is written in Python, so you'll need to install python.

The libraries required are in `requirements.txt` so:

`pip install requirements.txt`

or

`pip3 install requirements.txt`

Then... amend the scripts.

I've only had to do this twice so I haven't made the scripts super user-friendly.

But the edits should be simple enough.

### Export Admin Data JSON file

Amend `admin-extract.py` and change the following three lines:

```
    config['myblog']['user_name'] = ''   # add your user name here
    config['myblog']['user_password'] = ''  # add your password here
    config['myblog']['ghost_url']="https://myblog.ghost.io" # amend this to point to your ghost blog url
```


You need to add your username, password and url for the blog. And the user needs to have admin access to the blog.

So it might be:

```
    config['myblog']['user_name'] = 'adminusername@mycompany.com'   # add your user name here
    config['myblog']['user_password'] = 'theadminpassword'  # add your password here
    config['myblog']['ghost_url']="https://myblog.ghost.io" # amend this to point to your ghost blog url
```

The blog url is the url you use for Ghost admin.

And now you can create an admin extract of your posts.

```
python admin-extract.py
```

or

```
python3 admin-extract.py
```

This will create a file like `myblog_ghost_io_2022_06_22_18_00_00.json`


The filename is based on the blog url and the current date and time.

This file contains an admin extract of the blog with the versions of all the blog posts.

### Restore the Post

I then load the `.json` file into a text editor like Visual Studio code and do a text search for the title.

And I'm looking for the `id` of the post e.g.

```
{"id":"234usadfljwei2939wljrel","uuid":"1232jdfj-2k2j-23j3-34kds-34sji89","title":"My Blog Title",
```

I copy and paste the id value so I can add it to the `post-restore.py` file.


I want to amend the values of the file location and the post id.

e.g.

```
# AMEND THESE VALUES

# where is the extract file? i.e. the file written by admin-extract.py
importFilePath = cwd + '/myblog_ghost_io_2022-06-22-15-27-41.json'

# what is the post id to recover?
postId = '234usadfljwei2939wljrel'
```

Then I can run the script to restore the post versions.

`python post-restore.py`

or

`python3 post-restore.py`


### Find the right version

The script will write out all the versions it can find.

I use the `.txt` version as it is the version after all newlines etc. have been expanded and just has the content.

But the `rawcards.txt` or `.json` versions have the raw information pulled from the Admin file so if you want to do any additional processing use these.


## And That's It

I've used this twice now and it has saved me from rewrite hell.

My recommendation is to always write content in a separate system and paste it into Ghost editor, but... sometimes we need to write it quickly or we forget that things can go wrong.

I tend to write using Markdown so this is easier for me to do.

The scripts could be easier to use so if anyone wants to create pull requests then feel free.

Suggested TODOs:

- read a config file so we don't have to amend the scripts
- show a list of all extracted titles and ids so we don't have to edit the export json
- show the list as an easy to use menu for users to click the post to restore

## License

This set of scripts is MIT Licensed. Do with it what you will.


