from AttributesClassifier import AttributesClassifier

classifier = AttributesClassifier()
result = classifier.transform_dict_from_url(url="https://www.avia.ch/tankstellenfinder/jsonpassthru.php")
print(result)