import os
from time import sleep
import shutil
from pathlib import Path
conf="config.cfg"
from ctypes import WinDLL


def main():
    s="\\"
    paths=pathconfig()
    extension=extensionconfig()
    source_folder=paths["Source"]
    if("//" in source_folder):
        s="/"
    while(True):
        files=os.listdir(source_folder)
        if(files!=[]):
            for file in files:
                if(os.path.isfile(source_folder+s+file)):
                    ext=file.split(".")[-1]
                    for key in extension:
                        if(ext in extension[key]):
                            movefile(ext,source_folder,file,paths[key])
        sleep(1)

def pathconfig():
    paths={"Source":"","Destination":"","Documents":"","Audio":"","Compressed":"","Pictures":"","Executables":"","Videos":"","Torrents":""}
    try:
        with open(conf,'r') as f:
            c=False
            for line in f:
                line=line.strip(" ").strip("\n")
                if(line=="[PATH]"):
                    c=True
                if(line=="[EXTENSION]"):
                    c=False
                if(c==True):
                    for key in paths:
                        if(line.startswith(key+"=") or line.startswith(key+" =")):
                            paths[key]=line.split("=")[1].strip(" ")
        return paths

    except FileNotFoundError:
        loop=True
        while(loop):
            c=input("Config not found!! Go with the default folder settings? (Y/N/E)\n>").upper()
            if(c!='Y' and c!='N'):
                exit()
            with open(conf,'w') as f:
                f.write("[PATH]\n")
                if(c=="Y"):
                    paths["Source"]=str(Path.home()/"Downloads")+"\\"
                    f.write("Source="+paths["Source"]+"\n")
                    paths["Destination"]=paths["Source"]
                    f.write("Destination="+paths["Destination"]+"\n")
                    for key in paths:
                        if(key=="Source" or key=="Destination"):
                            continue
                        paths[key]=pathwrite(paths["Destination"],key,"\\",f)
                elif(c=="N"):
                    print("Please enter the path for folders below : (Leave blank to go with the default for that Path)")
                    paths["Source"]=input("Enter path to Source folder : ").strip(" ")
                    if(not(paths["Source"].endswith("\\")) and not(paths["Source"].endswith("/"))):
                        if(paths["Source"]=="." or ":\\" in paths["Source"] or ".\\" in paths["Source"]):
                            paths["Source"]=paths["Source"]+"\\"
                        else:
                            paths["Source"]=paths["Source"]+"/"
                    f.write("Source="+paths["Source"]+"\n")
                    paths["Destination"]=input("Enter path to Destination folder : ").strip(" ")
                    if(not(paths["Destination"].endswith("\\")) and not(paths["Destination"].endswith("/"))):
                        if(paths["Destination"]=="." or ":\\" in paths["Destination"] or ".\\" in paths["Source"]):
                            paths["Destination"]=paths["Destination"]+"\\"
                        else:
                            paths["Destination"]=paths["Destination"]+"/"
                    f.write("Destination="+paths["Destination"]+"\n")
                    for key in paths:
                        if(key=="Source" or key=="Destination"):
                            continue
                        paths[key]=pathprocess(paths["Destination"],key,f)
            

            with open(conf,'r') as f:
                print("The following Paths has been entered:\n")
                print(f.read())
            c=input("Do you want to continue with this setting? (Y/N/E)\n>").upper()
            if(c!='Y'):
                print("Deleting Config...")
                os.remove(conf)
                if(c!='N'):
                    print("Exiting...")
                    exit()
            else:
                loop=False
        return paths

def extensionconfig():
    extension={
        "Documents":"doc pdf ppt pps docx pptx epub xls txt xml xlsx odt pub".split(" "),
        "Compressed":"zip rar r0* r1* arj gz sit sitx sea ace bz2 7z tar iso".split(" "),
        "Audio":"mp3 wav wma mpa ram ra aac aif m4a tsa".split(" "),
        "Pictures":"JPG PNG GIF WEBP TIFF PSD RAW BMP HEIF INDD JPEG".lower().split(" "),
        "Executables":"exe msi".split(" "),
        "Videos":"flv avi mpg mpe mpeg asf wmv mov qt rm mp4 flv m4v webm ogv ogg mkv ts tsv".split(" "),
        "Torrents":["torrent"]
    }
    point=0
    with open(conf,'a') as f:
        point=f.tell()
    with open(conf,'r+') as f:    
        content=f.read()
        if("[EXTENSION]" in content):
            c=False
            content=content.split("\n")
            for line in content:
                if(line=="[EXTENSION]"):
                    c=True
                if(line=="[PATH]"):
                    c=False
                if(c==True):
                    for key in extension:
                        if(line.startswith(key+"=") or line.startswith(key+" =")):
                            extension[key]=line.split("=")[1].strip(" ").split(" ")
        else:
            loop=True
            while(loop):
                c=input("\nDo you want to go with the default extensions? (Y/N/E)\n>").upper()
                if(c!='Y' and c!='N'):
                    exit()
                f.seek(point)
                f.write("[EXTENSION]\n")
                if(c=='Y'):
                    for key in extension:
                        f.write(key+"="+" ".join(extension[key])+"\n")
                if(c=='N'):
                    for key in extension:
                        extlist=input("Extensions in "+key+" : "+", ".join(extension[key])+"\n>").lower().split(" ")
                        if(extlist!=[""] or extlist[0]!="d"): 
                            if(extlist[0]=='a' or extlist[0]=='add' or extlist[0]=='append'):
                                extension[key].extend(extlist[1:])
                            if(extlist[0]=='r' or extlist[0]=='rm' or extlist[0]=='remove'):
                                extension[key]=set(extension[key])^set(extlist[1:])
                        f.write(key+"="+" ".join(extension[key])+"\n")
                print("\n[EXTENSION]")
                for key in extension:
                    print(key+"="+", ".join(extension[key]))
                c=input("\nDo you want to continue with the above extensions? (Y/N/E)\n>").upper()
                if(c!='Y'):
                    print("Removing extensions added so far...")
                    if(c!='N'):
                        c=input("Do you want to delete the config file created so far? (Y/N/E)\n>").upper()
                        if(c=='Y'):
                            f.close()
                            os.remove(conf)
                            print("Config Deleted...")
                        print("Exiting...")
                        exit()
                else:
                    loop=False
    return extension 

def pathwrite(d,k,s,f):
    val=d+k+s
    f.write(k+"="+val+"\n")
    return val

def pathprocess(d,k,f):
    s="\\"
    val=""
    path=input("Enter path to "+k+" Folder : ").strip(" ")   

    if("//" in d and ":\\" not in path and ".\\" not in path):
        path=path.replace("\\","/")
    if((":\\" in d or ".\\" in d) and "//" not in path):
        path=path.replace("/","\\")

    if("//" in path or (("//" in d and ("/" in path or path.strip(" ")=="")))):
        s="/"
    print(s)
    if(path.strip(" ")==""):
        val=pathwrite(d,k,s,f)
        return val
    if(path=="." or path==".\\" or path=="./"):
        val=d
        f.write(k+"="+val+"\n")
        return val

    if(":\\" in path or "//" in path):
        val=path
    elif(path.startswith("\\") or path.startswith("/")):
        val=d+path[1:]
    elif(not(path.startswith("\\")) or not(path.startswith("/"))):
        val=d+path


    if(not(val.endswith(s))):
        val=val+s

    f.write(k+"="+val+"\n")
    return val

def filecheck(f,e,d,nf,i=1):
    if(os.path.isfile(d+nf)):
        nf=f.removesuffix("."+e)+"("+str(i)+")"+"."+e
        return filecheck(f,e,d,nf,i+1)
    else:
        return nf    

def movefile(e,s,f,d):
    if(not(os.path.isdir(d))):
        os.makedirs(d)
    nf=filecheck(f,e,d,f)
    shutil.move(s+"\\"+f,d+nf)      

def showhideconsole(switch):
    kernel32 = WinDLL('kernel32')
    user32 = WinDLL('user32')

    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, switch)

if __name__ =="__main__":
    main()