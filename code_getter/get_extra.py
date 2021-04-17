import re
import sublime

class GetExtra:
    def collapse_quoted(string):
        qm = ["\"","\'"]
        for i in range(2): #collapse strings and char. arrays
            string = re.sub(r"(\W){0}[^{0}]*{0}".format(qm[i]),r"\1{0}{0}".format(qm[i]),string)
        return string

    def filter_comments(string,cmt_symb):
        string = re.sub(r"(.*){0}.*$".format(cmt_symb),r"\1{0}".format(cmt_symb),string)
        return string

    def nested_skip( self,s, start,end, prefix="",suffix="" ):
        view = self.view
        row = view.rowcol(s.begin())[0]
        lastrow = view.rowcol(view.size())[0]
        level = 0

        while row <= lastrow:

            line = view.line(view.text_point(row, 0))
            line_string = view.substr(line)

            line_string = collapse_quoted(line_string)
            
            level += len(re.findall(r"{0}(?:{1}){2}".format(prefix,start,suffix),line_string))
            level -= len(re.findall(r"{0}(?:{1}){2}".format(prefix,end,suffix),line_string))

            #print(row,": ",level)
            if level == 0:
                s = sublime.Region(s.begin(), line.end())
                break

            row += 1

        return s

    def reversible_matching( self,s, up,dn, cmt_symb, prefix="",suffix="" ):
        view = self.view
        row = view.rowcol(s.begin())[0]
        lastrow = view.rowcol(view.size())[0]

        if isinstance(up,list):
            up = "|".join(up)
        if isinstance(dn,list):
            dn = "|".join(dn)

        level = 0
        step = 0
        while ( row <= lastrow) & ( row >= 0 ):

            line = view.line(view.text_point(row, 0))
            line_string = view.substr(line)
            
            line_string = collapse_quoted(line_string)
            line_string = filter_comments(line_string,cmt_symb)

            level += len(re.findall(r"{0}({1}){2}".format(prefix,up,suffix),line_string))
            level -= len(re.findall(r"{0}({1}){2}".format(prefix,dn,suffix),line_string))
            
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