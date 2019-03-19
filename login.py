#! /usr/bin/python3

# Full package imports
import webbrowser, time, imaplib, email, mailbox, datetime, os, mimetypes
#Partial package imports 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Local package imports
from secrets import blaze_user, blaze_password, fncc_user, fncc_password, gmail_password

def main():
    
    # login()
    # enterCredentials()
    # sendTwoFactor()
    # getVerificationCode()

    # Open and login to Blaze CC
    print("Logging into Blaze...")
    
    # Create browser instance and set arguments/options/location of .exe
    browser = webdriver.ChromeOptions()
    browser.add_argument('--ignore-certificate-errors')
    browser.add_argument('--disable-infobars')
    browser.binary_location = "/usr/bin/chromium"
    
    driver = webdriver.Chrome(options=browser)
    driver.get('https://blazecc.com/CardMemberServices/default.aspx')
    time.sleep(1)
    
    # Find username field, move to it with cursor, wait 1 sec, enter username
    user_field = driver.find_element_by_id('ctl00_ContentPlaceHolder1_LoginView1_Login1_UserName')
    user_field.send_keys(blaze_user)
    time.sleep(1)
    
    # Find password field, move to it with cursor, wait 1 sec, enter password           
    password_field = driver.find_element_by_id('ctl00_ContentPlaceHolder1_LoginView1_Login1_Password')
    password_field.send_keys(blaze_password)
    time.sleep(1)
    
    # Find login button, move to it with cursor, wait .5 sec, click to move to 2FA
    login = driver.find_element_by_id('ctl00_ContentPlaceHolder1_LoginView1_Login1_LoginButton').click()
  
    # 2FA - email selection, then send email button clicked
    two_factor = driver.find_element_by_id('rblCommunicationOptions_0').click()
    enter = driver.find_element_by_id('btnNext').click()
    time.sleep(5)
  
######### Email reading code #############################
    imap_url = 'imap.gmail.com'
    username = 'jamesa.benn@gmail.com' #'test1345637'
    password = gmail_password

    connection = imaplib.IMAP4_SSL(imap_url, 993)
    connection.login(username, password)
    connection.select('INBOX')
   
    # reponse = connection response code | data = data in rest of list
    response, data = connection.uid('search', None, "ALL")
    #print(data)
    inbox_item_list = data[0].split()
    #print(inbox_item_list)
    
    # Pull one email at a time by oldest/newest
    #oldest = inbox_item_list[0]
    most_recent = inbox_item_list[-1] # Find and assign most recent email 
    
    # Pull all/multiple emails 
    #for item in inbox_item_list:  >  Dealing with multiple messages 
    result2, email_data = connection.uid('fetch', most_recent, '(RFC822)' )
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    #print(dir(email_message))
    to_ = email_message['To']
    from_ = email_message['From']
    subject_ = email_message['Subject']
    date_ = email_message['Date']
    
    counter = 1
    for part in email_message.walk():
        if part.get_content_maintype() == "multipart":
            continue
        filename = part.get_filename()
        content_type = part.get_content_type()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                ext = '.bin'
            filename = 'msg-part-%08d%s' %(counter, ext)
            
        counter += 1
        
        # save file
        email_save_path = os.path.join(os.getcwd(), "emails", date_, subject_) 
        if not os.path.exists(email_save_path):
            os.makedirs(email_save_path)
        with open(os.path.join(email_save_path, filename), 'wb') as fp:
            fp.write(part.get_payload(decode=True))
        
        # Parse verification code from second index (3rd line) of mail body
        code = ''  
        with open(email_save_path + '/' + filename, 'r') as filehandle:
          #  line = filehandle.readline()
          #  count = 1
          #  while line:
          #      print('Line {}: {}'.format(count, line.strip()))
          #      line = filehandle.readline()
          #      count += 1
            
            for count, line in enumerate(filehandle):
                if count == 2:
                    soup = BeautifulSoup(line, "html.parser")
                    code = soup.get_text("|", strip=True) 
  
  ##################################################
  
    print("Got verification code from email...")
    # Find verification code field, enter code pulled from email, click Submit
    verification_code_field = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtPasscode')
    verification_code_field.send_keys(code)
    time.sleep(.1)
    final_submit = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSubmit').click()
    print("Logging in...")
    driver.save_screenshot(os.path.join('Screenshots/Blaze/screenshot_' + time.asctime() + '.png'))
    print("Took screenshot of Account Summary...")
    print("Closing...")
    driver.close()
     
#########################################################
    
    # Open and log into First National CC 
    print("Logging into FNCC...")
    browser = webdriver.ChromeOptions()
    browser.add_argument('--ignore-certificate-errors')
    browser.add_argument('--disable-infobars')
    browser.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(options = browser)
    driver.get('https://firstnationalcc.com/CardMemberServices/default.aspx')
    time.sleep(.2)
    user = driver.find_element_by_id('ctl00_ContentPlaceHolder1_LoginView1_Login1_UserName')
    user.send_keys(fncc_user)
    time.sleep(.1)
    pw = driver.find_element_by_id('ctl00_ContentPlaceHolder1_LoginView1_Login1_Password')
    pw.send_keys(fncc_password)
    login = driver.find_element_by_id('ctl00_ContentPlaceHolder1_LoginView1_Login1_LoginButton').click()
    time.sleep(1)
    two_factor = driver.find_element_by_id('rblCommunicationOptions_0').click()
  
    enter = driver.find_element_by_id('btnNext').click()
    time.sleep(3)
  
############ Email reading code ########################
    imap_url = 'imap.gmail.com'
    username = 'jamesa.benn@gmail.com' #'test1345637'
    password = gmail_password

    connection = imaplib.IMAP4_SSL(imap_url, 993)
    connection.login(username, password)
    connection.select('INBOX')
   
    # reponse = connection response code | data = data in rest of list
    response, data = connection.uid('search', None, "ALL")
    #print(data)
    inbox_item_list = data[0].split()
    #print(inbox_item_list)
    
    # Pull one email at a time by oldest/newest
    #oldest = inbox_item_list[0]
    most_recent = inbox_item_list[-1] # Find and assign most recent email 
    
    # Pull all/multiple emails 
    #for item in inbox_item_list:  >  Dealing with multiple messages 
    result2, email_data = connection.uid('fetch', most_recent, '(RFC822)' )
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    #print(dir(email_message))
    to_ = email_message['To']
    from_ = email_message['From']
    subject_ = email_message['Subject']
    date_ = email_message['Date']
    
    counter = 1
    for part in email_message.walk():
        if part.get_content_maintype() == "multipart":
            continue
        filename = part.get_filename()
        content_type = part.get_content_type()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                ext = '.bin'
            filename = 'msg-part-%08d%s' %(counter, ext)
            
        counter += 1
        
        # save file
        email_save_path = os.path.join(os.getcwd(), "emails", date_, subject_) 
        if not os.path.exists(email_save_path):
            os.makedirs(email_save_path)
        with open(os.path.join(email_save_path, filename), 'wb') as fp:
            fp.write(part.get_payload(decode=True))
        
        # Parse verification code from second index (3rd line) of mail body
        code = ''  
        with open(email_save_path + '/' + filename, 'r') as filehandle:
          #  line = filehandle.readline()
          #  count = 1
          #  while line:
          #      print('Line {}: {}'.format(count, line.strip()))
          #      line = filehandle.readline()
          #      count += 1
            
            for count, line in enumerate(filehandle):
                if count == 2:
                    soup = BeautifulSoup(line, "html.parser")
                    code = soup.get_text("|", strip=True) 
  
  #########################################################
  
    print("Got verification code from email...")
    # Find verification code field, enter code pulled from email, click Submit
    verification_code_field = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtPasscode')
    verification_code_field.send_keys(code)
    time.sleep(.1)
    final_submit = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSubmit').click()
    print("Logging in...")
    driver.save_screenshot(os.path.join('Screenshots/FNCC/screenshot_' + time.asctime() + '.png'))
    print("Took screenshot of Account Summary...")
    print("Closing...")
    driver.close()
    
    

main()
