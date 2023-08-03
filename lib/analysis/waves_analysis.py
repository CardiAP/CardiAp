import numpy
import matplotlib.pyplot as plt
import pandas as pd

def wave_propagation(list_img_row,slice_width=5):
    wp = pd.DataFrame(columns=['distance','time'])
    max_position_distance = 0
    for peak in range(len(list_img_row['slices'])):
        max_position_time = list_img_row['slices'][peak]['max_peaks_positions'][0]
        wp.loc[len(wp)] = [max_position_distance,max_position_time]
        max_position_distance += slice_width
    xData = list(wp ['distance'])
    yData = list(wp ['time'])
    # polynomial curve fit the test data
    fittedParameters = numpy.polyfit(xData, yData, 7)
    wave_propagation_df = pd.DataFrame(columns= ['slope_at_point','y_value_at_point'])
    for pointVal in range(len(list_img_row['slices'])*slice_width):
        wave_propagation_df = pd.concat([wave_propagation_df,pd.DataFrame([ModelScatter(xData,fittedParameters,pointVal)],columns= ['slope_at_point','y_value_at_point'])])
    return wave_propagation_df

'''Calculate tangent line of each point of the wave'''
def ModelScatter(xData, fittedParameters, pointVal):
    # create data for the fitted equation plot
    xModel = numpy.linspace(min(xData), max(xData))
    yModel = numpy.polyval(fittedParameters, xModel)
    
    # polynomial derivative from numpy
    deriv = numpy.polyder(fittedParameters)

    # value of derivative (slope) at a specific X value, so
    # that a straight line tangent can be plotted at the point
    # you might place this code in a loop to animate
    y_value_at_point = numpy.polyval(fittedParameters, pointVal)
    slope_at_point = numpy.polyval(deriv, pointVal)
    
    return [slope_at_point,y_value_at_point]

##########################################################
# graphics output section
def ModelAndScatterPlot(xData, yData,fittedParameters,graphWidth, graphHeight,pointVal):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)

    # first the raw data as a scatter plot
    axes.plot(xData, yData,  'D')

    # create data for the fitted equation plot
    xModel = numpy.linspace(min(xData), max(xData))
    yModel = numpy.polyval(fittedParameters, xModel)

    # now the model as a line plot
    axes.plot(xModel, yModel)

    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label

    # polynomial derivative from numpy
    deriv = numpy.polyder(fittedParameters)

    # for plotting
    minX = min(xData)
    maxX = max(xData)

    # value of derivative (slope) at a specific X value, so
    # that a straight line tangent can be plotted at the point
    # you might place this code in a loop to animate
    y_value_at_point = numpy.polyval(fittedParameters, pointVal)
    slope_at_point = numpy.polyval(deriv, pointVal)

    ylow = (minX - pointVal) * slope_at_point + y_value_at_point
    yhigh = (maxX - pointVal) * slope_at_point + y_value_at_point

    # now the tangent as a line plot
    axes.plot([minX, maxX], [ylow, yhigh])

    plt.show()
    plt.close('all') # clean up after using pyplot