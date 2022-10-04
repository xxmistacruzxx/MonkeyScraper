import string
import time
import threading
import json

import MonkeyType

class Scraper:
    #   CONSTRUCTOR: Constructor for the Scraper class.
    def __init__(self, apekeys:list, language:string = "english", mode:string = "time", mode2:string = "15"):
        self.apekeys = apekeys
        if (language not in MonkeyType.LANGUAGES):
            print("ERROR: Unknown language in Scraper constructor")
            return
        self.language = language
        if (mode not in MonkeyType.MODES):
            print("ERROR: Unknown mode in Scraper constructor")
            return
        self.mode = mode
        if (mode2 not in MonkeyType.MODES[mode]):
            print("ERROR: Unknown mode2 in Scraper constructor")
            return
        self.mode2 = mode2
        self.data = {}

    #   FUNCTION:   Gets leaderboard entries of the scraper's mode and mode2 in a given interval. 
    #   ARGS:   apekey - Your ApeKey from MonkeyType
    #           max - the max rank to retrieve from scraping
    #           start - the first rank to retrieve from scraping
    #           skip - the number of entries to move over for the next request (only important for multithreaded scraping).
    #           delay - enables sleep after a request to avoid the 30 requests per min cap from MonkeyType
    #           keyBy - key in which copy over the entries into the new dictionary. Ex. "rank" or "name" or "uid"
    def scrapeFinite(self, apekey: string, max: int, start: int = 0, skip: int = 50, delay : bool = True, keyBy : string = "rank"):
        curr = start
        while curr < max:
            scraped = None
            if (curr + 50) > max:
                scraped = MonkeyType.getLeaderboard(apekey, self.language, self.mode, self.mode2, curr, (max-curr))
            else:
                scraped = MonkeyType.getLeaderboard(apekey, self.language, self.mode, self.mode2, curr, 50)
            for i in scraped["data"]:
                self.data[i[keyBy]] = i
            curr += skip
            if delay == True:
                time.sleep(2)
        return self.data

    #   FUNCTION:   Same as ScrapeFinite except can use multiple apekeys to have multithreaded scraping
    #   ARGS:   max - the max rank to retrieve from scraping
    #           keyBy - key in which copy over the entries into the new dictionary. Ex. "rank" or "name" or "uid"
    def multiThreadedScrapeFinite(self, max: int, keyBy : string = "rank"):
        threads = []
        numOfApekeys = len(self.apekeys)
        for i in range(numOfApekeys):
            # self.scrape(self.apekeys[i], max, i*50, i*numOfApekeys, True)
            process = threading.Thread(target=self.scrapeFinite, args=[self.apekeys[i], max, i*50, (numOfApekeys)*50, True, keyBy])
            process.start()
            threads.append(process)
        for process in threads:
            process.join()
        return self.data


    def scrapeInfinite(self):
        # TODO: implement
        return None
    
    def multiThreadedScrapeInfinite(self):
        # TODO: implement
        return None

    def getData(self):
        return self.data

def main():
    print("MonkeyScraper.py main function")
    ## TESTING OF MONKEYSCRAPER FUNCTIONS
    # test = Scraper(MonkeyType.keysFromTextFileToList(), "english", "time", "15")
    # test.scrapeFinite(test.apekeys[0], 299, 0, 50, True)
    # test.multiThreadedScrapeFinite(100, "rank")
    # with open("sample.json", "w") as outfile:
        # json.dump(test.getData(), outfile)

if __name__ == "__main__":
    main()