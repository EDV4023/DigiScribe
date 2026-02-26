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


# ========== Similarity for World History Example 2 (Resistance Movements - My Handwriting) 
# original = """Ghost Dance
# Because culturally like americans, Indian removal act to OK b/c gold found, resistance in Ghost Dance: it was said that ancestors
# would come back
# Xhosa Cattle Killing Movement
# fought w/ brits. lots of Xhosa Cattle dying they thought it was Eur. Disease so they killed all cows hoping spirits would drive brits away
# didn't happen
# Tupac Amoru II Rebellion
# Angry of Spanish Colonizers
# Samory Toure's military Battles
# Empire in W Africa against french but unsuccesful
# Mahidist Wars
# Sudan revolt
# Believed in prophecy ancestral dead with come back + fight the Americans so ghost dance was supposed to bring the dead faster
# Armed rebellion, arrested officer, Peru, Amaru was executed
# fought for 40 yrs, died of famine from cow killing
# Violent Conflicts
# Gathered an army in 1880 and actually won against Brit.
# """.replace("\n"," ")

# new_extracted = """• Ghost Dance
# Becanve culturally like mmeraans, Indian removal act to OK be gold found, resistance in Ghost Dance: It was said that ancestors would love tort
# • Xhosa Cattle Killing Movement fught w/ brits, lots of those catthe dying they thought it was Eur. Disence So they killed all coves hoping spirits would dove brits away. didn't happen
# • Tupac Amaru II Rebellion • Angry of Spanish Colonters 4 Samory Toure's Military Battles • Empire in Afrin agrimst french but unsuccesful S. Mahidist Waß •Sudan revolt
# Belived in popphary. araestioal dead will come buck't Fight the tothelan Anglicans to bring the dead faster So ghost dance was supposed
# Armed rebellion, arrested officer, Peru, Aman was
# fought for 40 yrs, died of tumive from cow Killing
# • Viglent Violent Conflicts
# Gathered an army in 1880 and actually war""".replace("\n", " ")

# new_refined = """• Ghost Dance
# Became culturally like Americans. Indian Removal Act to Oklahoma, gold found, resistance in Ghost Dance: It was said that ancestors would return.
# • Xhosa Cattle Killing Movement Fought with Brits, lots of those cattle dying. They thought it was European disease, so they killed all cows hoping spirits would drive Brits away. Didn't happen.

# • Tupac Amaru II Rebellion • Angry at Spanish Colonists.

# Samory Toure's Military Battles • Empire in Africa against French, but unsuccessful.

# Mahdist War • Sudan revolt.

# Believed in prophecy, ancestral dead will come back. Fight the totalitarian Anglicans to bring the dead faster. So Ghost Dance was supposed to.

# Armed rebellion, arrested officer, Peru, Aman was.

# Fought for 40 years, died of tumult from cow killing.

# Violent Conflicts.

# Gathered an army in 1880 and actually warred.
# """.replace("\n", " ")

# print_similarity(original, new_extracted, new_refined)

# Levenshtein Distance: 0.8403670758535148
# Cosine Similarity: 0.7212676605697046





# ========== Similarity for Birthday Card Example 1 (Resistance Movements - My Handwriting) 
# original = """God bless you Emily This day is happy and good. 
# Virtues, riches best - all yours Much more to come all your ways. So dear and precious Your pranks we love to see. 
# Your nearness in days to come Energizes us, bred travellers. My precious, my dear darling! On our knees we pray 
# Methuselah and Dand's son The two rolled in one Music perfect is happy to hear. To hear our darling's prattle 
# Is happier still With Love and Kisses on your Birthday !! long live Emily
# """.replace("\n"," ")

# new_extracted = """God bless you Emily This day is happy and good Virtues, richess best - all yours. 
# Much more to come all your ways. So. dear and precious Your pranks we love to see 
# Your neamess im days to come Energizes aus, bred travellers. 
# My precious, my dear darbing! 6n our knees the pray Methuselah and Dand 's som The tus solled in one Music 
# perfect is happy to hear To hear our darling is prattle is happier still. 
# Tlike MY With Love and kisses on your Birthday!! Long live Emily""".replace("\n", " ")

# new_refined = """God bless you, Emily. This day is happy and good. Virtues, riches, best of all, 
# are yours. Much more to come all your ways. So dear and precious, Your pranks we love to see. 
# Your nearness in days to come Energizes us, bred travelers. My precious, my dear darling! 
# On our knees, we pray. Methuselah and Dand's son? The tus solled in one? Music perfect is happy to hear. 
# To hear our darling prattle Is happier still. Like My With love and kisses On your Birthday!! 
# Long live, Emily!
# """.replace("\n", " ")

# print_similarity(original, new_extracted, new_refined)

# Levenshtein Distance: 0.8486524446465337
# Cosine Similarity: 0.8771929824561403









# ============================ SIMILARITY SCORE SUMMARY: ===================================

# AP Calculus Notes (1):
# Levenshtein Distance: 0.845819930607015
# Cosine Similarity: 0.8620689655172413


# AP Calculus Notes (2):
# Levenshtein Distance: 0.8660383592923155
# Cosine Similarity: 0.8207826816681233


# AP World History (1):
# Levenshtein Distance: 0.8569512394296602
# Cosine Similarity: 0.9166666666666666


# My Handwriting AP World History:
# Levenshtein Distance: 0.8403670758535148
# Cosine Similarity: 0.7212676605697046


# Grandfather's Handwritten Birthday Card:
# Levenshtein Distance: 0.8486524446465337
# Cosine Similarity: 0.8771929824561403


# =============================== VISUALIZATION =====================================

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

labels = ["AP Calculus Notes (1)", "AP Calculus Notes (2)", "AP World History Notes", "My Handwritten Notes", "Grandfather's Birthday Card"]
levenshtein_scores = [0.845819930607015, 0.8660383592923155, 0.8569512394296602, 0.8403670758535148, 0.8486524446465337]
cosine_similarity_scores = [0.8620689655172413, 0.8207826816681233, 0.9166666666666666, 0.7212676605697046, 0.8771929824561403]

avg_lev = sum(levenshtein_scores) / len(levenshtein_scores)
avg_cos = sum(cosine_similarity_scores) / len(cosine_similarity_scores)

df = pd.DataFrame({
    "Handwritten Example": labels * 2,
    "Score": levenshtein_scores + cosine_similarity_scores,
    "Metric": ["Levenshtein"] * len(labels) + ["Cosine Similarity"] * len(labels)
})

plt.grid(True)

sns.set_theme(
    style="white",
    rc={"axes.facecolor": "#F2F6FA",
        "figure.facecolor": "#F2F6FA"}
)

palette = sns.light_palette("#A7D8F0", n_colors=2)

sns.barplot(
    data=df,
    x="Handwritten Example",
    y="Score",
    hue="Metric",
    palette=palette
)

plt.axhline(avg_lev, linestyle="--", linewidth=2, label="Average Levenshtein")
plt.axhline(avg_cos, linestyle=":", linewidth=2, label="Average Cosine")

# Add text slightly above each line
plt.text(
    x=0.0001, 
    y=avg_lev + 0.04, 
    s=f"Average Levenshtein: {avg_lev:.3f}",
    ha="left"
)

plt.text(
    x=len(labels)-0.5, 
    y=avg_cos + 0.04, 
    s=f"Average Cosine: {avg_cos:.3f}",
    ha="right"
)

plt.legend()

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()