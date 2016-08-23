# German IPA Transcriber
##[Django Web App Demo](https://kdelaney.pythonanywhere.com/german/)

For the most part, German is a phonetic language, which follows a number of pronunciation rules ranging in complexity and scope. Using the International Phonetic Alphabet, or IPA, these rules can be codified and expressed algorithmically, as this program does.


Additionally, the transcriber provides IPA transcriptions from Wiktionary using the [Java Wiktionary API](https://dkpro.github.io/dkpro-jwktl/). Since German diction does have a number of exceptions, especially in the case of foreign words, this allows for a more accurate and useful program.


## Getting Started

```
>>> python germanipa.py

Enter a German text below.
Then type "/" and hit enter.

>>> Du bist die Ruh,
>>> Der Friede mild,
>>> /

 Du bist die  Ruh,
ˈdu bɪst diː ˈɾuː 
 
 Der   Friede mild,
ˈdeːɾ ˈfɾiːdə mɪlt 

Enter a German text below.
Then type "/" and hit enter.

>>> /

Process finished with exit code 0

```

## Prerequisities
* Python 2.7.11

## Credits
* [DKpro JWKTL](https://dkpro.github.io/dkpro-jwktl/)
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
