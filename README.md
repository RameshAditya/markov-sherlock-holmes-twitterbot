# Markov Models and Word Prediction

#### This is a markov model implemented manually that probabilistically predicts the consequent word by using historically validated data, and leveraging nested dictionaries.
--------------------------------------------------------------------

NOTE: Works well for generating small sentences (albeit sometimes meaningless), and not so well for paragraphs or pages. Best when trained over a huge corpus.

* Good news is, it's never grammatically wrong, as expected from every other *proper* markov model. 

* Bad news is, it usually loses overall context after every sentence (or full stop) and sometimes mid-sentence too, due to the massive volume of the training set.

This implementation parses through a Sherlock Holmes book, and predicts words. Twitter APIs were also used (Tweepy) but the project is not live since it tweets from my main account and another account requires another phone number.
