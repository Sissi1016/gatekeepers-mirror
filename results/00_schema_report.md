# Schema report for iclr26v1.parquet

rows: 55906

## columns

- `year`: int64; example: '2017'
- `id`: object; example: 'B1-Hhnslg'
- `title`: object; example: 'Prototypical Networks for Few-shot Learning'
- `abstract`: object; example: 'A recent approach to few-shot classification called matching networks has demons'
- `authors`: object; example: 'Jake Snell, Kevin Swersky, Richard Zemel'
- `author_ids`: object; example: ''
- `decision`: object; example: 'Reject'
- `scores`: object; example: '[6 4 5]'
- `keywords`: object; example: "['deep learning' 'transfer learning']"
- `labels`: object; example: 'transfer learning'

## column mapping used

- year: `year`
- id: `id`
- title: `title`
- abstract: `abstract`
- decision: `decision`
- scores: `scores`
- authors: `authors`
- author_ids: `author_ids`
- keywords: `keywords`
- label: `labels`

## year counts

year
2017      489
2018     1012
2019     1569
2020     2593
2021     3009
2022     3422
2023     4955
2024     7401
2025    11663
2026    19793

## decision (normalized) by year

decision  accept  desk_reject  reject  unknown  withdrawn
year                                                     
2017         198            0     291        0          0
2018         336            0     581        0         95
2019         502            0     917        0        150
2020         687           11    1526        0        369
2021         859           17    1735        0        398
2022        1094           26    1525        0        777
2023        1573           18    2226        0       1138
2024        2261           52    3487        0       1601
2025        3703           70    4944        0       2946
2026           0            0       0    19673        120

## raw decision values (top 30)

decision_raw
                            19673
Reject                      17096
Withdrawn                    7594
Accept (Poster)              6173
Accept (poster)              1809
Accept: poster               1202
Accept (Spotlight)            775
Accept (Oral)                 383
Accept (spotlight)            366
Accept: notable-top-25%       280
Desk rejected                 194
Invite to Workshop Track      136
Accept: notable-top-5%         91
Accept (oral)                  86
Accept (Talk)                  48

## score coverage

rows with >=1 score: 35617

## newcomer teams by year

year
2017    1.000
2018    0.547
2019    0.388
2020    0.275
2021    0.213
2022    0.178
2023    0.130
2024    0.117
2025    0.097
2026    0.001
