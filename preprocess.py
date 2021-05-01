import pandas as pd
import utils

# Read the kaggle hotel review csv/dataset 
hotel = pd.read_csv('Hotel_Reviews.csv')

# Extract the city out of the adress column
hotel['city']=(hotel["Hotel_Address"].str.split(" ").str[-2])
hotel.loc[hotel['city']=='United', 'city'] = 'Londen'           # Correct 'United' to 'Londen'
# hotel['city'].unique()

# Set the Center latLong of the cities
hotel['latLong'] = hotel.apply (lambda row: utils.label_lat(row), axis=1)

# Save the updated dataset to a csv
hotel.to_csv('Hotel.csv',index=False)

updatedDataset = pd.read_csv('Hotel.csv')
updatedDataset.dtypes
updatedDataset.head()

distinctDf = hotel

distinctDf = distinctDf.drop_duplicates(subset=['lat'])

# f = lambda x: (hotel["Hotel_Address"].str.split(" ")) 
# hotel.apply(f)

# hotel.Hotel_Address.split(' ')[-1]

# hotel.info()
# lat = hotel['lat'].unique()

# hotelPos =hotel[hotel['Reviewer_Score'] > 5.5]

# lat = hotel['lat'].unique()
# lng = hotel['lng'].unqiue()

# anan = hotelPos.Reviewer_Nationality.value_counts().loc[lambda x: x>7500].reset_index()
# anan2 = anan.rename(columns = {'index':'country'})
# anan2

# # The percentage that is postive review in top countries
# topCountries = hotelPos[hotelPos['Reviewer_Nationality'].isin(anan2['country'])] 
# anan2['count'] = topCountries['Reviewer_Nationality'].value_counts().reset_index()['Reviewer_Nationality']
# anan2



# hotel[hotel['Reviewer_Nationality'].value_counts() >= 2412].index[0]

# anan['country'] = hotel.Reviewer_Nationality.value_counts().loc[lambda x: x>2412].reset_index()['index']


# hotel[hotel.Reviewer_Nationality.value_counts().loc[lambda x: x>2412]]
