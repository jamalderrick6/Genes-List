#simple crawler program that will scrape out the name of all the genes
import csv

import requests
from lxml import html
base_url = 'https://ghr.nlm.nih.gov'
fieldnames = ['INITIAL', 'GENE NAME', 'NORMAL FUNCTION', 'HEALTH CONDITIONS RELATED TO GENETIC CHANGE']
target_url = 'https://ghr.nlm.nih.gov/gene'
output = []
#scrape out the letters of genes from the main page
response = requests.get(target_url)
content = response.content
doc = html.fromstring(content)

letters_url = doc.xpath('//*[@id="skip"]//ol[@class="browse-btn clearfix"]/li/a/@href')
for letter_url in letters_url:
    list_url = base_url + letter_url
    #scrape out the name of the genes in every gene_url
    list_response = requests.get(list_url)
    list_content = list_response.content
    list_doc = html.fromstring(list_content)

    genes_list_url = list_doc.xpath('//*[@id="skip"]//ul[@class = "browse-results"]/li/a/@href')
    for gene_url in genes_list_url:
        gene = base_url + gene_url
        gene_response = requests.get(gene)
        gene_content = gene_response.content
        gene_doc = html.fromstring(gene_content)
        #scrape out the gene information
        gene_initial = ''.join(gene_doc.xpath('.//*[@id="skip"]//h1[@class = "genes"]/text()')).replace('gene','')
        gene_name = ''.join(gene_doc.xpath('.//*[@id="skip"]//h2[@class = "gene-full-name"]/text()'))
        normal_function = ''.join(gene_doc.xpath('normalize-space(string(.//div[@class="col-md-8"]/div))'))
        health_conditions = ''.join(gene_doc.xpath('normalize-space(string(.//div[@class="sub-section-ec-area"]/section))')).replace('More About This Health Condition','')
        values = [gene_initial, gene_name, normal_function, health_conditions]
        resp = dict(zip(fieldnames, values))
        output.append(resp)
    # print(output)
    print(len(output))

    with open("genes.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for row in output:
            writer.writerow(row)






