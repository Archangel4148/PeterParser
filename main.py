import os

from pypdf import PdfReader

try:
    os.makedirs("pdf_songs")
except FileExistsError:
    pass

try:
    os.makedirs("txt_outputs")
except FileExistsError:
    pass

filenames = os.listdir("pdf_songs")

for file in filenames:
    # creating a pdf reader object
    reader = PdfReader(f"pdf_songs/{file}")

    # printing number of pages in pdf file
    sections = []
    for page in reader.pages:
        # extracting text from page
        text_lines = page.extract_text().splitlines()
        section_header_lines = []
        section_keywords = ["verse", "chorus", "intro", "bridge", "ending", "outro", "interlude", "prechorus",
                            "breakdown",
                            "©"]
        bad_words = ["<<><>DELETE_THIS_LINE<><>>", "Instrumental"]
        song_sections = {}

        for i, line in enumerate(text_lines):
            clear_line = True
            for j, character in enumerate(line):
                if character.isalpha():
                    clear_line = False
                if j > 0 and line[j-1].islower() and line[j].isupper():
                    extra_line = line[j:]
                    text_lines[i] = text_lines[i][:j]
                    text_lines.insert(i, extra_line)
            if clear_line:
                text_lines[i] = "<<><>DELETE_THIS_LINE<><>>"
                continue
            for word in section_keywords:
                if word in line.casefold().split()[0]:
                    section_header_lines.append(i)
                    sections.append(word)
                    text_lines[i] = " >>> " + text_lines[i]

        section_header_lines.append(len(text_lines))
        sections.append(None)
        verse_text = []

        for i, verse_index in enumerate(section_header_lines):
            if i == 0:
                continue
            current_verse = text_lines[section_header_lines[i - 1]:verse_index]

            for word in bad_words:
                try:
                    current_verse.remove(word)
                except ValueError:
                    pass

            if len(current_verse) > 1:
                verse_text.append(current_verse)

        clean_text = "\n\n-=-=-=-=-=-=-=-\n\n".join(["\n".join(i) for i in verse_text])

        # print(clean_text)

        with open(f"txt_outputs/{file.replace('.pdf', '') + '_(parsed).txt'}", "w") as f:
            f.write(clean_text)
