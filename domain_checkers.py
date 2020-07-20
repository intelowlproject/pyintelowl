import geocoder
from datetime import datetime
import os




class mycolors():

    reset='\033[0m'
    reverse='\033[07m'
    bold='\033[01m'
    class foreground:
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        lightgreen='\033[92m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
        red='\033[31m'
        green='\033[32m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        yellow='\033[93m'
    class background:
        black='\033[40m'
        blue='\033[44m'
        cyan='\033[46m'
        lightgrey='\033[47m'
        purple='\033[45m'
        green='\033[42m'
        orange='\033[43m'
        red='\033[41m'

class Checkers():
    def __init__(self, results, value):
        self.results = results
        self.value = value
    
    def check_domain(self):
        vt = {}
        ha = {}
        otx = {}
        if bool(self.results):
            for i in self.results:
                if 'HybridAnalysis_Get_Observable' in i['name']:
                    ha.update(i)   
                elif 'VirusTotal_v2_Get_Observable' in i['name']:
                    vt.update(i)               
                elif "OTXQuery" in i['name']:
                    otx.update(i)
              
        if vt:
            try:
                if "VirusTotal_v2" in vt['name']:
                    domains = Domains(vt['report'],self.value)                    
                    domains.vtDomaincheck()
            except KeyError:
                print(mycolors.foreground.lightred + "\nERROR: Try using VirusTotal_v2_Get_Observable instead!\n")
        if ha:
            domains = Domains(ha['report'],self.value)
            domains.haDomaincheck()
        if otx:
            domains = Domains(otx['report'], self.value)
            domains.otxDomaincheck()
            
    def check_hash(self):
        vt = {}
        ha = {}
        otx = {}
        for i in self.results:
            if 'HybridAnalysis_Get_Observable' in i['name']:
                ha.update(i)   
            elif 'VirusTotal_v3_Get_Observable' in i['name']:
                vt.update(i)               
            elif "OTXQuery" in i['name']:
                otx.update(i)        
                
        if vt:
            if "VirusTotal_v3" in vt['name']:
                hashes = Hashes(vt['report'],self.value)
                hashes.vthash()
            else:
                print(mycolors.foreground.lightred + "\nERROR: Try using VirusTotal_v3_Get_Observable instead!\n")
        if ha:
            hashes = Hashes(ha['report'],self.value)            
            hashes.hahash()
        if otx:
            hashes = Hashes(otx['report'],self.value)                        
            hashes.otxhash()
            
    def check_ip(self):
        vt = {}
        ha = {}
        otx = {}
        abusedb = {}
        censys = {}
        greynoise = {}
        for i in self.results:
            if 'HybridAnalysis_Get_Observable' in i['name']:
                ha.update(i)   
            elif 'VirusTotal_v2_Get_Observable' in i['name']:
                vt.update(i)               
            elif "OTXQuery" in i['name']:
                otx.update(i)
            elif "AbuseIPDB" in i['name']:
                abusedb.update(i)
            elif "Censys_Search" in i['name']:
                censys.update(i)
            elif "GreyNoiseAlpha" in i['name']:
                greynoise.update(i)
        
        
        if abusedb:
            ips = IPs(abusedb['report']['data'], self.value)
            ips.abIPdbcheck()
        if censys:
            ips = IPs(censys['report'], self.value)            
            ips.censysIPcheck()
        if greynoise:
            ips = IPs(greynoise['report'], self.value)                        
            ips.gnoiseIPcheck()
        if vt:
            try:
                if "VirusTotal_v2" in vt['name']:
                    ips = IPs(vt['report'], self.value)                                            
                    ips.vtIPcheck()
            except KeyError:
                print(mycolors.foreground.lightred + "\nERROR: Try using VirusTotal_v2_Get_Observable instead!\n")
            
        if ha:
            ips = IPs(ha['report'], self.value)                                                        
            ips.haIPcheck()
        if otx:
            ips = IPs(otx['report'], self.value)                                                    
            ips.otxIPcheck()    

               
class Domains():
    def __init__(self, text, value):
        self.text = text
        self.value = value    
        
    def vtDomaincheck(self):
        try:
            print(mycolors.reset)
            print("\n\tDOMAIN SUMMARY REPORT")
            print("-"*20,"\n")
    
            
            print(mycolors.foreground.lightblue,mycolors.background.lightgrey)
            print("\nVIRUSTOTAL SUMMARY")
            print("-"*20) 
            print(mycolors.reset)            

    
            if 'undetected_referrer_samples' in self.text:
                print(mycolors.foreground.lightcyan + "Undetected Referrer Samples: ".ljust(17))
                if (bool(self.text['undetected_referrer_samples'])):
                    try:
                        for i in range(0, len(self.text['undetected_referrer_samples'])):
                            if (self.text['undetected_referrer_samples'][i].get('date')):
                                print("".ljust(28), end=' ')
                                print(f"Date: {self.text['undetected_referrer_samples'][i]['date']}")
                            if (self.text['undetected_referrer_samples'][i].get('positives')):
                                print("".ljust(28), end=' ')
                                print(f"Positives: {self.text['undetected_referrer_samples'][i]['positives']}")
                            if (self.text['undetected_referrer_samples'][i].get('total')):
                                print("".ljust(28), end=' ')
                                print(f"Total: {self.text['undetected_referrer_samples'][i]['total']}")
                            if (self.text['undetected_referrer_samples'][i].get('sha256')):
                                print("".ljust(28), end=' ')
                                print((f"SHA256: {self.text['undetected_referrer_samples'][i]['sha256']}"), end=' ')
                            print("\n")
                    except KeyError as e:
                        pass
    
    
    

    
            if 'detected_referrer_samples' in self.text:
                print("-"*20)
                print(mycolors.foreground.pink + "Detected Referrer Samples: ".ljust(17))                
                if (bool(self.text['detected_referrer_samples'])):
                    try:
                        for i in range(len(self.text['detected_referrer_samples'])):
                            if (self.text['detected_referrer_samples'][i].get('date')):
                                print("".ljust(28), end=' ')
                                print(f"Date: {self.text['detected_referrer_samples'][i]['date']}")
                            if (self.text['detected_referrer_samples'][i].get('positives')):
                                print("".ljust(28), end=' ')
                                print(f"Positives: {self.text['detected_referrer_samples'][i]['positives']}")
                            if (self.text['detected_referrer_samples'][i].get('total')):
                                print("".ljust(28), end=' ')
                                print(f"Total: {self.text['detected_referrer_samples'][i]['total']}")
                            if (self.text['detected_referrer_samples'][i].get('sha256')):
                                print("".ljust(28), end=' ')
                                print((f"SHA256: {self.text['detected_referrer_samples'][i]['sha256']}"), end=' ')
                            print("\n")
                    except KeyError as e:
                        pass
    
    
            print("-"*20)
            print(mycolors.foreground.yellow + "\nWhois Timestamp: ".ljust(17))
    
            if 'whois_timestamp' in self.text:
                if (bool(self.text['whois_timestamp'])):
                    try:
                        print("".ljust(28), end=' ') 
                        ts = self.text['whois_timestamp']
                        print((datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:{}')))
                    except KeyError as e:
                        pass
    
    

    
            if 'undetected_downloaded_samples' in self.text:
                print("-"*20)
                print(mycolors.foreground.lightgreen + "\nUndetected Downld. Samples: ".ljust(17))                
                if (bool(self.text['undetected_downloaded_samples'])):
                    try:
                        for i in range(len(self.text['undetected_downloaded_samples'])):
                            if (self.text['undetected_downloaded_samples'][i].get('date')):
                                print("".ljust(28), end=' ')
                                print(f"Date: {self.text['undetected_downloaded_samples'][i]['date']}")
                            if (self.text['undetected_downloaded_samples'][i].get('positives')):
                                print("".ljust(28), end=' ')
                                print(f"Positives: {self.text['undetected_downloaded_samples'][i]['positives']}")
                            if (self.text['undetected_downloaded_samples'][i].get('total')):
                                print("".ljust(28), end=' ')
                                print(f"Total: {self.text['undetected_downloaded_samples'][i]['total']}")
                            if (self.text['undetected_downloaded_samples'][i].get('sha256')):
                                print("".ljust(28), end=' ')
                                print((f"SHA256: {self.text['detected_referrer_samples'][i]['sha256']}"), end=' ')
                            print("\n")
                    except KeyError as e:
                        pass
    
            
    
            if 'detected_downloaded_samples' in self.text:
                print("-"*20)
                print(mycolors.foreground.orange + "\nDetected Downloaded Samples: ".ljust(17))                
                if (bool(self.text['detected_downloaded_samples'])):
                    try:
                        for i in range(len(self.text['detected_downloaded_samples'])):
                            if (self.text['detected_downloaded_samples'][i].get('date')):
                                print("".ljust(28), end=' ')
                                print(f"Date: {self.text['detected_downloaded_samples'][i]['date']}")
                            if (self.text['detected_downloaded_samples'][i].get('positives')):
                                print("".ljust(28), end=' ')
                                print(f"Positives: {self.text['detected_downloaded_samples'][i]['positives']}")
                            if (self.text['detected_downloaded_samples'][i].get('total')):
                                print("".ljust(28), end=' ')
                                print(f"total: {self.text['detected_downloaded_samples'][i]['total']}")
                            if (self.text['detected_downloaded_samples'][i].get('sha256')):
                                print("".ljust(28), end=' ')
                                print(f"sha256: {self.text['detected_downloaded_samples'][i]['sha256']}", end=' ')
                            print("\n")
                    except KeyError as e:
                        pass
                    
            
            
                              
            if 'detected_communicating_samples' in self.text:
                print("-"*20)                
                print(mycolors.foreground.lightcyan + "\nDetected Communicating Samples: \n".ljust(17))  
                if (bool(self.text['detected_communicating_samples'])):
                    try:
                        for i in range(0, len(self.text['detected_communicating_samples'])):
                            if (self.text['detected_communicating_samples'][i].get('date')):
                                print("".ljust(28), end=' ')
                                print(f"Date: {self.text['detected_communicating_samples'][i]['date']}")
                            if (self.text['detected_communicating_samples'][i].get('positives')):
                                print("".ljust(28), end=' ')
                                print(f"Positives: {self.text['detected_communicating_samples'][i]['positives']}")
                            if (self.text['detected_communicating_samples'][i].get('total')):
                                print("".ljust(28), end=' ')
                                print(f"Total: {self.text['detected_communicating_samples'][i]['total']}")
                            if (self.text['detected_communicating_samples'][i].get('sha256')):
                                print("".ljust(28), end=' ')
                                print((f"SHA256: {self.text['detected_communicating_samples'][i]['sha256']}"), end=' ')
                            print("\n")
                    except KeyError as e:
                        pass            
    
            
    
            if 'resolutions' in self.text:
                print("-"*20)
                print(mycolors.foreground.lightred + "Resolutions: ".ljust(17))                
                if (bool(self.text['resolutions'])):
                    try:
                        for i in range(len(self.text['resolutions'])):
                            if (self.text['resolutions'][i].get('last_resolved')):
                                print("".ljust(28), end=' ')
                                print(f"Last resolved: {self.text['resolutions'][i]['last_resolved']}")
                            if (self.text['resolutions'][i].get('ip_address')):
                                print("".ljust(28), end=' ')
                                print("IP address:   {}".format(self.text['resolutions'][i]['ip_address']), end=' ')
                                print("\t" + f"(City:{geocoder.ip(self.text['resolutions'][i]['ip_address']).city})")
                            print("\n")
                    except KeyError as e:
                        pass
    

    
            if 'subdomains' in self.text:
                print("-"*20)
                print(mycolors.foreground.lightgreen + "\nSubdomains: ".ljust(17))                
                if (bool(self.text['subdomains'])):
                    try:
                        for i in range(len(self.text['subdomains'])):
                            print("".ljust(28), end=' ') 
                            print((self.text['subdomains'][i]))
                    except KeyError as e:
                        pass
    
            
    
            if 'categories' in self.text:
                print("-"*20)                
                print(mycolors.foreground.lightcyan + "\nCategories: ".ljust(17))                
                if (bool(self.text['categories'])):
                    try:
                        for i in range(len(self.text['categories'])):
                            print("".ljust(28), end=' ')
                            print((self.text['categories'][i]))
                    except KeyError as e:
                        pass
    
    

    
            if 'domain_sublings' in self.text:
                print("-"*20)
                print(mycolors.foreground.lightcyan + "\nDomain Siblings: ".ljust(17))                
                if (bool(self.text['domain_sublings'])):
                    try:
                        for i in range(len(self.text['domain_siblings'])):
                            print("".ljust(28), end=' ')
                            print((self.text['domain_siblings'][i]), end=' ')
                        print("\n")
                    except KeyError as e:
                        pass
    
            

    
            if 'detected_urls' in self.text:
                print("-"*20)
                print(mycolors.foreground.yellow + "\nDetected URLs: ".ljust(17))                
                if (bool(self.text['detected_urls'])):
                    try:
                        for i in range(len(self.text['detected_urls'])):
                            if (self.text['detected_urls'][i].get('url')):
                                print("".ljust(28), end=' ')
                                print(("url: {}".format( self.text['detected_urls'][i]['url'])))
                            if (self.text['detected_urls'][i].get('positives')):
                                print("".ljust(28), end=' ')
                                print(("{}Positives: {}{}".format(mycolors.reset,mycolors.foreground.lightred,self.text['detected_urls'][i]['positives'])+mycolors.foreground.yellow))
                            if (self.text['detected_urls'][i].get('total')):
                                print("".ljust(28), end=' ')
                                print(("{}Total: {}{}".format(mycolors.reset,mycolors.foreground.lightgreen,self.text['detected_urls'][i]['total'])+mycolors.foreground.yellow))
                            if (self.text['detected_urls'][i].get('scan_date')):
                                print("".ljust(28), end=' ')
                                print("scan_date: {}".format( self.text['detected_urls'][i]['scan_date']), end=' ')
                            print("\n")
                    except KeyError as e:
                        pass
    

    
            if 'undetected_urls' in self.text:
                print("-"*20)
                print(mycolors.foreground.lightred + "\nUndetected URLs: ".ljust(17))                
                if (bool(self.text['undetected_urls'])):
                    try:
                        for i in range(len(self.text['undetected_urls'])):
                            print((mycolors.foreground.red + "".ljust(28)), end=' ')
                            print(("Data {}\n".format( i)))
                            for y in range(len(self.text['undetected_urls'][i])):
                                print((mycolors.foreground.lightgreen + "".ljust(28)), end=' ')
                                if (y == 0):
                                    print(("url:       "), end=' ')
                                if (y == 1):
                                    print(("sha256:    "), end=' ')
                                if (y == 2):
                                    print(("positives: "), end=' ')
                                if (y == 3):
                                    print(("total:     "), end=' ')
                                if (y == 4):
                                    print(("date:      "), end=' ')
                                print(self.text['undetected_urls'][i][y])
                        print("\n")
                    except KeyError as e:
                        pass
    
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to Virus Total!\n"))
            print(mycolors.reset)
        except (KeyError,TypeError):
            print(mycolors.foreground.lightred + "No results found in VirusTotal!\n")
            print(mycolors.reset) 
            pass            
            
    
    def haDomaincheck(self):
        try:
            print(mycolors.foreground.lightred,mycolors.background.lightgrey)
            print("\nHYBRIDANALYSIS SUMMARY")
            print("-"*20) 
            print(mycolors.reset)     
            
            print(mycolors.foreground.orange + "\nResults found: {}".format((self.text["count"])))
            print("-"*28)
            print(mycolors.reset)
            try:
                for i in range(len(self.text['result'])): 
                    if self.text['result'][i]['verdict'] != None:
                        print(mycolors.foreground.orange, "Verdict    => " + self.text['result'][i]['verdict'])
                    
                    print(mycolors.foreground.orange, "SHA256     => " + self.text['result'][i]['sha256'])
                    if self.text['result'][i]['av_detect'] != None:
                        print(mycolors.foreground.orange, "AV Detect  => " + self.text['result'][i]['av_detect'])
                    if self.text['result'][i]['vx_family'] != None:
                        print(mycolors.foreground.orange, "Mal Family => " + self.text['result'][i]['vx_family'])
                    if self.text['result'][i]['submit_name'] != None:
                        print(mycolors.foreground.orange, "FileName   => " + self.text['result'][i]['submit_name'])
                    if self.text['result'][i]['type_short'] != None:
                        print(mycolors.foreground.orange, "FileType   => " + self.text['result'][i]['type_short'] + "\n")
            except KeyError as e:
                pass     
            
        
            
            
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to HybridAnalysis!\n"))
            print(mycolors.reset)
        except KeyError:
            print(mycolors.foreground.lightred + "\nNo results found for HYBRIDANALYSIS")    
            print(mycolors.reset)
       
            
    
    def otxDomaincheck(self):
        try:
            print(mycolors.foreground.lightblue + mycolors.background.cyan)
            print("\nOTXQuery SUMMARY")
            print("-"*20,'n') 
            print(mycolors.reset)            
            
            # Get General Info
            if (bool(self.text['pulses'])):
                try:
                    print("-"*40)
                    num = 0
                    for i in range(0, len(self.text['pulses'])):
                        if (self.text['pulses'][i].get('name')):
                            num +=1
                            print("".ljust(28), end=' ')
                            print(f"Data {mycolors.foreground.orange}{num}")
                            print("".ljust(28), end=' ')                            
                            print(("Name: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['name'],mycolors.reset)))
                        if (self.text['pulses'][i].get('tags')):
                            print("".ljust(28), end=' ')
                            print((mycolors.foreground.orange + "Tags: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['tags'],mycolors.reset)))
                        if (self.text['pulses'][i].get('targeted_countries')):
                            print("".ljust(28), end=' ')
                            print((mycolors.foreground.orange + "Targeted Countries: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['targeted_countries'],mycolors.reset)))                                
                        if (self.text['pulses'][i].get('references')):
                            print("".ljust(28), end=' ')
                            print(mycolors.foreground.orange + "References: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['references'],mycolors.reset), end=' ')
                        print("\n")
                except KeyError as e:
                    pass     
                
                
                print("-"*20)
                # Get OTX domain detected malware samples
                print(mycolors.foreground.lightred + "\nDetected malware samples: ".ljust(17))                
                if 'malware_samples' in self.text:
                    if (bool(self.text['malware_samples'])):
                        try:
                            for i in range(0, len(self.text['malware_samples'])):
                                if (self.text['malware_samples'][i]):
                                    print("".ljust(28), end=' ')
                                    print(self.text['malware_samples'][i])                    
                        except KeyError as e:
                            pass     
                    else:
                        print("".ljust(28), end=' ')
                        print(mycolors.reset,"NONE")
                
                
                print("-"*20)
                # Get OTX domain detected URLs
                print(mycolors.foreground.lightcyan + "\nDetected URLs: ".ljust(17))  
                if 'url_list' in self.text:
                    if (bool(self.text['url_list'])):
                        try:
                            for i in range(0, len(self.text['url_list'])):
                                if (self.text['url_list'][i]).get('url'):
                                    print("".ljust(28), end=' ')
                                    print(self.text['url_list'][i]['url'])                    
                        except KeyError as e:
                            pass    
                    else:
                        print("".ljust(28), end=' ')
                        print(mycolors.reset,"NONE")
                
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to OTX_Query!\n"))
            print(mycolors.reset)
        except (KeyError,TypeError):
            print(mycolors.foreground.lightred + "\nNo results found for OTX_Query")    
            print(mycolors.reset)
              
        

class IPs():
    def __init__(self, text, value):
        self.text = text
        self.value = value
        
    def abIPdbcheck(self):
        try:
            print(mycolors.foreground.lightgreen,mycolors.background.lightgrey)
            print("\nABUSEIPDB SUMMARY")
            print("-"*25,"\n") 
            print(mycolors.reset) 
            
            print(mycolors.foreground.lightcyan)    
            if  self.text['isp'] != None:
                print("".ljust(28), end=' ')            
                print("ISP: {}".format((self.text['isp'])))
            if self.text['domain'] != None:
                print("".ljust(28), end=' ')                        
                print("Domain: =>\t{}".format((self.text['domain'])))
            if self.text['usageType'] != None:
                print("".ljust(28), end=' ')                        
                print("IP usage_type: =>\t{}".format((self.text['usageType'])))
            if self.text['countryName'] != None:
                print("".ljust(28), end=' ')                        
                print("Country Name: =>\t{}".format((self.text['countryName'])))        
        
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to AbuseIPDB!\n"))
            print(mycolors.reset)
        except KeyError:
            print(mycolors.foreground.lightred + "\nNo results found for AbuseIPDB")    
            print(mycolors.reset)        
    
    def gnoiseIPcheck(self):
        try:
            print(mycolors.foreground.lightblue,mycolors.background.lightgrey)
            print("\nGREY_NOISE SUMMARY")
            print("-"*25,"\n")   
            print(mycolors.reset)
            
            print(mycolors.foreground.orange + "\nResults found: {}".format((self.text['returned_count'])))
            print("-"*28)
            print(mycolors.reset)        
            print(mycolors.foreground.lightgrey)            
            for i in range(len(self.text['records'])):
                if self.text['records'][i]['name'] != None:
                    print("\nRecord:\t=>\t{}".format((self.text['records'][i]['name'])))
                if self.text['records'][i]['metadata'] != None:
                    print("".ljust(20), end=' ')                                            
                    print("Tor:\t=>\t{}".format((self.text['records'][i]['metadata']['tor'])))                
                if self.text['records'][i]['confidence'] != None:
                    print("".ljust(20), end=' ')                                            
                    print("Confidence:\t=>\t{}".format((self.text['records'][i]['confidence'])))     
                if self.text['records'][i]['last_updated'] != None:
                    print("".ljust(20), end=' ')                                            
                    print("Last_updated:\t=>\t{}".format((self.text['records'][i]['last_updated'])))                 
        
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to GreyNoise!\n"))
            print(mycolors.reset)
        except KeyError:
            print(mycolors.foreground.lightred + "\nNo results found for GreyNoise")    
            print(mycolors.reset)                    
        
    
    
    def censysIPcheck(self):
        try:
            print(mycolors.reset)
            print("".ljust(20), end=' ')                        
            print("\n\nIP ADDRESS SUMMARY REPORT")
            print("-"*25,"\n\n",mycolors.reset)
            
            print(mycolors.foreground.lightred,mycolors.background.lightgrey)
            print("\nCENSYS_IP SUMMARY")
            print("-"*25,"\n") 
            print(mycolors.reset)        
            
    
            for i in self.text['protocols']:
                print(mycolors.foreground.yellow)
                print("Services running: ")            
                print("".ljust(28), end=' ')
                print(i)
                
            print("\nLast updated: {}".format((self.text['updated_at'])))
            print("-"*40,"\n") 
            
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to Cencys!\n"))
            print(mycolors.reset)
        except KeyError:
            print(mycolors.foreground.lightred + "\nNo results found for Cencys")    
            print(mycolors.reset)            
        
    
    def vtIPcheck(self):
        try:
            print(mycolors.reset)
            print("".ljust(20), end=' ')                        
            print("\n\nIP ADDRESS SUMMARY REPORT")
            print("-"*25,"\n\n",mycolors.reset)     
            
            

    
            if 'resolutions' in self.text:
                print(mycolors.foreground.yellow + "\nResolutions")
                print("-" * 11)
                print(mycolors.reset)                
                num = 0
                if (self.text['resolutions']):
                    for i in self.text['resolutions']:
                        if num >= 6:
                            print(mycolors.foreground.lightgreen + "\n......" + mycolors.reset)
                            print(mycolors.foreground.green + f"\nToo many resolutions... Check the website at https://www.virustotal.com/gui/ip-address/{self.value}/relations *** " + mycolors.reset)
                            break                    
                        else:
                            print(mycolors.foreground.lightgreen + "\nLast Resolved:\t" + i['last_resolved'] + mycolors.reset)
                            print(mycolors.foreground.lightgreen + "Hostname:\t" + i['hostname'] + mycolors.reset)
                            num +=1
  
    

    
            if 'detected_urls' in self.text:
                print(mycolors.reset + "\nDetected URLs")
                print("-" * 13)                
                num = 0
                for j in self.text['detected_urls']:
                    if num >= 6:
                        print(mycolors.foreground.lightred + "\n......" + mycolors.reset)
                        print(mycolors.foreground.green + f"\n *** Too many Detected URLs... Check the website at https://www.virustotal.com/gui/ip-address/{self.value}/relations *** " + mycolors.reset)
                        break                
                    else:
                        print(mycolors.foreground.lightred + "\nURL:\t\t{}".format(j['url']) + mycolors.reset)
                        print(mycolors.foreground.lightred + "Scan date:\t{}".format(j['scan_date']), mycolors.reset)
                        print(mycolors.foreground.lightred + "Positives:\t{}".format(j['positives']), mycolors.reset)
                        print(mycolors.foreground.lightred + "Total:\t\t{}".format(j['total'] ), mycolors.reset)
                        num +=1
    

    
            if 'detected_downloaded_samples' in self.text:
                print(mycolors.reset + "\nDetected Downloaded Samples")
                print("-" * 27)                
                num = 0
                for k in self.text['detected_downloaded_samples']:
                    if num >= 6:
                        print(mycolors.foreground.yellow + "\n......" + mycolors.reset)
                        print(mycolors.foreground.green + f"\n *** Too many Detected Downloaded Samples... Check the website at https://www.virustotal.com/gui/ip-address/{self.value}/relations *** " + mycolors.reset)
                        break                
                    else:
                        print(mycolors.foreground.yellow + "\nSHA256:\t\t{}".format( k['sha256']) + mycolors.reset)
                        print(mycolors.foreground.yellow + "Date:\t\t{}".format( k['date']) + mycolors.reset)
                        print(mycolors.foreground.yellow + "Positives:\t%d".format( k['positives']) + mycolors.reset)
                        print(mycolors.foreground.yellow + "Total:\t\t%d".format( k['total']) + mycolors.reset)
                        num += 1
    
    
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to VirusTotal!\n"))
            print(mycolors.reset)
        except KeyError:
            print(mycolors.foreground.lightred + "\nNo results found for VirusTotal")    
            print(mycolors.reset) 

    
    def haIPcheck(self):
        try:
            print(mycolors.foreground.lightred,mycolors.background.lightgrey)
            print("\nHYBRIDANALYSIS SUMMARY")
            print("-"*25,"\n") 
            print(mycolors.reset)     
            
            print(mycolors.foreground.orange + "\nResults found: {}".format(self.text["count"]))
            print("-"*28)
            print(mycolors.reset)
            try:
                for i in range(len(self.text['result'])): 
                    if self.text['result'][i]['verdict'] != None:
                        print(mycolors.foreground.orange, "Verdict    => " + self.text['result'][i]['verdict'])
                    
                    print(mycolors.foreground.orange, "SHA256     => " + self.text['result'][i]['sha256'])
                    if self.text['result'][i]['av_detect'] != None:
                        print(mycolors.foreground.orange, "AV Detect  => " + self.text['result'][i]['av_detect'])
                    if self.text['result'][i]['vx_family'] != None:
                        print(mycolors.foreground.orange, "Mal Family => " + self.text['result'][i]['vx_family'])
                    print(mycolors.foreground.orange, "FileName   => " + self.text['result'][i]['submit_name'])
                    if self.text['result'][i]['type_short'] != None:
                        print(mycolors.foreground.orange, "FileType   => " + self.text['result'][i]['type_short'] + "\n")
            except KeyError as e:
                pass     
            
        
            
            
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to HybridAnalysis!\n"))
            print(mycolors.reset)
        except KeyError:
            print(mycolors.foreground.lightred + "\nNo results found for HYBRIDANALYSIS")    
            print(mycolors.reset)  
            
    
    def otxIPcheck(self):
        try:
            print(mycolors.foreground.lightblue + mycolors.background.lightgrey)
            print("\nOTXQuery SUMMARY")
            print("-"*25,"\n") 
            print(mycolors.reset)            
            print(mycolors.foreground.lightcyan + "General Info: ".ljust(17))
            
            # Get General Info
            if (bool(self.text['pulses'])):
                try:
                    print("-"*40)
                    num = 0
                    for i in range(0, len(self.text['pulses'])):
                        if (self.text['pulses'][i].get('name')):
                            num +=1
                            print("".ljust(28), end=' ')
                            print(f"Data {mycolors.foreground.orange}{num}")
                            print("".ljust(28), end=' ')                            
                            print(("Name: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['name'],mycolors.reset)))
                        if (self.text['pulses'][i].get('tags')):
                            print("".ljust(28), end=' ')
                            print((mycolors.foreground.orange + "Tags: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['tags'],mycolors.reset)))
                        if (self.text['pulses'][i].get('targeted_countries')):
                            print("".ljust(28), end=' ')
                            print((mycolors.foreground.orange + "Targeted Countries: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['targeted_countries'],mycolors.reset)))                                
                        if (self.text['pulses'][i].get('references')):
                            print("".ljust(28), end=' ')
                            print(mycolors.foreground.orange + "References: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['references'],mycolors.reset), end=' ')
                        print("\n")
                except KeyError as e:
                    pass     
                
                
                print("-"*20)
                # Get OTX IP detected malware samples
                print(mycolors.foreground.lightred + "\nDetected malware samples: ".ljust(17))                
                if 'malware_samples' in self.text:
                    if (bool(self.text['malware_samples'])):
                        try:
                            for i in range(0, len(self.text['malware_samples'])):
                                if (self.text['malware_samples'][i]):
                                    print("".ljust(28), end=' ')
                                    print(("{}".format( self.text['malware_samples'][i])))                    
                        except KeyError as e:
                            pass     
                    else:
                        print("".ljust(28), end=' ')
                        print(mycolors.reset,"NONE")
                
                
                print("-"*20)
                # Get OTX IP detected URLs
                print(mycolors.foreground.lightcyan + "\nDetected URLs: ".ljust(17))  
                if 'url_list' in self.text:
                    if (bool(self.text['url_list'])):
                        try:
                            for i in range(0, len(self.text['url_list'])):
                                if (self.text['url_list'][i]).get('url'):
                                    print("".ljust(28), end=' ')
                                    print(("{}".format( self.text['url_list'][i]['url'])))                    
                        except KeyError as e:
                            pass    
                    else:
                        print("".ljust(28), end=' ')
                        print(mycolors.reset,"NONE")
                
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to OTX_Query!\n"))
            print(mycolors.reset)
        except KeyError:
            print(mycolors.foreground.lightred + "\nNo results found for OTX_Query")    
            print(mycolors.reset)
    
class Hashes():
    def __init__(self, text, value):
        self.text = text
        self.value = value
        
    def vthash(self): 
        try:
            self.text = self.text["data"]
            timestamp = self.text['attributes']['first_submission_date']
            dt_object = datetime.fromtimestamp(timestamp)        

            print(mycolors.foreground.yellow + "\nScan date: ".ljust(13), dt_object)
            print(mycolors.reset)
                
                
            print(mycolors.foreground.lightblue + mycolors.background.lightgrey)            
            #print(mycolors.foreground.lightblue)
            print("\nVIRUSTOTAL SUMMARY")
            print("="*20,'n') 
            print(mycolors.reset)
    
            if self.text['attributes']['tags']:
                print("Tags:")
                try:
                    for i in range(len(self.text['attributes']['tags'])):
                        print("".ljust(28), end=' ') 
                        print(mycolors.foreground.orange, self.text['attributes']['tags'][i],mycolors.reset)
                except KeyError as e:
                    pass
    
            if self.text['attributes']['names']:
                print("-"*40)                            
                print("Name(s) of file:")                
                try:
                    for i in range(len(self.text['attributes']['names'])):
                        print("".ljust(28), end=' ') 
                        print(mycolors.foreground.orange, self.text['attributes']['names'][i],mycolors.reset)
                except KeyError as e:
                    pass
                
                        
            print("-"*40)  
            print("\n\n\n")
            print(f"Detection {mycolors.foreground.lightred}{self.text['attributes']['last_analysis_stats']['malicious']}{mycolors.reset}/{mycolors.foreground.lightgreen}60")
            print(mycolors.reset)
            
            if self.text['attributes']['last_analysis_results']:
                for x,y in self.text['attributes']['last_analysis_results'].items():
                    if y['result'] != None:
                        print(f"{mycolors.foreground.lightgreen}{x}:".ljust(20),"=>".ljust(10),f"{mycolors.foreground.lightred}{y['result']}{mycolors.reset}")
            
            print("-"*40)
            print("\n\n")                        
            print(mycolors.foreground.orange + "\nContacted URLs and Domains")
            print("-"*26)
            print(mycolors.reset)
            print(mycolors.foreground.red + "\nContacted URLs " + f"{self.text['relationships']['contacted_urls']['meta']['count']}")
            if self.text['relationships']['contacted_urls']['data']:
                try:
                    for i in range(len(self.text['relationships']['contacted_urls']['data'])):
                        print("".ljust(28), end=' ') 
                        print(mycolors.foreground.orange, self.text['relationships']['contacted_urls']['data'][i]['context_attributes']['url'],mycolors.reset)
                except KeyError as e:
                    pass   
            else:
                print("".ljust(28), end=' ')
                print(mycolors.reset,"NONE")
            
            
            print("-"*40)
            print(mycolors.foreground.red + "\nContacted Domains" + f" {self.text['relationships']['contacted_domains']['meta']['count']}")
            if self.text['relationships']['contacted_domains']['data']:
                try:
                    for i in range(len(self.text['relationships']['contacted_domains']['data'])):
                        print("".ljust(28), end=' ') 
                        print(mycolors.foreground.orange, self.text['relationships']['contacted_domains']['data'][i]['id'])
                except KeyError as e:
                    pass
            else:
                print("".ljust(28), end=' ')
                print(mycolors.reset,"NONE")
                    
                    
        except ValueError:
            print(mycolors.foreground.lightred + "Error while connecting to VirusTotal!\n")
            print(mycolors.reset)
        except (KeyError,TypeError):
            print(mycolors.foreground.lightred + "No results found in VirusTotal!\n")
            print(mycolors.reset) 
            pass
            
        
    def hahash(self):
        print(mycolors.foreground.lightred + mycolors.background.lightgrey)
        print("\n\nHYBRIDANALYSIS SUMMARY")
        print("="*24,'n') 
        print(mycolors.reset)            
        try:
            x = 0
            for i in range(len(self.text)): 
                x +=1
                print("".ljust(28), end=' ') 
                print(f"{mycolors.foreground.lightred}Detection {x}")
                print("".ljust(28), end=' ') 
                print("-"*20,mycolors.reset) 
                
                print("FileName   => " + mycolors.foreground.orange +self.text[i]['submit_name'] + mycolors.reset)
                
                if self.text[i]['verdict'] != None:
                    print("Verdict    => " + mycolors.foreground.orange + self.text[i]['verdict'] + mycolors.reset)
                
                if self.text[i]['submissions'] != None:
                    print("Number of submissions    => ", mycolors.foreground.orange, len(self.text[i]['submissions']), mycolors.reset)
                    
                if self.text[i]['type_short'] != None:
                    print("FileType   => " + mycolors.foreground.orange + f"{self.text[i]['type_short']}" + mycolors.reset)  
                
                if self.text[i]['av_detect'] != None:
                    print("AV Detect  => "+ mycolors.foreground.orange, self.text[i]['av_detect'], mycolors.reset)
                    
                if self.text[i]['vx_family'] != None:
                    print("Mal Family => " + mycolors.foreground.orange + self.text[i]['vx_family'] + mycolors.reset)
                
                if self.text[i]['environment_description'] != None:
                    print("Analysis environment => " + mycolors.foreground.orange + self.text[i]['environment_description'] + "\n")
                    
    
        except (KeyError,TypeError):
            print(mycolors.foreground.lightred + "No results found in HybridAnalysis!\n")
            print(mycolors.reset) 
            pass         
        
    def otxhash(self):
        try:
            print(mycolors.foreground.lightblue + mycolors.background.lightgrey)
            print("\nOTXQuery SUMMARY")
            print("-"*20,'n') 
            print(mycolors.reset)            
            print(mycolors.foreground.lightcyan + "General Info: ".ljust(17),mycolors.reset)
            
            # Get General Info
            if (bool(self.text['pulses'])):
                try:
                    print("-"*40)
                    num = 0
                    for i in range(0, len(self.text['pulses'])):
                        if (self.text['pulses'][i].get('name')):
                            num +=1
                            print("".ljust(28), end=' ')
                            print(f"Data {mycolors.foreground.orange}{num}")
                            print("".ljust(28), end=' ')                            
                            print(("Name: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['name'],mycolors.reset)))
                        if (self.text['pulses'][i].get('tags')):
                            print("".ljust(28), end=' ')
                            print((mycolors.foreground.orange + "Tags: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['tags'],mycolors.reset)))
                        if (self.text['pulses'][i].get('targeted_countries')):
                            print("".ljust(28), end=' ')
                            print((mycolors.foreground.orange + "Targeted Countries: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['targeted_countries'],mycolors.reset)))                                
                        if (self.text['pulses'][i].get('references')):
                            print("".ljust(28), end=' ')
                            print(mycolors.foreground.orange + "References: {0}{1}{2}".format(mycolors.foreground.lightred,self.text['pulses'][i]['references'],mycolors.reset), end=' ')
                        print("\n")
                except KeyError as e:
                    pass             
            
            #Get yara rule_name(s)
            if self.text['analysis']['plugins']['yarad']['results']['detection']:
                try:
                    print("Yara rule_name(s) Triggered:")
                    for i in range(len(self.text['analysis']['plugins'])):
                        print("".ljust(28), end=' ') 
                        print(mycolors.foreground.orange, self.text['analysis']['plugins']['yarad']['results']['detection'][i]['rule_name'],mycolors.reset)
                except IndexError:
                    pass
                
            
            
            print("-"*40)
            print("\nDetections:\n")
            for x,y in self.text['analysis']['plugins'].items():
                if 'clamav' in x:
                    print(f"{mycolors.foreground.lightgreen}{x}:".ljust(20),"=>".ljust(10),f"{mycolors.foreground.lightred}{y['results'].get('detection')}{mycolors.reset}")
                elif 'msdefender' in x:
                    print(f"{mycolors.foreground.lightgreen}{x}:".ljust(20),"=>".ljust(10),f"{mycolors.foreground.lightred}{y['results'].get('detection')}{mycolors.reset}")

                     
            for x,y in self.text['analysis']['plugins'].items():    
                if 'strings' in x:
                    res = input("\nWould you like to see the strings? (y | n): ")
                    with open("strings.txt",'w+') as f:
                        if res.lower() == "y":
                            print(f"{mycolors.foreground.lightgreen}{x}:".ljust(20),"\n")
                            for i in range(0, len(y['results'])): 
                                print(f"{mycolors.foreground.lightgreen}=> "f"{mycolors.foreground.lightred}{y['results'][i]}{mycolors.reset}")
                                f.write(f"{y['results'][i]}\n")
                            print(mycolors.foreground.lightgreen + "\nStrings have been written under {}\\strings.txt".format((os.getcwd())))
                        else:
                            pass
            
                
                
            print("-"*40)
            # Get OTX domain detected malware samples
            print(mycolors.foreground.lightred + "\nDetected malware samples: ".ljust(17))                
            if 'malware_samples' in self.text:
                if (bool(self.text['malware_samples'])):
                    try:
                        for i in range(0, len(self.text['malware_samples'])):
                            if (self.text['malware_samples'][i]):
                                print("".ljust(28), end=' ')
                                print((f"{self.text['malware_samples'][i]}"))                    
                    except KeyError as e:
                        pass   
                else:
                    print("".ljust(28), end=' ')
                    print(mycolors.reset,"NONE")
            
            
            print("-"*20)
            # Get OTX domain detected URLs
            print(mycolors.foreground.lightcyan + "\nDetected URLs: ".ljust(17))  
            if 'url_list' in self.text:
                if (bool(self.text['url_list'])):
                    try:
                        for i in range(0, len(self.text['url_list'])):
                            if (self.text['url_list'][i]).get('url'):
                                print("".ljust(28), end=' ')
                                print(f"{self.text['url_list'][i]['url']}")                    
                    except KeyError as e:
                        pass  
                else:
                    print("".ljust(28), end=' ')
                    print(mycolors.reset,"NONE")
            
        except ValueError:
            print((mycolors.foreground.red + "Error while connecting to OTX_Query!\n"))
            print(mycolors.reset)
        except (KeyError,TypeError):
            print(mycolors.foreground.lightred + "\nNo results found for OTX_Query")    
            print(mycolors.reset) 
       