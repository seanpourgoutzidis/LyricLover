def lyricsFormatting (lyrics, title):
    numDigits = 0

    #Count the number of digits at the beginning so that we may remove it at the end
    for char in lyrics:
        if char.isdigit():
            numDigits += 1
        else:
            break

    #Remove the embed statement at the end
    lyrics = lyrics[:len(lyrics) - 5 - numDigits]

    #Remove all header info from lyrics
    lyrics = lyrics[lyrics.find(title):]
    
    #Remove footer that occasionally appears
    lyrics = lyrics.replace("You might also like", "")

    #Properly format the header of the lyrics
    lyrics = lyrics[:lyrics.find("[")] + "\n\n" + lyrics[lyrics.find("["):]
    
    return lyrics

#Import statements and API setup

import lyricsgenius
import os
import getpass
import email
import zipfile
import shutil
import smtplib

from googleapiclient.http import MediaFileUpload
from Google import Create_Service #CODE FROM https://learndataanalysis.org/

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from colorama import Fore, Back, Style

genius = lyricsgenius.Genius('YOUR API KEY')
genius.verbose = False

stillSearching = True

while stillSearching:
    
    enteringArtist = True
    confirmingArtist = True
    enteringContent = True
    confirmingContent = True
    
    #Prompt the user for what they are looking for
    while enteringArtist:
        artistName = input("Please enter the name of the artist whose lyrics you are looking for (exactly): ")
        
        try: 
            artist = genius.search_artist(artistName, max_songs = 1, sort="title")
        except:
            print(Fore.RED + "Could not find your artist. Please type the name in exactly!")
            print(Style.RESET_ALL + "")
            artist = False
        
        if (artist):
            
            while confirmingArtist:
                yesOrNo = input("We found the artist: " + artist.name + ". Is this correct (y/n)?: ")

                if (yesOrNo[0].lower() == 'y'):
                    enteringArtist = False
                    confirmingArtist = False
                elif (yesOrNo[0].lower() == 'n'):
                    enteringArtist = True
                    confirmingArtist = False
                else:
                    print(Fore.RED + "Please enter either y/n.")
                    print(Style.RESET_ALL + "")
                    confirmingArtist = True
            
        else:
            print(Fore.RED + "Sorry, we could not find the artist you entered. Please try again!")
            print(Style.RESET_ALL + "")
    
    
    songOrAlbum = 'z'
    
    #User is specifying if they are looking for a song or an album
    while (songOrAlbum[0].lower() != 'a' and songOrAlbum[0].lower() != 's'):
        songOrAlbum = input("\nAre you looking for the lyrics to an album or song? (Album/Song): ")
        
        if (songOrAlbum[0].lower() != 'a' and songOrAlbum[0].lower() != 's'):
            print(Fore.RED + "Sorry, that input is not valid. Please try again!")
            print(Style.RESET_ALL + "")
    
    #Holds the type of content they are looking for
    content = 'z'
    
    #The user would like to search for an album
    if (songOrAlbum[0].lower() == 'a'):
        content = 'album'
    
    #The user is searching for a song   
    elif(songOrAlbum[0].lower() == 's'):
        content = 'song'
        
    #The user is entering content
    while enteringContent:
        
        contentName = input("Please enter the name of the " + content + " you are looking for: ")
        
    
        #The user would like to search for an album
        if (songOrAlbum[0].lower() == 'a'):
            try: 
                album = genius.search_album(contentName, artistName)
            except: 
                print(Fore.RED + "Could not find your album. Please type the name in exactly!")
                print(Style.RESET_ALL + "")
                album = False
            
            if album:
                while confirmingContent:
                    yesOrNo = input("We found the album: " + album.name + ". Is this correct? (y/n): ")
                    
                    if (yesOrNo[0].lower() == 'y'):
                        enteringContent = False
                        confirmingContent = False
                    elif (yesOrNo[0].lower() == 'n'):
                        enteringContent = True
                        confirmingContent = False
                    else:
                        print(Fore.RED + "Please enter either y/n.")
                        print(Style.RESET_ALL + "")
                        confirmingContent = True
            else:
                print(Fore.RED + "Sorry, we could not find the album you entered. Please try again!")
                print(Style.RESET_ALL + "")
                    
        #The user is searching for a song
        elif (songOrAlbum[0].lower() == 's'):
            try:
                song = genius.search_song(contentName, artistName)
            except: 
                print(Fore.RED + "Could not find your song. Please type the name in exactly!")
                print(Style.RESET_ALL + "")
                song = False
            
            if song:
                while confirmingContent:
                    yesOrNo = input("We found the song: " + song.title + ". Is this correct? (y/n): ")
                    
                    if (yesOrNo[0].lower() == 'y'):
                        enteringContent = False
                        confirmingContent = False
                    elif (yesOrNo[0].lower() == 'n'):
                        enteringContent = True
                        confirmingContent = False
                    else:
                        print(Fore.RED + "Please enter either y/n.")
                        print(Style.RESET_ALL + "")
                        confirmingContent = True
                        
            else:
                print("Sorry, we could not find the song you entered. Please try again!")
                
    #Now, the user needs to set the directory they would like to download from
    choosingDirectory = True
    confirmingDirectory = True
    chosenDirectory = "~"
    validDirectory = False
    
    print("Your lyrics are now ready to be downloaded, please enter the directory you would like to download them to")
    
    #User choosing the directory
    while choosingDirectory:
        
        print("Your current directory is: " + os.getcwd())
        
        confirmingDirectory = True
        
        while confirmingDirectory:
            yesOrNo = input("Is this the directory you want to save your file(s) in (y/n): ")

            if (yesOrNo[0].lower() == 'y'):
                choosingDirectory = False
                confirmingDirectory = False
            
            elif (yesOrNo[0].lower() == 'n'):
                
                choosingDirectory = True
                
                directoriesList = os.listdir(os.getcwd())
                
                print("Please choose one of this directories to change to (.. to move up a directory) \n")
                
                for directory in directoriesList:
                    print(directory)
                    
                
                validDirectory = False
                
                while not(validDirectory):
                    chosenDirectory = input("Input your choice of directory: ")
                    
                    if (chosenDirectory in directoriesList or chosenDirectory == '..'):
                        validDirectory = True
                        confirmingDirectory = False
                    
                    else:
                        print(Fore.RED + "Error, directory not found. Try again!")
                        print(Style.RESET_ALL + "")
                
                path = os.getcwd()
                
                if (chosenDirectory == '..'):
                    tempPath = path.split('/')
                    tempPath.pop()
                    path = "/".join(tempPath)
                else:
                    path = path + '/' + chosenDirectory
                    
                os.chdir(path)
                    
            else:
                print(Fore.RED + "Invalid input, try again!")
                print(Style.RESET_ALL + "")
                confirmingDirectory = True
            
    
    #The user would like to search for an album
    if (songOrAlbum[0].lower() == 'a'):
        
        #Make directory for song files and change to this directory
        try: os.mkdir(os.getcwd() + '/' + album.name + '- ' + album.artist.name)
        except: 
            print(Fore.YELLOW + "This directory already exists.")
            print(Style.RESET_ALL + "")
            pass
        
        os.chdir(os.getcwd() + '/' + album.name + '- ' + album.artist.name)
        
        #Iterate through all the songs and add to txt files
        for track in album.tracks:
            lyrics = lyricsFormatting(track.song.lyrics, track.song.title)
            
            while "/" in track.song.title:
                track.song.title = track.song.title.replace('/', '|')
            
            try:
                f = open(track.song.title + " lyrics.txt", "w")
                f.write(lyrics)
                f.close()
            except:
                print(Fore.RED + "Error copying a song")
                print(Style.RESET_ALL + "")
            
    
    #The user is searching for a song   
    elif(songOrAlbum[0].lower() == 's'):
        lyrics = lyricsFormatting(song.lyrics, song.title)
        
        while "/" in song.title:
            song.title = song.title.replace('/', '|')
            
        f = open(song.title + " lyrics.txt", "w")
        f.write(lyrics)
        f.close()
        
    
    print(Fore.GREEN + "Your lyrics have successfully been saved!\n\n\n\n\n")
    print(Style.RESET_ALL + "")
    
    #Ask the user if they'd like to email the lyrics to someone
    
    validInput = False
    
    while not(validInput):
        yesOrNo = input('Would you like to email these lyrics to someone? (y/n): ')
        
        if (yesOrNo[0].lower() == 'y'):
            
            receiver_email = input("Enter the email you would like to send your email to: ")
            subject = input("Enter the subject of your email: ")
            body = input("Enter the body of your email: ")
            print("\n")
            sender_email = input("Enter your email: ")
            password = getpass.getpass("Enter your password: ")
            
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message["Bcc"] = receiver_email  # Recommended for mass emails

            if (content == 'album'):
                #Set the correct directories
                path = os.getcwd()
                tempPath = path.split('/')
                tempPath.pop()
                path = '/'.join(tempPath)
                
                os.chdir(path) #Change directory to where the zip file is
                shutil.make_archive(album.name + '- ' + album.artist.name,'zip',path + "/" + album.name + '- ' + album.artist.name)
                filename = album.name + '- ' + album.artist.name + ".zip"
                
                #CODE FOR GOOGLE DRIVE API FILE UPLOAD & GOOGLE.py SETUP FILE FROM: https://learndataanalysis.org/ 

                #GOOGLE DRIVE API SET UP
                CLIENT_SECRET_FILE = 'PATH TO YOUR CLIENT SECRET FILE'
                API_NAME = 'drive'
                API_VERSION = 'v3'
                SCOPES = ['https://www.googleapis.com/auth/drive']
                service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

                #UPLOAD ZIP FILE TO GOOGLE DRIVE
                # Upload a file
                file_metadata = {
                    'name': filename,
                    'parents': ['FOLDER ID OF WHERE YOU WANT TO STORE ALBUMS']
                }
                
                media_content = MediaFileUpload(path + "/" + filename, mimetype='application/zip')

                file = service.files().create(
                    body=file_metadata,

                    media_body=media_content
                ).execute()

                #GET FILE ID FOR THE FILE
                # Update Sharing Setting
                file_id = file['id']

                request_body = {
                    'role': 'reader',
                    'type': 'anyone'
                }

                response_permission = service.permissions().create(
                    fileId=file_id,
                    body=request_body
                ).execute()

                # Print Sharing URL
                response_share_link = service.files().get(
                    fileId=file_id,
                    fields='webViewLink'
                ).execute()

                #APPEND TO THE MESSAGE BODY
                body = body + " -> Link to secure zip file: " + response_share_link['webViewLink']

            else:
                path = os.getcwd()
                filename = song.title + " lyrics.txt"
                with open(path + '/' + filename,'rb') as file:
                    message.attach(MIMEApplication(file.read(), Name=filename))

            # Add body to email
            message.attach(MIMEText(body, "plain"))
            
            # Add attachment to message and convert message to string
            #message.attach(part)
            text = message.as_string()
            
            #Setup email server and send email
            smtp_object = smtplib.SMTP('smtp.gmail.com',587)
            smtp_object.ehlo()
            smtp_object.starttls()
            
            smtp_object.login(sender_email,password)
            exampleDict = smtp_object.sendmail(sender_email,receiver_email,text)
            
            if not(exampleDict):
                print(Fore.GREEN + "\nEmail sent successfully!")
                print(Style.RESET_ALL + "")
            else:
                print(FORE.RED + "\nEmail did not send!")
                print(Style.RESET_ALL + "")
            
            smtp_object.quit()
            
            validInput = True
                
            
        elif (yesOrNo[0].lower() == 'n'):
            validInput = True
        else:
            print(Fore.RED + "Invalid input, try again!")
            print(Style.RESET_ALL + "")
            validInput = False
    
    #Prompt the user if they would like to use the program again
    
    validInput = False
    
    while not(validInput):
        yesOrNo = input("\nAre you done using this program? (y/n): ")
        
        if (yesOrNo[0].lower() == 'y'):
            stillSearching = False
            validInput = True
        elif (yesOrNo[0].lower() == 'n'):
            stillSearching = True
            validInput = True
        else:
            validInput = False
            print(Fore.RED + "Invalid input, try again!")
            print(Style.RESET_ALL + "")
    
    print("\n")
    
print("\n\nTHANK YOU FOR USING LYRICLOVER!")
