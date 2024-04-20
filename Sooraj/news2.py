from newsapi import NewsApiClient
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from heapq import nlargest

# Initialize NLTK
import nltk

# Initialize News API client
newsapi = NewsApiClient(api_key='a89fbfe1bfca4f899f939e0d257e6efd')

# Fetch news articles
articles='''The Adani Renewable Energy Park in northern India is unique for several reasons. First, it is a hybrid clean energy project that will harvest electricity from both solar panels and wind turbines. Second, it will be the largest such facility in the world when complete. Third, it will have a nameplate capacity of 30 GW — the Three Gorges Dam in China produces a mere 22.5 GW. Fourth, it is being built in a salt desert near the border with Pakistan where there is not a living soul for more than 20 miles in any direction — so there is no NIMBY backlash to worry about.
The hybrid wind and solar project is being constructed by Adani Green Energy, a division of Adani Group. The company explains the advantage of combining solar and wind power this way.
 “Variability in Solar and Wind generation has emerged as a concern in large-scale adoption of renewables, especially after it contributes a major share in the energy mix. Hybridization of a wind and solar plant is developing a solution which will reduce this variability due to complementary nature of their generation profile – solar generation is higher during the day, while wind generation can be higher in the night. Hybrid projects would have much higher capacity utilization, thus removing the intermittency challenge. Such projects also enjoy the additional benefit of a reduction in costs associated with sharing transmission lines.”
 The solar panels in the Adani hybrid wind and solar park are expected to generate 26 GW of electricity, while the wind turbines will contribute another 4 GW of power.
 At the present time, 70% of all the electricity in India comes from thermal generating stations that burn either coal or methane gas. That’s why India is the third largest emitter of carbon dioxide pollution in the world today, behind only China and the United States. But the country plans on having 500 GW of clean power available by 2030. Germany, by comparison, is targeting 330 GW of renewable energy by then.
 Hybrid Solar & Wind Park Is Seven Times Larger Than Paris When completed, the Adani hybrid solar and wind project will be about as large as Singapore, spreading out over 726 square kilometers (280 square miles). Up to eight thousand workers and 500 engineers will be needed to construct the new clean energy park. Today most of them are living in makeshift camps while construction is under way.
 “There are people working here from all over India,” said KSRK Verma, the project head for Adani Green Energy, which has contracted with the Indian government to build 20 GW of the project. Verma, with over 35 years of experience building dams across turbulent South Asian rivers and natural gas tanks under the Bay of Bengal, told the Associated Press this is one of the most difficult projects he has been in charge of.
 “It’s not at all (an) easy site to work at. There is no habitation, the land is marshy, there are a lot of high winds, rains and this is a high earthquake prone area,” said Vneet Jaain, managing director of Adani Green. He has overseen multiple ambitious projects for the Adani Group and said the first six months were spent just building basic infrastructure. “April is when we started working on the actual project,” he added.
 The industrial city of Mundra is about 200 kilometers away from where the hybrid solar and wind park is being built. That is where the Adani Group is manufacturing the solar and wind energy components needed for the project. Today, factories there can build 4 gigawatts of solar modules and 1.5 gigawatts of wind turbines per year. The solar factory is expected to grow into one of the world’s largest manufacturing centers for solar energy, with the ability to make 10 gigawatts of polysilicon, ingots, wafers, cells, and modules a year. The wind turbine plant will be expanded to produce 300 turbines a year. Each blade for those turbines will be nearly 79 meters (256 feet) long and weigh 22 metric tons (24 tons). Each one will be capable of producing 5.2 megawatts of electricity.
 India Avoids Environmental Reviews While acknowledging the importance of transitioning to renewable energy, environmental experts and social activists say India’s decision to allow several clean energy projects without any environmental impact assessments is bound to have adverse consequences. “The salt desert is a unique landscape” that is “rich in flora and fauna,” including flamingos, desert foxes, and migratory bird species that fly from Europe and Africa to winter in this region, according to Abi T Vanak, a conservation scientist with the Bengaluru-based Ashoka Trust for Research in Ecology and the Environment. Vanak has overseen multiple environment-related research projects in the Kutch region.
 Kutch and other similar regions are classified as “wastelands” by the Indian government, which Vanak said is extremely unfortunate. “They are not recognized as valid ecosystems,” he said. With renewable energy projects exempt from environmental impact assessments, “There is no system in place” to determine the best places for them, according to Sandip Virmani, an environmentalist based in Kutch.
 At a little over 45,000 square kilometers (17,374.5 square miles), the Kutch district is as big as Denmark and is India’s largest district. Virmani said there is enough land in Kutch for various renewable energy projects, but he fears that dairies and other local businesses in the region might be impacted by large scale renewable energy projects. “It has to be in the context of not compromising on another economy,” he said.
 Chip in a few dollars a month to help support independent cleantech coverage that helps to accelerate the cleantech revolution!
 Renewables & Green Hydrogen Indian companies also have big plans for making green hydrogen. At the port of Kandla in the state of Gujarat, four companies led by the Reliance Industries group are planning various production plants for green hydrogen and ammonia, with planned investments of around $12 billion.
 One of the hydrogen pioneers is the construction and mechanical engineering company Larsen + Toubro, which secured licenses for the electrolyzer technology from the French manufacturer McPhy last year. The company is now setting up electrolyzer production in a factory in the city of Hazira and has secured government subsidies. The first one megawatt electrolyzer was completed there at the beginning of March.    
 Green hydrogen is still more expensive than hydrogen made from methane gas, but India hopes to be able to significantly reduce costs thanks to cheap solar power from the Adami hybrid solar and wind project in the salt desert of Gunjarat where the average solar radiation is almost twice as high as it is in Germany'''
# articles = newsapi.get_everything(q='technology',
#                                       from_param='2024-04-17',
#                                       to='2024-04-18',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page_size=20,
#                                       page=2)
# Extract and preprocess text from articles
# print(articles)
# articles_text = [article['content'] for article in articles['articles'] if article['content']]

preprocessed_text = []

# for article_text in articles_text:
    # Tokenize sentences
sentences = sent_tokenize(articles)

# Tokenize words, remove stopwords, and stem words
stop_words = set(stopwords.words("english"))
ps = PorterStemmer()
word_frequencies = {}
for sentence in sentences:
    words = word_tokenize(sentence.lower())
    words = [ps.stem(word) for word in words if word.isalnum()]
    for word in words:
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

# Calculate weighted frequencies
maximum_frequency = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word] / maximum_frequency

# Calculate sentence scores based on word frequencies
sentence_scores = {}
for sentence in sentences:
    for word in word_tokenize(sentence.lower()):
        if word in word_frequencies.keys():
            if len(sentence.split(' ')) < 30:
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

# Select top N sentences for summary
summary_sentences = nlargest(3, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)
preprocessed_text.append(summary)

print(preprocessed_text)
# Display summaries
# for i, summary in enumerate(preprocessed_text):
#     print(f"Summary for article {i + 1}:")
#     print(summary)
#     print()

