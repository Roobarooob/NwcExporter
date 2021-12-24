import os
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import shutil

srv_vers="2019"
srv_ip = "192.168.123.21"
download_dir = "C:/Test"
finpath = 'S:/_18_ЖК_Кедрова Москва/12. BIM/05_АУДИТ/02_NWC'
rvt_list=[]
project = "_18_ЖК_Кедрова Москва"

def f_copy(x,y):
    try:
        shutil.copy(x,y)
    except shutil.SameFileError:
        pass
def rsn(pathlist,filenames):
    for path,name in zip(pathlist, filenames):
        print(path)
        download_path = os.path.join(download_dir,name)
        print(download_path) 
        rvt_list.append(download_path) 
        command1 = f'cd C:/Program Files/Autodesk/Revit {srv_vers}/RevitServerToolCommand'
        command2 = f'RevitServerTool createLocalRVT "{path}" -s {srv_ip} -d "{download_path}"'
        try:
            subprocess.call(command1+'&&'+command2, shell = True) #the method returns the exit code print("Returned Value: ", res)
        except:
            pass

def nwc(path):
    pathfile = os.path.join(path,'dirs_temp.txt')
    pfile = open(pathfile, 'w',encoding="utf-8")
    for i in rvt_list:
        pfile.writelines(i+'\n')
    pfile.close()
    nwf = os.path.join(path,'nwf_temp.nwf')        

    command1 = 'cd C:/Program Files/Autodesk/Navisworks Manage 2019'
    command2 = f'FiletoolsTaskRunner.exe/i "{pathfile}" /of "{nwf}" /version 2019'
    subprocess.call(command1+'&&'+command2, shell = True) #the method returns the exit code print("Returned Value: ", res)
    os.remove(pathfile)
    os.remove(nwf)

def ok():
    pathlist = []
    filenames = []
    for item in tree.selection():
        listitem = []
        it = tree.item(item,'text')
        filenames.append(it)
        parent = item
        while parent !='':
            parent = tree.parent(parent)
            listitem.append(tree.item(parent)['text'])
        listitem.pop()
        listitem.reverse()    
        x = '\\'.join(listitem)
        d = os.path.join(x, it)
        pathlist.append(d)  
    rsn(pathlist,filenames)
    print(rvt_list)
    nwc(download_dir)
    for rvt in rvt_list:
        nwc_file = (str(rvt)).replace('.rvt','.nwc')
        f_copy(nwc_file,finpath)
        os.remove(rvt)
        os.remove(nwc_file)

def process_directory(tree, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                if '.rvt' not in abspath:
                    process_directory(tree, oid, abspath)
                else:
                    pass
                

#Интерфея!

root = tk.Tk()
root.title("Экспорт NWC")
frame = tk.Frame(root)
frame.grid(row = 0, column = 0,sticky='ew')



vers = ['2019', '2021']        

vvar = tk.StringVar(root)
vvar.set(vers[0])
popupMenu_vers = ttk.OptionMenu(frame, vvar, vers[0], *vers)
tk.Label(frame, text="Версия").grid(row = 0, column = 0)
popupMenu_vers.grid(row = 1, column =0,sticky='w')

path = f'//{srv_ip}/Revit Server {vvar.get()}/Projects/'
dirs=[]
abspath = os.path.abspath(path)
dir = os.listdir(abspath)
for i in dir:
    if os.path.isdir(os.path.join(abspath,i)):
        dirs.append(i)
pvar = tk.StringVar(root)
pvar.set(dirs[0])



popupMenu_Proj = ttk.OptionMenu(frame, pvar, dirs[0], *dirs)
tk.Label(frame, text="Проект").grid(row = 0, column = 1)
popupMenu_Proj.grid(row = 1, column =1,sticky='w')

tree = ttk.Treeview(root)
ysb = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
xsb = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
tree.configure(yscroll=ysb.set, xscroll=xsb.set)
tree.grid(row=1, column=0,ipadx=200)
ysb.grid(row=1, column=1, sticky='ns')
xsb.grid(row=2, column=0, sticky='ew')
ok = tk.Button(root, text="Select",command=ok)
ok.grid(row=3, column=0,sticky='nsew',padx = 5, pady = 5)

root_node = tree.insert('', 'end', text=pvar.get(), open=True)
ppath = f'//{srv_ip}/Revit Server {vvar.get()}/Projects/{pvar.get()}'
process_directory(tree, root_node, ppath)

def v_change_dropdown(*args):

    path = f'//{srv_ip}/Revit Server {vvar.get()}/Projects/'
    dirs=[]
    abspath = os.path.abspath(path)
    dir = os.listdir(abspath)
    popupMenu_Proj['menu'].delete(0, 'end')
    for i in dir:
        if os.path.isdir(os.path.join(abspath,i)):
            dirs.append(i)
    pvar.set(dirs[0])
    for i in dirs:        
        popupMenu_Proj['menu'].add_command(label=i, command= lambda x=i: pvar.set(x)) 
    tree.delete(*tree.get_children())
    root_node = tree.insert('', 'end', text=pvar.get(), open=True)
    ppath = f'//{srv_ip}/Revit Server {vvar.get()}/Projects/{pvar.get()}'
    process_directory(tree, root_node, ppath)

def p_change_dropdown(*args):
    path = f'//{srv_ip}/Revit Server {vvar.get()}/Projects/'
    dirs=[]
    abspath = os.path.abspath(path)
    dir = os.listdir(abspath)
    for i in dir:
        if os.path.isdir(os.path.join(abspath,i)):
            dirs.append(i)
    tree.delete(*tree.get_children())
    root_node = tree.insert('', 'end', text=pvar.get(), open=True)
    ppath = f'//{srv_ip}/Revit Server {vvar.get()}/Projects/{pvar.get()}'
    process_directory(tree, root_node, ppath)    
    

# link function to change dropdown
vvar.trace('w', v_change_dropdown)
pvar.trace('w', p_change_dropdown)
root.mainloop()