# LendingClub Purpose / Application-Field Audit

No Shariah rules were created. This audit only records whether purpose-related fields exist and whether documentation places them at application time.

| column | availability | missingness_pct | unique_count | application_time_status |
| --- | --- | --- | --- | --- |
| purpose | PRESENT | 0.0 | 14 | SAFE_APPLICATION_TIME |
| title | PRESENT | 1.235975 | 61451 | SAFE_APPLICATION_TIME |
| desc | PRESENT | 91.162671 | 109539 | SAFE_APPLICATION_TIME |

`purpose` is a coarse category. `title` and `desc` are free text; raw examples are not published.
Details: `results/tables/lendingclub_purpose_audit.csv`.
