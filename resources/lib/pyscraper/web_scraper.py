import requests
from datetime import datetime
import time

from xbmcaddon import Addon

from scraper import AbstractScraper
from rcbexceptions import *
from util import Logutil as log
from util import __addon__


class WebScraper(AbstractScraper):
    _headers = {'User-Agent': 'RomCollectionBrowser {0}'.format(__addon__.getAddonInfo('version'))}

    """ The following attributes are overridden in child web scrapers"""
    _apikey = ''
    _search_url = ''
    _retrieve_url = ''

    # Note - this needs to map to the order of the consoleDict array.
    pmaps = ['MobyGames.com', 'GiantBomb.com', 'thegamesdb.net']

    # Mapping between the platform name in RCB and the platform identifier for the various web scrapers
    # FIXME Move to the appropriate scraper classes
    # consoleDict is the master list of all platforms that are supported by RCB. This list is also shown in configwizard to let the user select the platform
    # https://api.mobygames.com/v1/platforms?api_key=FH9VxTkB6BGAEsF3qlnnxQ==
    # https://www.giantbomb.com/api/platforms/?api_key=279442d60999f92c5e5f693b4d23bd3b6fd8e868
    # https://api.thegamesdb.net/v1/Platforms/?apikey=1e821bf1bab06854840650d77e7e2248f49583821ff9191f2cced47e43bf0a73

    consoleDict = {
        # name, mobygames-id, thegamesdb, giantbomb
        'Other': ['0', '', ''],
        '3DO': ['35', '26', '25'],
        'Acorn 32-bit': ['117', '', ''],
        'Acorn Archimedes': ['', '125', '4944'],
        'Acorn Electron': ['', '', '4954'],
        'Action Max': ['', '148', '4976'],
        'Alice 32/90': ['194', '', ''],
        'Amiga': ['19', '1', '4911'],
        'Amiga CD32': ['56', '39', '4947'],
        'Amstrad CPC': ['60', '11', '4914'],
        'Amstrad PCW': ['136', '', ''],
        'Android': ['91', '123', '4916'],
        'APF MP1000': ['213', '', '4969'],
        'Apple II': ['31', '12', '4942'],
        'Atari 2600': ['28', '40', '22'],
        'Atari 5200': ['33', '67', '26'],
        'Atari 7800': ['34', '70', '27'],
        'Atari 8-bit': ['39', '24', '4943'],
        # 'Atari Jaguar': ['17', '28', '28'],
        'Atari Jaguar CD': ['17', '171', '29'],
        # 'Atari Lynx': ['18', '7', '4924'],
        'Atari ST': ['24', '13', '4937'],
        'Atari XE': ['', '', '30'],
        'Bally Astrocade': ['160', '120', '4968'],
        'BBC Micro': ['92', '', '110'],
        'BREW': ['63', '', ''],
        'Casio Loopy': ['124', '126', ''],
        'Casio PV-1000': ['125', '149', '4964'],
        'CD-i': ['73', '27', '4917'],
        'Channel F': ['76', '66', '4928'],
        'Coleco Adam': ['156', '', ''],
        'ColecoVision': ['29', '47', '31'],
        'Commodore 16': ['115', '150', ''],
        'Commodore 64': ['27', '14', '40'],
        'Commodore 128': ['61', '58', '4946'],
        'Commodore PET/CBM': ['77', '62', ''],
        # 'Commodore VIC20': ['43', '30', '4945'],
        'DoJa': ['72', '', ''],
        'DOS': ['2', '94', ''],
        'Dragon 32/64': ['79', '61', '4952'],
        'Dreamcast': ['8', '37', '16'],
        'Electron': ['93', '', '4954'],
        'Entex Adventure Vision': ['210', '93', '4974'],
        'Epoch Cassette Vision': ['137', '135', '4965'],
        'Epoch Super Cassette Vision': ['138', '136', '4966'],
        'ExEn': ['70', '', ''],
        'Famicom Disk System': ['', '91', '4936'],
        'FM-7': ['126', '114', '4978'],
        'FM Towns': ['102', '108', '4932'],
        'Game & Watch': ['', '1183', '4950'],
        'Game Boy': ['10', '3', '4'],
        'Game Boy Advance': ['12', '4', '5'],
        'Game Boy Color': ['11', '57', '41'],
        'Game.Com': ['50', '77', '4940'],
        'GameCube': ['14', '23', '2'],
        'Game Gear': ['25', '5', '20'],
        'Game Wave': ['104', '105', ''],
        'Genesis': ['16', '6', '18'],
        'Gizmondo': ['55', '78', ''],
        'HyperScan': ['192', '104', ''],
        'Intellivision': ['30', '51', '32'],
        'Jaguar': ['17', '28', '28'],
        'LaserActive': ['163', '92', '4975'],
        'Leapfrog Didj': ['184', '144', ''],
        'Leapster': ['183', '89', ''],
        'Linux': ['1', '152', ''],
        'Lynx': ['18', '7', '4924'],
        'Macintosh': ['74', '17', '37'],
        'MAME': ['0', '84', '23'],
        'Mega Duck': ['', '137', '4948'],
        'Microbee': ['200', '168', ''],
        'Microvision': ['97', '90', '4972'],
        'Mophun': ['71', '', ''],
        'MSX': ['57', '15', '4929'],
        'Neo Geo': ['36', '25', '24'],
        'Neo Geo CD': ['54', '59', '4956'],
        'Neo Geo Pocket': ['52', '80', '4922'],
        'Neo Geo Pocket Color': ['53', '81', '4923'],
        'NES': ['22', '21', '7'],
        'N-Gage': ['32', '34', '4938'],
        'Nintendo 3DS': ['101', '117', '4912'],
        'Nintendo 64': ['9', '43', '3'],
        'Nintendo DS': ['44', '52', '8'],
        'Nintendo DSi': ['87', '52', ''],
        'Nintendo Switch': ['203', '157', '4971'],
        'Nuon': ['116', '85', '4935'],
        'Odyssey': ['75', '74', '4961'],
        'Odyssey 2': ['78', '60', '4927'],
        'Ouya': ['144', '154', '4921'],
        'PC-6001': ['149', '115', ''],
        'PC-88': ['94', '109', '4933'],
        'PC-98': ['95', '112', '4934'],
        'PC Booter': ['4', '94', ''],
        'PC Engine SuperGrafX': ['127', '119', ''],
        'PC-FX': ['59', '75', '4930'],
        'Pippin': ['112', '102', ''],
        'PlayStation': ['6', '22', '10'],
        'PlayStation 2': ['7', '19', '11'],
        'PlayStation 3': ['81', '35', '12'],
        'PlayStation 4': ['141', '146', '4919'],
        'Playdia': ['107', '127', ''],
        'Pokemon mini': ['152', '134', '4957'],
        'PSP': ['46', '18', '13'],
        'PS Vita': ['105', '129', '39'],
        'RCA Studio II': ['113', '131', '4967'],
        'SAM Coupe': ['120', '162', '4979'],
        'SEGA 32X': ['21', '31', '33'],
        'SEGA CD': ['20', '29', '21'],
        'SEGA Master System': ['26', '8', '35'],
        'SEGA Pico': ['103', '118', '4958'],
        'SEGA Saturn': ['23', '42', '17'],
        'SEGA SG-1000': ['114', '141', '4949'],
        'Sharp X1': ['121', '113', '4977'],
        'Sharp X68000': ['106', '95', '4931'],
        'Sharp MZ-80B/2000/2500': ['182', '128', ''],
        'Sharp MZ-80K/700/800/1500': ['181', '128', ''],
        'Socrates': ['190', '169', ''],
        'SNES': ['15', '9', '6'],
        'Spectravideo': ['85', '', ''],
        "Super A'can": ['110', '151', ''],
        'Supervision': ['109', '147', '4959'],
        'TI-99/4A': ['47', '48', '4953'],
        'Tomy Tutor': ['151', '165', '4960'],
        'TRS-80': ['58', '63', ''],
        'TRS-80 CoCo': ['62', '68', '4941'],
        'TurboGrafx-16': ['40', '55', '34'],
        'TurboGrafx CD': ['45', '53', '4955'],
        'Vectrex': ['37', '76', '4939'],
        'VIC-20': ['43', '30', '4945'],
        'Virtual Boy': ['38', '79', '4918'],
        'V.Smile': ['42', '82', ''],
        'Wii': ['82', '36', '9'],
        'Wii U': ['132', '139', '38'],
        'Windows': ['3', '94', '1'],
        'Windows 3.x': ['5', '94', ''],
        'WonderSwan': ['48', '65', '4925'],
        'WonderSwan Color': ['49', '54', '4926'],
        'Xbox': ['13', '32', '14'],
        'Xbox 360': ['69', '20', '15'],
        'Xbox One': ['142', '145', '4920'],
        'Zeebo': ['88', '122', ''],
        'Zodiac': ['68', '64', ''],
        'ZX Spectr': ['41', '16', '4913']}

    def __init__(self):
        pass

    def get_platform_for_scraper(self, platformname):
        """Get the platform identifier used on the corresponding website.

        Args:
            platformname: The RCB platform name

        Returns:
            String that is the identifier for the platform on the corresponding website.

        """
        try:
            #HACK: use same platform mapping for thegamesdb and legacy.thegamesdb
            #remove, when thegamesdbs update process is finished
            ix = self.pmaps.index(self._name)
        except ValueError:
            # Did not find a mapping
            log.warn("Did not find a platform mapping for {0}".format(self._name))
            ix = 0

        return self.consoleDict[platformname][ix]

    def open_json_url(self, **kwargs):
        log.info('Retrieving url %s, params = %s' %(kwargs['url'], kwargs['params']))
        
        try:
            r = requests.get(kwargs['url'], headers=self._headers, params=kwargs['params'])
        except ValueError:
            # Typically non-JSON response
            raise ScraperUnexpectedContentException("Non-JSON response received")

        log.debug(u"Retrieving {0} as JSON - HTTP{1}".format(r.url, r.status_code))

        if r.status_code == 401:
            # Mobygames and GiantBomb send a 401 if the API key is invalid
            raise ScraperUnauthorisedException("Invalid API key sent")

        if r.status_code == 429:
            raise ScraperExceededAPIQuoteException("Scraper exceeded API key limits")

        if r.status_code == 500:
            raise ScraperWebsiteUnavailableException("Website unavailable")

        return r.json()

    def open_xml_url(self, **kwargs):
        log.info('Retrieving url %s, params = %s' %(kwargs['url'], kwargs['params']))

        r = requests.get(kwargs['url'], headers=self._headers, params=kwargs['params'])

        log.debug(u"Retrieving {0} as XML - HTTP{1}".format(r.url, r.status_code))

        # Need to ensure we are sending back Unicode text
        return r.text.encode('utf-8')

    def _parse_date(self, datestr):
        """Extract the year from a given date string using a given format. This function is used to cater for
        an edge case identified in https://forum.kodi.tv/showthread.php?tid=112916&pid=1214507#pid1214507.

        Args:
            datestr: Input date

        Returns:
            Year as a %Y format string
        """
        if datestr is None:
            return '1970'

        x = None
        for fmt2 in ["%Y-%m-%d", "%Y-%m", "%Y", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y", "%m/%d/%Y"]:
            try:
                x = datetime.strptime(datestr, fmt2).strftime("%Y")
                break
            except ValueError as e:
                # Skip to the next format
                log.warn("ValueError in parseDate: %s" %e)
            except TypeError:
                log.warn("Unable to parse date using strptime, falling back to time function")
                try:
                    x = datetime(*(time.strptime(datestr, fmt2)[0:6])).strftime("%Y")
                    break
                except ValueError as ve:
                    log.warn("Unable to parse date %s using %s, try next format. %s" %(datestr, fmt2, ve))

        if x is not None:
            return x
        else:
            log.warn(u"Unexpected date format: {0}".format(datestr))
            return u"1970"

