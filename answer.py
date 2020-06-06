#-------------------------------------------------------
#Gizem Pesen
#170709050
#-------------------------------------------------------


#-------------------------------------------------------
# İMPORT PART
#-------------------------------------------------------
import os, sys
import threading
import requests
import time
import hashlib
from multiprocessing import Process 

os.system("clear")
os.system("ls")


#-------------------------------------------------------
#1 CHILD PROCESS
#-------------------------------------------------------

child = os.fork()
if child == 0:
  print("child proc id ",os.getpid())


#---
#PARENT AND CHILD PROCESS
#---
def parent_child(): 
    n = os.fork() 
 
     #n greater than 0  means parent process 
    if n > 0: 
        print("Parent process and id is : ", os.getpid()) 
  
     #n equals to 0 means child process 
    else: 
        print("Child process and id is : ", os.getpid()) 
          
 #Driver code 
parent_child() 

#---
#JUST CHILD PROCESS
#---
#pid = os.fork()
#print(pid)

#---
#Fork() in C
#---
#    if (fork() == 0) 
#        printf("Hello from Child!\n"); 
#    else
#        printf("Hello from Parent!\n"); 

#-------------------------------------------------------
#2 DOWNLOAD FİLES
#-------------------------------------------------------
def download(link, filelocation):
    r = requests.get(link, stream=True)
    with open(filelocation, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)

def createNewDownloadThread(link, filelocation):
    download_thread = threading.Thread(target=download, args=(link,filelocation))
    download_thread.start()

url=["http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg"]


file = ["C:\\image1.jpeg","C:\\image2.png","C:\\image3.jpg","C:\\image4.jpeg","C:\\image5.jpg"]

#print(file[0])
#print(file[1])
#createNewDownloadThread(url[0], file[0]) 
#createNewDownloadThread(url[1], file[1]) 
#...
#I used nested loop to write easier
for x in url:
  for y in file:
    createNewDownloadThread(x, y) 

#url = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup. jpeg/300px-MSKU-BlockchainResearchGroup.jpeg", "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1 _Ko%C3%A7man_%C3%9Cniversitesi_logo.png", "​https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024pxHawai%27i.jpg​", "​http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.j peg/300px-MSKU-BlockchainResearchGroup.jpeg​", "​https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024pxHawai%27i.jpg​"]



#local_filename = ["image1.jpeg","image2.png","image3.jpg","image4.jpeg","image5.jpg"]



#def download_file(url,local_filename):
#	with requests.get(url, stream=True) as r:
#		with open(local_filename, 'wb') as f:
#			for chunk in r.iter_content(chunk_size=8192): 
#					f.write(chunk)

#download_file(url[0],local_filename[0])
#download_file(url[1],local_filename[1])
#download_file(url[2],local_filename[2])
#download_file(url[3],local_filename[3])
#download_file(url[4],local_filename[4])


#-------------------------------------------------------
#3 ORPHAN PROCESS
#-------------------------------------------------------
#Orphan process is the situation when the parent finishes before child

def  avoid_orphan_process():
   child_pid = os.fork() 
   if (child_pid>0):
      print("avoided orphan process")
      time.sleep(50)

   else:
      exit(0)

avoid_orphan_process()

#int main() 
#{ 
#    // Fork returns process id 
#     // in parent process 
#    pid_t child_pid = fork(); 
  
#    // Parent process  
#    if (child_pid > 0) 
#        sleep(50); 
  
#    // Child process 
#    else        
#        exit(0); 
  
#    return 0; 
#} 
  
#def child():
#   print('A new child ',  os.getpid())
#   os._exit(0)  


#def parent():
#   while True:
#      newpid = os.fork()
#      if newpid == 0:
#         child()
#      else:
#         pids = (os.getpid(), newpid)
#         print("parent: , child: \n" % pids)
#      reply = input("q for quit / c for new fork")
#      if reply == 'c': 
#          continue
#      else:
#          break

#parent()

#-------------------------------------------------------
#4 Control duplicate files
#-------------------------------------------------------

#def check_duplicate(url):  
  
def check_duplicates(paths, hash=hashlib.sha1):
    hashes = {}
    for path in paths:
        for dirpath, dirnames, file in os.walk(path):
            for file in file:
                full_path = os.path.join(dirpath, file)
                hashobj = hash()
                for chunk in chunk_reader(open(full_path, 'rb')):
                    hashobj.update(chunk)
                file_id = (hashobj.digest(), os.path.getsize(full_path))
                duplicate = hashes.get(file_id, None)
                if duplicate:
                    print("Duplicate found: %s and %s" % (full_path, duplicate))
                else:
                    hashes[file_id] = full_path

if sys.argv[1:]:
    check_for_duplicates(sys.argv[1:])
else:
    print("Please pass the paths to check as parameters to the script")

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

#------------------
#MULTIPROCESSING PART SHOULD BE SO
#--------------------
#with Pool(5) as p:
#    print(p.map(check_duplicates, ["http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg","http://www.gunnerkrigg.com//comics/00000001.jpg"]))

print(check_duplicates(url))

#-------------
#GOOD EXAMPLE HASHLİB
#-------------

#def file_as_bytes(file):
#    with file:
#        return file.read()

#print hashlib.md5(file_as_bytes(open(full_path, 'rb'))).hexdigest()

#----
#def remove_duplicates(dir):
#    unique = []
#    for filename in os.listdir(dir):
#        if os.path.isfile(filename):
#            filehash = md5.md5(file(filename).read()).hexdigest()
#        if filehash not in unique: 
#            unique.append(filehash)
#        else: 
#            os.remove(filename)

#--------------
#Another Example
#------------- 
#import os, glob
#import Image
#import hashlib
#import shutil
 
#def Imge_md5hash(im_file):
#    im = Image.open(im_file)
#    return hashlib.md5(im.tostring()).hexdigest()
 
#def findDupImgMd5(data_path):
#    hashdict={}
#    deletionList=[]
 
#    for infile in glob.glob(data_path + os.sep +"*.jpg"):
#        fileNP, ext = os.path.splitext(infile)
#        ids = fileNP.split(os.sep)
#        hash_result = Imge_md5hash(infile)
#        if hashdict.has_key(hash_result):
#            deletionList.append(infile)
#            hashdict.setdefault(hash_result, []).append(ids)
#    return deletionList, hashdict
 
#if __name__=="__main__":
 
#    folderPath = r"your-image-data-folder"
#    deletionList, hashdict = findDupImgMd5(folderPath)
 
#    print("Start to save the data")
 
#    with open("dupImageList.txt", 'wb') as ofile:
#        _=[ofile.write(item+"\n") for item in deletionList]
 
#    with open("hashDupImageDict.txt",'wb') as ofile:
#        _=[ofile.write(k+"\t"+ "\t".join(v)+"\n") for (k,v) in hashdict.items()]
 
#    """Copy the duplicated image to Dup-folder, renamed with
#    hash-code and original id"""
 
#    DesFolder = os.path.join(folderPath, "DupImg")
 
#    if not os.path.exist(DesFolder):
#        os.madir(DesFolder)
 
#    for k,v in hashdict.items():
#        if len(v)>1:
#            for vi in v:
#                srcP = os.path.join(folderPath, vi+".jpg")
#                dstP = os.path.join(DesFolder, k+"_"+vi+".jpg")
#                shutil.copyfile(srcP,dstP)
