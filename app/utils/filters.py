# Filters allow us to format data for use in the Jinja templates
# Jinja template engine is part of Flask

# this filter receives a datetime object
def format_date(date):
  # and use the strftime method to cover the object to a string
  return date.strftime('%m/%d/%y')

# this is to test the format_date function
# run the following command to test it:
# python app/utils/filters.py
# from datetime import datetime
# print(format_date(datetime.now()))

# this filter removes all extraneous information from the URL string
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# this is to test the format_url function
# run the following command to test it:
# python app/utils/filters.py
# print(format_url('http://google.com/test/'))
# print(format_url('https://www.google.com?q=test'))

# this filter pluralizes words as applicable
def format_plural(amount, word):
  if amount != 1:
    return word + 's'

  return word

# this is to test the format_plural function
# run the following command to test it:
# python app/utils/filters.py
# print(format_plural(2, 'cat'))
# print(format_plural(1, 'dog'))