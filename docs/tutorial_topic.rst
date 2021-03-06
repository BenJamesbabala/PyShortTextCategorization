Supervised Classification with Topics as Features
=================================================

Topic Vectors as Intermediate Feature Vectors
---------------------------------------------

To perform classification using bag-of-words (BOW) model as features,
`nltk` and `gensim` offered good framework. But the feature vectors
of short text represented by BOW can be very sparse. And the relationships
between words with similar meanings are ignored as well. One of the way to
tackle this is to use topic modeling, i.e. representing the words
in a topic vector. This package provides the following ways to model
the topics:

- LDA (Latent Dirichlet Allocation)
- LSI (Latent Semantic Indexing)
- Random Projections
- Autoencoder

With the topic representations, users can use any supervised learning
algorithm provided by `scikit-learn` to perform the classification.

Topic Models in `gensim`: LDA, LSI, and Random Projections
----------------------------------------------------------

This package supports three algorithms provided by `gensim`, namely, LDA, LSI, and
Random Projections, to do the topic modeling.

>>> import shorttext
>>> import shorttext.classifiers.topic.LatentTopicModeling as ltm

First, load a set of training data (all NIH data in this example):

>>> trainclassdict = shorttext.data.nihreports(sample_size=None)

Initialize an instance of topic modeler, and use LDA as an example:

>>> topicmodeler = ltm.GensimTopicModeler(algorithm='lda')

For the algorithms, user can use `lsi` and `rp` in addition to `lda` in the example.
To train with 128 topics, enter:

>>> topicmodeler.train(trainclassdict, 128)

After the training is done, the user can retrieve the topic vector representation
with the trained model. For example,

>>> topicmodeler.retrieve_topicvec('stem cell research')

>>> topicmodeler.retrieve_topicvec('bioinformatics')

By default, the vectors are normalized. Another way to retrieve the topic vector
representation is as follow:

>>> topicmodeler['stem cell research']

>>> topicmodeler['bioinformatics']

In the training and the retrieval above, the same preprocessing process is applied.
Users can provide their own preprocessor while initiating the topic modeler.

Users can save the trained models, by calling:

>>> topicmodeler.savemodel('/path/to/nihlda128')

The following files for the topic model are produced:

::

    /path/to/nihlda128.json
    /path/to/nihlda128.gensimdict
    /path/to/nihlda128.gensimmodel.state
    /path/to/nihlda128.gensimtfidf
    /path/to/nihlda128.gensimmodel
    /path/to/nihlda128.gensimmat

All of them have to be present in order to be loaded. Note that the preprocessor is
not saved. To load the model, enter:

>>> topicmodeler2 = ltm.load_gensimtopicmodel('/path/to/nihlda128')

While initialize the instance of the topic modeler, the user can also specify
whether to weigh the terms using tf-idf (term frequency - inverse document frequency).
The default is to weigh. To not weigh, initialize it as

>>> topicmodeler3 = ltm.GensimTopicModeler(toweight=False)

AutoEncoder
-----------

Another way to find a new topic vector representation is to use the autoencoder, a neural network model
which compresses a vector representation into another one of a shorter (or longer, rarely though)
representation, by minimizing the difference between the input layer and the decoding layer.
For faster demonstration, use the subject keywords as the example dataset:

>>> subdict = shorttext.data.subjectkeywords()

To train such a model, we perform in a similar way with the LDA model (or LSI and random projections above):

>>> autoencoder = ltm.AutoencodingTopicModeler()
>>> autoencoder.train(subdict, 8)

After the training is done, the user can retrieve the encoded vector representation
with the trained autoencoder model. For example,

>>> autoencoder.retrieve_topicvec('linear algebra')

>>> autoencoder.retrieve_topicvec('path integral')

By default, the vectors are normalized. Another way to retrieve the topic vector
representation is as follow:

>>> autoencoder['linear algebra']

>>> autoencoder['path integral']

In the training and the retrieval above, the same preprocessing process is applied.
Users can provide their own preprocessor while initiating the topic modeler.

Users can save the trained models, by calling:

>>> autoencoder.savemodel('/path/to/sub_autoencoder8')

The following files are produced for the autoencoder:

::

    /path/to/sub_autoencoder.gensimdict
    /path/to/sub_autoencoder_encoder.json
    /path/to/sub_autoencoder_encoder.h5
    /path/to/sub_autoencoder_classtopicvecs.pkl

If specifying `save_complete_autoencoder=True`, then four more files are found:

::

    /path/to/sub_autoencoder_decoder.json
    /path/to/sub_autoencoder_decoder.h5
    /path/to/sub_autoencoder_autoencoder.json
    /path/to/sub_autoencoder_autoencoder.h5

Users can load the same model later by entering:

>>> autoencoder2 = ltm.load_autoencoder_topic('/path/to/sub_autoencoder8')

Like other topic models, while initialize the instance of the topic modeler, the user can also specify
whether to weigh the terms using tf-idf (term frequency - inverse document frequency).
The default is to weigh. To not weigh, initialize it as:

>>> autoencoder3 = ltm.AutoencodingTopicModeler(toweight=False)

Abstract Latent Topic Modeling Class
------------------------------------

Both :class:`shorttext.classifiers.bow.topic.LatentTopicModeling.GensimTopicModeler` and
:class:`shorttext.classifiers.bow.topic.LatentTopicModeling.AutoencodingTopicModeler` extends
:class:`shorttext.classifiers.bow.topic.LatentTopicModeling.LatentTopicModeler`,
an abstract class virtually. If user wants to develop its own topic model that extends
this, he has to define the methods `train`, `retrieve_topic_vec`, `loadmodel`, and
`savemodel`.

Classification Using Cosine Similarity
--------------------------------------

The topic modelers are trained to represent the short text in terms of a topic vector,
effectively the feature vector. However, to perform supervised classification, there
needs a classification algorithm. The first one is to calculate the cosine similarities
between topic vectors of the given short text with those of the texts in all class labels.

If there is already a trained topic modeler, whether it is
:class:`shorttext.classifiers.bow.topic.LatentTopicModeling.GensimTopicModeler` or
:class:`shorttext.classifiers.bow.topic.LatentTopicModeling.AutoencodingTopicModeler`,
a classifier based on cosine similarities can be initiated
immediately without training. Taking the LDA example above, such classifier can be initiated as follow:

>>> from shorttext.classifiers.topic.TopicVectorDistanceClassification import TopicVecCosineDistanceClassifier
>>> cos_classifier = TopicVecCosineDistanceClassifier(topicmodeler)

Or if the user already saved the topic modeler, one can initiate the same classifier by
loading the topic modeler:

>>> from shorttext.classifiers.topic.TopicVectorDistanceClassification import load_gensimtopicvec_cosineClassifier
>>> cos_classifier = load_gensimtopicvec_cosineClassifier('/path/to/nihlda128')

To perform prediction, enter:

>>> cos_classifier.score('stem cell research')

which outputs a dictionary with labels and the corresponding scores.

The same thing for autoencoder, but the classifier based on autoencoder can be loaded by another function:

>>> from shorttext.classifiers.topic.TopicVectorDistanceClassification import load_autoencoder_cosineClassifier
>>> cos_classifier = load_autoencoder_cosineClassifier('/path/to/sub_autoencoder8')

Classification Using Scikit-Learn Classifiers
---------------------------------------------

The topic modeler can be used to generate features used for other machine learning
algorithms. We can take any supervised learning algorithms in `scikit-learn` here.
We use Gaussian naive Bayes as an example. For faster demonstration, use the subject
keywords as the example dataset.

>>> subtopicmodeler = ltm.GensimTopicModeler()
>>> subtopicmodeler.train(subdict, 8)

We first import the class:

>>> from sklearn.naive_bayes import GaussianNB

And we train the classifier:

>>> from shorttext.classifiers.topic.SkLearnClassification import TopicVectorSkLearnClassifier
>>> classifier = TopicVectorSkLearnClassifier(subtopicmodeler, GaussianNB())
>>> classifier.train(subdict)

Predictions can be performed like the following example:

>>> classifier.score('functional integral')

which outputs a dictionary with labels and the corresponding scores.

You can save the model by:

>>> classifier.savemodel('/path/to/sublda8nb')

where the argument specifies the prefix of the path of the model files, including the topic
models, and the scikit-learn model files. The classifier can be loaded by calling:

>>> classifier2 = shorttext.classifiers.topic.SkLearnClassification.load_gensim_topicvec_sklearnclassifier('/path/to/sublda8nb')

The topic modeler here can also be an autoencoder, by putting `subtopicmodeler` as the autoencoder
will still do the work. However, to load the saved classifier with an autoencoder model, do

>>> classifier2 = shorttext.classifiers.topic.SkLearnClassification.load_autoencoder_topic_sklearnclassifier('/path/to/someprefix')

Notes about Text Preprocessing
------------------------------

The topic models are based on bag-of-words model, and text preprocessing is very important.
However, the text preprocessing step cannot be serialized. The users should keep track of the
text preprocessing step on their own. Unless it is necessary, use the standard preprocessing.

See more: :doc:`tutorial_textpreprocessing` .

Reference
---------

David M. Blei, "Probabilistic Topic Models," *Communications of the ACM* 55(4): 77-84 (2012).

Francois Chollet, "Building Autoencoders in Keras," *The Keras Blog*. [`Keras
<https://blog.keras.io/building-autoencoders-in-keras.html>`_]

Xuan Hieu Phan, Cam-Tu Nguyen, Dieu-Thu Le, Minh Le Nguyen, Susumu Horiguchi, Quang-Thuy Ha,
"A Hidden Topic-Based Framework toward Building Applications with Short Web Documents,"
*IEEE Trans. Knowl. Data Eng.* 23(7): 961-976 (2011).

Xuan Hieu Phan, Le-Minh Nguyen, Susumu Horiguchi, "Learning to Classify Short and Sparse Text & Web withHidden Topics from Large-scale Data Collections,"
WWW '08 Proceedings of the 17th international conference on World Wide Web. (2008) [`ACL
<http://dl.acm.org/citation.cfm?id=1367510>`_]

Home: :doc:`index`