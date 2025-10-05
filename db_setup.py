import sqlite3
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('override.db')  # This creates the file if it doesn't exist
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS override_lyrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_lyrics TEXT NOT NULL,
    correct_title TEXT NOT NULL,
    correct_artist TEXT NOT NULL
)
''')

conn.commit()
conn.close()

# Function to insert song data into the database
def insert_song(full_lyrics, title, artist):
    conn = sqlite3.connect('override.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO override_lyrics (full_lyrics, correct_title, correct_artist)
    VALUES (?, ?, ?)
    ''', (full_lyrics.strip(), title.strip(), artist.strip()))
    conn.commit()
    conn.close()

# Insert the lyrics data
insert_song(
    "Ngiboleken', ngibolekeni (Eh Ngibolekeni)",
    "Ngibolekeni",
    "DJ Maphorisa, XDuppy, Sean1401 ft. Leemckrazy, Scotts Maphuma, Blxckie, Pcee, Kabelo Sings"
)
insert_song(
    "Bo gogo ba re ke ngwana wa bone",
    "Bo Gogo",
    "Kelvin Momo & Da Muziqal Chef ft. Tracy, Thatohatsi"
)
insert_song(
    """They say you know when you know
    So, let's face it, you had me at Hello
    Hesitation never helps
    How could this be anything, anything else?
    When all I dream of is your eyes
    All I long for is your touch
    And, darling, something tells me that's enough, mm-mm-mm-mm
    You can say that I'm a fool
    And I don't know very much
    But I think they call this love
    One smile, one kiss, two lonely hearts is all that it takes
    Now, baby, you're on my mind every night, every day
    Good vibrations getting loud
    How could this be anything, anything else?
    When all I dream of is your eyes
    All I long for is your touch
    And, darling, something tells me that's enough, mm-mm-mm-mm
    You can say that I'm a fool
    And I don't know very much
    But I think they call this love
    Oh, I think they call this love
    Hmm, ooh-ooh, mm
    Mm
    What could this be
    Between you and me? Oh, oh
    All I dream of is your eyes
    All I long for is your touch
    And, darling, something tells me, tells me it's enough
    You can say that I'm a fool
    And I don't know very much
    But I think they call—
    Oh, I think they call—
    Yes, I think they call
    This love
    This love""",
    "I think they call this love",
    "Elliot James Raey"
)
print("Database created: override.db and lyrics table initialized.")