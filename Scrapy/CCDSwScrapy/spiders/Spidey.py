import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import GeneItem, CDSItem

"""CSS Selectors"""

#   URL:                    https://www.ncbi.nlm.nih.gov/gene/{Gene Id}/
#   Current URL:            response.request.url

#   Gene Name:              .gn
#   Gene ID:                .geneid
#   CCDS URL:               //*[@id="ui-portlet_content-3"]/ul/li/a[contains(text(), 'CCDS')] // bad .brieflinkpopper:nth-child(11) .brieflinkpopperctrl

#   CDS ID:                 h3+ table td:nth-child(1) small
#   CDS URL:                + a:nth-child(5)

#   Nucleotide Sequence:    table tr:nth-child(4) td table:nth-child(1) tr td:nth-child(3) tt font span font
#   Translation:            table tr:nth-child(4) td table:nth-child(1) tr td:nth-child(3) font tt font span


class Spidey(scrapy.Spider):
    name = "Parker"


    start_urls = [
        "https://www.ncbi.nlm.nih.gov/gene/207/",
        "https://www.ncbi.nlm.nih.gov/gene/324/",
        "https://www.ncbi.nlm.nih.gov/gene/6790/",
        "https://www.ncbi.nlm.nih.gov/gene/8313/",
        "https://www.ncbi.nlm.nih.gov/gene/581/",
        "https://www.ncbi.nlm.nih.gov/gene/657/",
        "https://www.ncbi.nlm.nih.gov/gene/673/",
        "https://www.ncbi.nlm.nih.gov/gene/699/",
        "https://www.ncbi.nlm.nih.gov/gene/701/",
        "https://www.ncbi.nlm.nih.gov/gene/843/",
        "https://www.ncbi.nlm.nih.gov/gene/595/",
        "https://www.ncbi.nlm.nih.gov/gene/11200/",
        "https://www.ncbi.nlm.nih.gov/gene/1499/",
        "https://www.ncbi.nlm.nih.gov/gene/1630/",
        "https://www.ncbi.nlm.nih.gov/gene/10395/",
        "https://www.ncbi.nlm.nih.gov/gene/1956/",
        "https://www.ncbi.nlm.nih.gov/gene/2033/",
        "https://www.ncbi.nlm.nih.gov/gene/4072/",
        "https://www.ncbi.nlm.nih.gov/gene/2064/",
        "https://www.ncbi.nlm.nih.gov/gene/2263/",
        "https://www.ncbi.nlm.nih.gov/gene/2261/",
        "https://www.ncbi.nlm.nih.gov/gene/201163/",
        "https://www.ncbi.nlm.nih.gov/gene/3553/",
        "https://www.ncbi.nlm.nih.gov/gene/3557/",
        "https://www.ncbi.nlm.nih.gov/gene/3659/",
        "https://www.ncbi.nlm.nih.gov/gene/1316/",
        "https://www.ncbi.nlm.nih.gov/gene/3845/",
        "https://www.ncbi.nlm.nih.gov/gene/553989/",
        "https://www.ncbi.nlm.nih.gov/gene/4163/",
        "https://www.ncbi.nlm.nih.gov/gene/4292/",
        "https://www.ncbi.nlm.nih.gov/gene/27030/",
        "https://www.ncbi.nlm.nih.gov/gene/4436/",
        "https://www.ncbi.nlm.nih.gov/gene/2956/",
        "https://www.ncbi.nlm.nih.gov/gene/4595/",
        "https://www.ncbi.nlm.nih.gov/gene/4893/",
        "https://www.ncbi.nlm.nih.gov/gene/4913/",
        "https://www.ncbi.nlm.nih.gov/gene/5157/",
        "https://www.ncbi.nlm.nih.gov/gene/5290/",
        "https://www.ncbi.nlm.nih.gov/gene/5320/",
        "https://www.ncbi.nlm.nih.gov/gene/5378/",
        "https://www.ncbi.nlm.nih.gov/gene/5395/",
        "https://www.ncbi.nlm.nih.gov/gene/5782/",
        "https://www.ncbi.nlm.nih.gov/gene/5795/",
        "https://www.ncbi.nlm.nih.gov/gene/285282/",
        "https://www.ncbi.nlm.nih.gov/gene/25788/",
        "https://www.ncbi.nlm.nih.gov/gene/54894/",
        "https://www.ncbi.nlm.nih.gov/gene/6223/",
        "https://www.ncbi.nlm.nih.gov/gene/30011/",
        "https://www.ncbi.nlm.nih.gov/gene/4089/",
        "https://www.ncbi.nlm.nih.gov/gene/4092/",
        "https://www.ncbi.nlm.nih.gov/gene/6714/",
        "https://www.ncbi.nlm.nih.gov/gene/6794/",
        "https://www.ncbi.nlm.nih.gov/gene/7048/",
        "https://www.ncbi.nlm.nih.gov/gene/7097/",
        "https://www.ncbi.nlm.nih.gov/gene/7157/"
        "https://www.ncbi.nlm.nih.gov/gene/100187710/",
        "https://www.ncbi.nlm.nih.gov/gene/100187711/",
        "https://www.ncbi.nlm.nih.gov/gene/2120/",
        "https://www.ncbi.nlm.nih.gov/gene/79695/",
        "https://www.ncbi.nlm.nih.gov/gene/100144748/",
        "https://www.ncbi.nlm.nih.gov/gene/4437/",
        "https://www.ncbi.nlm.nih.gov/gene/5424/",
        "https://www.ncbi.nlm.nih.gov/gene/5426/",
        "https://www.ncbi.nlm.nih.gov/gene/25913/",
        "https://www.ncbi.nlm.nih.gov/gene/10483/",
        "https://www.ncbi.nlm.nih.gov/gene/54658/"
    ]


    def parse(self, response):
        gene = GeneItem()
        
        gene['GeneName'] = response.css('.gn::text').extract_first()
        
        gene['GeneID'] = response.css('.geneid::text').extract_first().split(' ')[2][:-1] # its in the link as well
        
        gene['GeneURL'] = response.request.url
        
        #gene['CCDSURL'] = "https://www.ncbi.nlm.nih.gov" + response.xpath('//*[@id="ui-portlet_content-3"]/ul/li/a[contains(text(), "CCDS")]/@href').extract_first()
        gene['CCDSURL'] = 'https://www.ncbi.nlm.nih.gov/CCDS/CcdsBrowse.cgi?REQUEST=GENEID&DATA=' + gene['GeneID']

        return scrapy.Request(gene['CCDSURL'],
                             callback=self.CCDSs,
                             cb_kwargs=dict(gene=gene))


    def CCDSs(self, response, gene):
        
        #cdss = response.css('h3+ table td:nth-child(1) small::text, img+ a:nth-child(5)::attr(href)').extract()
        #cdss = {cdss[i]: 'https://www.ncbi.nlm.nih.gov/CCDS/CcdsBrowse.cgi' + cdss[i + 1] for i in range(0, len(cdss), 2)}
        
        #cdss = {cdss[i]: 'https://www.ncbi.nlm.nih.gov/CCDS/CcdsBrowse.cgi' + cdss[i + 1] for i in range(0, len(cdss), 2)}

        cdsurls = response.css('img+ a:nth-child(5)::attr(href)').extract()
        if(len(cdsurls) != 0):
            yield scrapy.Request('https://www.ncbi.nlm.nih.gov/CCDS/CcdsBrowse.cgi' + cdsurls[0],
                                callback=self.CDS,
                                cb_kwargs=dict(geneItem=gene, urls=cdsurls))
        else:
            yield gene


    def CDS(self, response, geneItem, urls):

        cds = CDSItem()

        cds['CDSID'] = response.css('h3+ table td:nth-child(1) small::text').extract_first()
        
        cds['CDSURL'] = response.request.url
        
        nt = response.css('table tr:nth-child(4) td table:nth-child(1) tr td:nth-child(3) tt font span font::text').extract()
        i = len(nt)
        n = 0
        while n in range(i):
            if len(nt[n]) !=3:
                nt[n:n+2] = [''.join(nt[n:n+2])]
                i -= 1
            n += 1
        cds['CDSNT'] = nt

        cds['CDSAA'] = response.css('table tr:nth-child(4) td table:nth-child(1) tr td:nth-child(3) font tt font span::text').extract()


        geneItem.setdefault('CCDS', []).append(cds)

        if(len(urls) == 1):
            yield geneItem
        else:
            del urls[0]
            yield scrapy.Request('https://www.ncbi.nlm.nih.gov/CCDS/CcdsBrowse.cgi' + urls[0],
                        callback=self.CDS,
                        cb_kwargs=dict(geneItem=geneItem, urls=urls))


""" For debugging only """
# process = CrawlerProcess()
# process.crawl(Spidey)
# process.start()