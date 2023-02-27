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