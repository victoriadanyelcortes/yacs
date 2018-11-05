import pandas as pd
import json
import re
import copy

index = {}
subject_list = [] # This is global only for testing purposes

def format_data(unformatted_json):
	# This function takes in a JSON string in the API's format
	# and returns a JSON string in Yacs format
	df = get_df(unformatted_json) # Get a pandas dataframe to do operations on

	global subject_list




	gallatin = {'longname': 'Gallatin','shortname': 'gallatin','subjects':subject_list}
	data = {'schools':[gallatin]}
	return json.dumps(data)

cols = ['COURSE', # ARTS-UG1275
'CREDIT', # 4
'DAYS', # Wed
'DAYS2', # Fri
'DESCRIPTION', # Text...
'HISTCULT',
'LIBARTS',
'INSTRUCTORS', # [{'name':'website'}]
'LEVEL', # U or G
'NOTES', # Extra text
'SECTION', # number
'TERM', # FA, SU, WI, or SP
'TIMES', # Time String
'TIMES2', # Time String
'TITLE', # Course Title
'TYPE', # Arts Workshops (ARTS-UG)
'YEAR'] # Integer

match_global = re.compile('^Global')

def should_include(row):
	# Returns true if the row should be included in the final output
	if match_global.match(row[index['type']]) is None:
		return True
	return False

def append_subject(subjects,df):
	pass

def append_section(subjects, df):
	# Adds the row data to the subjects dictionary
	pass

def append_period(subjects,df):
	pass

# Desired
# {
# 	"shortname": "ARTS-UG","longname": "Arts Workshops",
# 	"listings": [
# 			{
# 				"shortname": "1485","longname": "FullCourseName","min_credits": 4,"max_credits": 4,
# 				"description": "Course desc"
# 				"sections": [
# 					"shortname": "001",
# 					"periods": [
# 						{...}
# 					]
# 				]
# 			}
# 		]
# 	},
# 	{
# 		"shortname": "IDSEM-UG","longname": "Interdisciplinary Seminars",
# 		"listings": [
# 			...
# 		]
# 	}

def get_df(raw_json):
# Read in data, and do some simple formatting
	# Read in data
	df = pd.read_json(raw_json, orient = 'index')
	# For testing purposes only
	df['description'] = df['description'].str[0:5]
	# Drop useless columns
	df = df.drop(['syllabus', 'term','year','level'],axis = 1)
	# Drop  these two columns because they're annoying and IDK what to do with them
	for name in ['foundation-histcult','foundation-libarts']:
		if name in df.columns:
			df = df.drop(name,axis = 1)
	# Drop 'totalMatches' - it's not a record
	df = df.drop('totalMatches',axis=0)
	# To make it easier to work with, remove empty strings, None, and the like
	df = df.replace(r'^\s*$',pd.np.nan,regex=True).fillna(value=pd.np.nan)

# Filter out global courses
	# Preformats a series to be used for filtering
	type_col = df['type'].str.strip().str.lower()
	# Filter out those global courses using a mask
	df = df[type_col.str.startswith('global') == False]
	del type_col # No longer need the series
	# Reset index to integers (so that formatting doesn't screw up randomly)
	df = df.reset_index(drop=True)

# Format columns

	# Replace 'type' with 'subject_longname'
	# 'type' is formatted as :longname: (:shortname:-:level:)
	type_parts = df['type'].str[:-1].str.split(r"\s*\(", n = 1, expand = True)
	# Make the subject longname column
	df['subject_longname'] = type_parts[0]
	# Remove the 'type' column
	df = df.drop('type',axis = 1)
	del type_parts # we don't need this anymore

	# Replace course with 'subject_shortname' and 'course_id'
	# Change course into course shortname and course id
	course_parts = df['course'].str.split(r'(?<=[A-Z])(?=[0-9])',n=1,expand=True)
	df['subject_shortname'] = course_parts[0]
	df['course_shortname'] = course_parts[1]


	# making seperate first name column from new data frame
	data["First Name"]= new[0]

	# making seperate last name column from new data frame
	data["Last Name"]= new[1]

	# Dropping old Name columns
	data.drop(columns =["Name"], inplace = True)





	# Sort df so that we can directly append to list
	# Group by type first, then within each type group by course name
	df = df.sort_values(['type','course'])

	return df
