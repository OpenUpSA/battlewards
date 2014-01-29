from __future__ import division
from kartograph import Kartograph
import re

ROW_GAP = 1500
COL_MAP_SPACING = ROW_MAP_SPACING = 1500
COLS = 12

munics = open("munics.txt").readlines()
re_junk = re.compile(r"(<\?xml[^<>]*?>|<!DOCTYPE[^<>]*>)")
fp = open("final.svg", "w")
fp.write('<svg width="10in" height="10in">')

added = 0
added_rows = 0
for i, m in enumerate(munics):
    m = m.strip()
    if m.startswith("#"): 
        continue

    i += added
    row = i // COLS
    col = i % COLS
    # add a new line when ever we see a space
    # i'm using this so separate provinces
    if m == "":
        added += COLS - col - 1
        added_rows += 1
        continue
        
        
    print m
    css = open("style.css").read()
    config = {
        "layers" : [{
            "id" : "wards",
            "src" : "data/winners.shp",
            "filter" : {"Municipali" : m},
            "simplify" : 3,
            "attributes" : {
                "ward_id" : "WARD_ID",
                #"id" : "WARD_ID",
                "winner" : "Winner",
                "other_winner" : "OtherWinne",
                "margin" : "Margin",
                "votes" : "TotalVotes",
            },
        },
        {
            "id" : "towns",
            "src" : "data/cities_and_towns.shp",
            "labeling" : {
                "key" : "TOWN",
            },
            "attributes" : {
                "name" : "TOWN",
            }
        }]
    }

    outfile = "%d.svg" % i
    K = Kartograph()
    K.generate(config, outfile=outfile, stylesheet=css)
    
    text = open(outfile).read()
    text = re_junk.sub("", text)
    fp.write('<g transform="translate(%d,%d)">' % (col * COL_MAP_SPACING, row * ROW_MAP_SPACING + (ROW_GAP * added_rows)))
    fp.write(text)
    fp.write("</g>")
fp.write("</svg>")
fp.close()
