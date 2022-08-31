#messy code at the moment, will clean up later
from random import random

import xlsxwriter
from instagrapi import *
import PIL

#also need to install Pillow

#This is where you can change which hashtag to use, NO CAPITALS
hashtag = 'bronchitis'

#These are the list of suffixes to find in the Instagram Profile, you can add more by adding a comma and wrapping the word with ''
suffixes = ['M.D','Drs','Dr.','MDs', 'MD','dr','do','md','m.d.' 'dra','medicine','d.c','therapist','nutrition','np','N.P.','N.P','health', 'diet','coach','diet','medicine','clinic','founder', hashtag,'blog','nonprofit','profit','practioner']

#This is how many account you could screen, I went up to 4000 at one point but it might take a very very very long time to generate and failure could be very possible

#I would recommend the 100-200 range, or even lower
numberOfAccounts = 3


#DOWNLOAD AS A ZIP FILE AFTER RUNNING.

cl = Client()

#This is the instagram account used, ignore the too many requests error and continue login
cl.login("country.clubs", "cachetcountryclub")
print("Logged in ")

workbook = xlsxwriter.Workbook('Contacts.xlsx')
worksheet = workbook.add_worksheet()
number_format = workbook.add_format({'num_format': '#,##0'})

def hit(validname):
    print()
    print("Valid Name: " + validname)
    print()
missed_usernames = []
missed_full_names = []
missed_external_links = []
missed_profile_link = []
missed_biography = []
missed_followers = []
missed_email = []
missed_contact = []
usernames = []
full_names = []
external_links = []
profile_link = []
biography = []
followers = []
theSuffix = []
rating = []
email =[]
data = []
contact = []
users_list = []
medias = cl.hashtag_medias_top(hashtag, amount=numberOfAccounts)

for media in medias:
    userZ = cl.user_info_by_username(media.user.username)
    print(userZ)
    if userZ.username not in users_list:
        users_list.append(userZ.username)
        if int(userZ.follower_count) > 400:
            missed_usernames.append(userZ.username)
            missed_full_names.append((userZ.full_name))
            missed_external_links.append(userZ.external_url)
            missed_followers.append(userZ.follower_count)
            missed_biography.append(userZ.biography)
            missed_profile_link.append('https://www.instagram.com/' + userZ.username + '/')
            missed_email.append(userZ.public_email)
            missed_contact.append(userZ.business_contact_method)
            for suffix in suffixes:
                if suffix in userZ.full_name.lower() or suffix in userZ.username or suffix in userZ.biography.lower():
                    hit(userZ.username)
                    usernames.append(userZ.username)
                    full_names.append((userZ.full_name))
                    external_links.append(userZ.external_url)
                    followers.append(userZ.follower_count)
                    biography.append(userZ.biography)
                    profile_link.append('https://www.instagram.com/'+userZ.username+'/')
                    theSuffix.append(suffix)
                    email.append(userZ.public_email)
                    contact.append(userZ.business_contact_method)

                    missed_usernames.remove(userZ.username)
                    missed_full_names.remove((userZ.full_name))
                    missed_external_links.remove(userZ.external_url)
                    missed_followers.remove(userZ.follower_count)
                    missed_biography.remove(userZ.biography)
                    missed_profile_link.remove('https://www.instagram.com/' + userZ.username + '/')
                    missed_email.remove(userZ.public_email)
                    missed_contact.remove(userZ.business_contact_method)
                    break

print(len(missed_usernames),len(missed_biography),len(missed_followers),len(missed_full_names),len(missed_profile_link),len(missed_external_links))

for i in range(len(usernames)):
    data.append(['#', hashtag, '',usernames[i], '', full_names[i], '', '',external_links[i],profile_link[i],followers[i],theSuffix[i],email[i],contact[i], biography[i]])

for i in range(len(missed_usernames)):
    data.append(['#', hashtag, '',missed_usernames[i], '', missed_full_names[i], '', '',missed_external_links[i],missed_profile_link[i],missed_followers[i],'', missed_email[i],missed_contact[i],missed_biography[i]])



worksheet.add_table('A1:P1000',{'data':data,
                'columns':            [{'header': 'Valid'},
                                      {'header': 'Hashtag'},
                                      {},
                                      {'header': 'Username'},
                                      {},
                                      {'header': 'Name'},
                                      {},
                                      {},
                                      {'header': 'External Link'},
                                      {'header': 'Profile Link'},
                                      {'header': 'Follower Count',
                                       'format': number_format},
                                      {'header': 'Suffix'},
                                      {'header': 'Category'},
                                       {'header':'email'},
                                       {'header':'contact'},
                                       {'header': 'Biography'}
                            ]
                           }
                )




workbook.close()


for i in range(8):
  print()

print("Total pulled:",len(usernames))
print('OPEN THE CONTACTS.XLSX')