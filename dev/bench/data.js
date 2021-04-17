window.BENCHMARK_DATA = {
  "lastUpdate": 1618667182988,
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
      },
      {
        "commit": {
          "author": {
            "email": "54404810+jankaWIS@users.noreply.github.com",
            "name": "Jan Kadlec",
            "username": "jankaWIS"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c7111d7b543e07807061758664dd07afc05b1a69",
          "message": "docs(config): update docs - customise plots in report (#742)\n\n* update docs - customise plots in report",
          "timestamp": "2021-04-07T20:26:24+02:00",
          "tree_id": "3451795f100451a2fe3fd73b6d7c1d3a4ea50eb4",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/c7111d7b543e07807061758664dd07afc05b1a69"
        },
        "date": 1617820353051,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.1140736563022748,
            "unit": "iter/sec",
            "range": "stddev: 0.014654173244440712",
            "extra": "mean: 8.766265870799993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11414081111457179,
            "unit": "iter/sec",
            "range": "stddev: 0.04154964031286578",
            "extra": "mean: 8.761108233199991 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.40655671681280214,
            "unit": "iter/sec",
            "range": "stddev: 0.009955421050557196",
            "extra": "mean: 2.459681413800001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05012206160453755,
            "unit": "iter/sec",
            "range": "stddev: 0.17769889826754584",
            "extra": "mean: 19.951294260199983 sec\nrounds: 5"
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
          "id": "6d2a418eba03eebfb1383f476dcd33860d124914",
          "message": "docs: benchmarks",
          "timestamp": "2021-04-07T21:17:49+02:00",
          "tree_id": "f9557de2f027488c71dfddaf998118c00f72a19d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/6d2a418eba03eebfb1383f476dcd33860d124914"
        },
        "date": 1617823582724,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07707805085611169,
            "unit": "iter/sec",
            "range": "stddev: 0.08508296928195308",
            "extra": "mean: 12.973862064399981 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.0787297938312109,
            "unit": "iter/sec",
            "range": "stddev: 0.10501215525839262",
            "extra": "mean: 12.701671772999987 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.27084117104573435,
            "unit": "iter/sec",
            "range": "stddev: 0.040444952336820855",
            "extra": "mean: 3.692200842800003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.035499120342227575,
            "unit": "iter/sec",
            "range": "stddev: 0.16675819949818468",
            "extra": "mean: 28.16971210439999 sec\nrounds: 5"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "ab5cd93b8fd243c4dfb77c5851102b3e5e83f911",
          "message": "refactor: Monotonicity formatter",
          "timestamp": "2021-04-07T21:25:38+02:00",
          "tree_id": "d78086ebcdbdc76b5338906ab4c319e3ea910a72",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/ab5cd93b8fd243c4dfb77c5851102b3e5e83f911"
        },
        "date": 1617823999959,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10683018565277348,
            "unit": "iter/sec",
            "range": "stddev: 0.028524504635106782",
            "extra": "mean: 9.360650212200005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10739378984844364,
            "unit": "iter/sec",
            "range": "stddev: 0.03876180720019812",
            "extra": "mean: 9.311525381600006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.38681757907765746,
            "unit": "iter/sec",
            "range": "stddev: 0.01069813821570168",
            "extra": "mean: 2.585197917800008 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04908206928848887,
            "unit": "iter/sec",
            "range": "stddev: 0.09656826565082856",
            "extra": "mean: 20.374039124599996 sec\nrounds: 5"
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
          "id": "b42b22ad827e9e0caba4f84315e96da9a87b52e0",
          "message": "ci: benchmark increase min rounds to 10",
          "timestamp": "2021-04-07T21:36:15+02:00",
          "tree_id": "395f398df55cc68e5c2ad683a9e26b21745a9212",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/b42b22ad827e9e0caba4f84315e96da9a87b52e0"
        },
        "date": 1617825459986,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08753306780852092,
            "unit": "iter/sec",
            "range": "stddev: 0.17548346919011237",
            "extra": "mean: 11.424253999500001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.0861594136546925,
            "unit": "iter/sec",
            "range": "stddev: 0.24207765457272312",
            "extra": "mean: 11.606392819799987 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.30424749776147547,
            "unit": "iter/sec",
            "range": "stddev: 0.03232030166648409",
            "extra": "mean: 3.2867977793000023 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0400358290619211,
            "unit": "iter/sec",
            "range": "stddev: 0.21724676670455945",
            "extra": "mean: 24.977626876499993 sec\nrounds: 10"
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
          "id": "0a2d1dbf866b3491105e36d798ec8b089c89895e",
          "message": "perf: performance improvements (#755)\n\n* perf: do not infer dtypes in minimal mode\r\n* perf: reuse duplicate row statistics and exclude in minimal mode\r\n* perf: take top-n values in categorical histograms\r\n* perf: reuse sorted values for frequency tables\r\n* fix: unused imports",
          "timestamp": "2021-04-07T23:39:29+02:00",
          "tree_id": "0a428f903a8cdf498a138ba5648016171fb22588",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/0a2d1dbf866b3491105e36d798ec8b089c89895e"
        },
        "date": 1617832635998,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09727349201777626,
            "unit": "iter/sec",
            "range": "stddev: 0.11803337695806652",
            "extra": "mean: 10.280293009500008 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09820464218396817,
            "unit": "iter/sec",
            "range": "stddev: 0.1517309123330746",
            "extra": "mean: 10.182818019200004 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3312982519898185,
            "unit": "iter/sec",
            "range": "stddev: 0.07030942587925809",
            "extra": "mean: 3.0184282409999925 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05521960367306819,
            "unit": "iter/sec",
            "range": "stddev: 0.202714789536184",
            "extra": "mean: 18.109510635399978 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "27856297+dependabot-preview[bot]@users.noreply.github.com",
            "name": "dependabot-preview[bot]",
            "username": "dependabot-preview[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "94acd76f751a239d10613f2616c6785cf4d1a521",
          "message": "build(deps): update pytest-benchmark requirement from ~=3.2.2 to ~=3.2.3 (#757)\n\nUpdates the requirements on [pytest-benchmark](https://github.com/ionelmc/pytest-benchmark) to permit the latest version.\r\n- [Release notes](https://github.com/ionelmc/pytest-benchmark/releases)\r\n- [Changelog](https://github.com/ionelmc/pytest-benchmark/blob/master/CHANGELOG.rst)\r\n- [Commits](https://github.com/ionelmc/pytest-benchmark/compare/v3.2.2...v3.2.3)",
          "timestamp": "2021-04-08T13:29:13+02:00",
          "tree_id": "63aded0bf668377faa2a85c3012dacf6c4ee8a79",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/94acd76f751a239d10613f2616c6785cf4d1a521"
        },
        "date": 1617882667356,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0783662923537148,
            "unit": "iter/sec",
            "range": "stddev: 0.10782405771022217",
            "extra": "mean: 12.760588385199991 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08128959371712803,
            "unit": "iter/sec",
            "range": "stddev: 0.12816874416431287",
            "extra": "mean: 12.301697600799992 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.26186843261216847,
            "unit": "iter/sec",
            "range": "stddev: 0.02510973106170561",
            "extra": "mean: 3.8187115186999905 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04282149431921343,
            "unit": "iter/sec",
            "range": "stddev: 0.08393203439401889",
            "extra": "mean: 23.3527581393 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "66853113+pre-commit-ci[bot]@users.noreply.github.com",
            "name": "pre-commit-ci[bot]",
            "username": "pre-commit-ci[bot]"
          },
          "committer": {
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "e91019fc82acfac96720398f326ace8bb2cfdd8a",
          "message": "[pre-commit.ci] pre-commit autoupdate",
          "timestamp": "2021-04-15T10:23:14+02:00",
          "tree_id": "14dae48915a57c60f056098f60bbcba78b1aa429",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/e91019fc82acfac96720398f326ace8bb2cfdd8a"
        },
        "date": 1618476455329,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0708250748921598,
            "unit": "iter/sec",
            "range": "stddev: 0.24001784114867222",
            "extra": "mean: 14.119293223800009 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07165851240334967,
            "unit": "iter/sec",
            "range": "stddev: 0.24847235310689383",
            "extra": "mean: 13.955076186500003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2380057743200684,
            "unit": "iter/sec",
            "range": "stddev: 0.14858014379626502",
            "extra": "mean: 4.201578734199984 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.03863063479638454,
            "unit": "iter/sec",
            "range": "stddev: 0.29439803927464697",
            "extra": "mean: 25.88619123840001 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "7520bd73849ddbcf2c597b887204f08be85ff5cc",
          "message": "fix: banking example dataset's link dead, replaced with original source",
          "timestamp": "2021-04-16T15:30:00+02:00",
          "tree_id": "a85fdbf50fcfd2fd087853feec6c68afc495bb92",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/7520bd73849ddbcf2c597b887204f08be85ff5cc"
        },
        "date": 1618580758431,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10996883948740993,
            "unit": "iter/sec",
            "range": "stddev: 0.028902007217174744",
            "extra": "mean: 9.09348506959999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11087526924493316,
            "unit": "iter/sec",
            "range": "stddev: 0.046766365029035376",
            "extra": "mean: 9.019143825399988 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.37709414109849304,
            "unit": "iter/sec",
            "range": "stddev: 0.049004910879137886",
            "extra": "mean: 2.651857695499996 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06077296429327064,
            "unit": "iter/sec",
            "range": "stddev: 0.07336016049910782",
            "extra": "mean: 16.45468526389998 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "01bba41db88dc80dbc2fe83524793c18dcabbfcf",
          "message": "ci: commitlint conventional commits",
          "timestamp": "2021-04-16T17:09:32+02:00",
          "tree_id": "37c7a5bd2de792f656d18ed530772e3061dbf499",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/01bba41db88dc80dbc2fe83524793c18dcabbfcf"
        },
        "date": 1618586707137,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11090615608857031,
            "unit": "iter/sec",
            "range": "stddev: 0.030018191558607393",
            "extra": "mean: 9.016632036199994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11156768449875118,
            "unit": "iter/sec",
            "range": "stddev: 0.02210147135524629",
            "extra": "mean: 8.963168900499976 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3742289697805497,
            "unit": "iter/sec",
            "range": "stddev: 0.056240028690051555",
            "extra": "mean: 2.672160844699988 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06226931193204755,
            "unit": "iter/sec",
            "range": "stddev: 0.05081390439647024",
            "extra": "mean: 16.059274929699995 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "7592a082d403ab0df37ee4c2f95bd6a6623a08cb",
          "message": "feat: add RDW example",
          "timestamp": "2021-04-17T15:29:20+02:00",
          "tree_id": "f10f83a4f8a42bff095f0118ecfb35c355347c2d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/7592a082d403ab0df37ee4c2f95bd6a6623a08cb"
        },
        "date": 1618667177034,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10488613349708324,
            "unit": "iter/sec",
            "range": "stddev: 0.3811508273565195",
            "extra": "mean: 9.534148763599992 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10388984246555259,
            "unit": "iter/sec",
            "range": "stddev: 0.4450039847804693",
            "extra": "mean: 9.625580097799997 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3339536204800451,
            "unit": "iter/sec",
            "range": "stddev: 0.10764009940272985",
            "extra": "mean: 2.9944277847999956 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05641295592285948,
            "unit": "iter/sec",
            "range": "stddev: 0.5182249839487716",
            "extra": "mean: 17.726424429299993 sec\nrounds: 10"
          }
        ]
      }
    ]
  }
}