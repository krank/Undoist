#coding: utf-8

import datetime

class Project:
    
    def __init__(self, name, owner):
        # Create the root item node
        self.root = Item(name, 0, False)
        # Set owner
        self.owner = owner
        
    def __str__(self):
        return unicode(self.root)
    
    def get_as_file(self):
        # Create OPML header
        output = '<?xml version="1.0" encoding="UTF-8"?> \n' \
            + '<opml version="2.0"> \n' \
            + ' <head>\n' \
            + '  <title>' + self.root.text + '</title>\n' \
            + '  <ownerName>' + self.owner + '</ownerName>\n' \
            + ' </head>\n' \
            + ' <body>\n'

        # Add OPML outline elements
        output += unicode(self)
        
        # Add OPML footer
        output += ' </body>\n' \
            + '</opml>'
        
        return unicode(output)
        
    
class Item:    
    
    def __init__(self, text, parent, indent, date=False):
        self.text = text
        self.parent = parent
        self.indent = indent
        
        # Set and parse date
        self.date = date
        if self.date:
            dt = datetime.datetime.now()
            self.date = dt.strptime(self.date, "%a %b %d %H:%M:%S %Y")
            
        # Create empty subitems list
        self.subitems = []
        
    def __str__(self):
        # Create correct indent
        indent = ' ' * self.indent
        # Generate date string
        date = ''
        if self.date:
            date = ' due="' + self.date.strftime('%Y-%m-%d') + '"'
        # Create outline XML tag
        out = indent + '<outline text="' + self.text + '" status="open"' + date
        # If there are subitems, add them.
        if len(self.subitems) > 0:
            out += '>\n'
            for item in self.subitems:
                out += unicode(item)
            out += indent + '</outline>\n'
        else:
            out += '/>\n'
        
        # Return the result
        return out
        
    # A simple adder
    def additem(self, item):
        self.subitems.append(item)