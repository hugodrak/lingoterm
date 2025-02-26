import time
import random
import json
import os
import click
from termcolor import colored

# File to store progress
PROGRESS_FILE = "progress.json"

class FrenchTrainer:
    def __init__(self, dataset_file, mode):
        self.dataset_file = dataset_file
        self.mode = mode
        self.words = self.load_words()
        self.progress = self.load_progress()

    def load_words(self):
        words = []
        with open(self.dataset_file, "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                parts = line.split("\t")
                if len(parts) == 2:
                    words.append({"fr": parts[0], "en": parts[1]})
        random.shuffle(words)
        return words

    def load_progress(self):
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_progress(self):
        with open(PROGRESS_FILE, "w") as f:
            json.dump(self.progress, f)

    def get_unlearned_word(self):
        for _ in self.words:
            i = random.randint(0, len(self.words) - 1)
            word = self.words[i]
        
            key = word["fr"]
            if key not in self.progress or self.progress[key] < 3:
                return word
        return None

    def ask_question(self, word):
        fr, en = word["fr"], word["en"]
        correct_answer = en if self.mode == "fr2en" else fr
        prompt = fr if self.mode == "fr2en" else en

        print(colored(f"Translate: {prompt}", "cyan"))
        user_input = input("=> ").strip()
        return user_input.lower() == correct_answer.lower(), correct_answer

    def run(self):
        while True:
            word = self.get_unlearned_word()
            if not word:
                print(colored("🎉 You have mastered all words! 🎉", "green"))
                break
            correct, correct_answer = self.ask_question(word)
            fr_word = word["fr"]
            if correct:
                print(colored(f"✅ Correct! ({correct_answer})\n", "green"))
                self.progress[fr_word] = self.progress.get(fr_word, 0) + 1
            else:
                print(colored(f"❌ Incorrect! Correct answer: {correct_answer}\n", "red"))
                self.progress[fr_word] = max(0, self.progress.get(fr_word, 0) - 1)
                #time.sleep(random.uniform(1, 3))  # Random delay before repeating
            self.save_progress()

@click.command()
@click.option("--dataset", default="french_words.tsv", help="Path to the TSV dataset.")
@click.option("--mode", default="fr2en", type=click.Choice(["fr2en", "en2fr"]), help="Mode: French to English or English to French.")
def start_trainer(dataset, mode):
    trainer = FrenchTrainer(dataset, mode)
    trainer.run()

if __name__ == "__main__":
    start_trainer()
