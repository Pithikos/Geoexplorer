from lxml import etree

class GoogleResponse():
   
   # eTree
   root = None
   results = None
   
   # Parsed
   status = None
   
   # Stats
   resultsN = 0

   # Returns status of response
   def __init__(self, response):
      self.root = etree.fromstring(response)
      self.status = self.root[0].text
      self.results = []
      
      if (self.status=='OK'):
         for result in self.root.findall('result'):
            loc = result.findall('.//location')[0]
            newResult = {}
            newResult['location']  = (loc[0].text, loc[1].text)
            newResult['reference'] = result.findall('reference')[0].text
            newResult['id']        = result.findall('id')[0].text
            self.results.append(newResult)
            self.resultsN+=1
            #print(etree.tostring(result).decode("utf-8"))
