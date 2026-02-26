from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Levenshtein

# import nltk

# nltk.download('stopwords')


def cosine_similarity(x: str, y: str) -> float:
    x_list = word_tokenize(x) 
    y_list = word_tokenize(y)

    sw = stopwords.words('english') 
    l1 =[];l2 =[]

    x_set = {w for w in x_list if not w in sw} 
    y_set = {w for w in y_list if not w in sw}

    rvector = x_set.union(y_set) 
    for w in rvector:
        if w in x_set: l1.append(1)
        else: l1.append(0)
        if w in y_set: l2.append(1)
        else: l2.append(0)
    c = 0

    # cosine similarity formula 
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine

def print_similarity(original: str, new_extracted: str, new_refined: str):
    print(f"Levenshtein Distance: {max(Levenshtein.jaro(original, new_extracted),Levenshtein.jaro(original, new_refined))}")
    print(f"Cosine Similarity: {max(cosine_similarity(original, new_extracted),cosine_similarity(original, new_refined))}")
 
###########################################################################################################

# ========== Similarity for AP Calculus Example 1 (Intermediate Value Theorem):
#  
# original = """Intermediate Value Thm: If f is continous on [a,b] and k is btw f(a) and f(b) inclusive,
# then there is at least one number x in [a,b] such that f(x) = k
# if f is continous on [a,b] and f(a) and f(b) are non-zero w/ opposite signs then thee's at least one soln to f(x) = 0 on (a,b)""".replace("\n"," ")

# new_extracted = """Intermediate Value Thm: If f is continuous on [a,b] and k is btw f(a) and f(b) inclusive, 
# then there's at least one number x in [a,b] such that f(x)=k if f is continuous on [a,b] and f(a) and f(b) 
# are core non-zero w/ opposite signs, then there's at least soln to f(x)=0 on (a,b)""".replace("\n", " ")

# new_refined = """Intermediate Value Theorem: If f is continuous on [a,b] and k is between f(a) and f(b) inclusive, 
# then there's at least one number x in [a,b] such that f(x)=k. 
# If f is continuous on [a,b] and f(a) and f(b) are (of) non-zero with opposite signs, 
# then there's at least (one) solution to f(x)=0 on (a,b).""".replace("\n", " ")

# # print_similarity(original, new_extracted, new_refined)

# # Levenshtein Distance: 0.845819930607015
# # Cosine Similarity: 0.8620689655172413



###########################################################################################################


# ========== Similarity for AP Calculus Example 2 (Continous):
#  
# original = """• If 2 functions are continuous at x=c, then their sum, difference, product, and quotient
#  will always be continuous at x=c • A rational function is continuous at all values where the 
#  denominator ≠ 0""".replace("\n"," ")

# new_extracted = """• If 2 functions are continuous at x= c, then their sum, difference, product, and 
# quotient will always be continuous at x=c • A rational function is continuous at all valves where the denominator 
# ≠0""".replace("\n", " ")

# new_refined = """• If two functions are continuous at x = c, then their sum, difference, product, and quotient 
# will always be continuous at x = c. • A rational function is continuous at all values 
# where the denominator ≠ 0.""".replace("\n", " ")

# # print_similarity(original, new_extracted, new_refined)

# # Levenshtein Distance: 0.8660383592923155
# # Cosine Similarity: 0.8207826816681233


##############################################################################################################


# ========== Similarity for World History Example 1 (Caste System):
#  
# original = """How did India's caste system differ from China's class system?
# Caste system: limited to 0 social mobility governed by religion
# Class: allowed for social mobility power via Civil Service System
# Slavery vs Caste
# • Basically Secular • Based on ritual purity
# no pre-requisites • limited social mobility
# a chance for freedom • had individual rights, even sudras
# could be bought/sold (untouchables exp. social death)
# social death""".replace("\n"," ")

# new_extracted = """How did India's caste system differ from China's class system?

# Caste system: limited to O social mobility governed by religion

# Class: allowed for social mobility power via Civil Service System

# Slavery vs Caste

# • basically secular • based on ritual purity no pre-requisites • limited social mobility a chance for freedom
# • had individual rights, even sudras could be bought/sold (untouchables exp. social death) social death""".replace("\n", " ")

# new_refined = """How did India's caste system differ from China's class system?

# Caste system: limited to no social mobility, governed by religion.

# Class: allowed for social mobility, power via Civil Service System.

# Slavery vs. Caste:

# Basically secular.
# Based on ritual purity.
# No pre-requisites.
# Limited social mobility.
# A chance for freedom.
# Had individual rights, even (sudras).
# Could be bought/sold (untouchables experience social death).
# Social death.
# """.replace("\n", " ")

# print_similarity(original, new_extracted, new_refined)

# Levenshtein Distance: 0.8569512394296602
# Cosine Similarity: 0.9166666666666666


###########################################################################################################


# ========== Similarity for World History Example 2 (Caste System - My Handwriting) 
original = """How did India's caste system differ from China's class system?
Caste system: limited to 0 social mobility governed by religion
Class: allowed for social mobility power via Civil Service System
Slavery vs Caste
• Basically Secular • Based on ritual purity
no pre-requisites • limited social mobility
a chance for freedom • had individual rights, even sudras
could be bought/sold (untouchables exp. social death)
social death""".replace("\n"," ")

new_extracted = """How did India's caste system differ from China's class system?

Caste system: limited to O social mobility governed by religion

Class: allowed for social mobility power via Civil Service System

Slavery vs Caste

• basically secular • based on ritual purity no pre-requisites • limited social mobility a chance for freedom
• had individual rights, even sudras could be bought/sold (untouchables exp. social death) social death""".replace("\n", " ")

new_refined = """How did India's caste system differ from China's class system?

Caste system: limited to no social mobility, governed by religion.

Class: allowed for social mobility, power via Civil Service System.

Slavery vs. Caste:

Basically secular.
Based on ritual purity.
No pre-requisites.
Limited social mobility.
A chance for freedom.
Had individual rights, even (sudras).
Could be bought/sold (untouchables experience social death).
Social death.
""".replace("\n", " ")

print_similarity(original, new_extracted, new_refined)


