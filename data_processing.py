# importing neccesary libraries and dependencies
import pandas as pd
import datetime


# function to convert duration from MM:SS to seconds format
def convert_duration_to_seconds(duration):
    # Split the duration into minutes and seconds
    minutes, seconds = map(int, duration.split(':'))

    # Convert to seconds
    total_seconds = minutes * 60 + seconds

    return total_seconds
    # function to convert duration from HH:MM:SS to seconds format


def convert_duration_to_seconds_from_HH(duration):
    # Split the duration into hours, minutes and seconds
    hours, minutes, seconds = map(int, duration.split(':'))

    # Convert to seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds


def session(file_path):
    # Fields to extract
    fields_to_extract = ['Name',
                         'Project',
                         'Type',
                         'Duration (in seconds)',
                         'Pauses (in seconds)',
                         #'Duration (in minutes)',
                         #'Pauses (in minutes)',
                         'Start date',
                         'End date',
                         'Notes']

    # Field mappings
    field_mappings = {
        'Name': 'Task name',
        'Project': 'Project name',
        'Start date': 'Start time',
        'End date': 'End time',
        'Duration (in seconds)': 'Duration',
        'Pauses (in seconds)' : 'Breaks',
        'Notes': 'Notes',
        'Type' : 'Tags'
    }

    # Read the data
    data = pd.read_csv(file_path)

    # Extract necessary fields
    data = data[fields_to_extract]

    # Rename the fields
    data = data.rename(columns=field_mappings)

    # Save to output file
    output_file_path = 'output_data_application1.csv'
    data.to_csv(output_file_path, index=False)

    return


def toggle(file_path):
    # Fields to extract
    fields_to_extract = [#'User',
                         #'Email',
                         #'Client',
                         'Project',
                         'Task',
                         'Description',
                         #'Billable',
                         'Start date',
                         'Start time',
                         'End date',
                         'End time',
                         'Duration',
                         'Tags',
                         #'Amount (USD)'
                         ]

    # Field mappings
    field_mappings = {
        'Task': 'Task name',
        'Project': 'Project name',
        'duration': 'Duration',
        'Null' : 'Breaks',
        'notes': 'Notes',
        'Null' : 'Tags'
    }

    # Read the data
    data = pd.read_csv(file_path)

    # Extract necessary fields
    data = data[fields_to_extract]

    # Rename the fields
    data = data.rename(columns=field_mappings)

    # Converting duration to seconds from HH:MM:SS
    data['Duration'] = data['Duration'].apply(convert_duration_to_seconds_from_HH)

    # Convert to datetime format
    data['Start date'] = pd.to_datetime(data['Start date'])
    data['End date'] = pd.to_datetime(data['End date'])
    data['Start time'] = pd.to_datetime(data['Start time']).dt.time
    data['End time'] = pd.to_datetime(data['End time']).dt.time

    # Combine date and time
    data['Start time'] = data.apply(lambda row: datetime.datetime.combine(row['Start date'], row['Start time']), axis=1)
    data['End time'] = data.apply(lambda row: datetime.datetime.combine(row['End date'], row['End time']), axis=1)

    # Convert to railway time format
    data['Start time'] = data['Start time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data['End time'] = data['End time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Dropping the original 'Start date' and 'End date' columns
    data.drop(columns=['Start date', 'End date'], inplace=True)


    # Save to output file
    output_file_path = 'output_data_toggle.csv'
    data.to_csv(output_file_path, index=False)

    return


def timemator(file_path):
    # Fields to extract
    fields_to_extract = [#'unix_begin',
                         #'unix_end',
                         'date',
                         'begin',
                         'end',
                         'folder',
                         'task',
                         'duration',
                         #'duration_decimal',
                         #'rounding_to',
                         #'rounding_method',
                         #'hourly_rate',
                         #'revenue',
                         #'billing_status',
                         'notes']

    # Field mappings
    field_mappings = {
        'task': 'Task name',
        'folder': 'Project name',
        'Start date': 'Start time',
        'End date': 'End time',
        'duration': 'Duration',
        'Null' : 'Breaks',
        'notes': 'Notes',
        'Null' : 'Tags'
    }

    # Read the data
    data = pd.read_csv(file_path)

    # Extract necessary fields
    data = data[fields_to_extract]

    # Rename the fields
    data = data.rename(columns=field_mappings)

    # Converting duration to seconds from MM:SS
    data['Duration'] = data['Duration'].apply(convert_duration_to_seconds)

    # Convert to datetime format
    data['date'] = pd.to_datetime(data['date'])
    data['begin'] = pd.to_datetime(data['begin']).dt.time
    data['end'] = pd.to_datetime(data['end']).dt.time

    # Combine date and time
    data['Start time'] = data.apply(lambda row: datetime.datetime.combine(row['date'], row['begin']), axis=1)
    data['End time'] = data.apply(lambda row: datetime.datetime.combine(row['date'], row['end']), axis=1)

    # Convert to railway time format
    data['Start time'] = data['Start time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data['End time'] = data['End time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Dropping the original 'date', 'begin' and 'end' columns
    data.drop(columns=['date', 'begin', 'end'], inplace=True)


    # Save to output file
    output_file_path = 'output_data_timemator.csv'
    data.to_csv(output_file_path, index=False)

    return


def identify_application(file_path):

    data = pd.read_csv(file_path)

    # Checking if a unique field exists to identify the application
    if 'Type' in data.columns:
        return session
    elif 'User' in data.columns:
        return toggle
    elif 'unix_begin' in data.columns:
        return timemator
    else:
        raise ValueError("Unknown application")
