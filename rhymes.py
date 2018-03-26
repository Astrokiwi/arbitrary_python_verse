import pronouncing as P
import random
import numpy as np
import sys
import re
import os

def words_to_line(words):
    print(" ".join(words)+",")
#     os.system("say {}".format(" ".join(words)))

class commonword_manager:
    def __init__(self,wordlistfile):
        commonwords = np.loadtxt(wordlistfile,dtype=str)

        common_phones = [P.phones_for_word(x) for x in commonwords]
        pronunciation_known = [len(x)>=1 for x in common_phones]
        self.commonwords = list(commonwords[pronunciation_known])
        self.nallwords = len(self.commonwords)

        common_phones = [P.phones_for_word(x)[0] for x in self.commonwords]
        common_nsyllables = [P.syllable_count(x) for x in common_phones]
        common_rhymes = [list(set(P.rhymes(x)) & set(commonwords)) for x in self.commonwords]
        self.common_rhyme_indices = [ [self.commonwords.index(x) for x in rhymes] for rhymes in common_rhymes ]
        self.common_stresses = [P.stresses_for_word(x)[0] for x in self.commonwords]

    def search_stress(self,stress_pattern):
        r = re.compile(stress_pattern)
        return [self.commonwords[i] for i in range(self.nallwords) if r.match(self.common_stresses[i])]
    
    def random_stress(self,stress_pattern):
        return random.choice(self.search_stress(stress_pattern))

    def search_stress_rhymes(self,word,stress_pattern):
        word_index = self.commonwords.index(word)
        word_rhymes_indices = self.common_rhyme_indices[word_index]
        word_rhymes = [self.commonwords[i] for i in word_rhymes_indices]
        r = re.compile(stress_pattern)
#         print(word_rhymes)
        return [self.commonwords[i] for i in word_rhymes_indices if r.match(self.common_stresses[i])]
#         print(word_rhymes_indices)
#         print(word_rhymes)
#         nrhymes = len(word_rhymes)
#         r = re.compile(stress_pattern)
#         return [commonwords[i] for i in range(nrhymes) if r.match(P.stresses_for_word(word_rhymes[i][0]))]
    
    def random_stress_rhymes(self,word,stress_pattern):
        return random.choice(self.search_stress_rhymes(word,stress_pattern))
    
    def meter_line(self,stress_pattern_list,rhymeword=None):
        nsyllables = len(stress_pattern_list)
        nsyllables_so_far = 0
        words_syllables = []
        while nsyllables_so_far<nsyllables:
            words_syllables.append(random.randint(1,3))
            nsyllables_so_far+=words_syllables[-1]
        if nsyllables_so_far>nsyllables:
            words_syllables[-1]-=nsyllables_so_far-nsyllables
        nwords = len(words_syllables)
        word_syllable_indices = np.cumsum(words_syllables)[:-1]
        word_syllable_indices=np.insert(word_syllable_indices,0,0)
        word_stresses = ["".join(stress_pattern_list[word_syllable_indices[i]:word_syllable_indices[i]+words_syllables[i]])+"$" for i in range(nwords)]
        ngenerate = nwords-1 if rhymeword else nwords
        words = [self.random_stress(word_stresses[i]) for i in range(ngenerate)]
        if rhymeword:
            words.append(self.random_stress_rhymes(rhymeword,word_stresses[-1]))
        return words

    def couplet_stanza(self,ncouplets):
#         metre = ["0","[12]","0","[12]","0","[12]","0","[12]"]
        metre = ["0","[12]","0","[12]","0","[12]","0","[12]","0","[12]"] # iambic pentameter
        icouplet = 0
        while icouplet<ncouplets:
            try:
                first_line_words = self.meter_line(metre)
                first_line_lastword = first_line_words[-1]
                second_line_words = self.meter_line(metre,rhymeword = first_line_lastword)
                words_to_line(first_line_words)
                words_to_line(second_line_words)
                icouplet+=1
            except IndexError:
#                 print("failed attempt")
                pass # try again

    def generic_stanza(self,rhyme_lines_list,meters,meter_pattern):
        nlines = len(meter_pattern)
        stanza_complete = False
        while not stanza_complete:
            try:
                stanza = []
                rhyme_words = [None for x in rhyme_lines_list]
                for iline in range(nlines):
                    line_meter = meters[meter_pattern[iline]]
                    this_rhyme_index = None
                    for irhyme,rhyme_lines in enumerate(rhyme_lines_list):
                        if iline in rhyme_lines:
                            this_rhyme_index = irhyme
                    if this_rhyme_index is not None:
                        if rhyme_words[this_rhyme_index]:
                            line_words = self.meter_line(line_meter,rhymeword=rhyme_words[this_rhyme_index])
                        else:
                            line_words = self.meter_line(line_meter)
                            rhyme_words[this_rhyme_index] = line_words[-1]
                    else:
                        line_words = self.meter_line(line_meter)
                    stanza.append(line_words)
#                     words_to_line(line_words)
                stanza_complete = True
            except IndexError:
#                 print("failed attempt")
                pass # try again
        for line_words in stanza:
            words_to_line(line_words)
            


common3000 = commonword_manager("commonwords_3000.txt")

# for istanza in range(10):
#     common3000.couplet_stanza(6-abs(5-istanza))
#     print()

iambic_pentameter = ["0","[12]","0","[12]","0","[12]","0","[12]","0","[12]"]
iambic_tetrameter = ["0","[12]","0","[12]","0","[12]","0","[12]"]
iambic_trimeter = ["0","[12]","0","[12]","0","[12]"]
# mixitup_meter = ["0","[12]","0","[12]","0","[12]","0","0"]
mixitup_meter = ["0","[12]","0","[12]","0","0","[12]"]

# common3000.generic_stanza([[0,2,4],[1,3,5]],[iambic_pentameter,mixitup_meter],[0,1,0,1,0,1])


# ballad
print("BALLAD")
for istanza in range(6):
    common3000.generic_stanza([[0,2],[1,3]],[iambic_tetrameter,iambic_trimeter],[0,1,0,1])
    print()

# sonnet
print("SONNETS")
for istanza in range(4):
    common3000.generic_stanza([[0,2],[1,3],[4,6],[5,7],[8,10],[9,11],[12,13]],[iambic_pentameter],[0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    print()

# heroic verse
print("HEROIC VERSE")
for icouplets in range(20):
    common3000.generic_stanza([[0,1]],[iambic_pentameter],[0,0])


# for istanza in range(4):
#     common3000.generic_stanza([[0,2],[1,3],[4,5]],[iambic_pentameter,mixitup_meter],[0,0,0,0,1,1])
#     print()

sys.exit()

# def rhyming_stress_set(stress_pattern,n_syllables):
# 
# #     all_words_with_pattern = P.search_stresses(stress_pattern)
#     all_words_with_pattern = search_stress_syllables(stress_pattern,n_syllables)
# 
#     rhyme_box = [tuple(set(P.rhymes(x)).intersection(all_words_with_pattern)|{x}) for x in all_words_with_pattern]
#     rhyme_box = set(rhyme_box)
#     rhyme_box = [x for x in rhyme_box if len(x)>1]
# 
#     return rhyme_box
# 
# def filter_syllables(word_list,n_syllables):
#     return list(set(filter(lambda x:P.syllable_count(P.phones_for_word(x)[0])==n_syllables,word_list)) & set(commonwords))
# 
# def search_stress_syllables(stress_pattern,n_syllables):
#     return filter_syllables(P.search_stresses(stress_pattern),n_syllables)
# 
# def random_stress_syllables(stress_pattern,n_syllables):
#     return random.choice(search_stress_syllables(stress_pattern,n_syllables))
# 
# def search_rhymes_syllables(word,n_syllables):
#     return filter_syllables(P.rhymes(word),n_syllables)
# 
# def search_stress_rhymes_syllables(word,stress_pattern,n_syllables):
#     return list(set(search_rhymes_syllables(word,n_syllables)) & set(search_stress_syllables(stress_pattern,n_syllables)))
# 
# def random_stress_rhymes_syllables(word,stress_pattern,n_syllables):
#     return random.choice(search_stress_rhymes_syllables(word,stress_pattern,n_syllables))
# 
# def meter_line(stress_pattern_list,rhymeword=None):
#     nsyllables = len(stress_pattern_list)
#     nsyllables_so_far = 0
#     words_syllables = []
#     while nsyllables_so_far<nsyllables:
#         words_syllables.append(random.randint(1,3))
#         nsyllables_so_far+=words_syllables[-1]
#     if nsyllables_so_far>nsyllables:
#         words_syllables[-1]-=nsyllables_so_far-nsyllables
#     nwords = len(words_syllables)
#     word_syllable_indices = np.cumsum(words_syllables)[:-1]
#     word_syllable_indices=np.insert(word_syllable_indices,0,0)
#     word_stresses = ["".join(stress_pattern_list[word_syllable_indices[i]:word_syllable_indices[i]+words_syllables[i]]) for i in range(nwords)]
# #     print(word_stresses)
#     ngenerate = nwords-1 if rhymeword else nwords
#     words = [random_stress_syllables(word_stresses[i],words_syllables[i]) for i in range(ngenerate)]
#     if rhymeword:
#         words.append(random_stress_rhymes_syllables(rhymeword,word_stresses[-1],words_syllables[-1]))
# #     print(words)
#     return words
# #     outphrase = " ".join(words)
# #     return outphrase
# 
# # for i in range(6):
# #     print(meter_line(["[12]","0","0","[12]","0","0"]))
# 
# # print("setup")
# 
# 
# # last_iamb = None
# # last_iamb_rhymes = None
# 
# # print("generating")
# 
# 
# 
# # all_dactyls = search_stress_syllables("[12]00",3)
# # all_trochees = search_stress_syllables("[12]0",2)
# # all_rhyming_iambs = rhyming_stress_set("0[12]",2)
# # all_iambs = search_stress_syllables("0[12]",2)
# # 
# # def double_dactyl_two_rhyming_stanzas():
# #     print("---------------------------")
# #     iamb_rhymes = []
# #     while len(iamb_rhymes)<2:
# #         iamb_rhymes = random.choice(all_rhyming_iambs)
# # 
# #     iamb_rhymes = list(iamb_rhymes)
# #     random.shuffle(iamb_rhymes)
# #     iamb1 = iamb_rhymes[0]
# #     iamb2 = iamb_rhymes[1]
# # 
# #     for i in range(3):
# #         words_to_line([random.choice(all_dactyls),random.choice(all_dactyls)])
# # 
# #     words_to_line([random.choice(all_trochees),iamb1])
# #     print()
# # 
# #     for i in range(3):
# #         words_to_line([random.choice(all_dactyls),random.choice(all_dactyls)])
# # 
# #     words_to_line([random.choice(all_trochees),iamb2])
# 
# # for istanza in range(10):
# #     double_dactyl_two_rhyming_stanzas()
# 
# def couplet_stanza(ncouplets):
#     icouplet = 0
#     while icouplet<ncouplets:
#         try:
#             first_line_words = meter_line(["0","[12]","0","[12]","0","[12]","0","[12]"])
#             first_line_lastword = first_line_words[-1]
#             second_line_words = meter_line(["0","[12]","0","[12]","0","[12]","0","[12]"],rhymeword = first_line_lastword)
#             words_to_line(first_line_words)
#             words_to_line(second_line_words)
#             icouplet+=1
#         except IndexError:
# #             print("failed attempt")
#             pass # try again
# 
# for istanza in range(4):
#     couplet_stanza(3)
#     print()