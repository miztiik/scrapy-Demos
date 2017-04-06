# -*- coding: utf-8 -*-
import scrapy
import json

class kuralItem(scrapy.Item):
    KuralPaal       = scrapy.Field()
    KuralAthigaram  = scrapy.Field()
    KuralNo         = scrapy.Field()
    Kural           = scrapy.Field()
    KuralExpln1     = scrapy.Field()
    KuralExpln2     = scrapy.Field()

class getKuralWithSpdier(scrapy.Spider):
    name = "getKurals"
    allowed_domains = ["valaitamil.com"]

    # start_urls = ( 'http://www.dinamalar.com/kural_detail.asp?kural_no=1')
    start_urls = ['http://www.valaitamil.com/the-praise-of-god-141.html'
                  ,'http://www.valaitamil.com/the-blessing-of-rain-142.html'
                  ,'http://www.valaitamil.com/the-greatness-of-ascetics-143.html'
                  ,'http://www.valaitamil.com/assertion-of-the-strength-of-virtue-144.html'
                  ,'http://www.valaitamil.com/domestic-life-146.html'
                  ,'http://www.valaitamil.com/the-worth-of-a-wife-147.html'
                  ,'http://www.valaitamil.com/the-wealth-of-children-148.html'
                  ,'http://www.valaitamil.com/the-possession-of-love-149.html'
                  ,'http://www.valaitamil.com/hospitality-150.html'
                  ,'http://www.valaitamil.com/the-utterance-of-pleasant-words-151.html'
                  ,'http://www.valaitamil.com/gratitude-152.html'
                  ,'http://www.valaitamil.com/impartiality-153.html'
                  ,'http://www.valaitamil.com/the-possession-of-self-restraint-154.html'
                  ,'http://www.valaitamil.com/the-possession-of-decorum-155.html'
                  ,"http://www.valaitamil.com/not-coveting-another/'s-wife-156.html"
                  ,'http://www.valaitamil.com/the-possession-of-patience,-forbearance-157.html'
                  ,'http://www.valaitamil.com/not-envying-158.html'
                  ,'http://www.valaitamil.com/not-coveting-159.html'
                  ,'http://www.valaitamil.com/not-backbiting-160.html'
                  ,'http://www.valaitamil.com/against-vain-speaking-161.html'
                  ,'http://www.valaitamil.com/dread-of-evil-deeds-162.html'
                  ,'http://www.valaitamil.com/duty-to-society-163.html'
                  ,'http://www.valaitamil.com/giving-164.html'
                  ,'http://www.valaitamil.com/renown-165.html'
                  ,'http://www.valaitamil.com/compassion-167.html'
                  ,'http://www.valaitamil.com/abstinence-from-flesh-168.html'
                  ,'http://www.valaitamil.com/penance-169.html'
                  ,'http://www.valaitamil.com/imposture-170.html'
                  ,'http://www.valaitamil.com/the-absence-of-fraud-171.html'
                  ,'http://www.valaitamil.com/veracity-172.html'
                  ,'http://www.valaitamil.com/restraining-anger-173.html'
                  ,'http://www.valaitamil.com/not-doing-evil-174.html'
                  ,'http://www.valaitamil.com/not-killing-175.html'
                  ,'http://www.valaitamil.com/instability-176.html'
                  ,'http://www.valaitamil.com/renunciation-177.html'
                  ,'http://www.valaitamil.com/truth-conciousness-178.html'
                  ,'http://www.valaitamil.com/curbing-of-desire-179.html'
                  ,'http://www.valaitamil.com/fate-182.html'
                  ,'http://www.valaitamil.com/the-greatness-of-a-king-192.html'
                  ,'http://www.valaitamil.com/learning-193.html'
                  ,'http://www.valaitamil.com/ignorance-194.html'
                  ,'http://www.valaitamil.com/hearing-195.html'
                  ,'http://www.valaitamil.com/the-possession-of-knowledge-196.html'
                  ,'http://www.valaitamil.com/the-correction-of-faults-197.html'
                  ,'http://www.valaitamil.com/seeking-the-aid-of-great-men-198.html'
                  ,'http://www.valaitamil.com/avoiding-mean-associations-199.html'
                  ,'http://www.valaitamil.com/acting-after-due-consideration-200.html'
                  ,'http://www.valaitamil.com/the-knowledge-of-power-201.html'
                  ,'http://www.valaitamil.com/knowing-the-fitting-time-202.html'
                  ,'http://www.valaitamil.com/knowing-the-place-203.html'
                  ,'http://www.valaitamil.com/selection-and-confidence-204.html'
                  ,'http://www.valaitamil.com/selection-and-employment-205.html'
                  ,'http://www.valaitamil.com/cherishing-kinsmen-206.html'
                  ,'http://www.valaitamil.com/unforgetfulness-207.html'
                  ,'http://www.valaitamil.com/the-right-sceptre-208.html'
                  ,'http://www.valaitamil.com/the-cruel-sceptre-209.html'
                  ,'http://www.valaitamil.com/absence-of-terrorism-210.html'
                  ,'http://www.valaitamil.com/benignity-211.html'
                  ,'http://www.valaitamil.com/detectives-212.html'
                  ,'http://www.valaitamil.com/energy-213.html'
                  ,'http://www.valaitamil.com/unsluggishness-214.html'
                  ,'http://www.valaitamil.com/manly-effort-215.html'
                  ,'http://www.valaitamil.com/hopefulness-in-trouble-216.html'
                  ,'http://www.valaitamil.com/the-office-of-minister-of-state-217.html'
                  ,'http://www.valaitamil.com/power-of-speech-218.html'
                  ,'http://www.valaitamil.com/purity-in-action-219.html'
                  ,'http://www.valaitamil.com/power-in-action-220.html'
                  ,'http://www.valaitamil.com/modes-of-action-221.html'
                  ,'http://www.valaitamil.com/the-envoy-222.html'
                  ,'http://www.valaitamil.com/conduct-in-the-presence-of-the-king-223.html'
                  ,'http://www.valaitamil.com/the-knowledge-of-indications-224.html'
                  ,'http://www.valaitamil.com/the-knowledge-of-the-council-chamber-225.html'
                  ,'http://www.valaitamil.com/not-to-dread-the-council-226.html'
                  ,'http://www.valaitamil.com/the-land-228.html'
                  ,'http://www.valaitamil.com/the-fortification-229.html'
                  ,'http://www.valaitamil.com/way-of-accumulating-wealth-230.html'
                  ,'http://www.valaitamil.com/the-excellence-of-an-army-231.html'
                  ,'http://www.valaitamil.com/military-spirit-232.html'
                  ,'http://www.valaitamil.com/friendship-233.html'
                  ,'http://www.valaitamil.com/investigation-in-forming-friendships-234.html'
                  ,'http://www.valaitamil.com/familiarity-235.html'
                  ,'http://www.valaitamil.com/evil-friendship-236.html'
                  ,'http://www.valaitamil.com/unreal-friendship-237.html'
                  ,'http://www.valaitamil.com/folly-238.html'
                  ,'http://www.valaitamil.com/ignorance-239.html'
                  ,'http://www.valaitamil.com/hostility-240.html'
                  ,'http://www.valaitamil.com/the-might-of-hatred-241.html'
                  ,'http://www.valaitamil.com/knowing-the-quality-of-hate-242.html'
                  ,'http://www.valaitamil.com/enmity-within-243.html'
                  ,'http://www.valaitamil.com/not-offending-the-greatc-244.html'
                  ,'http://www.valaitamil.com/being-led-by-women-245.html'
                  ,'http://www.valaitamil.com/wanton-women-246.html'
                  ,'http://www.valaitamil.com/not-drinking-palm-wine-247.html'
                  ,'http://www.valaitamil.com/gambling-248.html'
                  ,'http://www.valaitamil.com/medicine-249.html'
                  ,'http://www.valaitamil.com/nobility-250.html'
                  ,'http://www.valaitamil.com/honour-251.html'
                  ,'http://www.valaitamil.com/greatness-252.html'
                  ,'http://www.valaitamil.com/perfectness-253.html'
                  ,'http://www.valaitamil.com/courtesy-254.html'
                  ,'http://www.valaitamil.com/wealth-without-benefaction-255.html'
                  ,'http://www.valaitamil.com/shame-256.html'
                  ,'http://www.valaitamil.com/the-way-of-maintaining-the-family-257.html'
                  ,'http://www.valaitamil.com/farming-258.html'
                  ,'http://www.valaitamil.com/poverty-259.html'
                  ,'http://www.valaitamil.com/mendicancy-260.html'
                  ,'http://www.valaitamil.com/the-dread-of-mendicancy-261.html'
                  ,'http://www.valaitamil.com/baseness-262.html'
                  ,'http://www.valaitamil.com/the-pre-marital-love-263.html'
                  ,'http://www.valaitamil.com/recognition-of-the-signs-264.html'
                  ,'http://www.valaitamil.com/rejoicing-in-the-embrace-265.html'
                  ,'http://www.valaitamil.com/the-praise-of-her-beauty-266.html'
                  ,"http://www.valaitamil.com/declaration-of-love's-special-excellence-267.html"
                  ,'http://www.valaitamil.com/the-abandonment-of-reserve-268.html'
                  ,'http://www.valaitamil.com/the-announcement-of-the-rumour-269.html'
                  ,'http://www.valaitamil.com/separation-unendurable-270.html'
                  ,'http://www.valaitamil.com/complainings-271.html'
                  ,'http://www.valaitamil.com/eyes-consumed-with-grief-272.html'
                  ,'http://www.valaitamil.com/the-pallid-hue-273.html'
                  ,'http://www.valaitamil.com/the-solitary-anguish-274.html'
                  ,'http://www.valaitamil.com/sad-memories-275.html'
                  ,'http://www.valaitamil.com/the-visions-of-the-night-276.html'
                  ,'http://www.valaitamil.com/lamentations-at-eventide-277.html'
                  ,'http://www.valaitamil.com/wasting-away-278.html'
                  ,'http://www.valaitamil.com/soliloquy-279.html'
                  ,'http://www.valaitamil.com/reserve-overcome-280.html'
                  ,'http://www.valaitamil.com/mutual-desire-281.html'
                  ,'http://www.valaitamil.com/the-reading-of-the-signs-282.html'
                  ,'http://www.valaitamil.com/desire-for-reunion-283.html'
                  ,'http://www.valaitamil.com/expostulation-with-oneself-284.html'
                  ,'http://www.valaitamil.com/pouting-285.html'
                  ,'http://www.valaitamil.com/feigned-anger-286.html'
                  ,'http://www.valaitamil.com/the-pleasures-of-temporary-variance-288.html'
                  ]

    def parse(self, response):

        xpathDict = {}

        xpathDict['paal']               = "//div[@class='breadcrumb']/a[@class='nbgblue']/text()"
        xpathDict['kuralAthigaram']     = "//div[@class='home_content MT3']/div/table/tr[3]/td/span/text()"
        xpathDict['kuralNo']            = "//div[@class='home_content MT3']/div/table/tr[4]/td/text()"
        xpathDict['kuralPart1']         = "//div[@class='home_content MT3']/div/table/tr[4]/td[2]/table/tr[2]/td/text()"
        xpathDict['kuralPart1']         = "//div[@class='home_content MT3']/div/table/tr[4]/td[2]/table/tr[2]/td/text()"
        xpathDict['kuralExp1']          = "//div[@class='cls100_p']/div[6]/p/text()"
        xpathDict['kuralExp2']          = "//div[@class='cls100_p']/div[8]/p/text()"

        kural = kuralItem()

        kural['KuralPaal']      = ''.join( response.xpath( xpathDict['paal'] ).extract() ).encode('utf-8')
        kural['KuralAthigaram'] = ''.join( response.xpath( xpathDict['kuralAthigaram'] ).extract() ).strip()
        kural['KuralNo']        = ''.join( response.xpath( xpathDict['kuralNo'] ).strip().split(": ")[1].strip()
        
        kuralPart = response.xpath( xpathDict['kuralPart1']
        kuralPart = ' '.join( ''.join( kuralPart ).split())

        kural['Kural']          = ''.join(  ).extract() ).encode('utf-8').replace('\n', ' ').replace('\r', '')
        

        kural['KuralExpln1']    = ''.join( response.xpath( xpathDict['kuralExp1'] ).extract() ).encode('utf-8')
        kural['KuralExpln2']    = ''.join( response.xpath( xpathDict['kuralExp2'] ).extract() ).encode('utf-8')

        yield kural
