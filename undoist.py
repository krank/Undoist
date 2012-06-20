#coding: utf-8

from todoist.base import StandardAPI
from undoist_c import *
import argparse

# Create an argument parser
parser = argparse.ArgumentParser()
# Add a description
parser.description = "Utility to download projects and items from a Todoist.com account and save them as OPML files."
# Add some arguments
parser.add_argument("email", type=str,
                    help="Your Todoist.com username.")
parser.add_argument("password", type=str,
                    help="Your Todoist.com password.")
parser.add_argument("-e", "--include_empty", help="Include projects reported as empty.", action="store_true")
# Parse the arguments
args = parser.parse_args()


# Set options
IGNORE_EMPTY_CACHED = not args.include_empty

# Set login info
EMAIL = args.email
PASS = args.password

# Try to login
print "--- Logging in..."
api = StandardAPI()
login = api.login(email = EMAIL, password = PASS)

def addToProject(itemlist, project):
    # Set initial root
    current_root = project.root
    
    # And initial level
    current_indent = 1
    
    # Last item added
    last_item = False
    
    # Go through all items
    for item in items:
        # If the item's indent is larger than the current root's,
        #  set the last item as root, meaning this item will be added as a subitemt o the last.
        if item['indent'] > current_indent:
            current_root = last_item
            current_indent += 1
            
        # if the item's ident is smaller than the current root's,
        #  go down through the tree until it matches
        while item['indent'] < current_indent:
            current_root = current_root.parent
            current_indent -= 1
    
        # Create the item and add it to the current root.
        last_item = Item(item[u'content'],current_root, current_indent, item[u'due_date'])
        current_root.additem(last_item)

# Check if login attempt was successful
if login == "LOGIN_ERROR":
    print "Username/password incorrect"
else:
    # LOGGED IN
    ownername = login['full_name']
    print "Successfully logged in as " + ownername
    
    # Create empty list of projects
    projects = []
    
    
    # Get list of all projects
    print "--- Retrieving projects..."
    remote_projects = api.get_projects()
    print str(len(remote_projects)) + " projects retrieved."
    
    print "--- Adding items..."
    
    i = 0
    for project in remote_projects:

        i += 1
        
        count = "[" + str(i) + "/" + str(len(remote_projects)) + "] "
        
        if project[u'cache_count'] == 0 and IGNORE_EMPTY_CACHED:
            print count + project[u'name'] + " appeared empty, ignored."
        
        else:
            # Create a new Project instance
            current_project = Project(project[u'name'], ownername)

            
        
            # Get all of the project's items
            items = api.get_uncompleted_items(project_id=project[u'id'])
            
            # Add the items to the project
            addToProject(items, current_project)
            
            # Append the new instance to the list
            projects.append(current_project)
            print count + project[u'name'] + " added."
            
    
    print "---Exporting to files..."
    
    # Go through the projects
    for project in projects:
        # Create the filename (consisting only of letters and numbers
        filename = "".join([x for x in project.root.text if x.isalpha() or x.isdigit()]) + ".xml"
        
        # Open the file
        fp = open(filename, 'w')
        # Encode the text as UTF-8
        s = project.get_as_file().encode('utf-8')
        # Write the text and close the file
        fp.write(s)
        fp.close()
        
        print "wrote " + filename
    
    print "--- Finished!"



#DOCUMENTATION OF TODOIST THINGS:
    
#USER:
#date_format
#start_day
#notifo
#start_page
#last_used_ip
#twitter
#mobile_number
#premium_until
#tz_offset
#email
#time_format
#msn
#join_date
#sort_order
#default_reminder
#full_name
#api_token
#mobile_host
#timezone
#jabber
#id
    
#PROJECT:
#last_updated
#name
#user_id
#color
#collapsed
#archived_date
#item_order
#indent
#is_archived
#archived_timestamp
#cache_count
#id

#ITEM:
#due_date
#item_order
#checked
#user_id
#mm_offset
#collapsed
#labels
#date_string
#in_history
#id
#content
#is_dst
#has_notifications
#is_archived
#indent
#project_id
#children
#priority