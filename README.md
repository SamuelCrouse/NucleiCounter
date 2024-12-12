# NucleiCounter
Contains files to normalize images and count the nuclei within them. Thresholds can be adjusted to calculate
any cell whose color stands out in the image. Works by marking pixels in the selected gray color range and filtering
pixels by an estimated cell size.

## Setup
The github repository https://github.com/SamuelCrouse/NucleiCounter contains the files and example main.py
to perform the counting.<br>
<ol>
<li>Download NucleiCounter repo and extract the files.</li>
<li>Insert CountNuclei.py into your python project.</li>
<li>Import into your file by writing "import CountNuclei as cn" at the top of your .py file.</li>
</ol>

## Workflow
<ol>
<li>Define the absolute path to your image data.</li>
<li>Use prepImage() or loadImageGrayscale() and normalizeImage() to prepare your image for counting.</li>
<li>Consider using provided images in this repository as normalToImg for standardized results across your images.</li>
<li>Pass this PIL obj image to countNuclei() with desired settings to get a count of cells.</li>
<li>View examples in CountNuclei.py main and examples in main.py to get a feeling for use.</li>
<li>Documentation at function heads show how to use functions.</li>
</ol>

## Example Workflow Output
___
#### Initial Image
This is the image that you want to count, but haven't done any pre-processing on.
![img2.png](images%2Fimg2.png)
___
#### Gray-scaled
This is the image after NucleiCounter loadImageGrayscale() has gray-scaled the image.
![gray2.png](images%2Fgray2.png)
___
#### Normalized
The above image after it has been normalized to itself or another, standard, image.
![gray2_normal.png](images%2Fgray2_normal.png)
___
#### Very Simple Marking Settings
Very simple marking settings for marking every acceptable area. Good for testing settings.
![gray2_normal_marked1.png](images%2Fgray2_normal_marked1.png)
___
#### Simple Marking Settings
Marks just the edges of the desired cell. Good for seeing cell size settings.
![gray2_normal_marked2.png](images%2Fgray2_normal_marked2.png)
___
#### Accurate Marking Settings Example 1
These are the most accurate settings. These take the longest to produce. Set verySimple and simple to False to get this
output.
![gray2_normal_marked3.png](images%2Fgray2_normal_marked3.png)
___
#### Accurate Marking Settings Example 2
A more restrictive count than the above settings. Shows how stricter settings result in smaller counts.
![gray2_normal_marked4.png](images%2Fgray2_normal_marked4.png)


