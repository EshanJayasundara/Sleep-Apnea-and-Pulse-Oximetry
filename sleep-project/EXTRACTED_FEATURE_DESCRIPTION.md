#### Extracted Features

_Statistical Features_

| #   | Feature | Category           | Description                                     |
| --- | ------- | ------------------ | ----------------------------------------------- |
| 1   | AV      | General Statistics | Mean SpO₂ over the entire signal                |
| 2   | MED     | General Statistics | Median SpO₂                                     |
| 3   | Min     | General Statistics | Minimum SpO₂ value                              |
| 4   | SD      | General Statistics | Standard deviation of SpO₂                      |
| 5   | RG      | General Statistics | Range (max - min) of SpO₂                       |
| 6   | Px      | General Statistics | xth percentile of SpO₂ values                   |
| 7   | Mx      | General Statistics | % of signal below median oxygen saturation      |
| 8   | ZCx     | General Statistics | Number of zero-crossings at x% level            |
| 9   | ∆Ix     | General Statistics | Mean difference between consecutive SpO₂ values |

_Periodicity Features_

| #   | Feature       | Category           | Description                                   |
| --- | ------------- | ------------------ | --------------------------------------------- |
| 10  | PRSADc_win10  | Periodicity (PRSA) | PRSA capacity with window size 10             |
| 11  | PRSADad_win10 | Periodicity (PRSA) | PRSA amplitude difference with window size 10 |
| 12  | PRSADos_win10 | Periodicity (PRSA) | PRSA overall slope with window size 10        |
| 13  | PRSADsb_win10 | Periodicity (PRSA) | PRSA slope before anchor with window size 10  |
| 14  | PRSADsa_win10 | Periodicity (PRSA) | PRSA slope after anchor with window size 10   |
| 15  | PRSADc_win20  | Periodicity (PRSA) | PRSA capacity with window size 20             |
| 16  | PRSADad_win20 | Periodicity (PRSA) | PRSA amplitude difference with window size 20 |
| 17  | PRSADos_win20 | Periodicity (PRSA) | PRSA overall slope with window size 20        |
| 18  | PRSADsb_win20 | Periodicity (PRSA) | PRSA slope before anchor with window size 20  |
| 19  | PRSADsa_win20 | Periodicity (PRSA) | PRSA slope after anchor with window size 20   |
| 20  | AC            | Periodicity        | Autocorrelation of SpO₂                       |
| 21  | PSDtotal      | Periodicity (PSD)  | Total power of the PSD                        |
| 22  | PSDband       | Periodicity (PSD)  | Power in 0.014–0.033 Hz band                  |
| 23  | PSDratio      | Periodicity (PSD)  | PSDband / PSDtotal                            |
| 24  | PSDpeak       | Periodicity (PSD)  | Peak amplitude in 0.014–0.033 Hz band         |

_Desaturation Features_

| #   | Feature      | Category     | Description                                  |
| --- | ------------ | ------------ | -------------------------------------------- |
| 25  | ODIx_thr3    | Desaturation | Oxygen Desaturation Index (threshold 3%)     |
| 26  | DLµ_thr3     | Desaturation | Mean duration (threshold 3%)                 |
| 27  | DLσ_thr3     | Desaturation | Std duration (threshold 3%)                  |
| 28  | DDmaxµ_thr3  | Desaturation | Mean depth (threshold 3%)                    |
| 29  | DDmaxσ_thr3  | Desaturation | Std depth (threshold 3%)                     |
| 30  | DD100µ_thr3  | Desaturation | Mean depth from 100% (threshold 3%)          |
| 31  | DD100σ_thr3  | Desaturation | Std depth from 100% (threshold 3%)           |
| 32  | DSµ_thr3     | Desaturation | Mean slope (threshold 3%)                    |
| 33  | DSσ_thr3     | Desaturation | Std slope (threshold 3%)                     |
| 34  | DAmaxµ_thr3  | Desaturation | Mean area from max baseline (threshold 3%)   |
| 35  | DAmaxσ_thr3  | Desaturation | Std area from max baseline (threshold 3%)    |
| 36  | DA100µ_thr3  | Desaturation | Mean area under 100% baseline (threshold 3%) |
| 37  | DA100σ_thr3  | Desaturation | Std area under 100% baseline (threshold 3%)  |
| 38  | TDµ_thr3     | Desaturation | Mean time between events (threshold 3%)      |
| 39  | TDσ_thr3     | Desaturation | Std time between events (threshold 3%)       |
| 40  | ODIx_thr5    | Desaturation | Oxygen Desaturation Index (threshold 5%)     |
| 41  | DLµ_thr5     | Desaturation | Mean duration (threshold 5%)                 |
| 42  | DLσ_thr5     | Desaturation | Std duration (threshold 5%)                  |
| 43  | DDmaxµ_thr5  | Desaturation | Mean depth (threshold 5%)                    |
| 44  | DDmaxσ_thr5  | Desaturation | Std depth (threshold 5%)                     |
| 45  | DD100µ_thr5  | Desaturation | Mean depth from 100% (threshold 5%)          |
| 46  | DD100σ_thr5  | Desaturation | Std depth from 100% (threshold 5%)           |
| 47  | DSµ_thr5     | Desaturation | Mean slope (threshold 5%)                    |
| 48  | DSσ_thr5     | Desaturation | Std slope (threshold 5%)                     |
| 49  | DAmaxµ_thr5  | Desaturation | Mean area from max baseline (threshold 5%)   |
| 50  | DAmaxσ_thr5  | Desaturation | Std area from max baseline (threshold 5%)    |
| 51  | DA100µ_thr5  | Desaturation | Mean area under 100% baseline (threshold 5%) |
| 52  | DA100σ_thr5  | Desaturation | Std area under 100% baseline (threshold 5%)  |
| 53  | TDµ_thr5     | Desaturation | Mean time between events (threshold 5%)      |
| 54  | TDσ_thr5     | Desaturation | Std time between events (threshold 5%)       |
| 55  | DLµ_thr83    | Desaturation | Mean duration (threshold 83)                 |
| 56  | DLσ_thr83    | Desaturation | Std duration (threshold 83)                  |
| 57  | DDmaxµ_thr83 | Desaturation | Mean depth (threshold 83)                    |
| 58  | DDmaxσ_thr83 | Desaturation | Std depth (threshold 83)                     |
| 59  | DD100µ_thr83 | Desaturation | Mean depth from 100% (threshold 83)          |
| 60  | DD100σ_thr83 | Desaturation | Std depth from 100% (threshold 83)           |
| 61  | DSµ_thr83    | Desaturation | Mean slope (threshold 83)                    |
| 62  | DSσ_thr83    | Desaturation | Std slope (threshold 83)                     |
| 63  | DAmaxµ_thr83 | Desaturation | Mean area from max baseline (threshold 83)   |
| 64  | DAmaxσ_thr83 | Desaturation | Std area from max baseline (threshold 83)    |
| 65  | DA100µ_thr83 | Desaturation | Mean area under 100% baseline (threshold 83) |
| 66  | DA100σ_thr83 | Desaturation | Std area under 100% baseline (threshold 83)  |
| 67  | TDµ_thr83    | Desaturation | Mean time between events (threshold 83)      |
| 68  | TDσ_thr83    | Desaturation | Std time between events (threshold 83)       |
| 69  | DLµ_thr85    | Desaturation | Mean duration (threshold 85)                 |
| 70  | DLσ_thr85    | Desaturation | Std duration (threshold 85)                  |
| 71  | DDmaxµ_thr85 | Desaturation | Mean depth (threshold 85)                    |
| 72  | DDmaxσ_thr85 | Desaturation | Std depth (threshold 85)                     |
| 73  | DD100µ_thr85 | Desaturation | Mean depth from 100% (threshold 85)          |
| 74  | DD100σ_thr85 | Desaturation | Std depth from 100% (threshold 85)           |
| 75  | DSµ_thr85    | Desaturation | Mean slope (threshold 85)                    |
| 76  | DSσ_thr85    | Desaturation | Std slope (threshold 85)                     |
| 77  | DAmaxµ_thr85 | Desaturation | Mean area from max baseline (threshold 85)   |
| 78  | DAmaxσ_thr85 | Desaturation | Std area from max baseline (threshold 85)    |
| 79  | DA100µ_thr85 | Desaturation | Mean area under 100% baseline (threshold 85) |
| 80  | DA100σ_thr85 | Desaturation | Std area under 100% baseline (threshold 85)  |
| 81  | TDµ_thr85    | Desaturation | Mean time between events (threshold 85)      |
| 82  | TDσ_thr85    | Desaturation | Std time between events (threshold 85)       |
| 83  | DLµ_thr90    | Desaturation | Mean duration (threshold 90)                 |
| 84  | DLσ_thr90    | Desaturation | Std duration (threshold 90)                  |
| 85  | DDmaxµ_thr90 | Desaturation | Mean depth (threshold 90)                    |
| 86  | DDmaxσ_thr90 | Desaturation | Std depth (threshold 90)                     |
| 87  | DD100µ_thr90 | Desaturation | Mean depth from 100% (threshold 90)          |
| 88  | DD100σ_thr90 | Desaturation | Std depth from 100% (threshold 90)           |
| 89  | DSµ_thr90    | Desaturation | Mean slope (threshold 90)                    |
| 90  | DSσ_thr90    | Desaturation | Std slope (threshold 90)                     |
| 91  | DAmaxµ_thr90 | Desaturation | Mean area from max baseline (threshold 90)   |
| 92  | DAmaxσ_thr90 | Desaturation | Std area from max baseline (threshold 90)    |
| 93  | DA100µ_thr90 | Desaturation | Mean area under 100% baseline (threshold 90) |
| 94  | DA100σ_thr90 | Desaturation | Std area under 100% baseline (threshold 90)  |
| 95  | TDµ_thr90    | Desaturation | Mean time between events (threshold 90)      |
| 96  | TDσ_thr90    | Desaturation | Std time between events (threshold 90)       |

`relstive threshold`: to calculate dofferent features of quick desaturation events within the signal. For example, if SpO2 quickly drops from 3%, calculate the count of such events per hour (ODI), mean desaturation of those events (DLµ) and etc.

`hard threshold`: to calculate dofferent features of the signal when the saturation goes below the hard threshold (when spo2 goes below threshold, it is considered as a desaturation event). For example, if SpO2 goes below 83 it is considerd as desaturation event, calculate the mean desaturation of those events (DLµ) and etc.

_Hypoxic Burden Features_

| #   | Feature     | Category       | Description                                        |
| --- | ----------- | -------------- | -------------------------------------------------- |
| 97  | PODx_tr3    | Hypoxic Burden | Time under desaturation (threshold 3), normalized  |
| 98  | AODmax_tr3  | Hypoxic Burden | Area under curve from max (threshold 3)            |
| 99  | AOD100_tr3  | Hypoxic Burden | Area under 100% (threshold 3)                      |
| 100 | CTx_tr3     | Hypoxic Burden | Cumulative time under x% (threshold 3)             |
| 101 | CAx_tr3     | Hypoxic Burden | Integral under x% (threshold 3)                    |
| 102 | PODx_tr5    | Hypoxic Burden | Time under desaturation (threshold 5), normalized  |
| 103 | AODmax_tr5  | Hypoxic Burden | Area under curve from max (threshold 5)            |
| 104 | AOD100_tr5  | Hypoxic Burden | Area under 100% (threshold 5)                      |
| 105 | CTx_tr5     | Hypoxic Burden | Cumulative time under x% (threshold 5)             |
| 106 | CAx_tr5     | Hypoxic Burden | Integral under x% (threshold 5)                    |
| 107 | PODx_tr83   | Hypoxic Burden | Time under desaturation (threshold 83), normalized |
| 108 | AODmax_tr83 | Hypoxic Burden | Area under curve from max (threshold 83)           |
| 109 | AOD100_tr83 | Hypoxic Burden | Area under 100% (threshold 83)                     |
| 110 | CTx_tr83    | Hypoxic Burden | Cumulative time under x% (threshold 83)            |
| 111 | CAx_tr83    | Hypoxic Burden | Integral under x% (threshold 83)                   |
| 112 | PODx_tr85   | Hypoxic Burden | Time under desaturation (threshold 85), normalized |
| 113 | AODmax_tr85 | Hypoxic Burden | Area under curve from max (threshold 85)           |
| 114 | AOD100_tr85 | Hypoxic Burden | Area under 100% (threshold 85)                     |
| 115 | CTx_tr85    | Hypoxic Burden | Cumulative time under x% (threshold 85)            |
| 116 | CAx_tr85    | Hypoxic Burden | Integral under x% (threshold 85)                   |
| 117 | PODx_tr90   | Hypoxic Burden | Time under desaturation (threshold 90), normalized |
| 118 | AODmax_tr90 | Hypoxic Burden | Area under curve from max (threshold 90)           |
| 119 | AOD100_tr90 | Hypoxic Burden | Area under 100% (threshold 90)                     |
| 120 | CTx_tr90    | Hypoxic Burden | Cumulative time under x% (threshold 90)            |
| 121 | CAx_tr90    | Hypoxic Burden | Integral under x% (threshold 90)                   |
