# Parametric study with Diana

The code I developed for a parametric study to create a particular crack pattern in concrete specimens.
The project is an extension of my presentation in the 2nd Nordic mini-seminar on residual service life and capacity of deteriorated concrete structures:

 [S.Fahimi, K.Zandi, C.G. Berrocal, I.F. Perez, “ Replication of crack pattern in FE analysis based on discretization of tension softening curves”, 2nd Nordic mini-seminar on residual service life and capacity of deteriorated concrete structures, Oslo, Norway, June 2016](https://www.researchgate.net/publication/308612153_Replication_of_crack_pattern_in_FE_analysis_based_on_discretization_of_tension_softening_curves)

 To run the code you need to install [Diana FEA](https://dianafea.com/)

 Then use `MainProgram.py` to create and analyze a set of models. Change the absolute directory addresses based on your main folder address.
 For more information on running a python script in Diana, Look at [here](https://dianafea.com/manuals/d95/GetStart/node137.html).

 `runOnCluster.py` and `UNIQABatch.sh` was used to run the model on [C3SE clusters](https://www.c3se.chalmers.se/).

`MakeModels` includes scripts to make models automatically in Diana FEA.
`MakeGifAnimation` includes scripts to make an animation from the results of an analysis. [More information](https://www.youtube.com/watch?v=hIOJr6EWoNg)

 