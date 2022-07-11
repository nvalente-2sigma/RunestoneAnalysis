import pandas as pd

log = pd.read_csv('data/data_log.csv', index_col=0)
actByInt = pd.read_csv('data/activity_by_interaction.csv', index_col=0)
actBySub = pd.read_csv('data/activity_by_subchapter.csv', index_col=0)

def scrub(input, hash_length=6):
  output = str(hash(input) % 10**hash_length)
  print(input,' --> ', output)
  return output

for name in actByInt.columns:
    # Split over '<br>' tag and store in dictionaries
    if '<br>' in name:
        last_first = name[:name.index('<')].split(', ')
        full_name = last_first[1] + ' ' + last_first[0]
        sid = name[name.index('>') + 2:-1]

        # Anonymize the data
        full_name = scrub(full_name)
        hashed_sid = scrub(sid)

        # Replace it in files
        log['sid'] = log['sid'].str.replace(sid, hashed_sid)
        actByInt.rename(columns={name: hashed_sid}, inplace=True)
        actBySub.rename(columns={name: hashed_sid}, inplace=True)

print("Saving...")

log.to_csv('hashed_data/data_log.csv')
actByInt.to_csv('hashed_data/activity_by_interaction.csv')
actBySub.to_csv('hashed_data/activity_by_subchapter.csv')

print("Scrub successful.")