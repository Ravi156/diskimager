#!/usr/bin/python

import os, sys, getopt
from datetime import datetime
import hashlib

def main(argv):
   inputfile = ''
   outputfile = ''
   flag_e = ''
   flag_s = ''
   intract = ''
   hcal = ''
   try:
      opts, args = getopt.getopt(argv,"hHIi:o:",["ifile=","ofile=","ofs=","ofe=","hashes="])
   except getopt.GetoptError:
      print 'Diskimager: Invalid option',argv
      print ' try :  \'-h\' option for more information.  '  
      print  'Diskimager Failed at',str(datetime.now())	 
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print '---------'
         print '| usage |'
         print '---------'
         print '	Diskimager.py [OPTION].. [FILE].. '
         print '	 Diskmager  is use for carate image file of disk.' 
         print '-----------'
         print '| options |'
         print '-----------'
         print '		 -i, --ifile      path of input Disk'
         print '		 -o, --ofile      path of output file'
         print '------------------'
         print '|Advance options |'
         print '------------------'
         print '		 --ofs  [arg]        staring sector number'
         print '		 --ofe  [arg]        ending sector number'
         print '		 --hashes [arg]      Hashes calulation by algoritham(sha256,md5)'
         print '		  -H                 Hashes calulation by all avallable algoritham'
         print '		  -I                 Intractive create Image'
         
         sys.exit()
      elif opt == '-I':
         intract = 1

      elif opt == '-H':
         hcal = 1

      elif opt in ("-i", "--ifile"):
         inputfile = arg
         print 'Input file is  :', inputfile
         
      elif opt in ("--hashes"):
         hcal = arg
            
      elif opt in ("-o", "--ofile"):
         outputfile = arg
         print 'Output file is :', outputfile

      elif opt in ("--ofs"):
         flag_s = 1
         spoint = arg
         
      elif opt in ("--ofe"):
         flag_e = 1
         epoint = arg
	
         
        
   if flag_s == 1 and flag_e == 1:
        print spoint
        ofsetimager(inputfile,outputfile,spoint,epoint)
   elif flag_s == 1 and flag_e == '':
        ofsetimager(inputfile,outputfile,spoint,0)
   elif intract == 1:
        inimager()
   else:
       
       imager(inputfile,outputfile,hcal)



def inimager():
     npath=''
     path=0
     dd={}
     print "\n\033[1;31m***********************************\033[1;m"
     print "*      WELCOME TO DISKIMAGER      *"
     print "\033[1;31m***********************************\033[1;m\n"

     f = os.popen("fdisk -l")
     c = 0
     print " NUMBER  |    DISK"
     print "----------------------"
     for i in f.readlines():
        if i.startswith("/"):
          temp = i.split()
          c = c+1
          cc=c
          print "  ",c,"  \t | ", temp[0]
          dd[c]=temp[0]
     
     path = raw_input("\n>>Enter Disk path number\n> ") 
     ipath = dd[int(path)]

     print "Your entered Disk path is ",dd[int(path)]
     opath = raw_input("\n>>Enter Destination path with file name (ex:/Desktop/abc)\n>")    
     print "Your entered file name is ",opath

     print "\n NUMBER  |  IMAGETYPE "
     print "----------------------"
     imaget={1: 'dd',2:'E01'} 
     for n in imaget:

       print "   ",n,"   |   ",imaget[n]

     itype = raw_input("\nEnter Image Type >> ")  
  
     opath=opath+"."+imaget[int(itype)]  
     
     print "\n OPTION  |  CALCULATION "
     print "-------------------------"
     hh={1: 'sha256',2: 'md5',3: 'all',0: 'no hashes'} 
     for n in hh:

       print "   ",n,"   |   ",hh[n]

   

     hcal = raw_input("\nEnter any one option for hashes calulation >>")

     words = ipath.split("/")
	  	
     blocks = int(open('/sys/class/block/{words[2]}/size'.format(**locals())).read())
     sblocks = blocks * 512
     print 'Number of Sector of your is : ', blocks
     with file(ipath) as f:
        stime = str(datetime.now())
	i=file(opath, "wb")
        i.write(f.read(10000))



      	if hcal == '1':
	       	 hashersha256 = hashlib.sha256()
		 buf = f.read(10000)
		 hashersha256.update(buf)
		 print("SHA256 : " + hashersha256.hexdigest())
		 h=file("/root/Desktop/hashes.hash", "wb")
		 h.write("SHA256 : " + hashersha256.hexdigest())

        if hcal == '2':
		 hashermd5 = hashlib.md5()
		 buf = f.read(10000)
		 hashermd5.update(buf)
		 print("MD5 : " + hashermd5.hexdigest())
		 h=file("/root/Desktop/hashes.hash", "wb")
		 h.write("MD5 : " + hashermd5.hexdigest())
         

      
        if hcal == '3':
		 hashersha256 = hashlib.sha256()
		 hashermd5 = hashlib.md5()
		   
		 buf1 = f.read(10000)
		 buf2 = f.read(10000)
		 hashersha256.update(buf1)
		 hashermd5.update(buf2)
		 print("SHA256 : " + hashersha256.hexdigest())
		 print("MD5    : " + hashermd5.hexdigest())
		 h=file("/root/Desktop/hashes.hash", "wb")
		 h.write("SHA256 : " + hashersha256.hexdigest())
		 h.write('\n')
		 h.write("MD5    : " + hashermd5.hexdigest())
          

     etime = str(datetime.now())

     print 'STARTING IMAGING TIME : ', stime
     print 'ENDING IMAGING TIME   : ', etime
     print 'Your disk image is Created.' 


def ofsetimager(ifile,ofile,ofs,ofe):

     
     print 'Output file is : ', ofile
      
     startB = int(ofs) * 512
     endinB = int(ofe) * 512
     words = ifile.split("/") 
     blocks = int(open('/sys/class/block/{words[2]}/size'.format(**locals())).read())
     
   
   

     with file(ifile) as f:
         stime = str(datetime.now())
         i=file(ofile, "wb")
         print startB,ifile
         f.seek(startB)
         if ofe == 0:
             i.write(f.read(1000))
         else:
             i.write(f.read(endinB))
         etime = str(datetime.now())

     print 'STARTING IMAGING TIME : ', stime
     print 'ENDING IMAGING TIME : ', etime
     print 'Your disk image is Created.' 

 

def imager(ifile,ofile,hcal):


    words = ifile.split("/")
  	
    blocks = int(open('/sys/class/block/{words[2]}/size'.format(**locals())).read())
    sblocks = blocks * 512
    print 'Sectors : ', sblocks
     
    with file(ifile) as f:

      stime = str(datetime.now())
      
      i=file(ofile, "wb")
      i.write(f.read(9999999))

  
      if hcal == 'sha256':
         hashersha256 = hashlib.sha256()
         buf = f.read(10000)
         hashersha256.update(buf)
         print("SHA256 : " + hashersha256.hexdigest())
         h=file("/root/Desktop/hashes.hash", "wb")
         h.write("SHA256 : " + hashersha256.hexdigest())

      if hcal == 'md5':
         hashermd5 = hashlib.md5()
         buf = f.read(10000)
         hashermd5.update(buf)
         print("MD5 : " + hashermd5.hexdigest())
         h=file("/root/Desktop/hashes.hash", "wb")
         h.write("MD5 : " + hashermd5.hexdigest())
         

      
      if hcal == 1:
         hashersha256 = hashlib.sha256()
         hashermd5 = hashlib.md5()
           
         buf1 = f.read(10000)
         buf2 = f.read(10000)
         hashersha256.update(buf1)
         hashermd5.update(buf2)
         print("SHA256 : " + hashersha256.hexdigest())
         print("MD5    : " + hashermd5.hexdigest())
         h=file("/root/Desktop/hashes.hash", "wb")
         h.write("SHA256 : " + hashersha256.hexdigest())
         h.write('\n')
         h.write("MD5    : " + hashermd5.hexdigest())

      etime = str(datetime.now())

      print 'STARTING IMAGING TIME : ', stime
      print 'ENDING IMAGING TIME : ', etime
      print 'Your disk image is Created.' 

if __name__ == "__main__":
   main(sys.argv[1:])
