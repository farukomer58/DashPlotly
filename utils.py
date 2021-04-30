
 
def label_lat (row):
    # """ Function that accept each row of pandas dataframe via a labda function Based on the city 
    # we return the latitude of the center of the city"""
  
   if row['city'] == 'Amsterdam' :
      return '52.379189;4.899431'
   if row['city'] == 'Londen' :
      return '51.509865;-0.118092'
   if row['city'] == 'Paris' :
      return '48.864716;2.349014'
   if row['city'] == 'Barcelona' :
      return '41.390205;2.154007'
   if row['city'] == 'Milan' :
      return '45.464664; 9.188540'
   if row['city'] == 'Vienna' :
      return '48.210033; 16.363449'
   return 'Other'