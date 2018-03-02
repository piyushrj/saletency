# importing necessory libraries
import re
import urllib.request as urllib2
from bs4 import BeautifulSoup
# parsing the html
url = 'https://www.fundoodata.com/companies-detail/BASF-India-Ltd/4899.html' #url of the webpage to scrape
htmlfile = urllib2.urlopen(url)
soup = BeautifulSoup(htmlfile, 'html.parser')
# company name
comp_name_box = soup.find('div', attrs={'class':'search-page-heading-red'})
comp_name = comp_name_box.text.strip()
# company type details
comp_box = soup.find_all('div', attrs={'class':'overview-box2'})
useful_comp_box = comp_box[:-2]

cb = []
for u in useful_comp_box:
    cb.append(u.text.strip())
comp_dict = {
    'Industry': cb[0][9:],
    'Company Type': cb[1][13:],
    'Sector': cb[2][7:]
    }
#company contact details
comp_contact_box = soup.find('div', attrs={'class':'detail-line'})
comp_contact = comp_contact_box.text.strip()
nl_pos = comp_contact.index('\n')
contact_dict = {
    'Phone': comp_contact[:(nl_pos-1)],
    'Website': comp_contact[(nl_pos+2):]
    }
#company address
regex = '<font style="color:#c00508">Address</font>\s*-\s*(.*)<br\s*[/,.]*>\n*\s*.*;(.*)<div'
pattern = re.compile(regex)
html_file = urllib2.urlopen(url)
html_text = html_file.read()
matches = re.findall(pattern, html_text.decode('utf-8'))

line1 = matches[0][0].split(',')
local_add = ''
for i in range(len(line1)):
    line1[i] = line1[i].strip()
    local_add += line1[i]+", "
local_add = local_add[:len(local_add)-2]

line2 = matches[0][1].split(',')
i2 = line2[0].index('\t')
comp_address = {
    'City': line2[0][:i2],
    'State': line2[0][(i2+17):],
    'Pin': line2[1].strip(),
    'Address': local_add
    }
# Concatenating the details into a single dictionary
company_details = {
    'Name': comp_name
}
company_details = {**company_details, **comp_address, **comp_dict, **contact_dict}

#Exporting the company details to a text file
f = open("Company_data.txt","w") # change the name of the output file here accordingly
f.write( str(company_details) )
f.close()
