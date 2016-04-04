from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from db_setup import Base, Catalog, Item, User

engine = create_engine('sqlite:///items_in_kyoto.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind = engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
user = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user)
session.commit()

# Catalog Sightseeing Spots and items
catalog = Catalog(user_id = 1, name = "Sightseeing Spots")
session.add(catalog)
session.commit()

item = Item( user_id = 1,	
	name = "Shouren-in's illuminations",
	description = "Shouren-in, in Higashiyama, is near the downtown areas of Kawaramachi and Gion, so it's recommended to drop by during sightseeing. On the temple grounds is a Japanese garden complete with a pond and a path around it. Every year from March to May and October to December only, the grounds are lit up beautifully in the evening.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/syoureninlightup.jpg", 
	homepage_url = "http://www.shorenin.com/english/index.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Nanzen Temple's Suirokaku Aqueduct",
	description = "Nanzen Temple is the head temple of the southern faction of the Rinzai school of Buddhism. With its large triple gate welcoming worshippers and its splendid temple building, it's one  of the many temples in Kyoto filled with modest charm. Its biggest charm is the Suirokaku Aqueduct that sits quietly in the Japanese landscape. It was built in 1888 to carry water from Lake Biwa, and the original brick arch still remains inside the temple. If you get a chance to walk around the area, it's recommended that you head there from Keage Station on the subway. Once you pass through the brick tunnel, Nanzen Temple will welcome you.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/nanzenji031.jpg", 
	homepage_url = "http://www.nanzen.net/english/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Honen-in",
	description = "Honen-in, in Shishigatani, is a hidden gem that is reminiscent of a secret hideout. Pass through the patched grass temple gate and enter the grounds that are surrounded by trees; you're taken into the stillness that separates you from the hustle and bustle of the main street.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/img2afad080zikfzj.jpeg", 
	homepage_url = "http://www.honen-in.jp/index.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Ishibei Alley",
	description = "Ishibe Alley is in is an area that conserves traditional architectural structures, and it's definitely one you should walk down when you come and go from Kodai Temple and the downtown areas. Among the scene of the houses' stone walls, are also many well-established restaurants and inns. These narrow streets of Kyoto definitely is a maze, but there are many attractive places to take photos.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/10photo06.jpg",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Shimogamo Shrine Tadasu no Mori",
	description = "On the grounds of the UNESCO World Heritage Site, Shimogamo Shrine, there is a large primeval forest, Tadasu no Mori. Inside of this forest, during autumn you can enjoy the leaves that turn bright red. It is also said to be a power spot and you can feel the sacred atmosphere. Shimogamo Shrine holds various events throughout the year, so it's recommended to check their web page if you want to visit.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/shimo16.jpg",
	homepage_url = "http://www.shimogamo-jinja.or.jp/english.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Fushimi Inari Shrine",
	description = "This is the head temple of the 30,000 Inari shrines that are all over Japan. Inari is the god of harvest and business. It is beloved by both local people and tourists. Since the entirety of Mt. Inari is part of the Shinto shrine precincts, there are torii gates all the way up to the summit. These gates are famous as a sightseeing spot. Also, since there is no entrance fee and no closing time, it's popular as a walking course around Mt. Inari.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/01/13968368327_02f5d954d8_b.jpg",
	homepage_url = "http://inari.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Jishu Shrine",
	description = "Jishu Shrine sits inside the grounds of Kiyomizudera, which is Kyoto's most famous spot for successful relationship. There is a legend that if you close your eyes and cross through the space between the two stones called the fortune-tellers, then your love will come true. There are love charms that come in a set for couples, love charms for single people who wish to get married and quite a few other kinds of charms and amulets.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/8271703939_3d885d34ff_k_d-1024x680.jpg",
	homepage_url = "http://www.jishujinja.or.jp/index.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Chikurin no Michi",
	description = "This road through a bamboo thicket connecting the great sights of Arashiyama is very popular among tourists. In the summer the tall bamboos absorb the heat, so you can enjoy the refreshing, pleasantly cool atmosphere. It feels like you've slipped back in time,as outside noise is completely blocked. The sunlight filtering through the trees and the rustling of the leaves will heal your travel exhaustion.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/a4599f0899bef46386f7e607731737e5_l.jpg",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Kuramadera Temple",
	description = "vThis spot is representative of Kurama, the area called \"Kyoto's inner parlor.\" Rare for a Kyoto shrine or temple, you can take a cable car from the temple gate to the grounds. This space has a feeling of holiness throughout it, possibly due to the legend that the Kurama kappa spirit lives here. On the grounds there is a paving stone which is considered a power spot. There are hot springs nearby where you can stop by on your way home.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/kuramaderanioumon.jpg",
	homepage_url = "http://kyoto.travel/en/shrine_temple/143",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Kifune Shrine",
	description = "This shrine is placed at the source of the Kamo River that runs through the center of Kyoto. The God protecting the water source is enshrined at this shrine. It's also famous for its God of marriage. Omikuji, paper fortunes, are drenched in water to forecast the future. Water fortunes are also popular. In the area, there are many restaurants and inns, so there are many travelers who repeatedly come to spend a while in Kifune.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/top4.jpg",
	homepage_url = "http://kifunejinja.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Gion Tatsumi Bridge",
	description = "Near the intersection between Shinbashi-dori and Shirakawa-minami-dori is a famous photo spot called \"the most picturesque place in Gion.\" The red-lacquered pillars and stone pavings next to the clear stream of the river creates a very Kyoto-like scenery with many people wearing a kimono. Especially in the spring, when the cherry blossoms bloom, it is a popular place to enjoy Kyoto's beauty.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/gionshirakawa4.jpg",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "District of preserved traditional buildings in Gion Shinbashi",
	description = "The Gion-Shinbashi district was developed as a tea house area in the Edo period. It suddenly appears in the downtown area and the district has a nostalgic atmosphere. Every tea house has its tatami tea rooms on the second floor, and if you walk here during the night you'll be able to hear singing and the sounds of shamisen. If you're lucky, you might encounter a maiko or a geiko (young geisha).",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/82339453.jpg",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Maruyama Park",
	description = "Maruyama Park is the oldest park in Kyoto, and spans 87,000 square meters and holds around 680 cherry blossom trees. In the center of the park is a huge weeping cherry blossom tree, so every year the park is crowded with people going for cherry blossom viewing. Many events such as college freshmen welcome parties are held there, so one of its charms is being able to experience Japan's party culture if you happen upon one of these events.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/9185609194_2307b21dad_k_d-1024x6801-1024x680.jpg",
	homepage_url = "http://kyoto.travel/en/thingstodo/entertainment/110",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Shokoku-ji Temple",
	description = "This is the head temple of the Japanese zen, Shokoku-ji sect temples. Since it's in a quiet residential area away from the downtown, you can take your time to visit. It's especially famous for the \"crying dragon\" that is on the ceiling of the temple's lecture hall. It is said that if you clap your hands directly below it, the echo sounds like the crying of a dragon.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/01_myoshinji.jpg",
	homepage_url = "http://www.shokoku-ji.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Kyoto University Clock Tower",
	description = "Kyoto University is a prestigious university in Japan. It's been a setting in manga and movies a lot lately, so the look of the campus itself has gained popularity as well. Among the popular spots is the clock tower, which was erected as the symbol of the university in 1925. In front of it is an ancient camphor tree, and most of the time there are college students freely spending their time around it. If you visit during the university festival held in November, you might find something interesting.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/014-1024x683.jpg",
	homepage_url = "http://www.kyoto-u.ac.jp/ja/clocktower",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Tetsugaku no Michi (\"Philosopher's Walk\")",
	description = "This is a walk that's about 2 km along a canal south of Ginkaku-ji. It was given this name because the philosopher Kitarou Nishida often strolled this path. In the spring it becomes a cherry blossom tunnel, in the summer it's full of fireflies, so it's full of seasonal enjoyments. The areas around it is dotted with cafes, so you can enjoy the scenery as well as a cup of coffee.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/075b0b7e61fa594dfbb334e0eeaa191a1-1024x768.jpg",
	homepage_url = "http://kyoto.travel/en/thingstodo/entertainment/111",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Toei Uzumasa Eigamura (Toei Kyoto Studio Park)",
	description = "This theme park is a place where you can experience the world of historical plays through events and attractions. The arched bridge and the tea house were actually used as a part of a set for a historical movie. You can also take a commemorative photo with that as the scenery. There are events that will make you feel like you've gone back in time, such as experiencing being a ninja and courses on sword fighting. This park is very popular among children.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/uzu11-1024x576.jpg",
	homepage_url = "http://www.toei-eigamura.com/en/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Fushimi Sake Distilleries",
	description = "Fushimi is an area blessed with underground water, and thanks to that water's quality, it's become famous for sake production. Famous sake makers like Gekkeikan and Kizakura Kappa Kantori have their distilleries here. It's an ideal spot for people who like sake to taste different types of sakes. It's recommended to visit in fall as they open up private cellars that people usually can't visit.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/50421fu3.jpg",
	homepage_url = "http://www.fushimi.or.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Fushimi Sake Distilleries",
	description = "Fushimi is an area blessed with underground water, and thanks to that water's quality, it's become famous for sake production. Famous sake makers like Gekkeikan and Kizakura Kappa Kantori have their distilleries here. It's an ideal spot for people who like sake to taste different types of sakes. It's recommended to visit in fall as they open up private cellars that people usually can't visit.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/50421fu3.jpg",
	homepage_url = "http://www.fushimi.or.jp/",
	catalog = catalog)
session.add(item)
session.commit()


# Catalog Food & Drink and items
catalog = Catalog(user_id = 1, name = "Food & Drink")
session.add(catalog)
session.commit()

item = Item( user_id = 1,	
	name = "Kyoto Sanjo Starbucks (Summer Only)",
	description = "When you're tired from shopping, you should stop by a Starbucks for a rest.  They have breeze-enjoying floor in summer time where you can enjoy the cool evenings; but in May and September, you can also enjoy in the daytime as well.  Enjoy coffee there while taking in the sight of the river!",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/cached.jpg", 
	homepage_url = "http://www.starbucks.co.jp/en/search/detail.php?id=68&search_condition=Kyoto&pref_code=26&pageID=2",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Chourakukan Cafe",
	description = "This cafe used to be a businessman's villa before it was remodeled. Since it was used as a reception hall by important people from both inside and outside the country, the beautiful fixtures such as chandeliers and stained glass windows have been kept. It's near Yasaka Shrine, so visit this cafe together and you can experience both the Japanese and the Western sides of Kyoto.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/pic_1_5_1.jpg", 
	homepage_url = "http://www.chourakukan.co.jp/cr/cafe.php",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Iyemon Salon",
	description = "This salon-cafe opened in 2008, in Karasumaoike with the concept that modern people should enjoy Japan's traditional tea culture in a fashionable way. In this modern-style building, you can enjoy a wide variety of menus, including dishes such as ochazuke (a rice dish with green tea poured over it) and desserts using tea. The seats from where you can see the garden are extremely popular.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/20120527-109.jpg", 
	homepage_url = "http://iyemonsalon.jp/concept/zoning.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "The Tea House at the summit of Mt. Yoshida",
	description = "The popular, gentle hiking course to the summit of Mt. Yoshida starts near Kyoto University. On the top of the mountain is a renovated tea house cafe named Moan. On certain days they hold tea ceremonies that don't require prior reservations to participate in. Enjoy the aroma of the freshly prepared tea.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/a0127090_22404546.jpg", 
	homepage_url = "http://www.mo-an.com/index.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Ponto-cho Robin",
	description = "Ponto-cho, in the middle of the geisha district, holds a distinct elegance where you can enjoy a refined dining experience. In Robin, a restaurant that is in a remodeled 150 year old home, you can dine out over the river during the summer. They offer delicate foods such as pike conger, blowfish and yuba, seasoned in a Kyoto style. During the high season the waiting time is especially long, so making a reservation prior to your visit is recommended.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/P019413361_480.jpg", 
	homepage_url = "http://www.robin-kyoto.com/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Demachi Futaba's Mame-mochi",
	description = "This Japanese confectionery shop, Futaba, in the northern part of Kyoto, has been featured on TV multiple times. This sweet is made of soft, stretchy mochi (rice cakes) kneaded with bean paste made of red peas. On weekends, be prepared to wait 20-30 minutes before being able to enter the shop. In the same shopping arcade, Demachi, there are various other traditional shops lined up, so it's worth taking a  stroll there.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/blog-futaba1.jpg", 
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Issen Yoshoku",
	description = "Issen Yoshoku is a \"one-coin\" (meaning 500 yen) okonomiyaki served at a candy store for children in the Taisho period (1912-1926). This restaurant serves an arranged version of issen yoshoku, now so popular that people line up for it. It is loved by gentlemen who love Gion and women who work there. The restaurant is decorated with all sorts of humorous goods, so eating at the restaurant is recommended.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/issen.jpg", 
	homepage_url = "http://www.issen-yosyoku.co.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Minokichi Honten Takeshigero",
	description = "Minokichi is a restaurant that is considered one part of the cornerstone of Kyoto's traditional food culture. It flourished in the Edo period as a restaurant specializing in freshwater fish cuisine, and was reborn into a residence prominent figure in Sukiya style, tea-ceremony arbor style. They added the name \"Takeshigero\" with the meaning \"we will continue to thrive like luxurious bamboo,\" and the sight of the bamboo surrounding the building is a highlight. It's often used as the venue for engagement parties, receptions, and other formal events.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/s_002r-1024x663.jpg", 
	homepage_url = "http://www.takeshigero.com/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Bozu Bar",
	description = "This bar opened in 2010, near the site of the Honno-ji Incident. The highlight of this bar is that the bartender is actually a chief priest with a quiet, gentle personality, and every day he gives a sermon at this bar. Many people go to speak with him about their problems. He'll also talk to you about Kyoto's traditions and Japanese culture. You can spend a luxurious time drinking the night away.",
	picture_url = "hhttps://www.tsunagujapan.com/wp-content/uploads/2015/02/DSC01723-1024x686.jpg", 
	homepage_url = "http://bozu-bar.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Mangetsu's Ajari-mochi",
	description = "This is a very popular traditional confectionery shop. They have a motto \"one type of red bean paste can only be used to make one kind of pastry\".  This mochi is made in the shape of the conical hats which the monks studying at Mt. Hiei wear. Its taste has not changed since the Taisho era (1912-1926), so it's beloved by both locals and tourists alike. You'll get addicted to the soft, sticky texture.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/4530-06.jpg", 
	homepage_url = "http://www.ajyarimochi.com/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Ramen from Ichijoji - Takayasu",
	description = "Because of the large number of students in Kyoto, it's a town that has an active ramen culture. Among them is Takayasu, a restaurant that has a large following due to its thick soup. It often has a very long queue. One of their side dishes, karaage chicken, is very popular because of its crunchiness. Why not try this side of Japanese culture next to students and businessmen?",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/130227-147.jpg", 
	homepage_url = "http://takayasuramen.com/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Eel and Rakugo at Kaneyo",
	description = "Kaneyo is a well-respected eel restaurant on Shinkyougoku-dori. It's unagi donburi (a dish made of eel resting on rice) is made by grilling the eel with their treasured sauce that has been passed down for 100 years. They also have an original dish called \"Kinshi-don,\" which is a dish with an egg on top of the eel. Once a month, they hold an event where you can enjoy rakugo (traditional comedic storytelling) as you eat your eel.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/%E4%B8%8A%E3%81%8D%E3%82%93%E3%81%97%E4%B8%BC-thumb-600x394-28.jpg", 
	homepage_url = "http://www.kyogokukaneyo.co.jp/info/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Japanese liquor bar Takahashi",
	description = "This bar is a popular spot among adults, not far from the business district. You can enjoy an assortment of Japanese liquors, judged as the best by the bar master. The handwritten menu gives the bar a chic atmosphere. Many people also go to eat the soba noodles that the owner makes from buckwheat flour. It's a great place for travelers to go due to its calm atmosphere and its reasonable price.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/36c8c9261c98e7c1b7d7d5e14410cdda-768x1024.jpg", 
	homepage_url = "http://tabelog.com/kyoto/A2601/A260201/26004934/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Cafe Style Resort Sagano-yu",
	description = "This cafe is a renovated bathhouse from the Taisho period. The bath tiles, mirrors, and shoe boxes were all left as they were, giving the place a nostalgic feel. The most popular items on the menu are the deluxe pancakes and the European-inspired curry. They also sell karinto (a type of fried dough snack) and original goods for souvenirs.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/0083-001.jpg", 
	homepage_url = "http://www.sagano-yu.com/",
	catalog = catalog)
session.add(item)
session.commit()

# Catalog Shopping and items
catalog = Catalog(user_id = 1, name = "Shopping")
session.add(catalog)
session.commit()

item = Item( user_id = 1,	
	name = "The scrubbing brushes of Naito Rikimatsu",
	description = "Located near the Sanjo Bridge, the Naito Rikimatsu store has no sign snugly fitting among the buildings. The shop specializes in daily necessities like scrubbing brushes and brooms made of hemp palm. When Terence Conran first saw these items and their high quality, he fell in love at first sight and added them to his stores in London.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/IMG_20130928_194957.jpg", 
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Mamemasa's Goshiki-mame",
	description = "Mamemasa was established in 1884, as a corn merchant and is now a Japanese confectionery store. Their cream Goshikimame is one of their best sellers. It's a soft treat made of peanuts covered in multicolored creams. Modernly arranged Japanese traditional confection is a very popular souvenir.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/f0229618_9562666.jpg", 
	homepage_url = "http://www.mamemasa.co.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Matsuhiro Shoten's clasp purses",
	description = "On offer at Matsuhiro are craftsman-made purses with metal clasps with Japanese patterns. Inside the shop are hundreds of purses that differ in both pattern and design, enough that you won't be able to easily choose one. The more you look at the clasp purses, the more you feel eager to use them, so many people buy a couple of purses in different patterns. The arabesque-patterned sign indicates the way to the store.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/15090912862_292592966d_k_d-1024x683.jpg", 
	homepage_url = "http://matsuhiroshoten.com/index.htm",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Nishiki Market",
	description = "Nishiki Market, also called \"Kyoto's kitchen\", lies beside the shopping district where young people gather. Along this 390 meter market are shops that have been decorating Kyoto's dining tables for the past 400 years. Kyoto vegetables and dried foods, pickles, sushi and other items are sold, and you can eat while you walk. Since it's a covered arcade, it's easy to shop there on rainy days too.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/P1030872-1024x768.jpg", 
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Kyukyodo's Incense Sticks",
	description = "This shop has been in Kyoto for 900 years and sells fragrances, art supplies and goods made of washi paper. Also, there are a wide variety of picture postcards and envelopes. Lately, aromatherapy candles and oils have been very popular along women. There are also many products made in collaboration with famous Kyoto brands. How about buying something as a souvenir for yourself?",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/img60987788-1024x768.jpg", 
	homepage_url = "http://www.kyukyodo.co.jp/index.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Ichizawa Shinzaburo Hanpu",
	description = "These are original canvas products that you can only buy at this store in the Higashiyama area of Kyoto. The bags sold here made by skilled craftsman, are extremely durable. They're also popular due to their cute designs, such as floral patterns or polka dots. Their standard items are bags that were originally designed for particular purposes, such as milk delivery or as liquor sacks.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/11578726375_c33809ab1f_k_d-1024x683.jpg", 
	homepage_url = "http://www.ichizawa.co.jp/en/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Nene no Michi Ten-Qoo-Ann's Business Card Fragrance",
	description = "Nene no Michi is a popular spot on an alleyway reminiscent of Kyoto. Ten-Qoo-Ann is a store that is almost hidden on the roadside there. They sell delicate, brilliant accessories such as faceted glass or tonbo glass beads. The recommended item is a scent for your business card case. Try out items that will make even your business hours Kyoto-like.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/PB242138-thumb-autox640-202.jpg", 
	homepage_url = "http://ten-qoo-ann.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,
	name = "Mamemo from Uragu Hacchi",
	description = "This variety shop opened in Higashiyama Yasaka in 2013. They sell small items that are made as a suitable gift for  friends and families. An \"umori\" is a unique card with an envelope shaped like an amulet from a shrine that you can write your message on. Other items are like this \"mamemo,\" a Japanese-style sticky note pad. You can spend hours in this adorable shop.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/551f8e11.jpg", 
	homepage_url = "http://www.uragu.com/infomation/",
	catalog = catalog)
session.add(item)
session.commit()

# Catalog Activity and items
catalog = Catalog(user_id = 1, name = "Activity")
session.add(catalog)
session.commit()

item = Item( user_id = 1,	
	name = "Akari Design Workshop",
	description = "Akari Design Workshop sells original light fixtures made from hand-made washi paper. They also make order-made items, so how does getting an original item for your home sound for you? They also have an area where you can experience making washi lights, so you can make your own lighting.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/prg_203002_point-1024x768.jpg", 
	homepage_url = "http://www.kyoto-akari.com/english",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Pottery-making at Kashogama",
	description = "Kashogama has created pottery bowls and tea instruments for four generations at Sannenzaka in Kiyomizu, Kyoto. You can experience making your original tea cup or tableware using a pottery wheel, in approximately 30 minutes . Since they only allow a few people at a time, the friendly instructors can help you personally, so you can make your work of art in peace.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/500_31448081.jpg", 
	homepage_url = "http://www.kashogama.com/school/index.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Yume Kobo's Oiran Experience",
	description = "\"Oiran\" were courtesans that entertained men in the red light district. Their beautiful outfits made them overflow with beauty and has become an aspiration for women nowadays. You can get dressed, have your hair and makeup done, and have a photography shoot for 5000 yen and up. ",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/o0753050012237944642.jpg", 
	homepage_url = "http://www.kyoto-oiran.com/index.html",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Otabe Dojo",
	description = "At the main store of the celebrated confectionery, Otabe, in the southern part of Kyoto, you can experience making sweets at their workshop. You can experience making nama-yatsuhashi, a type of sweet made with steamed ingredients wrapped in mochi and shaped into a triangle. You can also try many different flavors of yatsuhashi and look around the workshop. It's a perfect destination for a group tour.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/img_8.jpg", 
	homepage_url = "http://otabe.dt-r.com/",
	catalog = catalog)
session.add(item)
session.commit()

# Catalog Arts and items
catalog = Catalog(user_id = 1, name = "Arts")
session.add(catalog)
session.commit()

item = Item( user_id = 1,	
	name = "Kyoto International Manga Museum",
	description = "This museum was the first manga museum in Japan that opened in 2006 using an elementary school building that had closed down. The building retains a nostalgic atmosphere, reminiscent of the Showa period (1926-1989). There are around 50,000 volumes of manga available to read. There are also areas where popular animes of different eras are gathered, and it's indeed a treasure trove. On the days when the weather is nice, you can read out on the lawn.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/1200px-%E4%BA%AC%E9%83%BD%E5%9B%BD%E9%9A%9B%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%B8%E3%82%A2%E3%83%A0-1024x585.jpg", 
	homepage_url = "http://www.kyotomm.jp/english/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Kyoto Shijo Minami-za",
	description = "Minami-za is a theater that has been open since the Edo period (1603-1868), and the building retains the facade as it was. The building is actually registered as one of the country's tangible cultural properties. They hold a wide variety of events, from kabuki performances to concerts, so if there's anything on their schedule that you'd like to attend, you should make sure to get tickets beforehand.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/Kyoto_Minamiza_2010-7_hanamichi-1024x685.jpg", 
	homepage_url = "http://www.shochiku.co.jp/play/minamiza/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Ryozen Museum of History",
	description = "The Ryozen Museum of History is located in the Higashiyama area of Kyoto. A great number of materials about the end of the Tokugawa shogunate is on exhibition. You can experience a lot about beloved historical figures like Ryoma Sakamoto and the Shinsengumi. The area where you can see videos of the Bakumatsu in 3D is particularly popular. There are also places where you can see life-sized panels as well as touch their real battle weapons, so it's recommended as a family outing.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/JeIxou.jpeg", 
	homepage_url = "http://www.ryozen-museum.or.jp/",
	catalog = catalog)
session.add(item)
session.commit()

item = Item( user_id = 1,	
	name = "Gion Koubu Kabu Renjyo",
	description = "Located near Kennin Temple, this is a hall where geiko (young geisha) and maiko (apprentice geisha) have practices and  rehearsals. Every spring they hold a large performance called 'Miyako-odori,\" a dance performance that has been going on for 140 years. The gorgeous and luxurious stage art, expressing the landscapes of Kyoto is one of the highlights.",
	picture_url = "https://www.tsunagujapan.com/wp-content/uploads/2015/02/ecfc72c744f341c50e96528e45dd3fcb-1024x684.jpg", 
	homepage_url = "http://www.miyako-odori.jp/english/index.html",
	catalog = catalog)
session.add(item)
session.commit()

print "added items in Kyoto!"