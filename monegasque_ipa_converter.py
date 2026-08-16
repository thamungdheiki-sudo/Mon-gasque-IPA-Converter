import re

def split_into_syllables(text):

    vowel_pattern = r'([aeiouüàéèìòù🚘]+|iau|iau̯)'
    
    # Clean string punctuation for calculation
    clean_word = re.sub(r'[^\w\s]', '', text.lower())
    
    # Find all vowel clusters
    syllables = re.findall(vowel_pattern, clean_word)
    return len(syllables)

def monegasque_to_ipa_advanced(word):
    word_clean = word.lower().strip()
    
    
    # 2. Count Syllables
    num_syllables = split_into_syllables(word_clean)
    
    # 3. Detect Explicit Accent Marks
    # If the word already contains a written accent, we track its position
    has_explicit_accent = any(char in "àéèìòù" for char in word_clean)
    
    # 4. Standard Contextual Changes (from our previous basic engine)
    text = re.sub(r'ch', 'k', word_clean)
    text = re.sub(r'gh', 'ɡ', text)
    text = re.sub(r'c(?=[ei])', 'tʃ', text)
    text = re.sub(r'g(?=[ei])', 'dʒ', text)
    text = re.sub(r's(?=[tcpie])', 'ʃ', text)
    text = re.sub(r'([aeiouü])s([aeiouü])', r'\1z\2', text)
    
    # 5. Handle Single Character Mapping
    mapping = {'ç': 's', 'j': 'ʒ', 'r': 'ʁ', 'ü': 'y', 'c': 'k', 'g': 'ɡ',
               'à': 'a', 'é': 'e', 'è': 'ɛ', 'ì': 'i', 'ò': 'ɔ', 'ù': 'u'}
    
    ipa_chars = [mapping.get(char, char) for char in text]
    ipa_processed = "".join(ipa_chars)
    
    # 6. Apply Stress Placement Rules
    if num_syllables <= 1:
        # One-syllable words do not get a stress mark
        return f"[{ipa_processed}]"
        
    elif has_explicit_accent:
        for i, char in enumerate(word_clean):
            if char in "àéèìòù":
                # Find corresponding index in the modified IPA string
                # (Simple fallback approach: split before the vowel character)
                vowel_ipa = mapping[char]
                parts = ipa_processed.split(vowel_ipa, 1)
                return f"[{parts[0]}ˈ{vowel_ipa}{parts[1]}]"
                
    else:
        # Penultimate Rule: Stress the second-to-last syllable
        # We find the second-to-last vowel cluster using Regex
        vowel_indices = [m.start() for m in re.finditer(r'[aeiouü]', ipa_processed)]
        if len(vowel_indices) >= 2:
            stress_pos = vowel_indices[-2] # Target the penultimate vowel
            # Insert stress mark right before the vowel (or preceding consonant cluster)
            # For simplicity, we inject right before the vowel index
            return f"[{ipa_processed[:stress_pos]}ˈ{ipa_processed[stress_pos:]}]"

    return f"[{ipa_processed}]"

print(monegasque_to_ipa_advanced("Ciau"))
