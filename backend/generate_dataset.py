import random
import csv

positive_templates = [
    "Driver was very polite and helpful 😊",
    "Smooth ride, felt safe the whole time",
    "Reached on time, great experience!",
    "Driver was super friendly and chill 😎",
    "Car was clean and smelled nice",
    "Loved the ride, 5 stars ⭐⭐⭐⭐⭐",
    "Professional and respectful driver",
    "Great driving skills fr",
    "Very calm and responsible driving",
    "Awesomeeee ride bro 💯",
    "Driver handled traffic like a pro",
    "Such a nice experience ngl",
    "Totally satisfied with this trip",
    "Felt secure entire journey",
    "Top class service 👌",
    "Driver was early, nice!",
    "Super smooth braking and acceleration",
    "Honestly one of the best rides",
    "Driver was patient and cooperative",
    "Amazing trip overall ✨"
]

neutral_templates = [
    "Ride was okay nothing special",
    "Driver came on time",
    "Trip was fine",
    "Average experience overall",
    "It was normal",
    "Driver was quiet but okay",
    "Reached safely",
    "Nothing unusual during trip",
    "It was just fine",
    "Decent ride",
    "Car condition was normal",
    "Driver did his job",
    "Trip was alright 👍",
    "No issues faced",
    "Ride went as expected",
    "Everything was standard",
    "Driver was okayish",
    "Trip completed successfully",
    "It was manageable",
    "Not bad not great"
]

negative_templates = [
    "Driver was rude and arrogant 😡",
    "Reached very late",
    "Driving was rash and unsafe",
    "Driver kept using phone while driving",
    "Car was dirty and smelly 🤢",
    "Very unprofessional behavior",
    "Terrible experience overall",
    "Driver argued unnecessarily",
    "Felt unsafe entire trip",
    "He drove too fast!! 😤",
    "Worst ride ever",
    "Driver was shouting on call",
    "Braking was harsh and scary",
    "AC not working and driver ignored it",
    "Very bad service",
    "Driver didnt follow GPS properly",
    "Super disappointed with this ride",
    "He was careless and distracted",
    "Driver cancelled last min 😑",
    "Completely unsatisfactory trip"
]

sarcasm_phrases = [
    "Yeah right, amazing service 🙃",
    "Wow what a 'great' driver 😒",
    "Sure felt super safe lol",
    "Best ride ever... not.",
    "Totally professional huh 🙄"
]

slang_words = ["tbh", "ngl", "fr", "bro", "lowkey", "idk"]

def add_noise(text):
    if random.random() < 0.3:
        text += " " + random.choice(slang_words)
    if random.random() < 0.2:
        text = text.replace("very", "verrry")
    if random.random() < 0.2:
        text = text.replace("driver", "drivr")
    return text

rows = []

for _ in range(110):
    text = add_noise(random.choice(positive_templates))
    rows.append([text, "positive"])

for _ in range(10):
    text = random.choice(sarcasm_phrases)
    rows.append([text, "negative"])

for _ in range(120):
    text = add_noise(random.choice(neutral_templates))
    rows.append([text, "neutral"])

for _ in range(120):
    text = add_noise(random.choice(negative_templates))
    rows.append([text, "negative"])

random.shuffle(rows)

with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(rows)

print("Dataset generated with", len(rows), "rows.")