import json
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from binascii import hexlify, unhexlify



# Encoding function
#------------------------------------------------------------------------------
class BytesIntEncoder:

    @staticmethod
    def encode(b: bytes) -> int:
        return int(hexlify(b), 16) if b != b'' else 0

    @staticmethod
    def decode(i: int) -> int:
        return unhexlify('%x' % i) if i != 0 else b''

#For testing purposes you can use these options:
    
land_input = input('Please enter your desired kommun:')
land_input = BytesIntEncoder.encode(land_input.encode())
type_input = input('Please enter your desired housig type:')
type_input = BytesIntEncoder.encode(type_input.encode())
room_input = int(input('Please enter the number of rooms:'))
area_input = float(input('Please enter your desired area (m^2):'))


# Importing modifyed from DB (or final json file)
#------------------------------------------------------------------------------ 

#Reading data
with open('final_json.txt') as json_file:
    jdata = json.load(json_file)
json_file.close    
# labling str coloums of the data    
le = preprocessing.LabelEncoder()
typelst= []
landlst= []
roomlst= []
arealst= []
pricelst= []
for item in jdata:
    typelst.append(item['type_enc'])
    landlst.append(item['kommun_enc'])
    roomlst.append(item['room'])
    arealst.append(item['area'])
    pricelst.append(item['price'])


# Modeling stored data (K-Nearest Neighbor)
#------------------------------------------------------------------------------ 

features=list(zip(typelst,landlst,roomlst,arealst))
mainmodel = KNeighborsClassifier(n_neighbors=2)

mainmodel.fit(features,pricelst)

predicted= mainmodel.predict([[type_input,land_input,room_input,area_input]])
print(predicted)


# Model test (Accuracu test)
#------------------------------------------------------------------------------ 

X_train, X_test, y_train, y_test = train_test_split(features, pricelst, test_size=0.3)
knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))



