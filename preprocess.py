import json

filePath = 'Scrapy\\CCDSwScrapy\\results.json'
i = 0
aa = []

with open(filePath, 'r+') as f:
    data = json.load(f)
    for d in data:
        try:
            for c in d['CCDS']:
                for n in c['CDSNT']:
                    if(len(n) != 3):
                        i += 1
                        print(
                            'gene: ' + d["GeneName"] + '\n' +
                            'cdsId: ' + c["CDSID"]  + '\n' +
                            'Nucleotide: ' + n  + '\n'
                        )
                for a in c['CDSAA']:
                    if a not in aa:
                        aa.append(a)
        except:
            print(
                'gene: ' + d["GeneName"] + '\n' +
                'cdsId: None' + '\n'
            )

print('Total oopsies: ' + str(i/2))
print('Total # of amino acids: ' + str(len(aa)))
print('Amino acids:\n')
print(aa)
