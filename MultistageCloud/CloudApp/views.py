from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import pymysql
from django.core.files.storage import FileSystemStorage
import cv2
import os
import sys
import numpy
import matplotlib.pyplot as plt
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from struct import pack

global username, filename

def getCrowKey():
    key = "key must be 4 to 56 bytes".encode()
    return key

def DownloadFileAction(request):
    if request.method == 'GET':
        global username
        output = "Error in saving auth image"
        img = request.GET.get('fname', False)

        infile = open("CloudApp/static/files/"+img, 'rb')
        encryptedText = infile.read()
        infile.close()
        bs = Blowfish.block_size
        cipher = Blowfish.new(getCrowKey(),mode=Blowfish.MODE_CBC)
        decrypt = unpad(cipher.decrypt(encryptedText),8)

        response = HttpResponse(decrypt, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % img
        return response

def DownloadFile(request):
    if request.method == 'GET':
        global username
        font = '<font size="" color="white">'
        output = '<table border="1" align="center" width="100%"><tr><th>'+font+'Username</th><td>'+font+'Filename</th><td>'+font+'Download File</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'multistagecloud',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM files")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output+="<tr><td>"+font+row[0]+"</td><td>"+font+row[1]+"</td>"
                    output+='<td><a href=\'DownloadFileAction?fname='+row[1]+'\'><font size=3 color=white>Click Here</font></a></td></tr>'
        context= {'data':output}
        return render(request, "DownloadFile.html", context)

def UploadFileAction(request):
    if request.method == 'POST':
        filename = request.FILES['username'].name
        myfile = request.FILES['username'].read() #reading uploaded file from user
        bs = Blowfish.block_size  #generating size for the key
        cipher = Blowfish.new(getCrowKey(),mode=Blowfish.MODE_CBC) #generate key by using Crow Key algorithm
        plen = bs - len(myfile) % bs #find the length of the file
        padding = [plen]*plen
        padding = pack('b'*plen, *padding) #pad the file
        encrypted_data = cipher.iv + cipher.encrypt(myfile + padding) #encrypt file using key and padding data
        outfile = open("E:/venkat/2021/Feb22/MultistageCloud/CloudApp/static/files/"+filename, 'wb') #save the encrypted file
        outfile.write(encrypted_data)
        outfile.close()
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'multistagecloud',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO files(username,filename,filekeys) VALUES('"+username+"','"+filename+"','qwerty')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':'Encrypted file saved inside static/files folder'}
        return render(request, "UploadFile.html", context)

def LoginAuthImageAction(request):
    if request.method == 'GET':
        global username
        status = "Error in saving auth image"
        img = request.GET.get('imgname', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'multistagecloud',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM authimage")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == img:
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'welcome '+username}
            return render(request, "UserScreen.html", context)
        else:
            context= {'data':'Invalid Auth images selected. Please retry'}
            return render(request, 'User.html', context)

def UserLogin(request):
    global username
    if request.method == 'POST':
        global username
        status = "none"
        users = request.POST.get('username', False)
        password = request.POST.get('password', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'multistagecloud',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    username = users
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'Choose Your Image for authentication'}
            return render(request, "LoginAuthImages.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'User.html', context)

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def UploadFile(request):
    if request.method == 'GET':
       return render(request, 'UploadFile.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def User(request):
    if request.method == 'GET':
        return render(request, 'User.html', {})

def AuthImageAction(request):
    if request.method == 'GET':
        global username
        output = "Error in saving auth image"
        img = request.GET.get('imgname', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'multistagecloud',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO authimage(username,image_name,crop_image) VALUES('"+username+"','"+img+"','crop_"+img+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = "Authentication image successfully saved"
        context= {'data':output}
        imgs = cv2.imread("CloudApp/static/auth/"+img)
        y=10
        x=10
        h=80
        w=80
        crop = imgs[y:y+h, x:x+w]
        f, axarr = plt.subplots(1,2)
        axarr[0].set_title("Uploaded Auth Image")
        axarr[1].set_title("Cropped Image")
        axarr[0].imshow(imgs)
        axarr[1].imshow(crop)
        plt.title("Auth Selected & Crop Image")
        plt.show()
        return render(request, 'Register.html', context)

def Signup(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        password = request.POST.get('password', False)
        
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'multistagecloud',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break                
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'multistagecloud',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. Choose Your Auth Image"
        context= {'data':output}
        return render(request, 'AuthImages.html', context)
        

