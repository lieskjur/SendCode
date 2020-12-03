import re
import sublime

def nested_skip( self,s, start,end ):
    view = self.view
    row = view.rowcol(s.begin())[0]
    lastrow = view.rowcol(view.size())[0]
    level = 0

    while row <= lastrow:

        line = view.line(view.text_point(row, 0))
        level += len(re.findall(r"(?:{})".format(start),view.substr(line)))
        level -= len(re.findall(r"(?:{})".format(end),view.substr(line)))
        
        #print(row,": ",level)
        row += 1

        if level == 0:
            s = sublime.Region(s.begin(), line.end())
            break

    return s

def reversible_matching( self,s, up,dn, prefix="" ):
    view = self.view
    row = view.rowcol(s.begin())[0]
    lastrow = view.rowcol(view.size())[0]
    level = 0

    if len(up) >= 2:
        up = "|".join(up)
    if len(dn) >= 2:
        dn = "|".join(dn)
    
    step = 0
    while ( row <= lastrow) & ( row >= 0 ):

        line = view.line(view.text_point(row, 0))
        level += len(re.findall(r"{0}(?:{1})".format(prefix,up),view.substr(line)))
        level -= len(re.findall(r"{0}(?:{1})".format(prefix,dn),view.substr(line)))
        
        sign = (level > 0) - (level < 0)
        if sign:
            step = sign
        #print(row+1,": ",level,": ",step)
        row += step

        if level == 0:
            if step == 1:
                s = sublime.Region(s.begin(), line.end())
            elif step == -1:
                s = sublime.Region(line.begin(),s.end())
            break

    return s