import os
from datetime import datetime

import geocoder
from rich.console import Console

console = Console()
print = console.print


class MyColors:
    reset = "\033[0m"
    reverse = "\033[07m"
    bold = "\033[01m"

    class Foreground:
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        lightgreen = "\033[92m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"
        red = "\033[31m"
        green = "\033[32m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        yellow = "\033[93m"

    # noinspection SpellCheckingInspection
    class Background:
        black = "\033[40m"
        blue = "\033[44m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"
        purple = "\033[45m"
        green = "\033[42m"
        orange = "\033[43m"
        red = "\033[41m"


class Checkers:
    def __init__(self, results, value):
        self.results = results
        self.value = value

    @property
    def func_map(self):
        return {
            "domain": self.check_domain,
            "hash": self.check_hash,
            "url": self.check_url,
            "ip": self.check_ip,
        }

    def check_url(self):
        for result in self.results:
            if "name" in result:
                if "VirusTotal_v2_Get_Observable" in result["name"]:
                    urls = Urls(result["report"], self.value)
                    urls.vturl_check()
                elif "VirusTotal_v3" in result["name"]:
                    print("-" * 120)
                    print(
                        "[*] Try using VirusTotal_v2 for URLs"
                        "instead of VirusTotal_v3!"
                    )
                elif "HybridAnalysis" in result["name"]:
                    urls = Hybrid(result["report"], self.value)
                    urls.ha_check()
                elif "OTXQuery" in result["name"]:
                    urls = Hybrid(result["report"], self.value)
                    urls.otx_check()
                elif "URLhaus" in result["name"]:
                    urls = Urls(result["report"], self.value)
                    urls.hausurl_check()

    def check_domain(self):
        for result in self.results:
            if "name" in result:
                if "VirusTotal_v2" in result["name"]:
                    domains = Hybrid(result["report"], self.value)
                    domains.vt_check()
                elif "VirusTotal_v3" in result["name"]:
                    print("-" * 120)
                    print(
                        "[*] Try using VirusTotal_v2 for domains"
                        "instead of VirusTotal_v3!"
                    )
                elif "HybridAnalysis" in result["name"]:
                    domains = Hybrid(result["report"], self.value)
                    domains.ha_check()
                elif "OTXQuery" in result["name"]:
                    domains = Hybrid(result["report"], self.value)
                    domains.otx_check()
                elif "Hunter" in result["name"]:
                    domains = Domains(result["report"], self.value)
                    domains.hunter_domain()

    def check_hash(self):
        for result in self.results:
            if "HybridAnalysis_Get_Observable" in result["name"]:
                hashes = Hashes(result["report"], self.value)
                hashes.hahash()
            elif "VirusTotal_v3_Get_Observable" in result["name"]:
                hashes = Hashes(result["report"], self.value)
                hashes.vthash()
            elif "VirusTotal_v2_Get_Observable" in result["name"]:
                print("-" * 120)
                print(
                    "[*] Try using VirusTotal_v3 for hashes" "instead of VirusTotal_v2!"
                )
            elif "OTXQuery" in result["name"]:
                hashes = Hashes(result["report"], self.value)
                hashes.otxhash()

    def check_ip(self):
        for result in self.results:
            if "HybridAnalysis_Get_Observable" in result["name"]:
                ips = Hybrid(result["report"], self.value)
                ips.ha_check()
            elif "VirusTotal_v2_Get_Observable" in result["name"]:
                ips = Hybrid(result["report"], self.value)
                ips.vt_check()
            elif "VirusTotal_v3_Get_Observable" in result["name"]:
                print("-" * 120)
                print("[*] Try using VirusTotal_v2 for IPs" "instead of VirusTotal_v3!")
            elif "OTXQuery" in result["name"]:
                ips = Hybrid(result["report"], self.value)
                ips.otx_check()
            elif "AbuseIPDB" in result["name"]:
                ips = IPs(result["report"], self.value)
                ips.abipdbcheck()
            elif "Censys_Search" in result["name"]:
                ips = IPs(result["report"], self.value)
                ips.censysipcheck()
            elif "GreyNoiseAlpha" in result["name"]:
                ips = IPs(result["report"], self.value)
                ips.gnoiseipcheck()


class Domains:
    def __init__(self, text, value):
        self.text = text
        self.value = value

    def _hunter_email_info(self):

        # Show emails and Social Media accounts
        if self.text["meta"]["results"] > 0:
            emails = self.text["data"]["emails"]
            x = 0
            for email in emails:
                x += 1
                print(MyColors.Foreground.red, f"Email {x}")
                print("-" * 8)
                for key, value in email.items():
                    if "sources" in key:
                        print(MyColors.Foreground.orange, "Collection Source(s): ")
                        for source in value:
                            print(
                                MyColors.reset,
                                "\t\t=========>".ljust(20),
                                MyColors.Foreground.orange,
                                end=" ",
                            )
                            print(
                                "URi: "
                                + MyColors.Foreground.lightgreen
                                + source["uri"]
                                + MyColors.Foreground.orange
                                + " , Last Seen Date: "
                                + MyColors.Foreground.lightgreen
                                + source["last_seen_on"],
                                MyColors.reset,
                            )
                    elif value is not None:
                        print(
                            MyColors.Foreground.orange,
                            "{0}:\t{1}{2}".format(
                                key, MyColors.Foreground.lightgreen, value
                            ),
                            MyColors.reset,
                        )
                print("\n")
        else:
            print(MyColors.Foreground.lightred + "\nNo results found for Hunter")

    def hunter_domain(self):
        try:
            print(MyColors.Foreground.red + MyColors.Background.lightgrey)
            print("\nEmail HUNTER SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            self._hunter_email_info()

        except ValueError:
            print((MyColors.Foreground.red + "Error while connecting to Hunter!\n"))
        except (KeyError, TypeError):
            print(MyColors.Foreground.lightred + "\nNo results found for Hunter")


class Hybrid:
    def __init__(self, text, value):
        self.text = text
        self.value = value

    def _vt_detected_samples(self, lst, colour):
        num = 0
        for j in lst:
            if len(lst) < 6:
                if "date" in j:
                    print("\t\t====>".ljust(28), end=" ")
                    print(
                        "Scan date:\t{}".format(j["date"]),
                    )
                print("\t\t====>".ljust(28), end=" ")
                print(
                    "Detection:\t{0}{1}/{2}{3}{4}".format(
                        MyColors.Foreground.lightred,
                        j["positives"],
                        MyColors.reset,
                        MyColors.Foreground.lightgreen,
                        j["total"],
                    ),
                    colour,
                )
                print("\t\t====>".ljust(28), end=" ")
                print("SHA256:\t{}\n".format(j["sha256"]))
            else:
                while num <= 6:
                    if "date" in j:
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            "Scan date:\t{}".format(j["date"]),
                        )
                    print("\t\t====>".ljust(28), end=" ")
                    print(
                        "Detection:\t{0}{1}/{2}{3}{4}".format(
                            MyColors.Foreground.lightred,
                            j["positives"],
                            MyColors.reset,
                            MyColors.Foreground.lightgreen,
                            j["total"],
                        ),
                        colour,
                    )
                    print("\t\t====>".ljust(28), end=" ")
                    print("SHA256:\t{}".format(j["sha256"]))
                    print(colour)
                    num += 1

                    if num > 6:
                        url = (
                            f"https://www.virustotal.com/gui/domain/"
                            f"{self.value}/relations"
                        )
                        print(MyColors.Foreground.lightred + "\n......", MyColors.reset)
                        print(
                            f"\n*** Too many Detected samples... "
                            f"Check in browser: {url}"
                        )
                        print(MyColors.reset)
                        break

    def _vt_detected_urls(self, lst, colour):
        num = 0
        for j in lst:
            if len(lst) < 6:
                print("\t\t====>".ljust(28), end=" ")
                print("URL:\t{}".format(j["url"]))
                print("\t\t====>".ljust(28), end=" ")
                print(
                    "Scan date:\t{}".format(j["scan_date"]),
                )
                print("\t\t====>".ljust(28), end=" ")
                print(
                    "Detection:\t{0}{1}/{2}{3}{4}\n".format(
                        MyColors.Foreground.lightred,
                        j["positives"],
                        MyColors.reset,
                        MyColors.Foreground.lightgreen,
                        j["total"],
                    ),
                    colour,
                )
            else:
                while num <= 6:
                    print("\t\t====>".ljust(28), end=" ")
                    print("URL:\t{}".format(j["url"]))
                    print("\t\t====>".ljust(28), end=" ")
                    print(
                        "Scan date:\t{}".format(j["scan_date"]),
                    )
                    print("\t\t====>".ljust(28), end=" ")
                    print(
                        "Detection:\t{0}{1}/{2}{3}{4}\n".format(
                            MyColors.Foreground.lightred,
                            j["positives"],
                            MyColors.reset,
                            MyColors.Foreground.lightgreen,
                            j["total"],
                        ),
                        colour,
                    )
                    print(colour)
                    num += 1

                    if num > 6:
                        url = (
                            f"https://www.virustotal.com/gui/domain/"
                            f"{self.value}/relations"
                        )
                        print(MyColors.Foreground.lightred + "\n......", MyColors.reset)
                        print(
                            f"\n*** Too many Detected samples... "
                            f"Check in browser: {url}"
                        )
                        print(MyColors.reset)
                        break

    def _vt_get_undetected_referrer_samples(self):
        if "undetected_referrer_samples" in self.text:
            undetected_samples = self.text["undetected_referrer_samples"]
            if undetected_samples:
                print("-" * 120)
                print(MyColors.Foreground.lightcyan + "\nUndetected Referrer Samples:")
                print("_" * 33 + "\n")
                try:
                    Hybrid._vt_detected_samples(
                        self, undetected_samples, MyColors.Foreground.lightcyan
                    )
                except KeyError:
                    pass

    def _vt_get_detected_referrer_samples(self):
        if "detected_referrer_samples" in self.text:
            ref_samples = self.text["detected_referrer_samples"]
            if ref_samples:
                print("-" * 120)
                try:
                    print(MyColors.Foreground.pink + "\nDetected Referrer Samples:")
                    print("_" * 33 + "\n")
                    Hybrid._vt_detected_samples(
                        self, ref_samples, MyColors.Foreground.pink
                    )
                except KeyError:
                    pass

    def _vt_get_undetected_downloaded_samples(self):
        if "undetected_downloaded_samples" in self.text:
            undetected_samples = self.text["undetected_downloaded_samples"]
            if undetected_samples:
                print("-" * 120)
                print(MyColors.Foreground.lightgreen + "\nUndetected Download Samples:")
                print("_" * 33 + "\n")
                try:
                    Hybrid._vt_detected_samples(
                        self, undetected_samples, MyColors.Foreground.lightgreen
                    )
                except KeyError:
                    pass

    def _vt_get_detected_samples(self):

        if "detected_downloaded_samples" in self.text:
            download_samples = self.text["detected_downloaded_samples"]
            if download_samples:
                print("-" * 120)
                print(MyColors.Foreground.orange + "\nDetected Downloaded Samples:")
                print("_" * 33 + "\n")
                try:
                    Hybrid._vt_detected_samples(
                        self, download_samples, MyColors.Foreground.orange
                    )
                except KeyError:
                    pass

        if "detected_communicating_samples" in self.text:
            print("-" * 120)
            print(MyColors.Foreground.lightcyan + "\nDetected Communicating Samples:")
            print("_" * 33 + "\n")
            samples = self.text["detected_communicating_samples"]
            try:
                Hybrid._vt_detected_samples(
                    self, samples, MyColors.Foreground.lightcyan
                )
            except KeyError:
                pass

    def _vt_get_urls(self):
        if "detected_urls" in self.text:
            urls = self.text["detected_urls"]
            if urls:
                print("-" * 120)
                print(MyColors.Foreground.yellow + "\nDetected URLs:")
                print("_" * 19 + "\n")
                try:
                    Hybrid._vt_detected_urls(self, urls, MyColors.Foreground.yellow)
                except KeyError:
                    pass

    def _vt_get_timestamp(self):
        print(MyColors.Foreground.yellow + "\nWhois Timestamp:")
        print("_" * 22 + "\n")
        if "whois_timestamp" in self.text:
            try:
                print("\t\t====>".ljust(28), end=" ")
                ts = self.text["whois_timestamp"]
                print((datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:{}")))
            except KeyError:
                pass

    def _vt_get_resolutions(self):
        if self.text["resolutions"]:
            print("-" * 120)
            print(MyColors.Foreground.lightred + "Last Resolved:")
            print("_" * 15 + "\n")
            num = 0
            try:
                for resolve in self.text["resolutions"]:
                    if "ip_address" in resolve:
                        print("".ljust(28), end=" ")
                        print("IP address:   {}".format(resolve["ip_address"]))
                        print("".ljust(28), end=" ")
                        print("Date: {}\n".format(resolve["last_resolved"]))
                        print("".ljust(28), end=" ")
                        print(f"(City:{geocoder.ip(resolve['ip_address']).city})")
                        num += 1
                        if num > 6:
                            url = (
                                f"https://www.virustotal.com/gui/ip/"
                                f"{self.value}/details"
                            )
                            print(
                                MyColors.Foreground.lightred + "\n......",
                                MyColors.reset,
                            )
                            print(
                                f"\n*** Too many Detected samples... "
                                f"Check in browser: {url}"
                            )
                            print(MyColors.reset)
                            break

                    elif resolve["hostname"]:
                        print("\t\t====>".ljust(28), end=" ")
                        print("Hostname:   {}".format(resolve["hostname"]))
                        print("\t\t====>".ljust(28), end=" ")
                        print("Date: {}\n".format(resolve["last_resolved"]))
                        num += 1
                        if num > 6:
                            url = (
                                f"https://www.virustotal.com/gui/ip-address/"
                                f"{self.value}/relations"
                            )
                            print(
                                MyColors.Foreground.lightred + "\n......",
                                MyColors.reset,
                            )
                            print(
                                f"\n*** Too many Detected samples... "
                                f"Check in browser: {url}"
                            )
                            print(MyColors.reset)
                            break
                print("\n")
            except KeyError:
                pass

    def _vt_get_subdomains(self):
        if "subdomains" in self.text:
            print("-" * 120)
            print(MyColors.Foreground.lightgreen + "\nSubdomains:")
            print("_" * 19 + "\n")
            try:
                for subdomain in self.text["subdomains"]:
                    print("\t\t====>".ljust(28), end=" ")
                    print(subdomain)
            except KeyError:
                pass

    def _vt_get_domain_siblings(self):
        if "domain_siblings" in self.text:
            if self.text["domain_siblings"]:
                print("-" * 120)
                print(MyColors.Foreground.lightcyan + "\nDomain Siblings: ")
                print("_" * 20 + "\n")
                try:
                    for domain_sibling in self.text["domain_siblings"]:
                        print("\t\t====>".ljust(28), end=" ")
                        print(domain_sibling)
                except KeyError:
                    pass

    def _vt_get_categories(self):
        if "categories" in self.text:
            print("-" * 120)
            print(MyColors.Foreground.lightcyan + "\nCategories: ")
            print("_" * 24 + "\n")

            try:
                for category in self.text["categories"]:
                    print("\t\t====>".ljust(28), end=" ")
                    print(category)
            except KeyError:
                pass

    def _ha_get_results(self):
        try:
            if "result" in self.text:
                results = self.text["result"]
                if results:
                    print(
                        MyColors.Foreground.orange
                        + "\nResults found: {}".format(self.text["count"])
                    )
                    print("-" * 28)
                    for result in results:
                        if "verdict" in result:
                            print(
                                MyColors.Foreground.orange,
                                "Verdict\t=> ",
                                MyColors.Foreground.lightred,
                                result["verdict"],
                            )
                        if "av_detect" in result:
                            print(
                                MyColors.Foreground.orange,
                                "AV Detect\t=> ",
                                MyColors.Foreground.lightred,
                                result["av_detect"],
                            )
                        if "vx_family" in result:
                            print(
                                MyColors.Foreground.orange,
                                "Mal Family\t=> ",
                                MyColors.Foreground.lightred,
                                result["vx_family"],
                            )
                        if "submit_name" in result:
                            print(
                                MyColors.Foreground.orange,
                                "FileName\t=> ",
                                MyColors.Foreground.lightred,
                                result["submit_name"],
                            )
                        if "type_short" in result:
                            print(
                                MyColors.Foreground.orange,
                                "FileType\t=> ",
                                MyColors.Foreground.lightred,
                                result["type_short"],
                            )
                        if "sha256" in result:
                            print(
                                MyColors.Foreground.orange,
                                "SHA256\t=> ",
                                MyColors.Foreground.lightred,
                                result["sha256"] + "\n",
                            )
                else:
                    print(
                        MyColors.Foreground.lightred
                        + "\nNo results found for HYBRIDANALYSIS"
                    )

        except KeyError:
            pass

    def _otx_get_general_info(self):
        # Get General Info
        if "pulses" in self.text:
            pulses = self.text["pulses"]
            try:
                print("-" * 120)
                print(
                    MyColors.Foreground.cyan,
                    "\tReports found => {}\n".format(len(pulses)),
                    MyColors.Foreground.lightgreen,
                )
                num = 0
                for pulse in pulses:
                    if pulse.get("name"):
                        num += 1
                        print("\t\t====>".ljust(28), end=" ")
                        print(f"Data {MyColors.Foreground.orange}{num}")
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            (
                                "Name: {0}{1}{2}".format(
                                    MyColors.Foreground.lightred,
                                    pulse["name"],
                                    MyColors.reset,
                                )
                            )
                        )
                    if pulse.get("tags"):
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            (
                                MyColors.Foreground.orange
                                + "Tags: {0}{1}{2}".format(
                                    MyColors.Foreground.lightred,
                                    pulse["tags"],
                                    MyColors.reset,
                                )
                            )
                        )
                    if pulse.get("targeted_countries"):
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            (
                                MyColors.Foreground.orange
                                + "Targeted Countries: {0}{1}{2}".format(
                                    MyColors.Foreground.lightred,
                                    pulse["targeted_countries"],
                                    MyColors.reset,
                                )
                            )
                        )
                    if pulse.get("references"):
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            MyColors.Foreground.orange
                            + "References: {0}{1}{2}".format(
                                MyColors.Foreground.lightred,
                                pulse["references"],
                                MyColors.reset,
                            ),
                            end=" ",
                        )
                    print("\n")
            except KeyError:
                pass

    def _otx_get_detected_samples(self):

        # Get OTX domain detected malware samples
        if "malware_samples" in self.text:
            samples = self.text["malware_samples"]
            if samples:
                print("-" * 120)
                print(
                    MyColors.Foreground.lightred
                    + "\nDetected malware samples: ".ljust(17)
                )
                try:
                    for sample in samples:
                        if sample:
                            print("\t\t====>".ljust(28), end=" ")
                            print(sample)
                except KeyError:
                    pass
        else:
            print("\t\t====>".ljust(28), end=" ")
            print(MyColors.reset, "NONE")

    def _otx_get_detected_urls(self):
        # Get OTX domain detected URLs
        if "url_list" in self.text:
            url_list = self.text["url_list"]
            if url_list:
                print("-" * 120)
                print(MyColors.Foreground.lightcyan + "\nDetected URLs: ".ljust(17))
                try:
                    for url in url_list:
                        if url.get("url"):
                            print("\t\t====>".ljust(28), end=" ")
                            print(url["url"])
                except KeyError:
                    pass
            else:
                print("\t\t====>".ljust(28), end=" ")
                print(MyColors.reset, "NONE")

    def vt_check(self):
        try:
            print(MyColors.reset)
            print(MyColors.Foreground.lightblue, MyColors.Background.lightgrey)
            print("\nVIRUSTOTAL SUMMARY")
            print("=" * 25)
            print(MyColors.reset)

            self._vt_get_timestamp()
            self._vt_get_resolutions()
            self._vt_get_categories()
            self._vt_get_subdomains()
            self._vt_get_domain_siblings()
            self._vt_get_undetected_referrer_samples()
            self._vt_get_detected_referrer_samples()
            self._vt_get_undetected_downloaded_samples()
            self._vt_get_detected_samples()
            self._vt_get_urls()

        except ValueError:
            print(
                (MyColors.Foreground.red + "Error while connecting to Virus Total!\n")
            )
        except (KeyError, TypeError):
            print(MyColors.Foreground.lightred + "No results found in VirusTotal!\n")

    def ha_check(self):
        try:
            print(MyColors.Foreground.lightred, MyColors.Background.lightgrey)
            print("\nHYBRIDANALYSIS SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            self._ha_get_results()

        except ValueError:
            print(
                (
                    MyColors.Foreground.red
                    + "Error while connecting to HybridAnalysis!\n"
                )
            )
        except KeyError:
            print(
                MyColors.Foreground.lightred + "\nNo results found for HybridAnalysis"
            )

    def otx_check(self):
        try:
            print(MyColors.Foreground.lightblue + MyColors.Background.cyan)
            print("\nOTXQuery SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            self._otx_get_general_info()
            self._otx_get_detected_samples()
            self._otx_get_detected_urls()

        except ValueError:
            print((MyColors.Foreground.red + "Error while connecting to OTX_Query!\n"))
        except (KeyError, TypeError):
            print(MyColors.Foreground.lightred + "\nNo results found for OTX_Query")


class IPs:
    def __init__(self, text, value):
        self.text = text
        self.value = value

    def abip_get_info(self):

        print(MyColors.Foreground.lightcyan)
        if "isp" in self.text["data"]:
            print("\t\t====>".ljust(28), end=" ")
            print("ISP: {}".format((self.text["isp"])))
        if "domain" in self.text:
            print("\t\t====>".ljust(28), end=" ")
            print("Domain: =>\t{}".format((self.text["domain"])))
        if "usageType" in self.text:
            print("\t\t====>".ljust(28), end=" ")
            print("IP usage_type: =>\t{}".format((self.text["usageType"])))
        if "countryName" in self.text:
            print("\t\t====>".ljust(28), end=" ")
            print("Country Name: =>\t{}".format((self.text["countryName"])))

    def gnoise_get_ip_info(self):

        print(
            MyColors.Foreground.orange
            + "\nResults found: {}".format((self.text["returned_count"]))
        )
        print("_" * 20 + "\n")

        print(MyColors.Foreground.lightgrey)
        if "records" in self.text:
            records = self.text["records"]
            try:
                for record in records:
                    if "name" in record:
                        print("\nRecord:\t=>\t{}".format((record["name"])))
                    if "metadata" in record:
                        print("".ljust(20), end=" ")
                        print(
                            "Tor:\t=>\t{}".format((record["metadata"].get("tor", "")))
                        )
                    if "confidence" in record:
                        print("".ljust(20), end=" ")
                        print("Confidence:\t=>\t{}".format((record["confidence"])))
                    if "last_updated" in record:
                        print("".ljust(20), end=" ")
                        print("Last_updated:\t=>\t{}".format((record["last_updated"])))
            except KeyError:
                pass

    def abipdbcheck(self):
        try:
            print(MyColors.Foreground.orange, MyColors.Background.lightgrey)
            print("\nABUSEIPDB SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            self.abip_get_info()

        except ValueError:
            print((MyColors.Foreground.red + "Error while connecting to AbuseIPDB!\n"))
        except KeyError:
            print(MyColors.Foreground.lightred + "\nNo results found for AbuseIPDB")

    def gnoiseipcheck(self):
        try:
            print(MyColors.Foreground.lightblue, MyColors.Background.lightgrey)
            print("\nGREY_NOISE SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            self.gnoise_get_ip_info()

        except ValueError:
            print((MyColors.Foreground.red + "Error while connecting to GreyNoise!\n"))
        except KeyError:
            print(MyColors.Foreground.lightred + "\nNo results found for GreyNoise")

    def censysipcheck(self):
        try:
            print(MyColors.reset)
            print(MyColors.Foreground.lightred, MyColors.Background.lightgrey)
            print("\nCENSYS_IP SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            for i in self.text["protocols"]:
                print(MyColors.Foreground.yellow)
                print("Services running: ")
                print("\t\t====>".ljust(28), end=" ")
                print(i)

            print("\nLast updated: {}".format((self.text["updated_at"])))
            print("-" * 120)

        except ValueError:
            print((MyColors.Foreground.red + "Error while connecting to Cencys!\n"))
        except KeyError:
            print(MyColors.Foreground.lightred + "\nNo results found for Cencys")


class Hashes:
    def __init__(self, text, value):
        self.text = text
        self.value = value

    def _vt_get_scan_date(self):
        self.text = self.text["data"]
        timestamp = self.text["attributes"]["first_submission_date"]
        dt_object = datetime.fromtimestamp(timestamp)

        print(MyColors.Foreground.yellow + "\nScan date: ".ljust(13), dt_object)

    def _vt_get_general_info(self):

        try:
            if self.text["attributes"]["tags"]:
                tags = self.text["attributes"]["tags"]
                print("Tags:")
                print("_" * 9 + "\n")
                for tag in tags:
                    print("\t\t====>".ljust(28), end=" ")
                    print(MyColors.Foreground.orange, tag, MyColors.reset)
            if self.text["attributes"]["names"]:
                names = self.text["attributes"]["names"]
                print("-" * 120)
                print("Name(s) of file:")
                print("_" * 20 + "\n")
                for name in names:
                    print("\t\t====>".ljust(28), end=" ")
                    print(MyColors.Foreground.orange, name, MyColors.reset)
            print("\n")
        except KeyError:
            pass

    def _vt_get_analysis_results(self):

        print("-" * 120)
        print("\n\n")
        ct_malicious = MyColors.Foreground.lightred + str(
            self.text["attributes"]["last_analysis_stats"]["malicious"]
        )
        ct_sources = MyColors.Foreground.lightgreen + "60"
        print(f"Detection {ct_malicious}{MyColors.reset}/{ct_sources}")
        print("_" * 20 + "\n")
        print(MyColors.reset)

        if self.text["attributes"]["last_analysis_results"]:
            analysis = self.text["attributes"]["last_analysis_results"]
            for x, y in analysis.items():
                if y["result"] is not None:
                    print(
                        f"{MyColors.Foreground.lightgreen}{x}:".ljust(20),
                        "=>".ljust(10),
                        f"{MyColors.Foreground.lightred}{y['result']}{MyColors.reset}",
                    )

    def _vt_get_urls(self):

        print("-" * 120)
        ct_urls = self.text["relationships"]["contacted_urls"]["meta"]["count"]
        print(MyColors.Foreground.red + "\n\nContacted URLs: {}".format(ct_urls))
        print("_" * 22 + "\n")
        if self.text["relationships"]["contacted_urls"]["data"]:
            data = self.text["relationships"]["contacted_urls"]["data"]
            try:
                for i in data:
                    print("\t\t====>".ljust(28), end=" ")
                    print(
                        MyColors.Foreground.orange,
                        i["context_attributes"]["url"],
                        MyColors.reset,
                    )
                print("\n")
            except KeyError:
                pass
        else:
            print("\t\t====>".ljust(28), end=" ")
            print(MyColors.reset, "NONE\n")

    def _vt_get_domains(self):

        print("-" * 120)
        ct_domains = self.text["relationships"]["contacted_domains"]["meta"]["count"]
        print(MyColors.Foreground.red + "\nContacted Domains: {}".format(ct_domains))
        print("_" * 25 + "\n")
        if self.text["relationships"]["contacted_domains"]["data"]:
            data = self.text["relationships"]["contacted_domains"]["data"]
            try:
                for i in data:
                    print("\t\t====>".ljust(28), end=" ")
                    print(MyColors.Foreground.orange, i["id"])
            except KeyError:
                pass
        else:
            print("\t\t====>".ljust(28), end=" ")
            print(MyColors.reset, "NONE")

    def _ha_get_info(self):

        try:
            x = 0
            if self.text:
                for text in self.text:
                    x += 1
                    print("".ljust(28), end=" ")
                    print(f"{MyColors.Foreground.lightred}Detection {x}")
                    print("".ljust(28), end=" ")
                    print("-" * 20, MyColors.reset)

                    print(
                        "FileName => "
                        + MyColors.Foreground.orange
                        + text.get("submit_name", ""),
                        MyColors.reset,
                    )

                    if "verdict" in text:
                        print(
                            "Verdict => "
                            + MyColors.Foreground.orange
                            + text["verdict"],
                            MyColors.reset,
                        )

                    if "submissions" in text:
                        print(
                            "Number of submissions => ",
                            MyColors.Foreground.orange,
                            len(text["submissions"]),
                            MyColors.reset,
                        )

                    if "type_short" in text:
                        print(
                            "FileType => "
                            + MyColors.Foreground.orange
                            + f"{text['type_short']}",
                            MyColors.reset,
                        )

                    if "av_detect" in text:
                        print(
                            "AV Detect => " + MyColors.Foreground.orange,
                            text["av_detect"],
                            MyColors.reset,
                        )

                    if "vx_family" in text:
                        print(
                            "Mal Family => "
                            + MyColors.Foreground.orange
                            + text["vx_family"],
                            MyColors.reset,
                        )

                    if "environment_description" in text:
                        print(
                            "Analysis environment => ".ljust(28)
                            + MyColors.Foreground.orange
                            + text["environment_description"]
                            + "\n"
                        )
            else:
                print(
                    MyColors.Foreground.lightred
                    + "No results found in HybridAnalysis!\n"
                )

        except (KeyError, TypeError):
            print(
                MyColors.Foreground.lightred + "No results found in HybridAnalysis!\n"
            )

    def _otx_get_general_info(self):
        # Get General Info
        if self.text["pulses"]:
            pulses = self.text["pulses"]
            try:
                print(
                    MyColors.Foreground.cyan,
                    "\tReports found => {}\n".format(len(pulses)),
                    MyColors.Foreground.lightgreen,
                )
                num = 0
                for pulse in pulses:
                    if pulse.get("name"):
                        num += 1
                        print("\t\t====>".ljust(28), end=" ")
                        print(f"Data {MyColors.Foreground.orange}{num}")
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            (
                                "Name: {0}{1}{2}".format(
                                    MyColors.Foreground.lightred,
                                    pulse["name"],
                                    MyColors.reset,
                                )
                            )
                        )
                    if pulse.get("tags"):
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            (
                                MyColors.Foreground.orange
                                + "Tags: {0}{1}{2}".format(
                                    MyColors.Foreground.lightred,
                                    pulse["tags"],
                                    MyColors.reset,
                                )
                            )
                        )
                    if pulse.get("targeted_countries"):
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            (
                                MyColors.Foreground.orange
                                + "Targeted Countries: {0}{1}{2}".format(
                                    MyColors.Foreground.lightred,
                                    pulse["targeted_countries"],
                                    MyColors.reset,
                                )
                            )
                        )
                    if pulse.get("references"):
                        print("\t\t====>".ljust(28), end=" ")
                        print(
                            MyColors.Foreground.orange
                            + "References: {0}{1}{2}".format(
                                MyColors.Foreground.lightred,
                                pulse["references"],
                                MyColors.reset,
                            ),
                            end=" ",
                        )
                    print("\n")
            except KeyError:
                pass

    def _otx_get_yara(self):
        # Get yara rule_name(s)
        if self.text["analysis"]["plugins"]["yarad"]["results"]["detection"]:
            detection = self.text["analysis"]["plugins"]["yarad"]["results"][
                "detection"
            ]
            try:
                print("-" * 120)
                print("Yara rule_name(s) Triggered:")
                print("_" * 34 + "\n")
                for i in self.text["analysis"]["plugins"]:
                    print("".ljust(28), end=" ")
                    print(
                        MyColors.Foreground.orange,
                        detection[i]["rule_name"],
                        MyColors.reset,
                    )
            except IndexError:
                pass

    def _otx_get_detections(self):

        print("-" * 120)
        print("\nDetections:")
        print("_" * 15 + "\n")
        if self.text["analysis"]["plugins"]:
            plugins = self.text["analysis"]["plugins"]
            for x, y in plugins.items():
                if "clamav" in x:
                    print(
                        f"{MyColors.Foreground.lightgreen}{x}:".ljust(20),
                        "=>".ljust(10),
                        f"{MyColors.Foreground.lightred}"
                        f"{y['results'].get('detection')}{MyColors.reset}",
                    )
                elif "msdefender" in x:
                    print(
                        f"{MyColors.Foreground.lightgreen}{x}:".ljust(20),
                        "=>".ljust(10),
                        f"{MyColors.Foreground.lightred}"
                        f"{y['results'].get('detection')}{MyColors.reset}",
                    )

    def _otx_get_strings(self):

        for x, y in self.text["analysis"]["plugins"].items():
            if "strings" in x:
                res = input("\nWould you like to see the strings? (y | n): ")
                with open("strings.txt", "w+") as f:
                    if res.lower() == "y":
                        print(f"{MyColors.Foreground.lightgreen}{x}:".ljust(20), "\n")
                        for i in range(0, len(y["results"])):
                            results = y["results"][i]
                            print(
                                f"{MyColors.Foreground.lightgreen}=>"
                                f" {MyColors.Foreground.lightred}{results}"
                            )
                            f.write(f"{results}\n")
                        print(
                            MyColors.Foreground.lightgreen
                            + "\nStrings written under {}\\strings.txt".format(
                                (os.getcwd())
                            )
                        )

    def _otx_get_samples(self):

        print("-" * 120)
        # Get OTX domain detected malware samples
        print(MyColors.Foreground.lightred + "\nDetected malware samples: ")
        print("_" * 30 + "\n")
        if "malware_samples" in self.text:
            if bool(self.text["malware_samples"]):
                samples = self.text["malware_samples"]
                try:
                    for sample in samples:
                        if sample:
                            print("\t\t====>".ljust(28), end=" ")
                            print(f"{sample}")
                except KeyError:
                    pass
            else:
                print("\t\t====>".ljust(28), end=" ")
                print(MyColors.reset, "NONE")

    def _otx_get_urls(self):

        print("-" * 120)
        # Get OTX domain detected URLs
        print(MyColors.Foreground.lightcyan + "\nDetected URLs: ")
        print("_" * 19 + "\n")
        if "url_list" in self.text:
            if bool(self.text["url_list"]):
                urls = self.text["url_list"]
                try:
                    for url in urls:
                        if url.get("url"):
                            print("\t\t====>".ljust(28), end=" ")
                            print(f"{url['url']}")
                except KeyError:
                    pass
            else:
                print("\t\t====>".ljust(28), end=" ")
                print(MyColors.reset, "NONE")

    def vthash(self):
        try:
            print(MyColors.Foreground.lightblue + MyColors.Background.lightgrey)
            print("\nVIRUSTOTAL SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            self._vt_get_scan_date()
            self._vt_get_general_info()
            self._vt_get_analysis_results()
            self._vt_get_domains()
            self._vt_get_urls()

        except ValueError:
            print(
                MyColors.Foreground.lightred + "Error while connecting to VirusTotal!\n"
            )
        except (KeyError, TypeError):
            print(MyColors.Foreground.lightred + "No results found in VirusTotal!\n")

    def hahash(self):
        try:
            print(MyColors.Foreground.lightred + MyColors.Background.lightgrey)
            print("\n\nHYBRIDANALYSIS SUMMARY")
            print("=" * 25, "\n", MyColors.reset)

            self._ha_get_info()

        except ValueError:
            print(
                MyColors.Foreground.lightred
                + "Error while connecting to HybridAnalysis!\n"
            )
        except (KeyError, TypeError):
            print(
                MyColors.Foreground.lightred + "No results found in HybridAnalysis!\n"
            )

    def otxhash(self):
        try:
            print(MyColors.Foreground.lightblue + MyColors.Background.lightgrey)
            print("\nOTXQuery SUMMARY")
            print("=" * 25, "\n", MyColors.reset)
            print(
                MyColors.Foreground.lightcyan + "General Info: ".ljust(17),
                MyColors.reset,
            )

            self._otx_get_general_info()
            self._otx_get_yara()
            self._otx_get_detections()
            self._otx_get_strings()
            self._otx_get_samples()
            self._otx_get_urls()

        except ValueError:
            print((MyColors.Foreground.red + "Error while connecting to OTX_Query!\n"))
        except (KeyError, TypeError):
            print(MyColors.Foreground.lightred + "\nNo results found for OTX_Query")


class Urls:
    def __init__(self, text, value):
        self.text = text
        self.value = value

    def _vt_get_scan_date(self):
        date = self.text["scan_date"]
        print(MyColors.Foreground.yellow + "\nScan date: ".ljust(13), date)

    def _vt_get_analysis_results(self):
        print("-" * 120)
        print("\n\n")
        ct_malicious = MyColors.Foreground.lightred + str(self.text["positives"])
        ct_sources = MyColors.Foreground.lightgreen + str(self.text["total"])
        print(f"Detection {ct_malicious}{MyColors.reset}/{ct_sources}")
        print("_" * 20 + "\n")
        print(MyColors.reset)

        if self.text["scans"]:
            analysis = self.text["scans"]
            for x, y in analysis.items():
                if y["detected"] is not False:
                    print(
                        f"{MyColors.Foreground.lightgreen}{x}:".ljust(20),
                        "=>".ljust(10),
                        f"{MyColors.Foreground.lightred}{y['result']}{MyColors.reset}",
                    )

    def _haus_general_info(self):
        info = ["date_added", "threat", "reporter", "url_status", "urlhaus_reference"]
        for x, y in self.text.items():
            if x in info:
                print(
                    MyColors.Foreground.lightgreen,
                    x + ":\t",
                    MyColors.Foreground.cyan,
                    y,
                    MyColors.reset,
                )

    def _haus_payloads(self):
        info = [
            "response_md5",
            "urlhaus_download",
            "file_type",
            "firstseen",
            "signature",
        ]

        print("-" * 120)
        print(
            MyColors.Foreground.lightcyan
            + "\nPayloads Found: {}".format(len(self.text["payloads"]))
        )
        print("_" * 20)
        payloads = self.text["payloads"]
        num = 0

        for item in payloads:
            num += 1
            print("\n")
            print("\t\t".ljust(28), end=" ")
            print(MyColors.Foreground.orange, f"Payload {num}")
            print("\t\t".ljust(28), end=" ")
            print(" =======\n", MyColors.reset)
            for x, y in item.items():
                if x in info:
                    print("\t\t====>".ljust(28), end=" ")
                    print(
                        MyColors.Foreground.lightgreen,
                        x + ":\t",
                        MyColors.Foreground.orange,
                        y,
                        MyColors.reset,
                    )

    def vturl_check(self):
        print(MyColors.Foreground.lightblue + MyColors.Background.lightgrey)
        print("\nVIRUSTOTAL SUMMARY")
        print("=" * 25, "\n", MyColors.reset)

        if self.text["response_code"] == 1:
            try:
                self._vt_get_scan_date()
                self._vt_get_analysis_results()

            except ValueError:
                print(
                    MyColors.Foreground.lightred
                    + "Error while connecting to VirusTotal!\n"
                )
        else:
            print(MyColors.Foreground.lightred + "No results found in VirusTotal!\n")

    def hausurl_check(self):
        print(MyColors.Foreground.orange + MyColors.Background.lightgrey)
        print("\nURLHAUS SUMMARY")
        print("=" * 25, "\n", MyColors.reset)
        if self.text["query_status"] == "ok":
            try:
                self._haus_general_info()
                self._haus_payloads()

            except ValueError:
                print(
                    MyColors.Foreground.lightred
                    + "Error while connecting to URLHAUS!\n"
                )
        else:
            print(MyColors.Foreground.lightred + "\n\nNo results found in URLHAUS!\n")
