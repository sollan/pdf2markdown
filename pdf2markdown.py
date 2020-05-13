import pdftotext



COLUMN_WIDTH = 64

class Page:
    
    
    def __init__(self, page_string, skip = 'skip this line', bulletpoint_format = True, bullet = '', merge_lines = True, width = COLUMN_WIDTH):
        '''
        skip: skip line in output if page contains string, e.g., ' / 10' as page label
        '''
        self.page_string = page_string
        self.lines = self.page_string.replace('  ','').split('\n')
        self.parsed = self.lines
        self.skip = skip
        self.bulletpoint_format = bulletpoint_format
        self.bullet = bullet
        self.merge_lines = merge_lines
        self.width = width
    
    def makeTitle(self):
        self.title = '\n##### ' + self.lines[0]
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
                curr_line = Line(line.replace('↵',''), self.bullet)
                temp = line
                
                if self.bulletpoint_format == True:
                
                    try: 
                        if (temp.lstrip(' ')[0] == self.bullet)  or  (temp.lstrip(' ')[1] == self.bullet)  or  (temp.lstrip(' ')[1] == '.') :
                            is_list_item = True
                            curr_line.makeListItem()
                        elif (len(line) < self.width) and (self.merge_lines is True):
                            new_line = False

                    except IndexError:
                        if (len(line) < self.width) and (self.merge_lines is True):
                            new_line = False


                    curr_line = curr_line.parsed

                    if new_line == True:
                        string += '\n' + curr_line + ' '
                    else:
                        string += curr_line + ' '
                
                else: 
                    
                    string += '\n' + line + ' '
        
        self.parsed = string
        return self
    
    
class Line:
    
    
    def __init__(self, line_string, bullet):
        self.line_string = line_string
        self.parsed = line_string
        self.bullet = bullet

    def makeListItem(self):
        self.parsed = self.parsed.replace(self.bullet, '- ')
        return self
    
    
class PDF:
    
    
    def __init__(self, file, pw='', skip='skip this line', manual=False, bulletpoint_format=True, outfile='output.txt', bullet='- ', merge_lines=False, width = COLUMN_WIDTH):
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
        self.outfile = outfile
        self.bullet = bullet
        self.merge_lines = merge_lines
        self.width = width
        
    def parsePDF(self):
        
        if self.manual is False:
            
            with open(outfile, 'w') as output:

                for page in self.pdf:
                    output.write('\n')
                    cur_page = Page(page, self.skip, bulletpoint_format=self.bulletpoint_format, bullet=self.bullet, merge_lines=self.merge_lines, width = self.width)
                    cur_page = cur_page.makeTitle()
                    cur_page = cur_page.parsePage()
                    print(cur_page.parsed)
                    for parsed_line in cur_page.parsed:
                        output.write(parsed_line)
                
        else:
            for i, page in enumerate(self.pdf):
                with open(outfile, 'w') as output:
                    satisfied = False
                    while not satisfied:
                        print('\n------------processing page %i / %i------------\n'%(i+1, self.n_pages))


                        skip = str(input('skip lines containing the following (separate multiple with ";"), default "skip this line": ') or 'skip this line')
                        skip = skip.split(';')

                        merge_lines = input('merge broken lines? (T: yes -> form paragraphs, default / F: no, leave as they exist in the pdf): ') or 'T'
                        if merge_lines == 'F':
                            merge_lines = False
                        else:
                            merge_lines = True
                        
                        bulletpoint_format = input('modify format (T: bulletpoint_format, default / F: original document): ') or 'T'
                        if bulletpoint_format == 'T':
                            bulletpoint_format = True
                            bullet = str(input('identifier for bullet point: ') or '- ')
                        else:
                            bulletpoint_format = False
                            bullet = '- '

                        width = int(input('merge lines shorter than (max no. of characters): ') or 64)

                        cur_page = Page(page, skip, bulletpoint_format, bullet, merge_lines, width)
                        cur_page = cur_page.makeTitle()
                        cur_page = cur_page.parsePage()
                        print('\n ------------OUTPUT------------')
                        print(cur_page.parsed)
                        print('\n--------------------------------\n')
                        ok = input('satisfied? (y/n):')
                        if ok == 'y':
                            output.write('\n')
                            for parsed_line in cur_page.parsed:
                                output.write(parsed_line)
                            print('ok, start with the next page!')
                            satisfied = True
                        else:
                            print('\nRedo current page.')


if __name__ == "__main__":
    
    filename = input('filename: ')
    pw = str(input('password (if any): ') or '')
    manual = 0
    outfile = str(input('save as (default output.txt)') or 'output.txt')
    manual = input('go through document page by page with individual parameters (T: yes / F: no, default): ') or 'F'
    

    if manual == 'T':

        PDF(filename, pw, 'skip this line', True).parsePDF()

    elif manual == 'F':
        
        width = int(input('merge lines shorter than (max no. of characters): ') or COLUMN_WIDTH)

        skip = str(input('skip lines containing the following (separate multiple with ";"), default "skip this line": ') or 'skip this line')
        skip = skip.split(';')

        merge_lines = input('merge broken lines? (T: yes -> form paragraphs, default / F: no, leave as they exist in the pdf): ') or 'T'
        if merge_lines == 'F':
            merge_lines = False
        else:
            merge_lines = True
        
        bulletpoint_format = input('modify format (T: bulletpoint_format, default / F: original document): ') or 'T'
        if bulletpoint_format == 'T':
            bulletpoint_format = True
            bullet = str(input('identifier for bullet point: ') or '- ')
        else:
            bulletpoint_format = False

        PDF(filename, pw, skip, False, bulletpoint_format, outfile, bullet, merge_lines, width).parsePDF()