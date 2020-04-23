import pdftotext



COLUMN_WIDTH = 64

class Page:
    
    
    def __init__(self, page_string, skip = 'skip this line', bulletpoint_format = True):
        '''
        skip: skip line in output if page contains string, e.g., ' / 10' as page label
        '''
        self.page_string = page_string
        self.lines = self.page_string.replace('  ','').split('\n')
        self.parsed = self.lines
        self.skip = skip
        self.bulletpoint_format = bulletpoint_format
    
    def makeTitle(self):
        self.title = '##### ' + self.lines[0]
        temp = self.lines
        temp[0] = self.title
        self.parsed = temp
        return self
        
    def parsePage(self):
        string = ''
        
        for line in self.parsed:
            
            not_skipped = True
            new_line = True
            is_list_item = False
            
            if line == '':
                not_skipped = False
            
            if type(self.skip) == list:
                for skipping_item in self.skip:
                    if skipping_item in line:
                        not_skipped = False
            else:
                if self.skip in line:
                    not_skipped = False
                
            if not_skipped == True:
                curr_line = Line(line.replace('↵',''))
                temp = line
                
                if self.bulletpoint_format == True:
                
                    if temp.lstrip(' ')[0] == 'I' or temp.lstrip(' ')[1] == '.':
                        is_list_item = True
                        curr_line.makeListItem()
                    elif len(line) < COLUMN_WIDTH:
                        new_line = False

                    curr_line = curr_line.parsed

                    if new_line == True:
                        string += '\n' + curr_line
                    else:
                        string += curr_line
                
                else: 
                    
                    string += '\n' + line
        
        self.parsed = string
        return self
    
    
class Line:
    
    
    def __init__(self, line_string):
        self.line_string = line_string
        self.parsed = line_string
    
    def makeListItem(self):
        self.parsed = self.parsed.replace('I ', '- ')
        return self
    
    
class PDF:
    
    
    def __init__(self, file, pw='', skip='skip this line', manual=False, bulletpoint_format=True):
        self.file = file
        self.pw = pw
        
        with open(file, "rb") as f:
            if self.pw != '':
                pdf = pdftotext.PDF(f, self.pw)
            else:
                pdf = pdftotext.PDF(f)
            
        self.pdf = pdf
        self.n_pages = len(pdf)
        self.manual = manual
        self.bulletpoint_format = bulletpoint_format
        self.skip = skip
        
    def parsePDF(self):
        
        if self.manual is False:
            for page in self.pdf:
                cur_page = Page(page, self.skip, bulletpoint_format=self.bulletpoint_format)
                cur_page = cur_page.makeTitle()
                cur_page = cur_page.parsePage()
                print(cur_page.parsed)
        else:
            for i, page in enumerate(self.pdf):
                satisfied = False
                while not satisfied:
                    print('\n------------processing page %i / %i------------\n'%(i+1, self.n_pages))
                    skip = input('skip lines containing the following (separate multiple with ";"):')
                    skip = skip.split(';')
                    bulletpoint_format = input('modify format (T: bulletpoint_format / F: original document):')
                    if bulletpoint_format == 'T':
                        bulletpoint_format = True
                    else:
                        bulletpoint_format = False
                    cur_page = Page(page, skip, bulletpoint_format)
                    cur_page = cur_page.makeTitle()
                    cur_page = cur_page.parsePage()
                    print('\n ------------OUTPUT------------ \n')
                    print(cur_page.parsed)
                    print('\n--------------------------------\n')
                    ok = input('satisfied? (y/n):')
                    if ok == 'y':
                        print('ok, start with the next page!')
                        satisfied = True
                    else:
                        print('\n------------redo durrent page------------\n')


if __name__ == "__main__":
    
    filename = input('filename: ')
    pw = str(input('password (if any): ') or '')
    manual = 0
    
    while manual != 'T' and manual != 'F':
        manual = input('go through document page by page with individual parameters (T: yes / F: no, leave blank for false): ') or 'F'
    
    if manual == 'T':
        PDF(filename, pw, 'skip this line', True).parsePDF()
    elif manual == 'F':
        skip = str(input('skip lines containing the following (separate multiple with ";"): ') or 'skip this line')
        bulletpoint_format = input('modify format (T: bulletpoint_format / F: original document): ')
        if bulletpoint_format == 'T':
            bulletpoint_format = True
        else:
            bulletpoint_format = False
        PDF(filename, pw, skip, False, bulletpoint_format).parsePDF()





