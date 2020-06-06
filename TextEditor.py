#!/usr/bin/env/python3
#**************************************************************
#       Author: Bakari Saidi Chanoga(Beka The Programmer)     #
#       contact: +255742863986                                #
#                +255716162784                                #
#       Email: chanogab@gmail.com                             #
#              chanogab@yahoo.com                             #
#                                                             #
#                                                             #
#**************************************************************

#import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

#**************************************************************
#               Our Class                                     #
#**************************************************************
class Texteditor(Tk):
    def __init__(self):
        super().__init__()

        #fields
        self.filename = ''
        showline = 0
        line_label = None
        text_area = None
        hltln = 0
        file_menu_bar = None
        edit_menu_bar = None
        view_menu_bar = None
        about_menu_bar = None
        
        #our window properies
        self.title('pEditor')
        self.geometry('800x600')
        self.config(bg='antique white',relief='raised',bd=7)
        #decorate window with our theme
        self.option_readfile('optionDB.txt')
        
#***************************************************************
#           Methods for Text Manipulations                      #
#***************************************************************

    #new file
    def new_file(self,event=None):
        self.title('Untitled ')
        self.filename = None
        self.text_area.delete('1.0',END)
        self.update_line_number()
        return None
    
    #open file
    def open_file(self,event=None):
        self.filename = filedialog.askopenfilename(defaultextension='.txt',filetypes = [('All Files','*.*'),
                                                                                   ('Text','*.txt'),
                                                                                   ('Python','*.py'),
                                                                                   ('C','*.c'),
                                                                                   ('C++','*.cpp'),
                                                                                   ('Java','*.java')])
        if self.filename == '':#no file selected
            self.filename = None
            
        else:
            #set path to the window
            self.title(os.path.basename(self.filename)) #return the base name of file
            #delete all existing text
            self.text_area.delete('1.0',END)

            with open(self.filename,'r') as file:
                self.text_area.insert(INSERT,file.read())
                
        return None

    #save
    def save_file(self,event=None):
        try:
            with open(self.filename,'w') as file:
                text = self.text_area.get('1.0',END)
                file.write(text)
        except:
            self.save_file_as(self.text_area)

    #save_file_as
    def save_file_as(self,event=None):
        try:
            file_name = filedialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension='.txt',filetypes=[('All Files','*.*'),
                                                                                                                   ('Text','*.txt'),
                                                                                                                   ('Python','*.py'),
                                                                                                                   ('C','*.c'),
                                                                                                                   ('C++','*.cpp'),
                                                                                                                   ('Java','*.java')])
            with open(file_name,'w') as file:
                text = self.text_area.get('1.0',END)
                file.write(text)
                self.title(os.path.basename(file_name))
        except:
            pass

        return None
    
    #cut
    def cut_method(self):
        self.text_area.event_generate('<<Cut>>')
        self.update_line_number()
        return None

    #paste
    def paste_method(self):
        self.text_area.event_generate('<<Paste>>')
        self.update_line_number()
        return None

    #copy
    def copy_method(self):
        self.text_area.event_generate('<<Copy>>')
        return None

    #undo
    def undo_method(self):
        self.text_area.event_generate('<<Undo>>')
        self.update_line_number()
        return None

    #redo
    def redo_method(self):
        self.text_area.event_generate('<<Redo>>')
        self.update_line_number()
        return None

    #select all
    def select_all(self,event=None):
        self.text_area.tag_add('sel','1.0',END)
        return None

#*********************************************************************************
#******************** Search for a given Text in the text editor *****************
#*********************************************************************************
    def on_find(self,event=None):
        pop_window = Toplevel(self)
        pop_window.title("Find")
        pop_window.geometry('320x100')
        pop_window.transient(self)

        Label(pop_window,text='Find All:',fg='yellow').grid(row=0,column=0,sticky='e')

        text_value = StringVar()
        entry = Entry(pop_window,width=25,textvariable=text_value)
        entry.grid(row=0,column=1,padx=2,pady=2,sticky='we')
        entry.config(fg='gray',bg='white',relief='sunken',bd=5)
        entry.focus_set()

        checkb_value = IntVar()
        Checkbutton(pop_window,text='Ignore Case',variable = checkb_value).grid(row=1,column=1,sticky='e',padx=2,pady=2)

        Button(pop_window,text='Find:',fg='yellow',font='Monospaced,8',underline=0,
               command=lambda:self.search_for(text_value.get(),checkb_value.get(),
                                              self.text_area,pop_window,entry)).grid(row=0,column=2,sticky='e'+'w',padx=2,pady=2)

        #close
        def close_search():
            self.text_area.tag_remove('match','1.0',END)
            pop_window.destroy()

        pop_window.protocol('WM_DELETE_WINDOW',close_search) #override close

    #search_for
    def search_for(self,needle,cssnstv,textarea,pop_menu,entry):
        textarea.tag_remove('match','1.0',END)

        count = 0

        if needle:
            pos = '1.0'
            while True:
                pos = textarea.search(needle,pos,nocase=cssnstv,stopindex = END)
                if not pos:break
                lastpos = '%s+%dc' % (pos,len(needle))
                textarea.tag_add('match',pos,lastpos)
                count += 1
                pos = lastpos
                
        textarea.tag_config('match',foreground='red',background='light gray',font='Times,16')
        entry.focus_set()
        pop_menu.title('%d Matchs found '%count)
#*******************************End Search****************************************************

#*********************************************************************************************
#        Show Line numbers when selected
#*********************************************************************************************
    def update_line_number(self,event=None):
        txt = ''
        if self.showline.get():
            endline,endcolumn = self.text_area.index('end-1c').split('.')
            txt = '\n'.join(map(str, range(1, int(endline))))

        self.line_label.config(text=txt,anchor='nw')

        return None
    
        
#***********************************************************************
#       Exit window
#**********************************************************************
    def exit_window(self,event=None):
        if self.text_area.get('1.0',END) != '':
            if messagebox.askokcancel("Quit","Are you sure!"):
                self.destroy()
        return None
#***********************************************************************
#   About,Help                                                         #
#***********************************************************************
    def about(self):
        txt = 'This is a Simple Text editor Python Program written by Bakari Saidi Chanoga'
            
        messagebox.showinfo('About:',txt)

    def help(self,event=None):
        messagebox.showinfo('Help','To Learn more www.python.org')
        return None
#*********************************************************************
#       Highlight current line                                         #
#*********************************************************************
    def highlight_line(self,interval = 100):
        self.text_area.tag_remove('active_line','1.0','end')
        self.text_area.tag_add('active_line','insert linestart','insert lineend + 1c')
        self.text_area.after(interval,self.toggle_highlight)
        return None

    def undo_highlight(self):
        self.text_area.tag_remove('active_line','1.0','end')
        return None

    def toggle_highlight(self,event=None):
        val = self.hltln.get()
        self.undo_highlight() if not val else self.highlight_line()
        self.text_area.tag_configure('active_line',background='light gray')
        return None
#*********************************************************************
#   Themes                                                           #
#*********************************************************************
    def default_theme(self):
        self.configure(bg='antique white')
        self.text_area.configure(bg='white',fg='black')
        self.file_menu_bar.config(bg='gray',fg='white')
        self.edit_menu_bar.config(bg='gray',fg='white')
        self.view_menu_bar.config(bg='gray',fg='white')
        self.about_menu_bar.config(bg='gray',fg='white')
        return None
    def greygarious_grey(self):
        self.configure(bg='#83406A')
        self.text_area.configure(bg="#83406A",fg="#D1D4D1")
        self.file_menu_bar.config(bg='light gray',fg='white')
        self.edit_menu_bar.config(bg='light gray',fg='white')
        self.view_menu_bar.config(bg='light gray',fg='white')
        self.about_menu_bar.config(bg='light gray',fg='white')
        return None
    def Vivacious_Violet(self):
        self.configure(bg="#202B4B")
        self.text_area.configure(bg="#202B4B",fg="#E1E1FF",font='Italic,16')
        self.file_menu_bar.config(bg='white',fg='black')
        self.edit_menu_bar.config(bg='white',fg='black')
        self.view_menu_bar.config(bg='white',fg='black')
        self.about_menu_bar.config(bg='white',fg='black')
        return None
    def light_green(self):
        self.configure(bg='light green')
        self.text_area.configure(bg='light green',fg='gray',font='Sans-serif,16')
        self.file_menu_bar.config(bg='light blue',fg='gray')
        self.edit_menu_bar.config(bg='light blue',fg='gray')
        self.view_menu_bar.config(bg='light blue',fg='gray')
        self.about_menu_bar.config(bg='light blue',fg='gray')
        return None
    def solarised(self):
        self.configure(bg="#5B8340")
        self.text_area.configure(bg="#5B8340",fg="#D1E7E0",font='Sans,16')
        self.file_menu_bar.config(bg='gray',fg='white')
        self.edit_menu_bar.config(bg='gray',fg='white')
        self.view_menu_bar.config(bg='gray',fg='white')
        self.about_menu_bar.config(bg='gray',fg='white')
        return None
    def Boisterous_Blue(self):
        self.configure(bg="#4B4620")
        self.text_area.configure(bg="#4B4620",fg="#FFF0E1",font='Times,18')
        self.file_menu_bar.config(bg='light gray',fg='white')
        self.edit_menu_bar.config(bg='light gray',fg='white')
        self.view_menu_bar.config(bg='light gray',fg='white')
        self.about_menu_bar.config(bg='light gray',fg='white')
        return None
    def school_green(self):
        self.configure(bg="#202B4B")
        self.text_area.configure(bg="#D1E7E0",fg="#5B8340",font='Monospaced,16')
        self.file_menu_bar.config(bg='light blue',fg='gray')
        self.edit_menu_bar.config(bg='light blue',fg='gray')
        self.view_menu_bar.config(bg='light blue',fg='gray')
        self.about_menu_bar.config(bg='light blue',fg='gray')
    
    #file menu bar
    def fileMenuBar(self):
        self.file_menu_bar = Menubutton(self,text=' File')
        self.file_menu_bar.config(bg='gray',fg='white')
        #file menu
        self.file_menu = Menu(self.file_menu_bar,tearoff=0)
        #add menu items to the file menu bar
        self.file_menu.add_command(label='New',compound=LEFT,accelerator='Ctrl+N',command=self.new_file)
        self.file_menu.add_command(label='Open',compound=LEFT,accelerator='Ctrl+O',command=self.open_file)
        self.file_menu.add_command(label='Save',compound=LEFT,accelerator='Ctrl+S',command=self.save_file)
        self.file_menu.add_command(label='Save as',compound=LEFT,accelerator='Ctrl+Shift+S',command=self.save_file_as)
        self.file_menu.add_command(label='Print',compound=LEFT,accelerator='Ctrl+P')
        self.file_menu.add_command(label='Exit',compound=LEFT,accelerator='Ctrl+Q',command = self.exit_window)
        #add menu file to menu bar
        self.file_menu_bar.config(menu = self.file_menu)
        self.file_menu_bar.pack(side=RIGHT,expand=False,fill=None)
        return self.file_menu_bar

    #edit menu bar
    def editMenuBar(self):
        self.edit_menu_bar = Menubutton(self,text=' Edit')
        self.edit_menu_bar.config(bg='gray',fg='white')
        #edit menu
        self.edit_menu = Menu(self.edit_menu_bar,tearoff=0)
        #add menu items
        self.edit_menu.add_command(label='Undo',compound=LEFT,accelerator='Ctrl+Z',command=self.undo_method)
        self.edit_menu.add_command(label='Redo',compound=LEFT,accelerator='Ctrl+Y',command=self.redo_method)
        self.edit_menu.add_command(label='Copy',compound=LEFT,accelerator='Ctrl+C',command=self.copy_method)
        self.edit_menu.add_command(label='Paste',compound=LEFT,accelerator='Ctrl+V',command=self.paste_method)
        self.edit_menu.add_command(label='Cut',compound=LEFT,accelerator='Ctrl+X',command=self.cut_method)
        self.edit_menu.add_command(label='Find All',compound=LEFT,accelerator='Ctrl+F',command=self.on_find)
        self.edit_menu.add_command(label='Select All',compound=LEFT,accelerator='Ctrl+A',command=self.select_all)
        #add edit menu to menu bar
        self.edit_menu_bar.config(menu = self.edit_menu)
        self.edit_menu_bar.pack(side=RIGHT)
        return self.edit_menu_bar

    #view menu bar
    def viewMenuBar(self):
        self.view_menu_bar = Menubutton(self,text = 'View')
        self.view_menu_bar.config(bg='gray',fg='white')
        #view menu
        self.view_menu = Menu(self.view_menu_bar,tearoff=0)
        #add menu items
        self.showline = IntVar()
        self.showline.set(0)
        self.hltln = IntVar()
        self.view_menu.add_checkbutton(label='Show Line Number',variable=self.showline,command=self.update_line_number)
        #self.view_menu.add_checkbutton(label='Show Info Bar at Bottom')
        self.view_menu.add_checkbutton(label='Highlit Current Line',onvalue=1,offvalue=0,variable=self.hltln,command=self.toggle_highlight)
        #add cascade menu
        self.theme_menu = Menu(self.view_menu,tearoff=0)
        self.view_menu.add_cascade(label='Themes',menu = self.theme_menu)
        self.theme_menu.add_radiobutton(label='1.Default ',command=self.default_theme)
        self.theme_menu.add_radiobutton(label='2.Greygarious Grey',command=self.greygarious_grey)
        self.theme_menu.add_radiobutton(label='3.Vivacious Violet',command=self.Vivacious_Violet)
        self.theme_menu.add_radiobutton(label='4.Light Green',command=self.light_green)
        self.theme_menu.add_radiobutton(label='5.Solarised',command=self.solarised)
        self.theme_menu.add_radiobutton(label='6.Boisterous Blue',command=self.Boisterous_Blue)
        self.theme_menu.add_radiobutton(label='7.School Green',command=self.school_green)
        #add menu to menu bar
        self.view_menu_bar.config(menu = self.view_menu)
        self.view_menu_bar.pack(side=RIGHT)
        return self.view_menu_bar

    #about menu bar
    def aboutMenuBar(self):
        self.about_menu_bar = Menubutton(self,text='About')
        self.about_menu_bar.config(bg='gray',fg='white')
        #about menu
        self.about_menu = Menu(self.about_menu_bar,tearoff = 0)
        #add items to the about menu
        self.about_menu.add_command(label='About',command=self.about)
        self.about_menu.add_command(label='Help',command=self.help)
        #add about menu to the about menu bar
        self.about_menu_bar.config(menu = self.about_menu)
        #position about menu bar
        #self.about_menu_bar.pack(side=TOP,anchor='nw')
        self.about_menu_bar.pack(side=RIGHT)
        return self.about_menu_bar

#************************************************************************
#       Display Line Numbers                                            #
#************************************************************************
    #show line numbers
    def lineNumber(self):
        self.line_label = Label(self,width=3,bg='antique white')
        self.line_label.pack(side=LEFT,expand=False,fill=Y)
        Label(self,text='Chanogab',bg='antique white',fg='white',font='Times,5').pack(side=BOTTOM,anchor='se')
        return self.line_label

        
#*********************************************************************
#       Text Area,ScrollBar,MenuBar,Menus and Menu Items             #
#*********************************************************************
    #text area
    def text_area_method(self):
        self.text_area = Text(self,undo=True)
        self.text_area.pack(side=BOTTOM,expand=True,fill=BOTH)
        self.text_area.config(relief='sunken',bd=7)
        self.text_area.bind('<<Any-KeyPress>>',self.update_line_number)
        #scrollBar
        self.scroll_bar = Scrollbar(self.text_area)
        #vertical scroll
        self.text_area.config(yscrollcommand= self.scroll_bar.set)
        self.scroll_bar.config(command = self.text_area.yview)
        self.scroll_bar.pack(side=RIGHT,fill=Y)
        #key bingind
        self.text_area.bind("<Button-3>",self.popup)
        self.text_area.bind("<Control-N>",self.new_file)
        self.text_area.bind("<Control-n>",self.new_file)
        self.text_area.bind("<Control-O>",self.open_file)
        self.text_area.bind("<Control-o>",self.open_file)
        self.text_area.bind("<Control-F>",self.on_find)
        self.text_area.bind("<Control-f>",self.on_find)
        self.text_area.bind("<Control-S>",self.save_file)
        self.text_area.bind("<Control-s>",self.save_file)
        self.text_area.bind("<Control-Shift-S>",self.save_file_as)
        self.text_area.bind("<Control-Shift-s>",self.save_file_as)
        self.text_area.bind("<Control-A>",self.select_all)
        self.text_area.bind("<Control-a>",self.select_all)
        self.bind("<Control-Q>",self.exit_window)
        self.bind("<Control-q>",self.exit_window)
        return self.text_area

    #***********************Poppup Menu*****************
    def popup(self,event):
        pop_menu = Menu(self.text_area,tearoff=0)
        pop_menu.add_command(label="Cut",compound=LEFT,command=self.cut_method)
        pop_menu.add_command(label="Copy",compound=LEFT,command=self.copy_method)
        pop_menu.add_command(label="Paste",compound=LEFT,command=self.paste_method)
        pop_menu.add_command(label="Undo",compound=LEFT,command=self.undo_method)
        pop_menu.add_command(label="Redo",compound=LEFT,command=self.redo_method)
        pop_menu.add_separator()
        pop_menu.add_command(label='Select All',underline=7,command=self.select_all)

        self.text_area.bind("<Button-3>",pop_menu.tk_popup(event.x_root,event.y_root,0))
        return None
    

#***********************************************************************
#           Finally, God is Good All the Time                           #
#***********************************************************************
    
if __name__ == '__main__':
    texteditor = Texteditor()
    #invoking methods
    texteditor.lineNumber()
    texteditor.text_area_method()
    texteditor.aboutMenuBar()
    texteditor.viewMenuBar()
    texteditor.editMenuBar()
    texteditor.fileMenuBar()
    
    
    
    
        
