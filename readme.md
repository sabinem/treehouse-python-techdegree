#Learning Journal
I started analyzing Python framework in order to learn more about
meta programming. *peewee_validate* is the first framework I am studying.
It is very small and with a narrow purpose, that makes it a good choice for starting
my project
##Introduction: Peewee Validate
Peewee validate derives from *peewee* and *validate*. And that is where its
purpose lies: *validation* for *peewee*.
###What is peewee?
peewee is a lightweight orm for python. One of the features of being
lightweigth in peewee is that it does not offer any database field validation.
You can define your fields as being strings of 100 characters maximum, or
a date of a specific format, but when you enter you data into the database,
peewee does not check. Peewee model declarations look like this:
```python
from peewee import *

class Category(peewee.Model):
    code = peewee.IntegerField(unique=True)
    name = peewee.CharField(null=False, max_length=250)
```
But when you enter data, there is no check to make sure, that you follow the
specification. You can still enter a lot of chunk data that have nothing to
do with what you specified in your model.

###peewee_validate enters the scene
This is where peewee_validate comes into the picture. Its goal is to provide
the missing field validation for peewee.

So now you can say:
```python
obj = Category(code=42)

validator = ModelValidator(obj)
validator.validate()

print(validator.errors)
```
###How does peewee do this?:
So how is peewee_validate constructed? How does it do its job internally?
##Analyzing peewee_validate
The best way to explain how peewee_validate does this is in steps.
###Step 1: Find a problem that is related and has this problem as a special case.
This seems to be a good approach in general. The problem at hand is not so
clear since it contains a third party package *peewee*, but can you abstract it to get
*peewee out of the equation? Turns out you can.






