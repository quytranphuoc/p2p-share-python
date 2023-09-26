from tkinter import *
import tkinter as tk
import socket 
from tkinter import filedialog
from tkinter import messagebox
import os

root = Tk()
root.title("Shareit")
root.geometry("450x650+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False,False)

#window send
def Send():
    window=Toplevel(root)
    window.title("Send")
    window.geometry('450x560+500+200')
    window.configure(bg="#f4fdfe")
    window.resizable(False,False)
    
    def select_file():
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                          title='Select Image File', 
                                          filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
    
          
    def sender():
        s=socket.socket()
        host=socket.gethostname()
        port=8080
        s.bind((host,port))
        s.listen(1)
        print(host)
        print('watting for any incoming connections ....')
        conn,addr=s.accept()
        file=open(filename,'rb')
        file_data=file.read(1024)
        conn.send(file_data)
        print("Data has been transmitted successfully..")


    #icon
    image_icon1=PhotoImage(file="image/send.png")
    window.iconphoto(False,image_icon1)

    Sbackground=PhotoImage(file="image/AnyConv.com__sender.png")
    Sbackground = Sbackground.zoom(2, 1)
    Label(window, image=Sbackground).place(x=-2,y=0)


    Mbackground=PhotoImage(file="image/id.png")
    Mbackground = Mbackground.subsample(4, 4)
    Label(window,image=Mbackground,bg='#f4fdfe').place(x=150,y=400)
    
    #id
    host=socket.gethostname()
    Label(window,text=f'ID: {host}', bg='white',fg='black').place(x=150,y=400)

    
   


    Button(window,text="+ select file",width=10, height=1, font='arial 14 bold', bg="#fff",fg="#000",command=select_file).place(x=100,y=250)
    Button(window,text="SEND",width=8,height=1,font='arial 14 bold', bg="#000", fg="#000",command=sender).place(x=250,y=250)

    window.mainloop()
#window receive
def Receive():
    main=Toplevel(root)
    main.title("Receive")
    main.geometry('450x560+500+200')
    main.configure(bg="#f4fdfe")
    main.resizable(False,False)

    def receiver():
        ID=SenderID.get()
        filename1=incoming_file.get()

        s=socket.socket()
        port=8080
        s.connect((ID,port))
        file=open(filename1,'wb')
        file_data=s.recv(1024)
        file.write(file_data)
        file.close()
        print("File has been received successfully")


    #icon
    image_icon1=PhotoImage(file="image/receive.png")
    main.iconphoto(False,image_icon1)

    Hbackground=PhotoImage(file="Image/receiver.png")
    Hbackground = Hbackground.zoom(2,1)
    Label(main,image=Hbackground).place(x=-2,y=0)

    logo=PhotoImage(file='image/profile.png')
    logo = logo.subsample(4, 4 )
    Label(main,image=logo).place(x=20,y=270)

    Label(main,text="Receive",font=('arial',20),bg="#f4fdfe").place(x=100,y=280)

    Label(main,text="Input sender id", font=('arial',10,'bold'),bg='#f4fdfe').place(x=20,y=350)
    SenderID = Entry(main,width=25,fg="#000",border=2,bg="#f4fdfe",font=('arial',15))
    SenderID.place(x=20,y=370)
    SenderID.focus()

    Label(main,text="Filename for the incoming file:", font=("arial",10,"bold"),bg="#f4fdfe").place(x=20,y=430)
    incoming_file = Entry(main,width=25,fg="#000",border=2,bg="#f4fdfe", font=('arial',15))
    incoming_file.place(x=20,y=450)

    imageicon=PhotoImage(file="Image/AnyConv.com__arrows.png")
    imageicon = imageicon.subsample(9,9)
    rr=Button(main,text="Receive",compound=LEFT,image=imageicon,width=130,bg="#39c790",font="arial 14 bold",command=receiver)
    rr.place(x=20,y=500)

    main.mainloop()

#icon
image_icon = PhotoImage(file="Image/icon.png")
root.iconphoto(False,image_icon)

Label(root,text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'),bg="#f4fdfe").place(x=20,y=30)

Frame(root,width=400,height=2,bg="#f3f5f6").place(x=25,y=80)

send_image = PhotoImage(file="Image/send.png")
send_image = send_image.subsample(4, 4)
send = Button(root,image=send_image,bg="#f4fdfe",bd=0, command=Send)
send.place(x=100,y=100)

receive_image = PhotoImage(file="Image/receive.png")
receive_image = receive_image.subsample(4, 4)
receive = Button(root,image=receive_image,bg="#f4fdfe",bd=0, command=Receive)
receive.place(x=300,y=100)

#label 
Label(root,text="Send" ,font=('Acumin Varible Concept', 17, 'bold'),bg="#f4fdfe").place(x=100,y=170)
Label(root,text="Receive" ,font=('Acumin Varible Concept', 17, 'bold'),bg="#f4fdfe").place(x=290,y=170)

background = PhotoImage(file="Image/background.png")
background = background.zoom(2, 2)
Label(root,image=background).place(x=-2,y=323)

root.mainloop()
