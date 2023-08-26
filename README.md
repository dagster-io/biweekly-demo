# Population Analysis

Collection of Dagster assets and jobs which represent and forecast population growth.

# Notes

Couple notes if you end up using it:

* Un-comment the lines in transformations.py to build your dbt manifest.
* There are AMPs on the population and dbt assets. I omitted adding it to the forecasting group because the features are partitioned and it gets wonky explaining partitions and AMPs together
* The finished state and starter state are in two code locations. This'll break once you add a key prefix to the assets in the starter state, so change the code based on how you demo. I usually only write the population assets, then jump to the finished state to discuss everything else.