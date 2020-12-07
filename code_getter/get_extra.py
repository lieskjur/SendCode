import re
import sublime

def filter(self,string):
    
    qm = ["\"","\'"]

    for i in range(2): #colapse strings and char. arrays
        string = re.sub(r"(\W){0}[^{0}]*{0}".format(qm[i]),r"\1{0}{0}".format(qm[i]),string)

    print(string)
    return string

def nested_skip( self,s, start,end ):
    view = self.view
    row = view.rowcol(s.begin())[0]
    lastrow = view.rowcol(view.size())[0]
    level = 0

    while row <= lastrow:

        line = view.line(view.text_point(row, 0))
        line_string = view.substr(line)

        line_string = filter(self,line_string)
        
        level += len(re.findall(r"(?:{})".format(start),line_string))
        level -= len(re.findall(r"(?:{})".format(end),line_string))
        
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

    if len(up) >= 2:
        up = "|".join(up)
    if len(dn) >= 2:
        dn = "|".join(dn)

    level = 0
    step = 0
    while ( row <= lastrow) & ( row >= 0 ):

        line = view.line(view.text_point(row, 0))
        line_string = view.substr(line)
        
        line_string = filter(self,line_string)

        level += len(re.findall(r"{0}(?:{1})".format(prefix,up),line_string))
        level -= len(re.findall(r"{0}(?:{1})".format(prefix,dn),line_string))
        
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