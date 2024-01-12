import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("hierarchy_free.csv")

df.info()

df.sort_values(by=['hierarchy_free'], inplace=True, ascending=False)

df.plot.bar(x='hierarchy_free', y='asn', rot=90)
plt.show()
exit()

#fig, ax = plt.subplots()

plt.barh(df['hierarchy_free'], df['asn'], align='center')
plt.invert_yaxis()  # labels read top-to-bottom
plt.set_xlabel('Hierarchy Free')
plt.set_ylabel('ASN')
plt.set_title('Hierarchy Free per ASN')

plt.savefig('hierarchy_free.png')
