# Name_similarity_check
Needed to check the similarity of names between two csv files, one with an older format and another with a new format for the new system, to determine if they were typos or different people entirely.

Found out about the jaro-winkler distance algorithm and implemented it python. Through trial and error, discovered that around 0.85 is when you can differentiate between typos and different people with similar names.
