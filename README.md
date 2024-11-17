# PV-Toolkit
## Attention
This program is developed for the relevant instruments of the ***Institute of Functional Nano & Soft Materials at Soochow University***, and may not be universally applicable.

## Functions
### 1 - iv-helper
:question: Why do I need to develop this module? Because the parameters (Voc; Jsc; P_max; FF; PCE) by the source meter paired with the photovoltaic testing system are inaccurate.

:star: This function will help you recalculate the parameters and generate statistical data. Futhermore, this function will work correctly regardless of whether your devices is an n-i-p or p-i-n structure, and whether it is in forward or reverse sweep mode.

### 2 - steady-state-current-helper
This function will help you find the smoothest part of the steady-state current curve and calculate the most accurate current value.

### 3 - eqe-helper
This function will reprocess the original data and calculate the integrated current. 

## How to use
Run the PV-Toolkit.exe and call the function according to the prompts. For different functions, you need to preliminarily organize the data files according to the following requirements.
### 1 - iv-helper
:arrow_forward: Before running this function, you should organize your data files like the following.
* First folder (you can name it as you like)
  * Second folder1 (you can name it as you like)
    * data1.txt
    * data2.txt
    * ...
  * Second folder2 (you can name it as you like)
    *  data3.txt
    *  ...
  * ...
   
:arrow_forward: After running iv-helper, your data files will look like the following. Forward scan data will be automatically marked in blue.
* First folder (you can name it as you like)
  * Second folder1 (you can name it as you like)
    * data1.txt
    * data2.txt
    * ...
  * Second folder2 (you can name it as you like)
    *  data3.txt
    *  ...
  * ...
   * **First folder.xlsx**
   * **Statistical data.xlsx**
   * **JV_curve_data.xlsx**
### 2 - steady-state-current-helper
:arrow_forward: Before running this function, you should organize your data files like the following.
* First folder (you can name it as you like)
  * Second folder1 (you can name it as you like)
    * data1.txt
    * data2.txt
    * ...
  * Second folder2 (you can name it as you like)
    *  data3.txt
    *  ...
  * ...

:arrow_forward: After running steady-state-current-helper, your data files will look like the following.
* First folder (you can name it as you like)
  * Second folder1 (you can name it as you like)
    * data1.txt
    * data2.txt
    * ...
  * Second folder2 (you can name it as you like)
    *  data3.txt
    *  ...
   * ...
   * **First folder.xlsx**
### 3 - eqe-helper
:arrow_forward: Before running this function, you should organize your data files like the following.
* First folder (you can name it as you like)
  * Second folder1 (you can name it as you like)
    * data1.txt
    * data2.txt
    * ...
  * Second folder1 (you can name it as you like)
    * data3.txt
    * ...
      
:arrow_forward: After running eqe-helper, your data files will look like the following.
* First folder (you can name it as you like)
  * Second folder1 (you can name it as you like)
    * data1.txt
    * data2.txt
    * ...
  * Second folder1 (you can name it as you like)
    * data3.txt
    * ...
  * ...
  * **First folder.xlsx**
 
## Other Info
None.


