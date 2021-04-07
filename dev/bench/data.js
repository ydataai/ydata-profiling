window.BENCHMARK_DATA = {
  "lastUpdate": 1617817935228,
  "repoUrl": "https://github.com/pandas-profiling/pandas-profiling",
  "entries": {
    "Pandas Profiling Benchmarks": [
      {
        "commit": {
          "author": {
            "email": "sfbbrugman@gmail.com",
            "name": "sbrugman",
            "username": "sbrugman"
          },
          "committer": {
            "email": "sfbbrugman@gmail.com",
            "name": "sbrugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "011e3f77a4a22882b4f8ccd1b7e0c505142009c8",
          "message": "ci(benchmark): github actions SIGKILL due to memory usage of benchmarks",
          "timestamp": "2021-04-07T18:54:37+02:00",
          "tree_id": "caf20b40961d5ab00095b9fee41f8ed3a70e704f",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/011e3f77a4a22882b4f8ccd1b7e0c505142009c8"
        },
        "date": 1617814814263,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07647946069634827,
            "unit": "iter/sec",
            "range": "stddev: 0.08550454823133359",
            "extra": "mean: 13.07540600960001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07511037759876639,
            "unit": "iter/sec",
            "range": "stddev: 0.13246235047667185",
            "extra": "mean: 13.313739485400003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2578540335612629,
            "unit": "iter/sec",
            "range": "stddev: 0.01974421087856087",
            "extra": "mean: 3.878163107199998 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bbea211ee34763b5a713917fc5a99e8d840f48bb",
          "message": "Split tests and coverage in CI/CD (#754)\n\n* Split tests and coverage in CI/CD\r\n\r\nCo-authored-by: chanedwin <edwinchan@u.nus.edu>",
          "timestamp": "2021-04-07T19:09:24+02:00",
          "tree_id": "4a4e9a11a27d77f0a504d49c42398b2b82ef075f",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/bbea211ee34763b5a713917fc5a99e8d840f48bb"
        },
        "date": 1617815629119,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09528599312196534,
            "unit": "iter/sec",
            "range": "stddev: 0.046725770567867884",
            "extra": "mean: 10.494721912800003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09621246824237442,
            "unit": "iter/sec",
            "range": "stddev: 0.020040485298812204",
            "extra": "mean: 10.3936632982 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.34419827978019574,
            "unit": "iter/sec",
            "range": "stddev: 0.010350385961682996",
            "extra": "mean: 2.905302143400013 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "sfbbrugman@gmail.com",
            "name": "sbrugman",
            "username": "sbrugman"
          },
          "committer": {
            "email": "sfbbrugman@gmail.com",
            "name": "sbrugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "1780bc2996d40d224139e9f4944ba33f6ffac2f5",
          "message": "Merge branch 'develop' of https://github.com/pandas-profiling/pandas-profiling into develop",
          "timestamp": "2021-04-07T19:39:31+02:00",
          "tree_id": "723c7a0ab0aa04a924d8f175c14ff133b0cdc81a",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/1780bc2996d40d224139e9f4944ba33f6ffac2f5"
        },
        "date": 1617817412367,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11387477764480958,
            "unit": "iter/sec",
            "range": "stddev: 0.1219784785317657",
            "extra": "mean: 8.781575873800005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11298269833978357,
            "unit": "iter/sec",
            "range": "stddev: 0.11822176817063018",
            "extra": "mean: 8.850912703399995 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4082012579467626,
            "unit": "iter/sec",
            "range": "stddev: 0.07455069344379953",
            "extra": "mean: 2.449771970400002 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "sfbbrugman@gmail.com",
            "name": "sbrugman",
            "username": "sbrugman"
          },
          "committer": {
            "email": "sfbbrugman@gmail.com",
            "name": "sbrugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "6f90be0cd74708d490ce27b019c5dd74ba0f80c0",
          "message": "ci(benchmark): add RDW 100k sample",
          "timestamp": "2021-04-07T19:45:47+02:00",
          "tree_id": "5834d4669ae671dd5c54d4f180a32fc7e4bb4b16",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/6f90be0cd74708d490ce27b019c5dd74ba0f80c0"
        },
        "date": 1617817929257,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11098109083926899,
            "unit": "iter/sec",
            "range": "stddev: 0.3350029587565377",
            "extra": "mean: 9.010543980399992 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.1100625799170337,
            "unit": "iter/sec",
            "range": "stddev: 0.30829952048622317",
            "extra": "mean: 9.085740137599993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.40530164196313456,
            "unit": "iter/sec",
            "range": "stddev: 0.02881320843783394",
            "extra": "mean: 2.467298171200002 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04870599924501749,
            "unit": "iter/sec",
            "range": "stddev: 0.4232692085979508",
            "extra": "mean: 20.531351691800012 sec\nrounds: 5"
          }
        ]
      }
    ]
  }
}