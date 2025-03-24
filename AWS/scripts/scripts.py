import os
import re
import socket

def get_ip_address():
    # Tries to figure out the container's IP address using the hostname
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Unknown IP"

def tokenize(text, handle_contractions=False):
    # This function breaks a string into words/tokens.
    # If handle_contractions is True, we'll expand common English contractions like "can't" -> "can not".
    
    # If we're dealing with contractions, let's replace them with their expanded forms first.
    if handle_contractions:
        contractions_dict = {
            "I'm": "I am",
            "i'm": "i am",
            "can't": "can not",
            "won't": "will not",
            "n't": " not",  
            "'re": " are",
            "'ll": " will",
            "'ve": " have",
            "'m": " am",
            "'d": " would",
        }

        # Replace each known contraction with its expanded version
        for contraction, expansion in contractions_dict.items():
            text = text.replace(contraction, expansion)

    # Now split the text on anything that's not a letter or a digit
    tokens = re.split(r'[^a-zA-Z0-9]+', text)
    
    # Filter out empty entries and convert everything to lowercase
    tokens = [t.lower() for t in tokens if t.strip() != ""]
    return tokens

def count_words_and_top3(filepath, handle_contractions=False):
    # Opens a file, tokenizes its content, and returns:
    #   1) the total word count
    #   2) a dictionary with the top 3 most frequent words (word -> frequency)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Tokenize the text, optionally handling contractions
    tokens = tokenize(text, handle_contractions=handle_contractions)
    total_words = len(tokens)

    # Let's count how often each word shows up
    frequency = {}
    for word in tokens:
        frequency[word] = frequency.get(word, 0) + 1

    # Sort words by their frequency in descending order
    sorted_words = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    
    # Extract just the top 3 words and their counts
    top_3 = sorted_words[:3]
    
    # Convert the top 3 list of tuples into a nice dictionary: { word: count, ... }
    top_3_dict = {word: count for word, count in top_3}
    return total_words, top_3_dict

def main():
    # Paths inside the container
    if1_path = "/home/data/IF-1.txt"
    always_path = "/home/data/AlwaysRememberUsThisWay-1.txt"
    output_path = "/home/data/output/result.txt"

    # First, let's do IF-1.txt without handling contractions
    if1_word_count, if1_top3 = count_words_and_top3(if1_path, handle_contractions=False)

    # Next, AlwaysRememberUsThisWay-1.txt with contraction handling
    always_word_count, always_top3 = count_words_and_top3(always_path, handle_contractions=True)

    # Compute the total word count across both files
    grand_total = if1_word_count + always_word_count

    # Grab the IP address of this container (for the assignment requirement)
    ip_address = get_ip_address()

    # We’ll assemble the output lines in a list, then join them together
    results = []
    results.append(f"Total words in IF-1.txt: {if1_word_count}")
    results.append(f"Top 3 frequent words in IF-1.txt: {if1_top3}")
    results.append("")
    results.append(f"Total words in AlwaysRememberUsThisWay-1.txt: {always_word_count}")
    results.append(f"Top 3 frequent words in AlwaysRememberUsThisWay-1.txt (with contractions handled): {always_top3}")
    results.append("")
    results.append(f"Grand total of words across both files: {grand_total}")
    results.append(f"Container IP address: {ip_address}")

    # Turn the list into a single string
    output_text = "\n".join(results)

    # Ensure the output folder exists (/home/data/output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the result to result.txt
    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.write(output_text)

    # Also print everything to the console so we can see it right away
    print(output_text)

if __name__ == "__main__":
    main()
