import treetaggerwrapper
import os

tagdir = os.getenv('TREETAGGER_ROOT')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR=tagdir)
tags = tagger.TagText(u"Save the time of the reader. SAMPLETEST. SampleTest.")
for tag in tags:
    print tag
    #print type(tag)
