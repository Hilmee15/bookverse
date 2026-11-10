"""Seed dataset: 55 books & novels (international + Indonesian).

All data is dummy/public bibliographic data used for educational purposes.
Descriptions are written with overlapping keywords (magic, war, murder, love,
space, school, colonial, ...) so the TF-IDF recommender produces sensible
similar-book matches.
"""

BOOKS = [
    # ---------- Fantasy ----------
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937, "rating": 4.7,
     "description": "A hobbit named Bilbo joins a company of dwarves and a wizard on a quest to reclaim a mountain kingdom from a dragon, discovering a magic ring and courage along the adventure."},
    {"title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1954, "rating": 4.8,
     "description": "The first volume of the epic of Middle-earth: a hobbit, a wizard, elves, dwarves and men form a fellowship to destroy a dark magic ring before the dark lord conquers the world."},
    {"title": "A Game of Thrones", "author": "George R.R. Martin", "genre": "Fantasy", "year": 1996, "rating": 4.4,
     "description": "Noble families wage a bloody war for the Iron Throne while an ancient threat stirs beyond the Wall; political intrigue, dragons, winter and betrayal in a medieval fantasy world."},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "Fantasy", "year": 1997, "rating": 4.7,
     "description": "An orphan boy discovers he is a wizard and attends a magic school of Hogwarts, where he learns spells, makes loyal friends and faces a dark wizard who killed his parents."},
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "genre": "Fantasy", "year": 2007, "rating": 4.5,
     "description": "The memoir of Kvothe, a gifted orphan who survives tragedy to enter a famous magic university and grows into a legendary magician, musician and arcanist."},
    {"title": "Mistborn: The Final Empire", "author": "Brandon Sanderson", "genre": "Fantasy", "year": 2006, "rating": 4.6,
     "description": "In a world ruled by an immortal tyrant, a street urchin joins a crew of thieves to overthrow the empire using an ingenious magic system of burning metals."},
    {"title": "Bumi", "author": "Tere Liye", "genre": "Fantasy", "year": 2015, "rating": 4.3,
     "description": "Seorang remaja bernama Raib menemukan dunia paralel penuh sihir dan makhluk ajaib, lalu belajar di akademi khusus sambil menyembunyikan identitas aslinya dari teman-temannya."},

    # ---------- Sci-Fi ----------
    {"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "year": 1965, "rating": 4.5,
     "description": "On a desert planet that produces the most valuable spice in the galaxy, a young noble heir leads desert tribes in a war of prophecy, politics and giant sandworms."},
    {"title": "Foundation", "author": "Isaac Asimov", "genre": "Sci-Fi", "year": 1951, "rating": 4.4,
     "description": "A mathematician predicts the fall of a galactic empire and builds an institution to shorten the coming dark age; a classic of science, politics and civilization on a galactic scale."},
    {"title": "Ender's Game", "author": "Orson Scott Card", "genre": "Sci-Fi", "year": 1985, "rating": 4.4,
     "description": "Gifted children are trained in an orbital battle school through war games to command humanity's fleet against an alien insectoid invasion."},
    {"title": "The Martian", "author": "Andy Weir", "genre": "Sci-Fi", "year": 2011, "rating": 4.4,
     "description": "An astronaut stranded alone on Mars after a dust storm must use engineering, botany and humor to survive and signal Earth for a desperate rescue mission."},
    {"title": "Project Hail Mary", "author": "Andy Weir", "genre": "Sci-Fi", "year": 2021, "rating": 4.5,
     "description": "A lone scientist wakes on a spaceship with amnesia and must save Earth from an extinction-level microbe using science, first contact with an alien and relentless problem solving."},
    {"title": "Neuromancer", "author": "William Gibson", "genre": "Sci-Fi", "year": 1984, "rating": 4.0,
     "description": "A washed-up hacker is hired for one last job: to break through cyberspace and artificial intelligence defenses in a neon dystopia of corporations and data."},

    # ---------- Mystery ----------
    {"title": "The Da Vinci Code", "author": "Dan Brown", "genre": "Mystery", "year": 2003, "rating": 3.9,
     "description": "A symbologist and a cryptologist follow clues hidden in famous paintings and cathedrals to solve a murder and uncover a secret guarded for centuries."},
    {"title": "Gone Girl", "author": "Gillian Flynn", "genre": "Mystery", "year": 2012, "rating": 4.1,
     "description": "A wife disappears on her anniversary and her husband becomes the prime suspect; a twisted psychological thriller of marriage, lies and media manipulation."},
    {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "genre": "Mystery", "year": 2005, "rating": 4.1,
     "description": "A disgraced journalist and a genius hacker investigate the decades-old disappearance of a heiress inside a wealthy, violent family dynasty."},
    {"title": "And Then There Were None", "author": "Agatha Christie", "genre": "Mystery", "year": 1939, "rating": 4.3,
     "description": "Ten strangers are lured to an isolated island and killed one by one as an unseen murderer punishes hidden crimes; the definitive closed-circle whodunit."},
    {"title": "A Study in Scarlet", "author": "Arthur Conan Doyle", "genre": "Mystery", "year": 1887, "rating": 4.2,
     "description": "The first case of detective Sherlock Holmes and Dr. Watson: a murder in London traced by pure deduction to a revenge story born in the American desert."},
    {"title": "The Silent Patient", "author": "Alex Michaelides", "genre": "Mystery", "year": 2019, "rating": 4.0,
     "description": "A psychotherapist obsesses over a famous painter who shot her husband and never spoke again; a psychological thriller of trauma and an unreliable mind."},

    # ---------- Dystopia ----------
    {"title": "1984", "author": "George Orwell", "genre": "Dystopia", "year": 1949, "rating": 4.6,
     "description": "Under a totalitarian regime of surveillance and propaganda, a civil servant dares to keep a diary and love a woman while Big Brother watches everyone."},
    {"title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopia", "year": 1932, "rating": 4.2,
     "description": "A genetically engineered society buys happiness with drugs and entertainment until an outsider questions the cost of a perfectly controlled civilization."},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "genre": "Dystopia", "year": 1953, "rating": 4.2,
     "description": "In a future where books are banned and burned, a fireman who destroys forbidden literature begins to read and rebel against the censorship state."},
    {"title": "The Hunger Games", "author": "Suzanne Collins", "genre": "Dystopia", "year": 2008, "rating": 4.3,
     "description": "A brave girl volunteers for a televised fight-to-the-death between children of oppressed districts, becoming a symbol of rebellion against the Capitol."},
    {"title": "Hujan", "author": "Tere Liye", "genre": "Dystopia", "year": 2016, "rating": 4.3,
     "description": "Di tahun 2050, seorang gadis berbakat dan pemuda pembunuh profesional menghadapi dunia rusak akibat perang, bencana, dan teknologi yang mengubah nasib manusia."},

    # ---------- Classic ----------
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Classic", "year": 1813, "rating": 4.4,
     "description": "The witty Elizabeth Bennet clashes with the proud Mr. Darcy in a comedy of manners about love, class, marriage and first impressions in rural England."},
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "genre": "Classic", "year": 1847, "rating": 4.3,
     "description": "An orphan governess with an independent spirit survives hardship and falls in love with a brooding master hiding a dark secret in his mansion."},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic", "year": 1960, "rating": 4.5,
     "description": "Seen through a child's eyes, a principled lawyer defends a Black man falsely accused in the racist American South, teaching his children about justice and empathy."},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "year": 1925, "rating": 3.9,
     "description": "A mysterious millionaire throws lavish parties to win back a lost love, exposing the hollowness of wealth and obsession in the Jazz Age of New York."},

    # ---------- Historical ----------
    {"title": "The Kite Runner", "author": "Khaled Hosseini", "genre": "Historical", "year": 2003, "rating": 4.3,
     "description": "A boy from Kabul betrays his loyal friend and spends adulthood seeking redemption across war-torn Afghanistan and America; friendship, guilt and fatherhood."},
    {"title": "All the Light We Cannot See", "author": "Anthony Doerr", "genre": "Historical", "year": 2014, "rating": 4.3,
     "description": "A blind French girl and a German boy soldier cross paths in occupied France during World War II, where radio waves, a diamond and quiet kindness decide fates."},
    {"title": "The Book Thief", "author": "Markus Zusak", "genre": "Historical", "year": 2005, "rating": 4.5,
     "description": "Narrated by Death, a foster girl in Nazi Germany steals forbidden books and shares them while bombs fall, in a story of words, courage and found family."},
    {"title": "Schindler's Ark", "author": "Thomas Keneally", "genre": "Historical", "year": 1982, "rating": 4.2,
     "description": "The true story of an industrialist and member of the Nazi party who spent his fortune saving more than a thousand Jewish workers from the Holocaust."},
    {"title": "Bumi Manusia", "author": "Pramoedya Ananta Toer", "genre": "Historical", "year": 1980, "rating": 4.6,
     "description": "Minke, pemuda pribumi terdidik di masa kolonial Belanda, bergulat dengan diskriminasi, cinta terlarang, dan kebangkitan kesadaran nasional di awal abad ke-20."},
    {"title": "Cantik Itu Luka", "author": "Eka Kurniawan", "genre": "Historical", "year": 2002, "rating": 4.2,
     "description": "Kisah keluarga Dewi Ayu dan kecantikan yang jadi kutukan melintasi pendudukan Jepang, masa kolonial, dan kekacauan politik pasca-kemerdekaan di sebuah kota kecil Halimunda."},

    # ---------- Romance ----------
    {"title": "Norwegian Wood", "author": "Haruki Murakami", "genre": "Romance", "year": 1987, "rating": 4.1,
     "description": "A quiet student in 1960s Tokyo is torn between two women while grief, mental illness and growing up pull them apart; a melancholy story of young love and loss."},
    {"title": "The Fault in Our Stars", "author": "John Green", "genre": "Romance", "year": 2012, "rating": 4.2,
     "description": "Two sharp-witted teenagers meet in a cancer support group and fall in love, confronting mortality, humor and the pain of an unfinished story."},
    {"title": "Me Before You", "author": "Jojo Moyes", "genre": "Romance", "year": 2012, "rating": 4.2,
     "description": "A cheerful small-town girl becomes caretaker for a wealthy man paralyzed after an accident, and their unlikely bond changes both lives forever."},
    {"title": "Perahu Kertas", "author": "Dee Lestari", "genre": "Romance", "year": 2003, "rating": 4.2,
     "description": "Kugy dan Keenan, dua anak muda yang saling mengagumi dari jauh, mengejar mimpi, cinta, dan takdir yang terasa seperti perahu kertas di lautan luas."},
    {"title": "Ayat-Ayat Cinta", "author": "Habiburrahman El Shirazy", "genre": "Romance", "year": 2004, "rating": 4.1,
     "description": "Fahri, mahasiswa Indonesia di Kairo Mesir, menghadapi ujian cinta, keyakinan, dan tanggung jawab bersama empat perempuan dengan latar islami yang kuat."},

    # ---------- Horror ----------
    {"title": "It", "author": "Stephen King", "genre": "Horror", "year": 1986, "rating": 4.2,
     "description": "Seven friends return to their hometown to fight a shape-shifting evil clown that feeds on children and fear, resurfacing every twenty-seven years in the sewers of Derry."},
    {"title": "The Shining", "author": "Stephen King", "genre": "Horror", "year": 1977, "rating": 4.2,
     "description": "A winter caretaker brings his wife and psychic son to an isolated haunted hotel, where madness, ghosts and the boy's shining gift collide in blood."},
    {"title": "Dracula", "author": "Bram Stoker", "genre": "Horror", "year": 1897, "rating": 4.0,
     "description": "Count Dracula moves from Transylvania to England spreading vampirism, hunted through diary entries and letters by Van Helsing and his brave companions."},
    {"title": "Frankenstein", "author": "Mary Shelley", "genre": "Horror", "year": 1818, "rating": 4.0,
     "description": "A scientist assembles a creature from dead bodies and abandons it; the monster's loneliness turns to revenge in the founding classic of science gone wrong."},

    # ---------- Fiction ----------
    {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "Fiction", "year": 1988, "rating": 4.0,
     "description": "A shepherd boy travels from Spain to the Egyptian desert chasing a recurring dream about treasure, learning to read omens and follow his Personal Legend."},
    {"title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "genre": "Fiction", "year": 1943, "rating": 4.3,
     "description": "A pilot stranded in the Sahara meets a prince from a tiny asteroid; a gentle fable about friendship, love, loss and what is essential being invisible to the eye."},
    {"title": "Laskar Pelangi", "author": "Andrea Hirata", "genre": "Fiction", "year": 2005, "rating": 4.5,
     "description": "Sepuluh anak Belitung berjuang mengejang pendidikan di sekolah muallimat yang nyaris roboh, dengan guru hebat, persahabatan, mimpi, dan keajaiban kehidupan."},
    {"title": "Ronggeng Dukuh Paruk", "author": "Ahmad Tohari", "genre": "Fiction", "year": 1982, "rating": 4.4,
     "description": "Srintil, penari ronggeng cantik dari kampung miskin, menjadi korban politik 1965; kisah seni tradisi, cinta, dan pengkhianatan di tengah tragedi sejarah."},
    {"title": "Supernova: Ksatria, Puteri, dan Bintang Jatuh", "author": "Dee Lestari", "genre": "Fiction", "year": 2001, "rating": 4.4,
     "description": "Dua ilmuwan muda meneliti cinta dan kesadaran lewat kisah rekan, ferre, dan supernova; perpaduan filsafat, sains, dan metafora indah tentang jatuh cinta."},
    {"title": "Filosofi Kopi", "author": "Dee Lestari", "genre": "Fiction", "year": 2006, "rating": 4.2,
     "description": "Kumpulan kisah Jodoh dan Ben tentang kopi, mimpi, dan cita rasa kehidupan, dari menyeduh espresso sampai memahami manusia lewat secangkir kopi."},
    {"title": "Pulang", "author": "Tere Liye", "genre": "Fiction", "year": 2015, "rating": 4.2,
     "description": "Bujang, gadis pemberani dari Sumatra, berkelana mencari makna rumah dan pulang, berjumpa guru-guru kehidupan yang mengajar tentang kehilangan dan kasih."},
    {"title": "Orang-Orang Bloomington", "author": "Budi Darma", "genre": "Fiction", "year": 1980, "rating": 4.3,
     "description": "Kumpulan cerita ganjil dan gelap tentang kesepian manusia di Bloomington, Amerika; mahakarya cerpen psikologis yang mencekam dan puitis."},

    # ---------- Self-Help / Nonfiction ----------
    {"title": "Atomic Habits", "author": "James Clear", "genre": "Self-Help", "year": 2018, "rating": 4.4,
     "description": "A practical system for building good habits and breaking bad ones through tiny changes, identity, environment design and the compound effect of 1% daily improvement."},
    {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "genre": "Nonfiction", "year": 2011, "rating": 4.1,
     "description": "A Nobel laureate explains the two systems that drive thinking: fast intuition and slow reason, and the biases that quietly shape every decision humans make."},
    {"title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "genre": "Nonfiction", "year": 2011, "rating": 4.4,
     "description": "A sweeping history of humanity from foraging bands to capitalism and artificial intelligence, explaining how shared myths like money, religion and empires built our world."},
    {"title": "Educated", "author": "Tara Westover", "genre": "Nonfiction", "year": 2018, "rating": 4.3,
     "description": "A memoir of a woman raised by survivalist parents who never set foot in a classroom until seventeen, who then earns a PhD and must choose between family and herself."},
]
