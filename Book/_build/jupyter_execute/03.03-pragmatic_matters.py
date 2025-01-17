#!/usr/bin/env python
# coding: utf-8

# (datawrangling)=
# 
# # Data Wrangling

# >*The garden of life never seems to confine itself to the plots philosophers have
# laid out for its convenience. Maybe a few more tractors would do the trick.*
# >
# >--Roger Zelazny [^note1]
# 
# [^note1]: The quote comes from *Home is the Hangman*, published in 1975.]
# 

# This is a somewhat strange chapter, even by my standards. My goal in this chapter is to talk a bit more honestly about the realities of working with data than you'll see anywhere else in the book. The problem with real world data sets is that they are *messy*. Very often the data file that you start out with doesn't have the variables stored in the right format for the analysis you want to do. Sometimes might be a lot of missing values in your data set. Sometimes you only want to analyse a subset of the data. Et cetera. In other words, there's a lot of **_data manipulation_** that you need to do, just to get all your data set into the format that you need it. The purpose of this chapter is to provide a basic introduction to all these pragmatic topics. Although the chapter is motivated by the kinds of practical issues that arise when manipulating real data, I'll stick with the practice that I've adopted through most of the book and rely on very small, toy data sets that illustrate the underlying issue. Because this chapter is essentially a collection of "tricks" and doesn't tell a single coherent story, it may be useful to start with a list of topics:
# 
# - [Dataframes](pandas)
# - [Tabulating data](freqtables)
# - [Transforming or recoding a variable](transform)
# - [Some useful mathematical functions](mathfunc)
# - [Slicing](slicing) and dicing
# - [Extracting a subset of a data frame](subsets)
# - [Sorting, flipping or merging data sets](manipulations)
# - [Reshaping a data frame](reshaping)
# 
# 
# I may dump more trick and tips here later, and I'm really only scratching the surface of several fairly different and important topics. My advice, as usual, is to read through the chapter once and try to follow as much of it as you can. Don't worry too much if you can't grasp it all at once, especially the later sections. The rest of the book is only lightly reliant on this chapter, so you can get away with just understanding the basics. However, what you'll probably find is that later on you'll need to flick back to this chapter in order to understand some of the concepts that I refer to here.

# (pandas)=
# 
# ## Dataframes

# We've already used the `pandas` package [here](descriptives) and [there](DrawingGraphs), and [even over here](loadingcsv), but now it's time to look more closely at `pandas` dataframes. 
# 
# In order to understand why we use dataframes, it helps to try to see what problem the solve. So let's imagine a little scenario in which I collected some data from nine participants. Let's say I divded the participants in two groups ("test" and "control"), and gave them a task. I then recorded their score on the task, as well as the time it took them to complete the task. I also noted down how old they were.
# 
# the data look like this:

# In[1]:


age = [17, 19, 21, 37, 18, 19, 47, 18, 19]
score = [12, 10, 11, 15, 16, 14, 25, 21, 29]
rt = [3.552, 1.624, 6.431, 7.132, 2.925, 4.662, 3.634, 3.635, 5.234]
group = ["test", "test", "test", "test", "test", "control", "control", "control", "control"]


# So there are four variables in active memory: `age`, `rt`, `group` and `score`. And it just so happens that all four of them are the same size (i.e., they're all lists with 9 elements). Aaaand it just so happens that `age[0]` corresponds to the age of the first person, and `rt[0]` is the response time of that very same person, etc. In other words, you and I both know that all four of these variables correspond to the *same* data set, and all four of them are organised in exactly the same way. 
# 
# However, Python *doesn't* know this! As far as it's concerned, there's no reason why the `age` variable has to be the same length as the `rt` variable; and there's no particular reason to think that `age[1]` has any special relationship to `score[1]` any more than it has a special relationship to `score[4]`. In other words, when we store everything in separate variables like this, Python doesn't know anything about the relationships between things. It doesn't even really know that these variables actually refer to a proper data set. The data frame fixes this: if we store our variables inside a data frame, we're telling Python to treat these variables as a single, fairly coherent data set. 
# 
# To see how they do this, let's create one. So how do we create a data frame? One way we've already seen: if we use `pandas` to [import our data from a CSV file](loadingcsv), it will store it as a data frame. A second way is to create it directly from some existing lists using the `pandas.Dataframe()` function. All you have to do is type a list of variables that you want to include in the data frame. The output is, well, a data frame. So, if I want to store all four variables from my experiment in a data frame called `df` I can do so like this[^notedict]:
# 
# [^notedict]: Although it really doesn't matter at this point, you may have noticed a new symbol here: the "curly brackets" or "curly braces". Python uses these to indicate yet another variable type: the dictionary. Here we are using the dictionary variable type in passing to feed our lists into a `pandas` dataframe.

# In[2]:


import pandas as pd

df = pd.DataFrame(
    {'age': age,
     'score': score,
     'rt': rt,
     'group': group
    })


# In[3]:


df


# Note that `df` is a completely self-contained variable. Once you've created it, it no longer depends on the original variables from which it was constructed. That is, if we make changes to the original `age` variable, it will *not* lead to any changes to the age data stored in `df`. 

# (indexingdataframes)=
# ### Pulling out the contents of a data frame

# Let's take another look at our dataframe. We have created a dataframe called `df`, which contains all of our data for "The Very Exciting Psychology Experiment". Each row contains the data for one participant, so we can see that e.g. the first participant (in row zero, because Python!) was 17 years old, had a score of 12, responded in 3.552 seconds, and was placed in the test group. That's great, but how do we get this information out again? After all, there's no point in storing information if you don't use it, and there's no way to use information if you can't access it. So let's talk a bit about how to pull information out of a data frame. 
# 
# The first thing we might want to do is pull out one of our stored variables, let's say `score`. To access the data in the `score` column by the column name, we can write:

# In[4]:


score_data = df['score']
score_data


# Pretty easy, right? We could also choose to ask for only data from e.g. the first 4 particpants. To do this, we write:

# In[5]:


score_data = df['score'][0:4]
score_data


# As always, we have to be very careful about the numbering, and things are even more confusing than I have let on, because what we are doing here is what Python calls *slicing* the data, and slice numbers work a little differently than index numbers. To get a slice of data from the first to the fourth rows, we need to write `[0:4]`, rather than `[0:3]`, because when slicing the data, we need to specify the start and end point of the slice, but the end point _does not include the value specified as the end._ Is this confusing? Yes, I think so! In any case, this is the way Python behaves, and we just need to get used to it. The best way to get the hang of it just to practice slicing a bunch of data, until you learn how to get the results you want.

# What if we want to get data from a row instead? In this case, we will use the loc attribute of a pandas dataframe, and use a number instead of name (i.e., no quotation marks), like this:

# In[6]:


score_data = df.loc[2]
score_data


# Now we have what we need to get the data for columns and rows. Great! Unfortunately, there is one more thing I should mention[^note7]. If you look at the contents of score_data above, you will see that it is still not just the data: it also has information about the data, including which column and row it came from. And if we use type() to check, we can see that it is yet another variable type: this time, a pandas.core.series.Series. Yikes!
# [^note7]: Actually, there are lots more things I should mention, but now is not the time. Working with dataframes takes practice, and there are some catches, but it's worth the effort!

# In[7]:


type(score_data)


# Luckily, it's not too hard to get the raw data out of a `pandas` series. The simplest way is to just turn it into a list variable, using the command `list()`:

# In[8]:


my_row = list(score_data)
my_row


# If you want to get fancy, you can combine these steps, and do it all in one go:

# In[9]:


my_row = list(df.loc[2])
my_column = list(df['score'])
print(my_row)
print(my_column)


# ### Some more dataframe tips for the road
# 
# One problem that sometimes comes up in practice is that you forget what you called all your variables. To get a list of the column names, you can use the command:

# In[10]:


list(df)


# We can easily check to see how many rows and columns our dataframe has using `.shape`

# In[11]:


df.shape


# The first number gives us the number of rows, and the second number is the number of columns. Our dataframe `df` is 9 rows long, and 4 columns wide.

# Sometimes dataframes can be very large, and we just want to peek at them, to check what they look like, without data scrolling endlessly over the screen. The dataframe attribute head() is useful for this. By default it shows the first 5 lines of the dataframe:

# In[12]:


df.head()


# And if you want to see the last rows of the dataframe? `tail()` has got you covered:

# In[13]:


df.tail()


# Finally, if you just want to get all of your data out of the dataframe and into a list, then .values.tolist() will do the job, giving you a list of lists, with each item in the list containing the data for a single row:

# In[14]:


df.values.tolist()


# (freqtables)=
# 
# ## Tabulating and cross-tabulating data
# 
# A very common task when analysing data is the construction of frequency tables, or cross-tabulation of one variable against another. There are several functions that you can use in Python for that purpose.
# 
# Let's start with a simple example. As the father of a small child, I naturally spend a lot of time watching TV shows like *In the Night Garden*, and I have transcribed a short section of the dialogue. Let's make a `pandas` dataframe with two variables, `speaker` and `utterance`. When we take a look at the data, it becomes very clear what happened to my sanity. 

# In[15]:


import pandas as pd

data = {'speaker':["upsy-daisy",  "upsy-daisy",  "upsy-daisy",  "upsy-daisy",  "tombliboo",   "tombliboo",   "makka-pakka", "makka-pakka",
  "makka-pakka", "makka-pakka"],
       'utterance':["pip", "pip", "onk", "onk", "ee",  "oo",  "pip", "pip", "onk", "onk"]}

df = pd.DataFrame(data, columns=['speaker','utterance'])

df


# With these as my data, one task I might find myself needing to do is construct a frequency count of the number of utterances each character produces during the show. As usual, there are more than one way to achieve this, but the `crosstab` method from `pandas` provides an easy way to do this:

# In[16]:


pd.crosstab(index = df["speaker"], columns = "count")


# The output here shows a column called "speaker", and a column called "count". In the "speaker" column, we can see the names of all the speakers, and in the "count" column, we can see the number of utterances for each speaker. In other words, it’s a frequency table. Notice that we set the argument `columns` to "count". If instead we want to cross-tabulate the speakers with the utterances, we can set `columns` to the "utterances" column in the dataframe:

# In[17]:


pd.crosstab(index=df["speaker"], columns=df["utterance"],margins=True)


# ### Converting a table of counts to a table of proportions
# 
# The tabulation commands discussed so far all construct a table of raw frequencies: that is, a count of the total number of cases that satisfy certain conditions. However, often you want your data to be organised in terms of proportions rather than counts. This could be as a proportion of the row totals or the column totals. Currently, these are both just called "All", so let's first save the output of our crosstab to a variable, and rename the row and column totals to "rowtotals" and "coltotals".

# In[18]:


tabs = pd.crosstab(index=df["speaker"], columns=df["utterance"],margins=True)

tabs.columns = list(tabs.columns)[0:-1] + ['rowtotals']
tabs.index = list(tabs.index)[0:-1] + ['coltotals']

tabs


# Before we go on, it might be worthwhile looking at the steps used to rename the final column and row, because they give us some important information about the way `pandas` dataframes work. We saw before that you can get a list of the columns in your dataframe by using `list`:

# In[19]:


list(tabs)


# In[20]:


Now we see that we can also get the names of the columns of our dataframe `tabs` by writing `tabs.columns`


# In[85]:


tabs.columns


# In[86]:


type(tabs.columns)


# If we check to see what kind of object this is, we can see that it is a `pandas.core.indexes.base.Index` object. Isn't that a nice name? Furthermore, we can convert this object to a list in the usual way:

# In[87]:


list(tabs.columns)


# and now that it is a list, we can do the usual sorts of things that we can with lists, such as replace items in the list with other items. This allows us make changes to the column headers, and then we can re-assign our list to be the new column headers of the dataframe. Hoo boy! Finally, note that the dataframe also has an index of row names, called `.index`. So in our case, this is `tabs.index`. Sometimes these row names will be actual names, such as is the case in our dataframe `tabs`. Other times, like in the dataframe `df` from above, the `index` of the dataframe will just be numbers:

# In[88]:


list(df.index)


# Either way, names or numbers, each `pandas` dataframe will have a `columns` and an `index` index.
# 
# Now, after that fascinating digression into the structure of dataframes, back to our project which, as you surely recall, was converting our table of counts to a table of proportions. Having renamed the final column and row, now we can divide the entire frequency table by the totals in each column:

# In[89]:


tabs/tabs.loc['coltotals']


# The columns sum to one, so we can see that makka-pakka and upsy-daisy each produced 40% of the utterances, while tombliboo only produced 20%. We can also see the proportion of characters associated with each utterance. For instance, whenever the utterance “ee” is made (in this data set), 100% of the time it’s a Tombliboo saying it. 
# 
# The procedure to obtain the row-wise proportion, the procedure is slightly different. I'm _not_ going to get into it now. It just _is_, ok?

# In[90]:


tabs.div(tabs["rowtotals"], axis=0)


# Each row now sums to one, but that’s not true for each column. What we’re looking at here is the proportions of utterances made by each character. In other words, 50% of Makka-Pakka’s utterances are “pip”, and the other 50% are “onk”.

# (transform)=
# 
# ## Transforming and recoding a variable
# 
# It's not uncommon in real world data analysis to find that one of your variables isn't quite equivalent to the variable that you really want. For instance, it's often convenient to take a continuous-valued variable (e.g., age) and break it up into a smallish number of categories (e.g., younger, middle, older). At other times, you may need to convert a numeric variable into a different numeric variable (e.g., you may want to analyse at the absolute value of the original variable). In this section I'll describe a few key tricks that you can make use of to do this.
# 
# ### Creating a transformed variable
# 
# The first trick to discuss is the idea of **_transforming_** a variable. Taken literally, *anything* you do to a variable is a transformation, but in practice what it usually means is that you apply a relatively simple mathematical function to the original variable, in order to create new variable that either (a) provides a better way of describing the thing you're actually interested in or (b) is more closely in agreement with the assumptions of the statistical tests you want to do.  Since -- at this stage -- I haven't talked about statistical tests or their assumptions, I'll show you an example based on the first case. 
# 
# To keep the explanation simple, the variable we'll try to transform isn't inside a data frame, though in real life it almost certainly would be. However, I think it's useful to start with an example that doesn't use data frames because it illustrates the fact that you already know how to do variable transformations. To see this, let's go through an example. Suppose I've run a short study in which I ask 10 people a single question: 
# 
# >On a scale of 1 (strongly disagree) to 7 (strongly agree), to what extent do you agree with the proposition that "Dinosaurs are awesome"?
# 
# The data look like this:

# In[91]:


data = [1, 7, 3, 4, 4, 4, 2, 6, 5, 5]


# However, if you think about it, this isn't the best way to represent these responses.   Because of the fairly symmetric way that we set up the response scale, there's a sense in which the midpoint of the scale should have been coded as 0 (no opinion), and the two endpoints should be $+3$ (strong agree) and $-3$ (strong disagree). By recoding the data in this way, it's a bit more reflective of how we really think about the responses. The recoding here is trivially easy: we just subtract 4 from the raw scores. Since these data are in a list, we can use a "list comprehension" to step through each element in the list, and subtract 4 from it:

# In[92]:


data = [1, 7, 3, 4, 4, 4, 2, 6, 5, 5]
data = [x-4 for x in data]
data


# If your data is in a `numpy array` rather than a `list`, it is even easier: just subtract 4 from array, and Python takes care of the rest:

# In[93]:


import numpy as np
data = np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
data = data - 4
data


# One reason why it might be useful to center the data is that there are a lot of situations where you might prefer to analyse the *strength* of the opinion separately from the *direction* of the opinion. We can do two different transformations on this variable in order to distinguish between these two different concepts. Firstly, to compute an `opinion_strength` variable, we want to take the absolute value of the centred data (using the `abs()` function that we've seen previously), like so:

# In[94]:


data = np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
data = data -4
data = abs(data)
data


# Secondly, to compute a variable that contains only the direction of the opinion and ignores the strength, we can use the `numpy.sign()` method to do this. This method is really simple: all negative numbers are converted to $-1$, all positive numbers are converted to $1$ and zero stays as $0$. So, when we apply `numpy.sign()` to our data we obtain the following:

# In[95]:


data = np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
data = data - 4
data = np.sign(data)
data


# And we're done. We now have three shiny new variables, all of which are useful transformations of the original likert data. Before moving on, you might be curious to see what these calculations look like if the data had started out in a data frame. So, we can put our data in a dataframe, in a column called "scores"...

# In[96]:


import pandas as pd
df = pd.DataFrame(
    {'scores': np.array([1, 7, 3, 4, 4, 4, 2, 6, 5, 5])
    })

df


# ... and then do some calculations:

# In[97]:


df['centered'] = df['scores']-4
df['opinion_strength'] = abs(df['centered'])
df['opinion_direction'] = np.sign(df['scores']-4)
df


# In other words, even though the data are now columns in a dataframe, we can use exactly the same means to calculate new variable. Even better, we can simply create new columns willy-nilly within the same dataframe, so we can keep everything together, all neat and tidy.

# ### Cutting a numeric variable into categories
# 
# One pragmatic task that arises more often than you'd think is the problem of cutting a numeric variable up into discrete categories. For instance, suppose I'm interested in looking at the age distribution of people at a social gathering:

# In[98]:


#age = [60,58,24,26,34,42,31,30,33,2,9]
import pandas as pd
df = pd.DataFrame(
    {'age': np.array([60,58,24,26,34,42,31,30,33,2,9])
    })

df


# In some situations it can be quite helpful to group these into a smallish number of categories. For example, we could group the data into three broad categories: young (0-20), adult (21-40) and older (41-60). This is a quite coarse-grained classification, and the labels that I've attached only make sense in the context of this data set (e.g., viewed more generally, a 42 year old wouldn't consider themselves as "older").
# 
# As it happens, `pandas` has a convenient method called `cut` for grouping data in this way:

# In[99]:


df['categories'] = pd.cut(x = df['age'], bins = [0,20,40,60], labels = ['young', 'adult', 'older'])
df


# Note that there are four numbers in the `bins` argument, but only three labels in the `labels` argument; this is because the `cut()` function requires that you specify the *edges* of the categories rather than the mid-points. In any case, now that we've done this, we can use the `cut()` function to assign each observation to one of these three categories. There are several arguments to the `cut()` function, but the three that we need to care about are:
# 
# - `x`. The variable that needs to be categorised. 
# - `bins`. This is either a vector containing the locations of the breaks separating the categories, or a number indicating how many categories you want.
# - `labels`. The labels attached to the categories. This is optional: if you don't specify this Python will attach a boring label showing the range associated with each category.

# In the example above, I made all the decisions myself, but if you want to you can delegate a lot of the choices to Python. For instance, if you want you can specify the *number* of categories you want, rather than giving explicit ranges for them, and you can allow Python to come up with some labels for the categories. To give you a sense of how this works, have a look at the following example:

# In[100]:


df['categories'] = pd.cut(x = df['age'], bins = 3)
df


# With this command, I've asked for three categories, but let Python make the choices for where the boundaries should be. All of the important information can be extracted by looking at the tabulated data:

# In[101]:


pd.crosstab(index = df["categories"], columns = "count")


# This output takes a little bit of interpretation, but it's not complicated. What Python has done is determined that the lowest age category should run from 1.94 years up to 21.3 years, the second category should run from 21.3 years to 40.7 years, and so on. These labels are not nearly as easy on the eyes as our "young, adult, and older" categories, so it's usually a good idea to specify your own, meaningful labels to the categories.
# 
# Before moving on, I should take a moment to talk a little about the mechanics of the `cut()` function. Notice that Python has tried to divide the `age` variable into three roughly equal sized bins. Unless you specify the particular breaks you want, that's what it will do. But suppose you want to divide the `age` variable into three categories of different size, but with approximately identical numbers of people. How would you do that? Well, if that's the case, then what you want to do is have the breaks correspond to the 0th, 33rd, 66th and 100th percentiles of the data. One way to do this would be to calculate those values using the `np.quantile()` function and then use those quantiles as input to the `cut()` function. That's pretty easy to do, but it does take a couple of lines to type. So instead, the `pandas` library has a function called `qCut()` that does exactly this:

# In[102]:


df['categories'] = pd.qcut(x = df['age'], q = [0, .33, .66, 1] )
df


# Notice the difference in the boundaries that the `qcut()` method selects. The first and third categories now span an age range of about 25 years each, whereas the middle category has shrunk to a span of only 6 years. There are some situations where this is genuinely what you want (that's why I wrote the function!), but in general you should be careful. Usually the numeric variable that you're trying to cut into categories is already expressed in meaningful units (i.e., it's interval scale), but if you cut it into unequal bin sizes then it's often very difficult to attach meaningful interpretations to the resulting categories. 
# 
# More generally, regardless of whether you're using the original `cut()` method or the `qcut()` version, it's important to take the time to figure out whether or not the resulting categories make any sense at all in terms of your research project. If they don't make any sense to you as meaningful categories, then any data analysis that uses those categories is likely to be just as meaningless. More generally, in practice I've noticed that people have a very strong desire to carve their (continuous and messy) data into a few (discrete and simple) categories; and then run analysis using the categorised data instead of the original one.[^note2] I wouldn't go so far as to say that this is an inherently bad idea, but it does have some fairly serious drawbacks at times, so I would advise some caution if you are thinking about doing it. 
# 
# [^note2]: If you've read further into the book, and are re-reading this section, then a good example of this would be someone choosing to do an ANOVA using age categories as the grouping variable, instead of running a regression using `age` as a predictor. There are sometimes good reasons for do this: for instance, if the relationship between `age` and your outcome variable is highly non-linear, and you aren't comfortable with trying to run non-linear regression! However, unless you really do have a good rationale for doing this, it's best not to. It tends to introduce all sorts of other problems (e.g., the data will probably violate the normality assumption), and you can lose a lot of power.

# (mathfunc)=
# 
# ## A few more mathematical functions and operations

# (rounding)=
# ###  Rounding
# 
# As you might expect, Python can round numbers with decimals to whole numbers. As you might also have come to expect by now, Python will not necessarily do it the way you expect! Take a look below:

# In[157]:


print(round(4.4))
print(round(4.5))
print(round(4.51))


# Python rounds 4.4 to 4 and 4.51 to 5. However, notice what it does with 4.5: it rounds to this to 4 as well. This is just one of many ways to round numbers, so Python is not doing anything wrong; you just have to be aware that this is what it will do.
# 
# You can add a second argument to indicate the number of decimal places desired:

# In[158]:


a = 3.777298672345782376823578287355
round (a, 5)


# ### Row-wise means of a dataframe

# In[ ]:


df['mean'] = df.mean(axis = 1)


# In[ ]:





# (slicing)=
# ## Slicing and dicing your data

# ### slicing a list:
# 
# "Slicing" is the most common way to get chunks of data out of a list. In theory, it is quite simple. The syntax is as follows: listname[first:last:step_size]. The first number in the square brackets is where the slice should start, the second is where it ends, and the third indicates the size of any jumps that should be made (e.g. take every 2nd or every 3rd item). If you put nothing in this third argument, it defaults to one.
# 
# However, counting can be very tricky in Python! In my experience, even when you think you understand how it works, you can still get tripped up. The best thing to do is just take a list of data and start slicing it as many ways as you can think of, until you get a feeling for how it works.

# In[138]:


age = [17, 19, 21, 37, 18, 19, 47, 18, 19]


# Return the first four elements in the list:

# In[143]:


age[0:4]


# Return the last four elements in the list

# In[149]:


age[-4:]


# A different way to get the last four elements in the list:

# In[144]:


age[5:len(age)]


# Return every second element, starting with the first

# In[145]:


age[::2]


# Return every second element, starting with second

# In[150]:


age[1::2]


# ### "popping" items out of a list
# 
# Sometimes it is useful to remove an item from a list. In Python, lists have a property called `.pop()` that allow you to do just that. Nothing against spinach, but there is one item in the list of fruits below that isn't like the others. So let's `.pop` it out:

# In[166]:


fruits = ['apples', 'pears', 'bananas', 'spinach', 'strawberries', 'grapes']
fruits.pop(3)
fruits


# (subsets)=
# ## Extracting a subset of a dataframe

# In[ ]:





# In[66]:


age = [17, 19, 21, 37, 18, 19, 47, 18, 19]
score = [12, 10, 11, 15, 16, 14, 25, 21, 29]
rt = [3.552, 1.624, 6.431, 7.132, 2.925, 4.662, 3.634, 3.635, 5.234]
group = ["test", "test", "test", "test", "test", "control", "control", "control", "control"]

import pandas as pd

df = pd.DataFrame(
    {'age': age,
     'score': score,
     'rt': rt,
     'group': group
    })

df


# In[64]:


df_test = df[df['group'] == 'test']
df_test


# In[65]:


df_control = df[df['group'] == 'control']
df_control


# In[69]:


df_old = df[df['age']> 21] 
df_old


# In[ ]:





# In[71]:


df_youngish = df[(df['age'] < 21 ) & (df['age'] > 17)]
df_youngish


# In[73]:


old_and_slow = df[(df['age'] > 21) & (df['rt'] > 3)]
old_and_slow


# In[74]:


old_and_slow_control = df[(df['age'] > 21) & (df['rt'] > 3) & (df['group'] == 'control')]
old_and_slow_control


# (manipulations)=
# ## Sorting, flipping, and merging dataframes

# ### Sorting dataframes

# In[86]:


import pandas as pd


age = [17, 19, 21, 37, 18, 19, 47, 18, 19]
score = [12, 10, 11, 15, 16, 14, 25, 21, 29]
rt = [3.552, 1.624, 6.431, 7.132, 2.925, 4.662, 3.634, 3.635, 5.234]
group = ["test", "test", "test", "test", "test", "control", "control", "control", "control"]

df = pd.DataFrame(
    {'age': age,
     'score': score,
     'rt': rt,
     'group': group
    })

df


# #### Sorting by a column

# In[89]:


df_sorted = df.sort_values(by=['age'])
df_sorted


# #### Sorting from largest to smallest

# In[92]:


df_sorted = df.sort_values(by=['age'], ascending = False)
df_sorted


# #### Sorting by multiple columns

# In[93]:


df_sorted = df.sort_values(by=['age', 'score'])
df_sorted


# ### Flipping (transposing) a dataframe

# In[104]:


import pandas as pd

df_cakes = pd.read_csv("https://raw.githubusercontent.com/ethanweed/pythonbook/main/Data/cakes.csv")
df_cakes


# In[105]:


df_cakes_flipped = df_cakes.transpose()
df_cakes_flipped


# An important point to recognise is that transposing a data frame is not always a sensible thing to do: in fact, I’d go so far as to argue that it’s usually not sensible. It depends a lot on whether the “cases” from your original data frame would make sense as variables, and to think of each of your original “variables” as cases. Still, there are some situations where it is useful to flip your data frame, so it’s nice to know that you can do it. A lot of statistical tools make the assumption that the rows of your data frame (or matrix) correspond to observations, and the columns correspond to the variables. That’s not unreasonable, of course, since that is a pretty standard convention. However, think about our cakes example here. This is a situation where you might want do an analysis of the different cakes (i.e. cakes as variables, time points as cases), but equally you might want to do an analysis where you think of the times as being the things of interest (i.e., times as variables, cakes as cases). If so, then it’s useful to know how to flip a data frame around.

# ### Joining dataframes
# 
# Maybe we got our cake data in two batches (haha, sorry!) [^notesorry]. First we recorded times 1-3, and then later recorded times 4-5 in a separate dataframe, so that they looked like this: 
# 
# [^notesorry]: Not sorry.

# In[ ]:


first_three = df_cakes.loc[:, ['time.1', 'time.2', 'time.3']] 
last_two = df_cakes.loc[:, ['time.4', 'time.5']]


# In[121]:


first_three


# In[122]:


last_two


# What we want to do is `.join()` those suckers back together:

# In[123]:


df_joined = first_three.join(last_two)
df_joined


# ### Concatenating dataframes
# 
# A similar situation might have occured with our Very Exciting Psychology Experiment[^notetrademark]. We saved the data for the test group in one dataframe, and the data for the control group in a different dataframe, so that they look like this:
# 
# [^notetrademark]: Registered trademark, patent pending.

# In[125]:


df_test = df[df['group'] == 'test']
df_control = df[df['group'] == 'control']
df_test


# In[124]:


df_control


# Just like the cake data from before, we want to squish these data together into one dataframe, but unlike the cake data, we want to put one dataframe _on top_ of the other one. After all, the columns are all the same, it's just that the data are for two different groups. Luckily, we _did_ remember to add a column to each dataframe recording which group the data were from, so all we need to do is stack these two datarames together. This is called _concatenating_ the data, and we can accomplish it with `.concat()`:

# In[126]:


df_concatenated = pd.concat([df_test, df_control])
df_concatenated


# (reshaping)=
# ## Reshaping a dataframe

# One of the most annoying tasks that you need to undertake on a regular basis is that of reshaping a data frame. Framed in the most general way, reshaping the data means taking the data in whatever format it’s given to you, and converting it to the format you need it. Of course, if we’re going to characterise the problem that broadly, then about half of this chapter can probably be thought of as a kind of reshaping. So we’re going to have to narrow things down a little bit. I'm going to begin with two of the most common ways we need to reshape data: moving from wide-format data to long-format data, and moving from long-format data to wide-format data.

# ### Reshaping from wide to long format
# 
# The most common format in which you might obtain data is as a “case by variable” layout, commonly
# known as the wide form of the data. To get a sense of what I’m talking about, consider an experiment in which we are interested in the different effects that alcohol and and caffeine have on people’s working memory capacity (WMC). We recruit 10 participants, and measure their WMC under three different conditions: a “no drug” condition, in which they are not under the influence of either caffeine or alcohol, a “caffeine” condition, in which they are under the inflence of caffeine, and an “alcohol” condition, in which... well, you can probably guess. Ideally, I suppose, there would be a fourth condition in which both drugs are administered, but for the sake of simplicity let’s ignore that. The `drugs` data frame gives you a sense of what kind of data you might observe in an experiment like this:

# In[167]:


import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/ethanweed/pythonbook/main/Data/drugs1.csv")


# In[168]:


df


# This is a data set in “wide form”, in which each participant corresponds to a single row. We have two variables that are characteristics of the subject (i.e., their id number and their gender) and three variables that refer their performance in one of the three testing conditions (alcohol, caffeine or no drug). Because all of the testing conditions (i.e., the three drug types) are applied to all participants, drug type is an example of a **within-subject** factor. This is a case that can be fairly easily handled by `pandas` `.melt()` method:

# In[169]:


df_long = pd.melt(df, id_vars=[ 'id', 'gender'])
df_long.head(13)


# Sometimes, though, we want to do something a little more complex. For example, what if we didn't just measure working memory capacity (WMC), but we also measured their reaction time (RT). These data might look something like this:

# In[170]:


df = pd.read_csv("https://raw.githubusercontent.com/ethanweed/pythonbook/main/Data/drugs.csv")
df.head()


# We want to reshape the data from wide format to long format, but we want to group the WMC data in one column, and the RT data in another column. `pandas` has a solution for this as well, and it's called `wide_to_long()`. I wonder why they picked that name? 
# 
# `wide_to_long` is pretty powerful, but it has some niggling details that you have to get right, otherwise you will find yourself sitting sadly, wondering about your life choices. Basically, to get `wide_to_long` to do your bidding, you need to specify _at least_ four things: 
# 
# 1. the dataframe
# 2. some "stubnames"
# 3. one or more "id variables"
# 4. the name of the "sub-observation variable". 
# 
# Ugh. Plus, you might need some more things too. Let's take a look. First I'll show you the command that we need, and then I'll go through what it all means.

# In[6]:


df_long = pd.wide_to_long(df, stubnames = ['WMC','RT'], 
                          i=['id','gender'], 
                          j='drug', 
                          sep = '_', 
                          suffix = '.+')
df_long.head(10)


# First of all we need the name of the dataframe in wide format that we want to convert to long format. That's easy enough. Next, we need the `stubnames`.  If you look at the column headers in the original, wide data, you will notice that each of the data columns has a prefix: either WMC or RT, to indicate whether the column shows working memory capacity data or reaction time data. These prefixes are the "stubs", and `wide_to_long` will use them to group the data. Your columns _have to have some kind of grouping prefix_ for `wide_to_long` to work!
# 
# Next, we have the argument `i`. This is where we put the id variables. These variable remain consistent for each participant throughout the experiment. Participant 1's RT may change as a result of intaking caffeine or alchol, but presumably her gender does not.
# 
# Next up, we have the argument `j`. Here we put the name that of the column where `wide_to_long` will put the _labels_ that followed the prefix. In our case, these labels are "alchol", "caffeine", and "no.drug", so a logical choice for `j` might be "drug". 
# 
# Now, depending on our data, we might be able to stop here. These are the four required arguments to `wide_to_long`.  But in this case, we need two more variables. 
# 
# The first of these is `sep`. This is where we can indicate if there is some character that has been used to separate the prefix from the label in the original column names. We used an underscore `_` to separate e.g. "WMC" from "alchol", so we can specify this here. Now, technically, we _could_ have just used "WMC_" as our stubname instead of "WMC", and left off the `sep` argument, but in that case our new columns would be called "WMC_" and "RT_", and that wouldn't look quite as prof, now would it?
# 
# The second extra argument we need is `suffix`. By default, `wide_to_long` expects the labels to be numbers. I can't really imagine why the `pandas` authors would build in this assumption, but there it is. I'm sure they had their reasons. In any case, our labels are "alcohol", "caffeine", and "no.drug" are letters, not numbers, so we have to tell `pandas` to look for non-numeric labels. In the `suffix` argument we can enter a regular expression that searches for the pattern that we are interested in. Regular expressions deserve (and have received) entire books devoted entirely to their explanation, so we won't go further into this here. Suffice it to say that entering `.+` in the `suffix` argument will allow us to search for whatever might come after our separator `_`.
# 
# There is one final step before our data is truly usable. Because `pandas` tries to preserve the idex information from the original dataframe, we end up with a somewhat odd-looking structure:

# In[7]:


df_long.head(4)


# This is called a MultiIndex. It is quite clear for a human to read, but it is cumbersome if we want to do further calculations with our data, which we probably do. The solution is to thow out the old index information, and reset the index, like so:

# In[8]:


df_long = df_long.reset_index()
df_long.head(15)


# Ah. Now we have our wide format data in a nice long format.

# ### Reshaping from long to wide format
# 
# 

# Going the other way, from long to wide, is also not too hard, although it is still not quite as straightforward as one might wish. On the other hand it still far, far better than copy-pasting columns in Excel, which is a recipe for disaster. Trust me. I've been there.
# 
# To go from long to wide, we can start with our shiny new long format dataframe `df_long` and use `.pivot` to "swivel" our long-format columns into a wider format. `.pivot()` takes three critical arguments: index, columns, and values.
# 
# The "index" column keeps track of which data belongs with which: very important! In our case, we have a column called ` id` which contains a participant id-number for each participant, so we'll use that as our index. Then we know that in the wide dataframe, the right data will still go with the right participant.
# 
# Next we have the "columns" argument. Here we can use `drug` to make new columns called "alcohol", "caffeine", and "no.drug". There is one more level of categorization in our data, however: we have two measurements: "WMC" and "RT". So we can use the `values` argument to gather together this information as well, so that each value ends up in the right row and column.

# In[47]:


df_wide = pd.pivot(df_long, index=['id'], columns='drug', values=['gender', 'WMC', 'RT'])
df_wide


# And voilà! Our data have been shifted back into a format that nearly resembles how it started. There are some differences, though. Once again, `pandas` has used a "MultiIndex" to keep track of our data. As before, this is pretty easy to read, but less easy, perhaps, to work with. Remember, in our original data, WMC and RT were indicated as prefixes to the drug names, but this coupling was severed when we used these prefixes as "stubs" in the wide to long conversion. Let's put them back where the belong!
# 
# One way to do this is to split our new wide dataframe into three separate dataframes: one for WMC, one for RT, and one for gender. Then we can rename the columns with the appropriate prefixes before reassembling them into one.
# 
# We can start by selecting only the WMC data:

# In[48]:


df_WMC = df_wide['WMC']
df_WMC


# We can access the column names using the `.columns` method, then use a list comprehension to add the "WMC_" prefix again:

# In[49]:


df_WMC.columns = ['WMC_' + col for col in df_WMC.columns]
df_WMC    


# We can do the same for the RT data...

# In[50]:


df_RT = df_wide['RT']
df_RT.columns = ['RT_' + col for col in df_RT.columns]
df_RT


# The gender data are a little different, because here we just have three columns of repeated data:

# In[53]:


df_gender = df_wide['gender']
df_gender


# We really only need one of these, and since all columns contain the same information, we could choose any of them. We can use "chained" slicing to drill down to the "alcohol" column. Then, we can rename this column "gender":

# In[56]:


df_gender = pd.DataFrame(df_wide['gender']['alcohol'])
df_gender.columns = ['gender']
df_gender


# Now that we have three dataframe (df_WMC, df_RT, and df_gender) that all share the same index (`id`) we can join them back together, using the `.join()` method. First we can tack df_WMC onto df_gender:

# In[58]:


df_wide = df_gender.join(df_WMC, on = 'id', how = 'left')
df_wide


# Then we can attach `df_RT` to the right of the new `df_wide`:

# In[59]:


df_wide = df_wide.join(df_RT, on = 'id', how = 'left')
df_wide


# As a final touch, we'll `.reset()` the index to flatten out the MultiIndex, and we are back to where we started:

# In[60]:


df_wide = df_wide.reset_index()
df_wide


# In[ ]:




