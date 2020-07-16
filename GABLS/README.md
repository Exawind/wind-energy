GABLS ABL COMPARISON
--------------------

Input files and data related to GABLS ABL runs.  General case
description can be found online at [metoffice
webpage](http://gabls.metoffice.com/description.html) and official
setup instructions at [description.pdf](description.pdf).


**Contents**: 

| Directory/File                 | Contents                                              |
|--------------------------------|-------------------------------------------------------|
| [gabls_data](gabls_data)       | Results from other LES codes                          |
| [NaluWindRun01](NaluWindRun01) | Fine mesh (incomplete run, ignore for now)            |
| [NaluWindRun02](NaluWindRun02) | 6.25m mesh with initial velocity perturbations        |
| [NaluWindRun03](NaluWindRun03) | 3.125m mesh with initial velocity perturbations       |
| [NaluWindRun04](NaluWindRun04) | 6.25m mesh **without** initial velocity perturbations |
|                                |                                                       |

The [gabls_data](gabls_data) is also available from the [met office
webpage](http://gabls.metoffice.com/lem_data.html), and more details
can also be found in the paper by 
[Beare et al](https://link.springer.com/content/pdf/10.1007/s10546-004-2820-6.pdf):
```
Beare, Robert J., et al. "An intercomparison of large-eddy simulations of the stable boundary layer." 
Boundary-Layer Meteorology 118.2 (2006): 247-272.
```

In each of the completed Nalu-Wind directories there is a Jupyter
workbook, e.g.
[postpro_gabls.ipynb](NaluWindRun03/postpro_gabls.ipynb), with a
comparison of results.
