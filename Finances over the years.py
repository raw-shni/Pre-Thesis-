import matplotlib.pyplot as plt
import numpy as np

# Data from your table
years = [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
data_series = {
    #"Sourcing per year": [66253.628, 17906.978, 133760.108, 161932.035, 176831.378, 165230.233, 189354.735, 198013.807, 189099.703, 153392.329, 144510.878, 120123.024, 94213.893, 91776.145, 143630.574, 147698.918, 153937.201, 223706.877, 272599.400, 285221.915, 328625.617, 329720.864, 345495.567, 330022.809, 361915.066, 374882.849],
    #"Sales per year": [240000, 228000, 228000, 240000, 234000, 216000, 222000, 216000, 216000, 240000, 228000, 240000, 252000, 240000, 228000, 204000, 219000, 216000, 228000, 228000, 216000, 222000, 216000, 180000, 192000, 192000],
    "Revenue per year": [795043.532, 214883.740, 1605121.298, 1943184.424, 2121976.537, 1982762.792, 2272256.825, 2376165.683, 2269196.431, 1840707.943, 1734130.533, 1441476.287, 1130566.716, 1101313.739, 1723566.883, 1772387.022, 1847246.410, 2684482.527, 3271192.796, 3422662.976, 3943507.408, 3956650.365, 4145946.807, 3960273.711, 4342980.792, 4498594.189],
    "Profits per year": [678760.883, 496290.701, 756960.243, 965796.106, 932182.367, 679845.349, 799040.129, 729020.710, 715649.554, 940176.986, 781149.475, 840369.072, 857302.099, 755328.435, 779168.791, 518774.189, 494774.189, 697769.026, 767560.316, 1069348.649, 978791.090, 1195407.639, 1197871.943, 950243.351, -159034.214, 88563.701, 384000.000]
}

# Find the length of the longest data series
max_length = max(len(data) for data in data_series.values())

# Interpolate shorter data series to match the length of the longest series
for label, data in data_series.items():
    if len(data) < max_length:
        data_series[label] = np.interp(range(max_length), range(len(data)), data)

# Create the line chart
plt.figure(figsize=(12, 6))
for label, data in data_series.items():
    plt.plot(years, data, label=label, marker='o')

# Add labels and legend
plt.xlabel('Year')
plt.ylabel('Amount (in Rupees)')
plt.title('Financial Performance Over the Years')
plt.legend()

# Show the chart
plt.grid(True)
plt.tight_layout()
plt.show()
