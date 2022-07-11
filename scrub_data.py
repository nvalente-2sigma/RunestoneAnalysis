import pandas as pd

pd.options.mode.chained_assignment = None  # default = 'warn'

log = pd.read_csv('data/data_log.csv', index_col=0)
actByInt = pd.read_csv('data/activity_by_interaction.csv', index_col=0)
actBySub = pd.read_csv('data/activity_by_subchapter.csv', index_col=0)

for name in actByInt.columns:
    # Split over '<br>' tag and store in dictionaries
    if '<br>' in name:
        last_first = name[:name.index('<')].split(', ')
        full_name = last_first[1] + ' ' + last_first[0]
        sid = name[name.index('>') + 2:-1]

        # Anonymize the data
        full_name = hash(full_name)

        hashed_sid = hash(sid)
        log['sid'] = log['sid'].str.replace(sid, hashed_sid)
        actByInt.rename(columns={name: hashed_sid}, inplace=True)
        actBySub.rename(columns={name: hashed_sid}, inplace=True)

log.to_csv('data_log_hashed.csv')
actByInt.to_csv('actByInt_hashed.csv')
actBySub.to_csv('actBySub_hashed.csv')