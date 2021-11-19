window.BENCHMARK_DATA = {
  "lastUpdate": 1637345571732,
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
          "id": "caa9a903568eecf9854c53bb68bb338da617af1c",
          "message": "chore: merge",
          "timestamp": "2021-04-18T14:24:30+02:00",
          "tree_id": "f10f83a4f8a42bff095f0118ecfb35c355347c2d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/caa9a903568eecf9854c53bb68bb338da617af1c"
        },
        "date": 1618749840764,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0915807149580639,
            "unit": "iter/sec",
            "range": "stddev: 0.05582962772915735",
            "extra": "mean: 10.91932947300001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.0858999976299177,
            "unit": "iter/sec",
            "range": "stddev: 0.23896140715358785",
            "extra": "mean: 11.641443860200003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2896061974388951,
            "unit": "iter/sec",
            "range": "stddev: 0.04559420630815801",
            "extra": "mean: 3.4529647806000185 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04797064181830628,
            "unit": "iter/sec",
            "range": "stddev: 0.29682089444192183",
            "extra": "mean: 20.84608339800002 sec\nrounds: 10"
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
          "id": "4d676361e7b164e1d192ed5ffb87223ec3680296",
          "message": "build(deps): update pytest-benchmark requirement from ~=3.2.3 to ~=3.4.1 (#764)\n\nUpdates the requirements on [pytest-benchmark](https://github.com/ionelmc/pytest-benchmark) to permit the latest version.\r\n- [Release notes](https://github.com/ionelmc/pytest-benchmark/releases)\r\n- [Changelog](https://github.com/ionelmc/pytest-benchmark/blob/master/CHANGELOG.rst)\r\n- [Commits](https://github.com/ionelmc/pytest-benchmark/compare/v3.2.3...v3.4.1)",
          "timestamp": "2021-04-19T09:00:07+02:00",
          "tree_id": "d599b7cf753c35155b6080d4cdcb39ecb7ce5596",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/4d676361e7b164e1d192ed5ffb87223ec3680296"
        },
        "date": 1618816934791,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07695119597036089,
            "unit": "iter/sec",
            "range": "stddev: 0.11216246736225208",
            "extra": "mean: 12.995249617500003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07832454383004385,
            "unit": "iter/sec",
            "range": "stddev: 0.08983259273490196",
            "extra": "mean: 12.767390030000001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2553128594831377,
            "unit": "iter/sec",
            "range": "stddev: 0.08498839056272596",
            "extra": "mean: 3.9167631510000205 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.042169826171353175,
            "unit": "iter/sec",
            "range": "stddev: 0.18322400692061014",
            "extra": "mean: 23.71363818139996 sec\nrounds: 10"
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
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b91771d7995c349430ea4b115477ed3707eae49a",
          "message": "build: pre-commit autoupdate (#765)\n\nbuild: pre-commit autoupdate (#765)\r\n\r\n- [github.com/nbQA-dev/nbQA: 0.6.0 → 0.7.0](https://github.com/nbQA-dev/nbQA/compare/0.6.0...0.7.0)\r\n- [github.com/PyCQA/flake8: 3.9.0 → 3.9.1](https://github.com/PyCQA/flake8/compare/3.9.0...3.9.1)",
          "timestamp": "2021-04-19T20:56:58+02:00",
          "tree_id": "55313ae5fb6d4ff1eadd6850d7d250126f636798",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/b91771d7995c349430ea4b115477ed3707eae49a"
        },
        "date": 1618859770344,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09058826361268033,
            "unit": "iter/sec",
            "range": "stddev: 0.07825543820496805",
            "extra": "mean: 11.038957588099994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.090711246688242,
            "unit": "iter/sec",
            "range": "stddev: 0.0844299027248511",
            "extra": "mean: 11.0239913628 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2845612818485304,
            "unit": "iter/sec",
            "range": "stddev: 0.030837985429857898",
            "extra": "mean: 3.5141815270999928 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.048011722531495465,
            "unit": "iter/sec",
            "range": "stddev: 0.6136125436189179",
            "extra": "mean: 20.828246671300008 sec\nrounds: 10"
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
          "id": "16689a662e28f9468586d523754a95878bd885e4",
          "message": "test: skip test if dataset is unavailable\n\nCI will not be blocked if the UCI ML repository is down.",
          "timestamp": "2021-05-05T16:51:07+02:00",
          "tree_id": "b029a1a84eece8f44f80badcab6a9ed59b0e1383",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/16689a662e28f9468586d523754a95878bd885e4"
        },
        "date": 1620227213445,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11168471809007288,
            "unit": "iter/sec",
            "range": "stddev: 0.015784748867532127",
            "extra": "mean: 8.953776461999999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11186111743308753,
            "unit": "iter/sec",
            "range": "stddev: 0.016327755009562052",
            "extra": "mean: 8.93965680789998 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.37536386627398394,
            "unit": "iter/sec",
            "range": "stddev: 0.04489034481397876",
            "extra": "mean: 2.6640816814000003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06124466631903344,
            "unit": "iter/sec",
            "range": "stddev: 0.0963140347702214",
            "extra": "mean: 16.32795245860002 sec\nrounds: 10"
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
          "id": "ad765be82ba4c9338f3659480abbfd68e44918dd",
          "message": "test: skip test if dataset is unavailable\n\nCI will not be blocked if the UCI ML repository is down.",
          "timestamp": "2021-05-05T17:31:04+02:00",
          "tree_id": "d6b7cc59ec24b6c4d23bfa45e162b31071252882",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/ad765be82ba4c9338f3659480abbfd68e44918dd"
        },
        "date": 1620229827465,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09103056991697629,
            "unit": "iter/sec",
            "range": "stddev: 0.0945308820824282",
            "extra": "mean: 10.985320655600002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09197562213764704,
            "unit": "iter/sec",
            "range": "stddev: 0.06689696774910624",
            "extra": "mean: 10.872446163000017 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3077717050837234,
            "unit": "iter/sec",
            "range": "stddev: 0.05756907113011046",
            "extra": "mean: 3.249161581399983 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04904282476614554,
            "unit": "iter/sec",
            "range": "stddev: 0.14685645343927908",
            "extra": "mean: 20.39034261930002 sec\nrounds: 10"
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
          "id": "1d4c9b58b132f8cd56fae0d5f57635bf675e86ca",
          "message": "chore: update changelog",
          "timestamp": "2021-05-05T17:50:56+02:00",
          "tree_id": "617a96ce437dcd50b33096c8faf640ab21a2045d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/1d4c9b58b132f8cd56fae0d5f57635bf675e86ca"
        },
        "date": 1620231269937,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07274872836899486,
            "unit": "iter/sec",
            "range": "stddev: 0.17417363899624702",
            "extra": "mean: 13.745944739100002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07429356886061063,
            "unit": "iter/sec",
            "range": "stddev: 0.13804018548922",
            "extra": "mean: 13.46011526079999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2441572999838877,
            "unit": "iter/sec",
            "range": "stddev: 0.09799054822847966",
            "extra": "mean: 4.095720259300014 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.03970646341083946,
            "unit": "iter/sec",
            "range": "stddev: 0.2126523333151881",
            "extra": "mean: 25.184816629299963 sec\nrounds: 10"
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
          "id": "662fdad8dbc3ef47d54a8a9532bc8d74d5f8ec54",
          "message": "Merge pull request #762 from pandas-profiling/develop\n\nv2.12.0 release",
          "timestamp": "2021-05-05T18:26:55+02:00",
          "tree_id": "617a96ce437dcd50b33096c8faf640ab21a2045d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/662fdad8dbc3ef47d54a8a9532bc8d74d5f8ec54"
        },
        "date": 1620233277017,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08106939846783359,
            "unit": "iter/sec",
            "range": "stddev: 0.0989138455113763",
            "extra": "mean: 12.3351106447 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08177942992487176,
            "unit": "iter/sec",
            "range": "stddev: 0.19249808789215703",
            "extra": "mean: 12.228013828399991 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2759590820953517,
            "unit": "iter/sec",
            "range": "stddev: 0.043573987621462695",
            "extra": "mean: 3.6237256350000164 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04499363561552959,
            "unit": "iter/sec",
            "range": "stddev: 0.08087478455713736",
            "extra": "mean: 22.225365572700003 sec\nrounds: 10"
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
          "id": "2f686b5c6d4c24515ace17920ac365ccb0186607",
          "message": "ci: flake8 stronger qa\n\n- blacklist (ignore) instead of whitelist\n- additional dependencies: comprehensions, sfs, simplify, eradicate, print",
          "timestamp": "2021-05-05T18:28:12+02:00",
          "tree_id": "9a555b3c7bb6c932c93788948ae084935e7150f4",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/2f686b5c6d4c24515ace17920ac365ccb0186607"
        },
        "date": 1620233689531,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08800313356270772,
            "unit": "iter/sec",
            "range": "stddev: 0.09660143582431746",
            "extra": "mean: 11.363231734099987 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08863388705365272,
            "unit": "iter/sec",
            "range": "stddev: 0.09434592954988856",
            "extra": "mean: 11.28236652190003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.28017906542405835,
            "unit": "iter/sec",
            "range": "stddev: 0.06051942435230497",
            "extra": "mean: 3.569146033400011 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04696434433640822,
            "unit": "iter/sec",
            "range": "stddev: 0.20784053841601757",
            "extra": "mean: 21.292749087199944 sec\nrounds: 10"
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
          "id": "7303bd8a7c6ad19321a96e50e1b4cb81defbe3ce",
          "message": "ci: migrate dependabot",
          "timestamp": "2021-05-05T18:53:42+02:00",
          "tree_id": "4d7350347507b414e71c5d4e5d04fd5e932ae8e8",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/7303bd8a7c6ad19321a96e50e1b4cb81defbe3ce"
        },
        "date": 1620234583152,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10649864743007369,
            "unit": "iter/sec",
            "range": "stddev: 0.5466780301478531",
            "extra": "mean: 9.389790613599985 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11168556706377257,
            "unit": "iter/sec",
            "range": "stddev: 0.25864077994621604",
            "extra": "mean: 8.953708400199991 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3722184015099269,
            "unit": "iter/sec",
            "range": "stddev: 0.07615180733793321",
            "extra": "mean: 2.68659474100001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06077300961259465,
            "unit": "iter/sec",
            "range": "stddev: 0.46101203137145336",
            "extra": "mean: 16.454672993400003 sec\nrounds: 10"
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
          "id": "02bbbdb764019a4db407518eed37cda94af735bd",
          "message": "feat: configurable numeric precision",
          "timestamp": "2021-05-05T19:27:40+02:00",
          "tree_id": "6c55c859fd0fbb30e2496ea60c81495d9cf8e4dc",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/02bbbdb764019a4db407518eed37cda94af735bd"
        },
        "date": 1620236586010,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11237323674703767,
            "unit": "iter/sec",
            "range": "stddev: 0.019837703498433345",
            "extra": "mean: 8.89891604929998 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11265715774883328,
            "unit": "iter/sec",
            "range": "stddev: 0.018226486766941476",
            "extra": "mean: 8.876488808899996 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3830811855306876,
            "unit": "iter/sec",
            "range": "stddev: 0.04395222987733586",
            "extra": "mean: 2.61041272130002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06306286842156482,
            "unit": "iter/sec",
            "range": "stddev: 0.09500337470640795",
            "extra": "mean: 15.857191799700036 sec\nrounds: 10"
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
          "id": "d9dee084a6db37eb7de836a97e53ee3813679c5d",
          "message": "build: bump visions frm 0.6.0 to 0.7.1\n\nBumps [visions](https://github.com/dylan-profiler/visions) from 0.6.0 to 0.7.1.\n- [Release notes](https://github.com/dylan-profiler/visions/releases)\n- [Commits](https://github.com/dylan-profiler/visions/compare/v0.6.0...v0.7.1)\n\nCo-authored-by: ieaves <ian.k.eaves@gmail.com>",
          "timestamp": "2021-05-05T20:26:41+02:00",
          "tree_id": "22507ee627264a71627b389aa60121a6bf135389",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/d9dee084a6db37eb7de836a97e53ee3813679c5d"
        },
        "date": 1620240552638,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07691253816594155,
            "unit": "iter/sec",
            "range": "stddev: 0.08012960890667904",
            "extra": "mean: 13.001781294 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07864874279314084,
            "unit": "iter/sec",
            "range": "stddev: 0.09045425464937773",
            "extra": "mean: 12.714761412400003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2591779483137732,
            "unit": "iter/sec",
            "range": "stddev: 0.04282349700375245",
            "extra": "mean: 3.858352944400008 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0421683674246334,
            "unit": "iter/sec",
            "range": "stddev: 0.08277561332170416",
            "extra": "mean: 23.71445851650003 sec\nrounds: 10"
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
          "id": "4ed5c64e32035ec505d8aa99dc6d719e49840d51",
          "message": "build: update coverage requirement from <5 to ~=5.5\n\nUpdates the requirements on [coverage](https://github.com/nedbat/coveragepy) to permit the latest version.\n- [Release notes](https://github.com/nedbat/coveragepy/releases)\n- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)\n- [Commits](nedbat/coveragepy@coverage-3.0b1...coverage-5.5)",
          "timestamp": "2021-05-05T20:39:55+02:00",
          "tree_id": "236f659b8a8e47040d000a4e3cac4b9e80e1c9cb",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/4ed5c64e32035ec505d8aa99dc6d719e49840d51"
        },
        "date": 1620241094644,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09520968774118614,
            "unit": "iter/sec",
            "range": "stddev: 0.14570122236852592",
            "extra": "mean: 10.503132860999989 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09621655682126712,
            "unit": "iter/sec",
            "range": "stddev: 0.18653819698523805",
            "extra": "mean: 10.393221634999998 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.330748763819465,
            "unit": "iter/sec",
            "range": "stddev: 0.07289468416293891",
            "extra": "mean: 3.0234428950000165 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05316264182482516,
            "unit": "iter/sec",
            "range": "stddev: 0.19307158058886364",
            "extra": "mean: 18.810201405999987 sec\nrounds: 10"
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
            "email": "66853113+pre-commit-ci[bot]@users.noreply.github.com",
            "name": "pre-commit-ci[bot]",
            "username": "pre-commit-ci[bot]"
          },
          "distinct": true,
          "id": "df7366f7675b9ef9e21f3a29dd64de9e4302716c",
          "message": "[pre-commit.ci] auto fixes from pre-commit.com hooks\n\nfor more information, see https://pre-commit.ci",
          "timestamp": "2021-05-08T21:40:43Z",
          "tree_id": "7116462b32dbddef888969f8011fca622d8ff775",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/df7366f7675b9ef9e21f3a29dd64de9e4302716c"
        },
        "date": 1620511139099,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10178070529021481,
            "unit": "iter/sec",
            "range": "stddev: 0.05399385859676663",
            "extra": "mean: 9.8250449056 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.1021013553133502,
            "unit": "iter/sec",
            "range": "stddev: 0.029882705417020743",
            "extra": "mean: 9.794189283100001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3443103066193121,
            "unit": "iter/sec",
            "range": "stddev: 0.05028388903632352",
            "extra": "mean: 2.9043568570999923 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05502215441030101,
            "unit": "iter/sec",
            "range": "stddev: 0.06965651650035622",
            "extra": "mean: 18.174497358700012 sec\nrounds: 10"
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
          "id": "eab186ea2633b3b6a60cd3914a8743d9f3051d07",
          "message": "chore: version bump",
          "timestamp": "2021-05-08T23:46:57+02:00",
          "tree_id": "7116462b32dbddef888969f8011fca622d8ff775",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/eab186ea2633b3b6a60cd3914a8743d9f3051d07"
        },
        "date": 1620511789497,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11054423025480688,
            "unit": "iter/sec",
            "range": "stddev: 0.04732820555902305",
            "extra": "mean: 9.04615281770001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11297524316768187,
            "unit": "iter/sec",
            "range": "stddev: 0.06643950647693649",
            "extra": "mean: 8.851496770100017 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3821479468470284,
            "unit": "iter/sec",
            "range": "stddev: 0.05280464992128378",
            "extra": "mean: 2.616787577299988 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06227006746880217,
            "unit": "iter/sec",
            "range": "stddev: 0.09989747829417135",
            "extra": "mean: 16.059080078900003 sec\nrounds: 10"
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
          "id": "56ac42c69415787b958706337af35b3d0c7f56ee",
          "message": "chore: version bump",
          "timestamp": "2021-05-08T23:51:19+02:00",
          "tree_id": "7a9db3f4971b49bf0d10ea22289d24e09d6355d8",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/56ac42c69415787b958706337af35b3d0c7f56ee"
        },
        "date": 1620512871361,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07484885862677815,
            "unit": "iter/sec",
            "range": "stddev: 0.10398799189890959",
            "extra": "mean: 13.360257168199984 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07682869281898656,
            "unit": "iter/sec",
            "range": "stddev: 0.14748219804065743",
            "extra": "mean: 13.015970509300029 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.25007061754171506,
            "unit": "iter/sec",
            "range": "stddev: 0.03854345054108778",
            "extra": "mean: 3.998870438400013 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.04104712950273687,
            "unit": "iter/sec",
            "range": "stddev: 0.1409750350849414",
            "extra": "mean: 24.362239506500053 sec\nrounds: 10"
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
          "id": "02ed31ab2600cb69e2d2184a0883d576fe277397",
          "message": "Merge pull request #777 from pandas-profiling/develop\n\nv2.13.0",
          "timestamp": "2021-05-09T00:46:31+02:00",
          "tree_id": "cf3a5b6dd93fad1f4b13d29e988752fda71010ce",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/02ed31ab2600cb69e2d2184a0883d576fe277397"
        },
        "date": 1620515055933,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0980960783581525,
            "unit": "iter/sec",
            "range": "stddev: 0.10817847822456102",
            "extra": "mean: 10.194087436899997 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09823652601785235,
            "unit": "iter/sec",
            "range": "stddev: 0.05314656095663748",
            "extra": "mean: 10.179513064400016 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3339207845755354,
            "unit": "iter/sec",
            "range": "stddev: 0.03846937261772329",
            "extra": "mean: 2.994722240100009 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.055304415262119135,
            "unit": "iter/sec",
            "range": "stddev: 0.1951306172577907",
            "extra": "mean: 18.081738958100004 sec\nrounds: 10"
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
          "id": "b770e0f6777958470cf730ce57e94d7743b447cf",
          "message": "perf: string type detection improvement",
          "timestamp": "2021-05-09T00:46:04+02:00",
          "tree_id": "cf3a5b6dd93fad1f4b13d29e988752fda71010ce",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/b770e0f6777958470cf730ce57e94d7743b447cf"
        },
        "date": 1620515080371,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09215926924537858,
            "unit": "iter/sec",
            "range": "stddev: 0.195811935715776",
            "extra": "mean: 10.850780482399994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09415670568581885,
            "unit": "iter/sec",
            "range": "stddev: 0.08251322014842416",
            "extra": "mean: 10.620592476299986 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3213006161135221,
            "unit": "iter/sec",
            "range": "stddev: 0.07058247309614922",
            "extra": "mean: 3.1123500854000214 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.052136510400501046,
            "unit": "iter/sec",
            "range": "stddev: 0.2948826524625287",
            "extra": "mean: 19.180416800400007 sec\nrounds: 10"
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
          "id": "6fc0e7ff4e5fb94c15657a5a37b997b6245a3655",
          "message": "build: tangled-up-in-unicode 0.0.7",
          "timestamp": "2021-05-09T22:47:34+02:00",
          "tree_id": "d22a26d2aa1efe3d799ddf793c07c0223522c653",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/6fc0e7ff4e5fb94c15657a5a37b997b6245a3655"
        },
        "date": 1620594123089,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.1180108112246116,
            "unit": "iter/sec",
            "range": "stddev: 0.19215037423698514",
            "extra": "mean: 8.473799896999997 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.12498659728877856,
            "unit": "iter/sec",
            "range": "stddev: 0.11658283268109981",
            "extra": "mean: 8.000857865499961 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.412443508995289,
            "unit": "iter/sec",
            "range": "stddev: 0.07146207614319537",
            "extra": "mean: 2.424574464600005 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06662507898411274,
            "unit": "iter/sec",
            "range": "stddev: 0.27121682160281624",
            "extra": "mean: 15.0093630694 sec\nrounds: 10"
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
          "id": "d9a2e1cb014ccc4ce31bc92cdc269a4d217940ff",
          "message": "chore: version bump",
          "timestamp": "2021-05-10T00:04:39+02:00",
          "tree_id": "5ec21bd8d7d09dc5d8a9ece6d451efe93beeb02a",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/d9a2e1cb014ccc4ce31bc92cdc269a4d217940ff"
        },
        "date": 1620598899908,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11276265690867264,
            "unit": "iter/sec",
            "range": "stddev: 0.2695134933703401",
            "extra": "mean: 8.868184090499994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11534231443013536,
            "unit": "iter/sec",
            "range": "stddev: 0.13831777269112655",
            "extra": "mean: 8.669845103599993 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4316031316979075,
            "unit": "iter/sec",
            "range": "stddev: 0.039394289115215995",
            "extra": "mean: 2.316943336500003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07170290282235213,
            "unit": "iter/sec",
            "range": "stddev: 0.169453762901712",
            "extra": "mean: 13.946436763899987 sec\nrounds: 10"
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
          "id": "615db5a959a9973a60b3b33b435d0d8b821b6ccc",
          "message": "build: upgrade ``tangled-up-in-unicode`` to 0.1.0",
          "timestamp": "2021-05-10T18:15:59+02:00",
          "tree_id": "b75b05a9a8b99fad54d0a3c4414d19fbc099c0ab",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/615db5a959a9973a60b3b33b435d0d8b821b6ccc"
        },
        "date": 1620664445049,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09361609365185358,
            "unit": "iter/sec",
            "range": "stddev: 0.08123536829916438",
            "extra": "mean: 10.68192402599999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09253007606977422,
            "unit": "iter/sec",
            "range": "stddev: 0.1647621660150525",
            "extra": "mean: 10.807296853900016 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3462164146586127,
            "unit": "iter/sec",
            "range": "stddev: 0.0671761307884811",
            "extra": "mean: 2.888366806600004 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05701964515403961,
            "unit": "iter/sec",
            "range": "stddev: 0.41388310968931585",
            "extra": "mean: 17.537815209099982 sec\nrounds: 10"
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
          "id": "62f8e3fd81720d444041069191c4aacd03d79ad5",
          "message": "refactor: type annotations",
          "timestamp": "2021-05-11T00:05:09+02:00",
          "tree_id": "ed73fb1137e1dbaf9b1d511c9968b5184f464438",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/62f8e3fd81720d444041069191c4aacd03d79ad5"
        },
        "date": 1620685737505,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.06955125304409379,
            "unit": "iter/sec",
            "range": "stddev: 0.234934795175403",
            "extra": "mean: 14.3778861808 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07112669647832182,
            "unit": "iter/sec",
            "range": "stddev: 0.2252952160819983",
            "extra": "mean: 14.059418608100021 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2513154225624602,
            "unit": "iter/sec",
            "range": "stddev: 0.05096916339369689",
            "extra": "mean: 3.979063400899986 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.040882988341317816,
            "unit": "iter/sec",
            "range": "stddev: 0.5232236373044756",
            "extra": "mean: 24.46005149260002 sec\nrounds: 10"
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
          "id": "22da35e06511d78f09ca71e856a60dcb0ac5710e",
          "message": "Merge pull request #780 from pandas-profiling/develop\n\nv3.0.0",
          "timestamp": "2021-05-12T00:08:15+02:00",
          "tree_id": "ed73fb1137e1dbaf9b1d511c9968b5184f464438",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/22da35e06511d78f09ca71e856a60dcb0ac5710e"
        },
        "date": 1620772274375,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07138174042414547,
            "unit": "iter/sec",
            "range": "stddev: 0.15724061929951805",
            "extra": "mean: 14.009184898799997 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07235335694043797,
            "unit": "iter/sec",
            "range": "stddev: 0.2189818692419409",
            "extra": "mean: 13.821058790999984 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.2612537245730974,
            "unit": "iter/sec",
            "range": "stddev: 0.15222435169002654",
            "extra": "mean: 3.8276966256999914 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.043304608238063244,
            "unit": "iter/sec",
            "range": "stddev: 0.22254060017608646",
            "extra": "mean: 23.092230612099957 sec\nrounds: 10"
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
          "id": "abaa9bc44545c874e7a6512f30e5894f6eb127be",
          "message": "Merge pull request #783 from pandas-profiling/feat/prep-spark\n\nrefactor: multiple dispatch architecture",
          "timestamp": "2021-05-14T23:14:11+02:00",
          "tree_id": "adc72cac5b37fe79978841b5adf79d6792301836",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/abaa9bc44545c874e7a6512f30e5894f6eb127be"
        },
        "date": 1621027844540,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10202940392333758,
            "unit": "iter/sec",
            "range": "stddev: 0.08712135311777308",
            "extra": "mean: 9.80109616979999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10219780975389271,
            "unit": "iter/sec",
            "range": "stddev: 0.12395513186605292",
            "extra": "mean: 9.784945513100002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3781520965953106,
            "unit": "iter/sec",
            "range": "stddev: 0.14893635136758493",
            "extra": "mean: 2.6444385975999922 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06186608711535147,
            "unit": "iter/sec",
            "range": "stddev: 0.1861340659828912",
            "extra": "mean: 16.16394452320001 sec\nrounds: 10"
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
          "id": "04c0c683141a9ed892c58e2cd28c9bf949b38373",
          "message": "build: multimethod visions",
          "timestamp": "2021-05-16T19:01:12+02:00",
          "tree_id": "8051d5c96a6cb5bfdcbc0b348b0f2d8c8c5992ff",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/04c0c683141a9ed892c58e2cd28c9bf949b38373"
        },
        "date": 1621185524667,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09443042497026623,
            "unit": "iter/sec",
            "range": "stddev: 0.12608670583760323",
            "extra": "mean: 10.589807260900022 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.0946879495641844,
            "unit": "iter/sec",
            "range": "stddev: 0.14762543087986962",
            "extra": "mean: 10.561005963299987 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.35209116433999105,
            "unit": "iter/sec",
            "range": "stddev: 0.13003287895970658",
            "extra": "mean: 2.8401735154999983 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.057996184360020436,
            "unit": "iter/sec",
            "range": "stddev: 0.233383989747029",
            "extra": "mean: 17.242513641799995 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "dbcda6b6f60e8607bd223e17ff7ce021b315144e",
          "message": "build: markupsafe",
          "timestamp": "2021-05-16T19:17:37+02:00",
          "tree_id": "7f16cbd6bcb0c0b536f3c81bb59ac8c574fcb117",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/dbcda6b6f60e8607bd223e17ff7ce021b315144e"
        },
        "date": 1621186533704,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09348489271303415,
            "unit": "iter/sec",
            "range": "stddev: 0.23867938063258037",
            "extra": "mean: 10.69691552270001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09220246113636488,
            "unit": "iter/sec",
            "range": "stddev: 0.2551329084688164",
            "extra": "mean: 10.845697475700002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3511752994962654,
            "unit": "iter/sec",
            "range": "stddev: 0.03536551001220331",
            "extra": "mean: 2.8475806852999765 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.056264649969599526,
            "unit": "iter/sec",
            "range": "stddev: 0.44953665758220623",
            "extra": "mean: 17.773148869499984 sec\nrounds: 10"
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
          "id": "113277ede126e52717c1ee54014ed8f91fce5d02",
          "message": "refactor: typing progress_bar.py",
          "timestamp": "2021-05-16T19:50:24+02:00",
          "tree_id": "6a858f2addaff6d884851d5be32b9e7f5b1f9edf",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/113277ede126e52717c1ee54014ed8f91fce5d02"
        },
        "date": 1621188416133,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09726661681790418,
            "unit": "iter/sec",
            "range": "stddev: 0.11151225579134055",
            "extra": "mean: 10.281019662400007 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09748798265830334,
            "unit": "iter/sec",
            "range": "stddev: 0.13893027238162423",
            "extra": "mean: 10.257674563899974 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.44035892492013173,
            "unit": "iter/sec",
            "range": "stddev: 0.107388475669673",
            "extra": "mean: 2.2708748328000183 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0647956795894228,
            "unit": "iter/sec",
            "range": "stddev: 0.2533678518291119",
            "extra": "mean: 15.433127738400003 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "46691715+briangrahamww@users.noreply.github.com",
            "name": "Brian Graham",
            "username": "briangrahamww"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "17523d8e81f5841ebda9f80e1977b7fc26e8afef",
          "message": "fix: config accept environment variables (#786)\n\nfix: config accept environment variables\r\n\r\nCo-authored-by: Simon Brugman <sbrugman@users.noreply.github.com>",
          "timestamp": "2021-05-16T20:36:27+02:00",
          "tree_id": "991468760f87dd216405e554cf052dbe57bbdc42",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/17523d8e81f5841ebda9f80e1977b7fc26e8afef"
        },
        "date": 1621191007486,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11790073423750443,
            "unit": "iter/sec",
            "range": "stddev: 0.10774760533358824",
            "extra": "mean: 8.48171138599999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11654289294994981,
            "unit": "iter/sec",
            "range": "stddev: 0.13957853546072413",
            "extra": "mean: 8.580531808399996 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.505361860177102,
            "unit": "iter/sec",
            "range": "stddev: 0.09368476249944888",
            "extra": "mean: 1.9787801153999909 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.08062324967842537,
            "unit": "iter/sec",
            "range": "stddev: 0.5176087011370724",
            "extra": "mean: 12.403370045100008 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gent.rexha@gmail.com",
            "name": "Gent Rexha",
            "username": "gentrexha"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "3371e25759eb4fdfc3ea4d349ead5083387bcfc5",
          "message": "docs: Readme link fix (#799)\n\ndocs: updated link of bank_marketing_data example with the correct working one.",
          "timestamp": "2021-06-13T21:28:18+02:00",
          "tree_id": "88f71d7a1437ff011e874293b893340da67b563b",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/3371e25759eb4fdfc3ea4d349ead5083387bcfc5"
        },
        "date": 1623613436060,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.1008719343414636,
            "unit": "iter/sec",
            "range": "stddev: 0.07858335816711275",
            "extra": "mean: 9.913560263599981 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.1013000163452813,
            "unit": "iter/sec",
            "range": "stddev: 0.10538127074696035",
            "extra": "mean: 9.871666719100006 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4622295854368021,
            "unit": "iter/sec",
            "range": "stddev: 0.06556903321997988",
            "extra": "mean: 2.163427074999993 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0704692491549482,
            "unit": "iter/sec",
            "range": "stddev: 0.1526193395864674",
            "extra": "mean: 14.19058684449999 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "43691873+kaustubhgupta@users.noreply.github.com",
            "name": "Kaustubh Gupta",
            "username": "kaustubhgupta"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "7678a3ca17096fff1e5b5ca0b3a18a5712539c21",
          "message": "docs: adding blog link (#802)",
          "timestamp": "2021-06-27T22:16:39+02:00",
          "tree_id": "afcabf2690baddc7ae29d7523815579e85eb2bf7",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/7678a3ca17096fff1e5b5ca0b3a18a5712539c21"
        },
        "date": 1624825811727,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11898526670678418,
            "unit": "iter/sec",
            "range": "stddev: 0.07546647429364417",
            "extra": "mean: 8.404401886700004 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11910813669653939,
            "unit": "iter/sec",
            "range": "stddev: 0.07726959961343798",
            "extra": "mean: 8.395732044299995 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.5391931531018926,
            "unit": "iter/sec",
            "range": "stddev: 0.055992555363649096",
            "extra": "mean: 1.8546229570000263 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.08310631245881564,
            "unit": "iter/sec",
            "range": "stddev: 0.1272195778621771",
            "extra": "mean: 12.0327803077 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "49699333+dependabot[bot]@users.noreply.github.com",
            "name": "dependabot[bot]",
            "username": "dependabot[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f05376e93c8f700f3e2cc2301a58dceaf1e524af",
          "message": "build(deps): update markupsafe requirement from ~=1.1.1 to ~=2.0.1 (#793)\n\nUpdates the requirements on [markupsafe](https://github.com/pallets/markupsafe) to permit the latest version.\r\n- [Release notes](https://github.com/pallets/markupsafe/releases)\r\n- [Changelog](https://github.com/pallets/markupsafe/blob/main/CHANGES.rst)\r\n- [Commits](https://github.com/pallets/markupsafe/compare/1.1.1...2.0.1)\r\n\r\nSigned-off-by: dependabot[bot] <support@github.com>\r\n\r\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2021-09-15T21:48:58+02:00",
          "tree_id": "37a6037515f792701ee768f6517e873417c5859b",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/f05376e93c8f700f3e2cc2301a58dceaf1e524af"
        },
        "date": 1631736402733,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09422409415521499,
            "unit": "iter/sec",
            "range": "stddev: 0.34386212909610253",
            "extra": "mean: 10.612996696499982 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09349647357296041,
            "unit": "iter/sec",
            "range": "stddev: 1.1758494104755712",
            "extra": "mean: 10.695590558499998 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.40305368608046677,
            "unit": "iter/sec",
            "range": "stddev: 0.061738616635250126",
            "extra": "mean: 2.481059061199994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06236135310587666,
            "unit": "iter/sec",
            "range": "stddev: 0.4239859937528345",
            "extra": "mean: 16.035572517199988 sec\nrounds: 10"
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
          "id": "44ce4e527dcc82cad388516b6fcef7394121e3d3",
          "message": "Update .pre-commit-config.yaml",
          "timestamp": "2021-09-15T21:54:41+02:00",
          "tree_id": "af13b5c1c67e517a3882127f73bad51c51dd8cfb",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/44ce4e527dcc82cad388516b6fcef7394121e3d3"
        },
        "date": 1631736575605,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11222971705751507,
            "unit": "iter/sec",
            "range": "stddev: 0.11079658368041576",
            "extra": "mean: 8.910296009100012 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10334453321292879,
            "unit": "iter/sec",
            "range": "stddev: 1.2272809654004624",
            "extra": "mean: 9.676370572400014 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.49547924295275747,
            "unit": "iter/sec",
            "range": "stddev: 0.07130753300115625",
            "extra": "mean: 2.0182480179000093 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07812504426516177,
            "unit": "iter/sec",
            "range": "stddev: 0.15873536377678288",
            "extra": "mean: 12.799992747600005 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "endremborza@gmail.com",
            "name": "Endre Mark Borza",
            "username": "endremborza"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "93063d8aba0dea955419046da848317284abd1fc",
          "message": "feat: matplotlib Agg set to cfg (#798)",
          "timestamp": "2021-09-15T22:08:03+02:00",
          "tree_id": "b7285008336bd45dd4068ba3ff98e3b460210425",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/93063d8aba0dea955419046da848317284abd1fc"
        },
        "date": 1631737608290,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08420477980508724,
            "unit": "iter/sec",
            "range": "stddev: 0.18813900859958177",
            "extra": "mean: 11.875810403100001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08520417816842608,
            "unit": "iter/sec",
            "range": "stddev: 0.15082865071703117",
            "extra": "mean: 11.736513648700008 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3732990972448987,
            "unit": "iter/sec",
            "range": "stddev: 0.06984391601875878",
            "extra": "mean: 2.6788170863000005 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.058023648521676394,
            "unit": "iter/sec",
            "range": "stddev: 0.26641646999402774",
            "extra": "mean: 17.234352293899985 sec\nrounds: 10"
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
          "id": "aa1a563ab55743af4ad814d9ef4554fa0a557a72",
          "message": "chore: add python 3.10 support",
          "timestamp": "2021-09-15T22:23:48+02:00",
          "tree_id": "bc3eeed61ead8b3b5427bd7c54a6baa6f814ad22",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/aa1a563ab55743af4ad814d9ef4554fa0a557a72"
        },
        "date": 1631738584382,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08423556376271099,
            "unit": "iter/sec",
            "range": "stddev: 0.1227122342003894",
            "extra": "mean: 11.87147037819999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.085039038271519,
            "unit": "iter/sec",
            "range": "stddev: 0.13074976021770485",
            "extra": "mean: 11.759305141799995 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3710311547049612,
            "unit": "iter/sec",
            "range": "stddev: 0.053808437513379735",
            "extra": "mean: 2.6951914612000336 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05948824877018376,
            "unit": "iter/sec",
            "range": "stddev: 0.21332403542617695",
            "extra": "mean: 16.810042666799973 sec\nrounds: 10"
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
          "id": "ba5ce0cb8d9ce45f853747643675b810352c67e0",
          "message": "docs: update readme",
          "timestamp": "2021-09-15T22:31:25+02:00",
          "tree_id": "812fbdac3ee5196a4114f9fac04d90f9bf8b3b03",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/ba5ce0cb8d9ce45f853747643675b810352c67e0"
        },
        "date": 1631738751657,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11182356087522584,
            "unit": "iter/sec",
            "range": "stddev: 0.12274996797338174",
            "extra": "mean: 8.942659240800003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10873071626986072,
            "unit": "iter/sec",
            "range": "stddev: 0.872917787920346",
            "extra": "mean: 9.197033131999996 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.5034648683075625,
            "unit": "iter/sec",
            "range": "stddev: 0.08327622085191895",
            "extra": "mean: 1.9862359082999774 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07845200846995443,
            "unit": "iter/sec",
            "range": "stddev: 0.15525726868773349",
            "extra": "mean: 12.746646255500014 sec\nrounds: 10"
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
          "id": "4de76d366adf89c45bec56b9422befd93aaa4acb",
          "message": "docs: update readme",
          "timestamp": "2021-09-15T23:07:35+02:00",
          "tree_id": "3ab7983dafbbb1bd6417ccabb18a780186afd166",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/4de76d366adf89c45bec56b9422befd93aaa4acb"
        },
        "date": 1631741097765,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09418773044347299,
            "unit": "iter/sec",
            "range": "stddev: 0.10304247602353246",
            "extra": "mean: 10.617094129899993 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08314140523079111,
            "unit": "iter/sec",
            "range": "stddev: 1.8821850044783965",
            "extra": "mean: 12.027701447000004 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4232579861103208,
            "unit": "iter/sec",
            "range": "stddev: 0.0878860711197356",
            "extra": "mean: 2.362625237600014 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06533284927645155,
            "unit": "iter/sec",
            "range": "stddev: 0.1537081143607914",
            "extra": "mean: 15.306235853399983 sec\nrounds: 10"
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
          "id": "4b442f8f38ed6765bd4dfbce70640c324bbe74e6",
          "message": "docs: update readme",
          "timestamp": "2021-09-16T00:41:12+02:00",
          "tree_id": "6fc0e3da0af465e0717d48306409a6df0caea35d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/4b442f8f38ed6765bd4dfbce70640c324bbe74e6"
        },
        "date": 1631746638632,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0995590309121529,
            "unit": "iter/sec",
            "range": "stddev: 0.11035340785028551",
            "extra": "mean: 10.044292223799989 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09213429853676053,
            "unit": "iter/sec",
            "range": "stddev: 1.3604519502119952",
            "extra": "mean: 10.853721316400009 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4518480646300664,
            "unit": "iter/sec",
            "range": "stddev: 0.07888186823784932",
            "extra": "mean: 2.2131333035999887 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06865663648045565,
            "unit": "iter/sec",
            "range": "stddev: 0.1791584199659879",
            "extra": "mean: 14.565234349700017 sec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "81109309+abhicantdraw@users.noreply.github.com",
            "name": "abhicantdraw",
            "username": "abhicantdraw"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "8a20b065bdfcdd48eb987dbb979b31d1db2d6ed1",
          "message": "fix: Phi K correlation variable order (#829)\n\n* fix: Order of columns for phi-k now matches the rest of the correlation matrices (#825)",
          "timestamp": "2021-09-16T10:31:52+02:00",
          "tree_id": "80bde7a9d7ce07a78e37a995d8bb8730afde1898",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/8a20b065bdfcdd48eb987dbb979b31d1db2d6ed1"
        },
        "date": 1631782119801,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09494522872458816,
            "unit": "iter/sec",
            "range": "stddev: 0.20315119538566345",
            "extra": "mean: 10.532388129800017 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08941497073040378,
            "unit": "iter/sec",
            "range": "stddev: 1.1113156026309132",
            "extra": "mean: 11.183809510099968 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.40210204762731083,
            "unit": "iter/sec",
            "range": "stddev: 0.08238868695166993",
            "extra": "mean: 2.486930882099989 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06406037385985383,
            "unit": "iter/sec",
            "range": "stddev: 0.2806702164609386",
            "extra": "mean: 15.610274179600015 sec\nrounds: 10"
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
          "id": "5921db36f7e82ddd3c77ebcd8bdf1fdb856a1ca5",
          "message": "deps: bump visions",
          "timestamp": "2021-09-27T23:27:16+02:00",
          "tree_id": "d90cb268295098d9ab0162325a467de5a841a9f2",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/5921db36f7e82ddd3c77ebcd8bdf1fdb856a1ca5"
        },
        "date": 1632778977246,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0996316046862397,
            "unit": "iter/sec",
            "range": "stddev: 0.11876283110297914",
            "extra": "mean: 10.036975748299994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09980097005517763,
            "unit": "iter/sec",
            "range": "stddev: 0.09566722018057207",
            "extra": "mean: 10.019942686399975 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4453978603329174,
            "unit": "iter/sec",
            "range": "stddev: 0.0807119819690914",
            "extra": "mean: 2.2451836639999554 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06857562378498129,
            "unit": "iter/sec",
            "range": "stddev: 0.19439675812385127",
            "extra": "mean: 14.582441176700012 sec\nrounds: 10"
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
          "id": "82b314380c53aa038a364b1513ac50aa403381f2",
          "message": "deps: bump visions",
          "timestamp": "2021-09-27T23:41:52+02:00",
          "tree_id": "1152f72ae85a2c150af0c8999fd711c2951f58bc",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/82b314380c53aa038a364b1513ac50aa403381f2"
        },
        "date": 1632780016842,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08322124839901669,
            "unit": "iter/sec",
            "range": "stddev: 0.13893435161826767",
            "extra": "mean: 12.016161968699999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08366979457646558,
            "unit": "iter/sec",
            "range": "stddev: 0.22076450156184568",
            "extra": "mean: 11.951744414599977 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.36595674701698827,
            "unit": "iter/sec",
            "range": "stddev: 0.0676655425227816",
            "extra": "mean: 2.732563364799989 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0573283852267068,
            "unit": "iter/sec",
            "range": "stddev: 0.28881934893020794",
            "extra": "mean: 17.443365900600032 sec\nrounds: 10"
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
          "id": "f4e09c27847bc84e2995101e2125892bfa1cdb08",
          "message": "feat: py3.10 compatibility",
          "timestamp": "2021-09-28T00:16:15+02:00",
          "tree_id": "4e3839acc7288a44b40894cf49319fc0acfc2027",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/f4e09c27847bc84e2995101e2125892bfa1cdb08"
        },
        "date": 1632781823431,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11104592294200219,
            "unit": "iter/sec",
            "range": "stddev: 0.13568392993974332",
            "extra": "mean: 9.005283341399997 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11145393216694666,
            "unit": "iter/sec",
            "range": "stddev: 0.10644897957279002",
            "extra": "mean: 8.972316907600009 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.498548137635849,
            "unit": "iter/sec",
            "range": "stddev: 0.08380311193181247",
            "extra": "mean: 2.005824361799989 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07683337141876065,
            "unit": "iter/sec",
            "range": "stddev: 0.18433104038882622",
            "extra": "mean: 13.015177930300046 sec\nrounds: 10"
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
          "id": "659c23860b7217e3ae722cdac261fae3e8096c25",
          "message": "ci: upgrade pre-commit versions",
          "timestamp": "2021-09-28T00:13:51+02:00",
          "tree_id": "9d755001d6bf7e9662bed8315f6b830812c3e3c3",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/659c23860b7217e3ae722cdac261fae3e8096c25"
        },
        "date": 1632782015743,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07880791118637477,
            "unit": "iter/sec",
            "range": "stddev: 0.1310158677229809",
            "extra": "mean: 12.68908139990001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.0765581738645994,
            "unit": "iter/sec",
            "range": "stddev: 0.3334645918111814",
            "extra": "mean: 13.061962551099999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3385862966416682,
            "unit": "iter/sec",
            "range": "stddev: 0.0777176090845755",
            "extra": "mean: 2.9534567993999987 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.053344687742152994,
            "unit": "iter/sec",
            "range": "stddev: 0.14314409284971813",
            "extra": "mean: 18.74600906530004 sec\nrounds: 10"
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
          "id": "ae95d455cad4ec66128d1170aca5701c8593209f",
          "message": "test: disable broken pandas test",
          "timestamp": "2021-09-28T00:22:28+02:00",
          "tree_id": "02b7554a922ec23d5188583e66c4dce1a8a25056",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/ae95d455cad4ec66128d1170aca5701c8593209f"
        },
        "date": 1632782502936,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08073038685449378,
            "unit": "iter/sec",
            "range": "stddev: 0.1674331169108078",
            "extra": "mean: 12.3869095512 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08087748808611063,
            "unit": "iter/sec",
            "range": "stddev: 0.19019224395884413",
            "extra": "mean: 12.36438004769999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.34816732061274774,
            "unit": "iter/sec",
            "range": "stddev: 0.08796342248451743",
            "extra": "mean: 2.8721822548999625 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05490249206410322,
            "unit": "iter/sec",
            "range": "stddev: 0.3551019962145208",
            "extra": "mean: 18.214109458499934 sec\nrounds: 10"
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
          "id": "f403f714d62c7f748d15914c6efe01c25497f312",
          "message": "test: disable broken pandas test",
          "timestamp": "2021-09-28T00:23:54+02:00",
          "tree_id": "573ca5d3271aaed32ce766364c056f21afa6dbe8",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/f403f714d62c7f748d15914c6efe01c25497f312"
        },
        "date": 1632782645755,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07656872965747155,
            "unit": "iter/sec",
            "range": "stddev: 0.12765028579710075",
            "extra": "mean: 13.060161824199998 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07660634148148646,
            "unit": "iter/sec",
            "range": "stddev: 0.18199080787037913",
            "extra": "mean: 13.053749606899988 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.33404911259308445,
            "unit": "iter/sec",
            "range": "stddev: 0.0994641273377625",
            "extra": "mean: 2.9935717901999963 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05248022006189277,
            "unit": "iter/sec",
            "range": "stddev: 0.24432619519082963",
            "extra": "mean: 19.05479814719995 sec\nrounds: 10"
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
          "id": "f500ba4bcb0ee85533cceb201b7e9f011be184d6",
          "message": "Merge pull request #832 from pandas-profiling/develop\n\nv3.1.0",
          "timestamp": "2021-09-28T00:43:22+02:00",
          "tree_id": "573ca5d3271aaed32ce766364c056f21afa6dbe8",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/f500ba4bcb0ee85533cceb201b7e9f011be184d6"
        },
        "date": 1632783652845,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07887544825320784,
            "unit": "iter/sec",
            "range": "stddev: 0.6089221731118291",
            "extra": "mean: 12.678216379700007 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08897506248572085,
            "unit": "iter/sec",
            "range": "stddev: 1.1104615967956102",
            "extra": "mean: 11.239104217099987 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.42097777347079696,
            "unit": "iter/sec",
            "range": "stddev: 0.12213280627562811",
            "extra": "mean: 2.375422321600001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06482264249455665,
            "unit": "iter/sec",
            "range": "stddev: 0.25773686710616617",
            "extra": "mean: 15.426708346300028 sec\nrounds: 10"
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
          "id": "f5bf3775737ed031518a9abc449ff43120fc45d1",
          "message": "Merge pull request #833 from pandas-profiling/develop\n\nchore: bump",
          "timestamp": "2021-09-28T00:45:05+02:00",
          "tree_id": "2e89083561a9199abea7907e7215ba5663105209",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/f5bf3775737ed031518a9abc449ff43120fc45d1"
        },
        "date": 1632783755886,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08696752501634979,
            "unit": "iter/sec",
            "range": "stddev: 0.1651807087414921",
            "extra": "mean: 11.498545000699988 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09000541416732274,
            "unit": "iter/sec",
            "range": "stddev: 0.12904513011816865",
            "extra": "mean: 11.110442735599998 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3884892700853892,
            "unit": "iter/sec",
            "range": "stddev: 0.09529197842082296",
            "extra": "mean: 2.574073666899994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06106409800786228,
            "unit": "iter/sec",
            "range": "stddev: 0.27054167907233007",
            "extra": "mean: 16.37623468820002 sec\nrounds: 10"
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
          "id": "53e1aeefed7bad1dc0a82e5b6b11d97316a74ef3",
          "message": "chore: bump",
          "timestamp": "2021-09-28T00:43:45+02:00",
          "tree_id": "2e89083561a9199abea7907e7215ba5663105209",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/53e1aeefed7bad1dc0a82e5b6b11d97316a74ef3"
        },
        "date": 1632783789491,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08214686405365586,
            "unit": "iter/sec",
            "range": "stddev: 0.12627125926001076",
            "extra": "mean: 12.173319231600004 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.0813257901266266,
            "unit": "iter/sec",
            "range": "stddev: 0.12139603757296298",
            "extra": "mean: 12.296222372299997 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3439522816269443,
            "unit": "iter/sec",
            "range": "stddev: 0.10156452869355086",
            "extra": "mean: 2.907380044899992 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0543600993917276,
            "unit": "iter/sec",
            "range": "stddev: 0.21128414901844594",
            "extra": "mean: 18.395845688100007 sec\nrounds: 10"
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
          "id": "71e1497cbee6f26e05ddc18c25c6d4302512c02b",
          "message": "docs: direct link",
          "timestamp": "2021-09-30T13:32:20+02:00",
          "tree_id": "cf6667c8f0d608f32e57c02e05856a95b4780576",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/71e1497cbee6f26e05ddc18c25c6d4302512c02b"
        },
        "date": 1633002766923,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07634997402842175,
            "unit": "iter/sec",
            "range": "stddev: 0.16018927601466565",
            "extra": "mean: 13.097581403600003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07646224183592701,
            "unit": "iter/sec",
            "range": "stddev: 0.14100340383080615",
            "extra": "mean: 13.07835051640003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3330588496102148,
            "unit": "iter/sec",
            "range": "stddev: 0.07483074985533779",
            "extra": "mean: 3.002472389400009 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05297224715401142,
            "unit": "iter/sec",
            "range": "stddev: 0.28914757554140613",
            "extra": "mean: 18.877809678200016 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "1aa16bbfda9e76709cafbf1925b94a56e46130d2",
          "message": "ci: update dependencies",
          "timestamp": "2021-10-01T17:56:06Z",
          "tree_id": "00424b49db2455eaf7e17a8e9d3494d6ac92dcd5",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/1aa16bbfda9e76709cafbf1925b94a56e46130d2"
        },
        "date": 1633111933984,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09763960997638184,
            "unit": "iter/sec",
            "range": "stddev: 0.14968373707912377",
            "extra": "mean: 10.2417451303 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09592024182443507,
            "unit": "iter/sec",
            "range": "stddev: 0.10987208018252571",
            "extra": "mean: 10.425328178699989 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.42070767436731227,
            "unit": "iter/sec",
            "range": "stddev: 0.10747162092936786",
            "extra": "mean: 2.376947369700031 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06698682528126548,
            "unit": "iter/sec",
            "range": "stddev: 0.2517352781178852",
            "extra": "mean: 14.928308601000003 sec\nrounds: 10"
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
          "id": "3ec3b271bfa55fbcf1bc20577fb9e56d509ed382",
          "message": "ci: remove deprecated flag",
          "timestamp": "2021-10-02T13:39:51+02:00",
          "tree_id": "35280d857cc73ea89b97ce2b2385021100cda769",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/3ec3b271bfa55fbcf1bc20577fb9e56d509ed382"
        },
        "date": 1633175715776,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.1037792470245226,
            "unit": "iter/sec",
            "range": "stddev: 0.3899407130457125",
            "extra": "mean: 9.635837883500006 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10310499078316798,
            "unit": "iter/sec",
            "range": "stddev: 0.1673383659067227",
            "extra": "mean: 9.698851553199995 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4469898324956217,
            "unit": "iter/sec",
            "range": "stddev: 0.07763762979004844",
            "extra": "mean: 2.2371873526000057 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.070739278850926,
            "unit": "iter/sec",
            "range": "stddev: 0.27506911743268847",
            "extra": "mean: 14.136417789999985 sec\nrounds: 10"
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
          "id": "bb53fe3de7c30620534a49e92b100f2bf05ece81",
          "message": "Merge pull request #840 from pandas-profiling/dependabot/pip/coverage-approx-eq-6.0\n\nbuild(deps): update coverage requirement from ~=5.5 to ~=6.0",
          "timestamp": "2021-10-04T12:41:30+02:00",
          "tree_id": "1cf4d4bc467de0568fc88733ceacec9e31959683",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/bb53fe3de7c30620534a49e92b100f2bf05ece81"
        },
        "date": 1633345132709,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08985391989349957,
            "unit": "iter/sec",
            "range": "stddev: 0.14128293527405178",
            "extra": "mean: 11.129175011900003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08948149650603184,
            "unit": "iter/sec",
            "range": "stddev: 0.14918095333534453",
            "extra": "mean: 11.175494812300007 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3770077354583639,
            "unit": "iter/sec",
            "range": "stddev: 0.05766681801541526",
            "extra": "mean: 2.652465469399999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06023056200543383,
            "unit": "iter/sec",
            "range": "stddev: 0.19738065577168523",
            "extra": "mean: 16.602866828800018 sec\nrounds: 10"
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
          "id": "ba3c39117aa70b6ec85e36c9925aa37dfae36f35",
          "message": "Merge pull request #839 from pandas-profiling/feat/tryceratops\n\nci: tryceratops",
          "timestamp": "2021-10-04T12:41:13+02:00",
          "tree_id": "6898e18a72d86a2001344b66e3c73be4d12fc9a3",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/ba3c39117aa70b6ec85e36c9925aa37dfae36f35"
        },
        "date": 1633345278423,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07692017168014408,
            "unit": "iter/sec",
            "range": "stddev: 0.18999775675085834",
            "extra": "mean: 13.00049100459999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07737782395766982,
            "unit": "iter/sec",
            "range": "stddev: 0.09459323203316053",
            "extra": "mean: 12.923599409400016 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3325485903133289,
            "unit": "iter/sec",
            "range": "stddev: 0.09665703030906708",
            "extra": "mean: 3.007079353600011 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05176514234934655,
            "unit": "iter/sec",
            "range": "stddev: 0.29060565713722103",
            "extra": "mean: 19.318018933500014 sec\nrounds: 10"
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
          "id": "adcf6d7ad61595be36e5f9127bcf7ba55fab94af",
          "message": "Merge pull request #834 from pandas-profiling/dependabot/pip/tangled-up-in-unicode-0.2.0\n\nbuild(deps): bump tangled-up-in-unicode from 0.1.0 to 0.2.0",
          "timestamp": "2021-10-04T17:36:18+02:00",
          "tree_id": "911774b11a01d6402f34d56ced3331daa8194030",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/adcf6d7ad61595be36e5f9127bcf7ba55fab94af"
        },
        "date": 1633362894286,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08357153178949335,
            "unit": "iter/sec",
            "range": "stddev: 0.12437749427725668",
            "extra": "mean: 11.965797186999993 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08383085872857975,
            "unit": "iter/sec",
            "range": "stddev: 0.12013628231182212",
            "extra": "mean: 11.92878153900001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3610524352051472,
            "unit": "iter/sec",
            "range": "stddev: 0.08906522352042098",
            "extra": "mean: 2.7696808067000234 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05737591666292802,
            "unit": "iter/sec",
            "range": "stddev: 0.20661778170790232",
            "extra": "mean: 17.428915443300003 sec\nrounds: 10"
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
          "id": "1ccffc36c4dd165a4d7be5c17fbbf00ebca948d4",
          "message": "Merge pull request #850 from pandas-profiling/fix/character-split-pandas\n\nfix: character split new pandas",
          "timestamp": "2021-10-05T00:26:45+02:00",
          "tree_id": "3cd24777c59556189b56fd8d6f4c13cb974c8e18",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/1ccffc36c4dd165a4d7be5c17fbbf00ebca948d4"
        },
        "date": 1633387432820,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09178226839816066,
            "unit": "iter/sec",
            "range": "stddev: 0.12290307964747431",
            "extra": "mean: 10.895350675599996 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08828009436076235,
            "unit": "iter/sec",
            "range": "stddev: 0.4871455742217154",
            "extra": "mean: 11.32758191119999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4130192244225168,
            "unit": "iter/sec",
            "range": "stddev: 0.11760144150087387",
            "extra": "mean: 2.4211948036999957 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06535490511927806,
            "unit": "iter/sec",
            "range": "stddev: 0.20229685140848247",
            "extra": "mean: 15.301070335499958 sec\nrounds: 10"
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
          "id": "41d2fab5f225bbdf85eadaf44a4d3a21e778ab11",
          "message": "chore: version bump",
          "timestamp": "2021-10-05T00:36:46+02:00",
          "tree_id": "8612fb079e7214293518d287afe971a05bbf5b65",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/41d2fab5f225bbdf85eadaf44a4d3a21e778ab11"
        },
        "date": 1633387910532,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10310223851506982,
            "unit": "iter/sec",
            "range": "stddev: 0.28059062102658777",
            "extra": "mean: 9.69911045970002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.1046581875333105,
            "unit": "iter/sec",
            "range": "stddev: 0.07956312224214307",
            "extra": "mean: 9.554914178899963 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4642395413409249,
            "unit": "iter/sec",
            "range": "stddev: 0.09367740733031168",
            "extra": "mean: 2.1540603739000064 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07172826413059327,
            "unit": "iter/sec",
            "range": "stddev: 0.5123798688442229",
            "extra": "mean: 13.941505655000004 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "a1683315ae3b1f65620e2399b9e8ad5a9de8a876",
          "message": "ci: update dependencies",
          "timestamp": "2021-10-05T17:52:17Z",
          "tree_id": "335db6fb59463ff22a21edf1e06df1a30462f466",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/a1683315ae3b1f65620e2399b9e8ad5a9de8a876"
        },
        "date": 1633457499531,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0808089929623623,
            "unit": "iter/sec",
            "range": "stddev: 0.46164208431830467",
            "extra": "mean: 12.374860313700003 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07794744952494975,
            "unit": "iter/sec",
            "range": "stddev: 0.1636979676561831",
            "extra": "mean: 12.829156131399987 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.35464329415807505,
            "unit": "iter/sec",
            "range": "stddev: 0.07028477286000698",
            "extra": "mean: 2.8197346924999804 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05462222247685982,
            "unit": "iter/sec",
            "range": "stddev: 0.31248803198235897",
            "extra": "mean: 18.307567042400013 sec\nrounds: 10"
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
          "id": "69b6684ef18688d848bf1ff3cdbf343033826557",
          "message": "Merge pull request #851 from pandas-profiling/develop\n\nv3.1.1",
          "timestamp": "2021-10-07T20:29:27+02:00",
          "tree_id": "335db6fb59463ff22a21edf1e06df1a30462f466",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/69b6684ef18688d848bf1ff3cdbf343033826557"
        },
        "date": 1633632492872,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.0821183283597565,
            "unit": "iter/sec",
            "range": "stddev: 0.13816377007521108",
            "extra": "mean: 12.17754939699999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08251616420897177,
            "unit": "iter/sec",
            "range": "stddev: 0.06806385490888191",
            "extra": "mean: 12.118837679700004 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3688702033421613,
            "unit": "iter/sec",
            "range": "stddev: 0.07907081392091443",
            "extra": "mean: 2.7109806943999954 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.058160200778793254,
            "unit": "iter/sec",
            "range": "stddev: 0.2791567458696478",
            "extra": "mean: 17.193888374000018 sec\nrounds: 10"
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
          "id": "c188d97c40b9b144571339c3f12a0f6259106121",
          "message": "Merge pull request #857 from pandas-profiling/dependabot/pip/joblib-approx-eq-1.1.0\n\nbuild(deps): update joblib requirement from ~=1.0.1 to ~=1.1.0",
          "timestamp": "2021-10-08T14:33:22+02:00",
          "tree_id": "a7a15d4ebb48ca80e72d20f56c03cba73427b679",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/c188d97c40b9b144571339c3f12a0f6259106121"
        },
        "date": 1633697227996,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11354110796257119,
            "unit": "iter/sec",
            "range": "stddev: 0.09115267203772369",
            "extra": "mean: 8.807382788000007 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.11266939716152481,
            "unit": "iter/sec",
            "range": "stddev: 0.07662534458306572",
            "extra": "mean: 8.875524545199994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.5143956460231919,
            "unit": "iter/sec",
            "range": "stddev: 0.06849290539543433",
            "extra": "mean: 1.9440288963000172 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.08342740905396964,
            "unit": "iter/sec",
            "range": "stddev: 0.5180016166540876",
            "extra": "mean: 11.986468372200012 sec\nrounds: 10"
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
          "id": "5089a302bf6e6bc4f702014c30ab9c6962ebad3d",
          "message": "Update LICENSE",
          "timestamp": "2021-10-16T01:41:53+02:00",
          "tree_id": "d25b84a4380bba15f9151627ede9db02ddb130c2",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/5089a302bf6e6bc4f702014c30ab9c6962ebad3d"
        },
        "date": 1634342181848,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10830568575175295,
            "unit": "iter/sec",
            "range": "stddev: 0.12054255110315322",
            "extra": "mean: 9.233125602400008 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10219283615177563,
            "unit": "iter/sec",
            "range": "stddev: 1.119767259051051",
            "extra": "mean: 9.785421734599982 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.49893378899547863,
            "unit": "iter/sec",
            "range": "stddev: 0.07890021095602524",
            "extra": "mean: 2.004273957899977 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07716433200782781,
            "unit": "iter/sec",
            "range": "stddev: 0.11350313147067856",
            "extra": "mean: 12.959355365099986 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "fe92f3b2be0a961758a863efff15c01b6d019d49",
          "message": "ci: update dependencies",
          "timestamp": "2021-10-19T17:52:32Z",
          "tree_id": "5c56bc1c83328d1c7955795b50f3cfb65c00665d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/fe92f3b2be0a961758a863efff15c01b6d019d49"
        },
        "date": 1634666938046,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09554151612422015,
            "unit": "iter/sec",
            "range": "stddev: 0.16082899641576778",
            "extra": "mean: 10.466654084700002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.0880224470707463,
            "unit": "iter/sec",
            "range": "stddev: 1.3623238400478879",
            "extra": "mean: 11.360738462500024 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.429436907862975,
            "unit": "iter/sec",
            "range": "stddev: 0.10799085762012163",
            "extra": "mean: 2.328630776 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06715259612381017,
            "unit": "iter/sec",
            "range": "stddev: 0.2196380250461819",
            "extra": "mean: 14.891457035499958 sec\nrounds: 10"
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
          "id": "f59a9c7a3a08c63053b3cfbb9d9e0927f15e444f",
          "message": "Merge pull request #868 from patrickdemers6/864-extreme-values\n\n#864 - Fix Extreme Values Sub-Tab Titles",
          "timestamp": "2021-10-24T13:40:24+02:00",
          "tree_id": "b13bcc38460ff0796070aee7988ba86e52f96b0e",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/f59a9c7a3a08c63053b3cfbb9d9e0927f15e444f"
        },
        "date": 1635076456998,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11498573384401413,
            "unit": "iter/sec",
            "range": "stddev: 0.08269178299406929",
            "extra": "mean: 8.696731034099997 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10704919762026104,
            "unit": "iter/sec",
            "range": "stddev: 1.0893780122166836",
            "extra": "mean: 9.3414992567 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.5199023386644467,
            "unit": "iter/sec",
            "range": "stddev: 0.07322413868220855",
            "extra": "mean: 1.9234381644999985 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07879984129044393,
            "unit": "iter/sec",
            "range": "stddev: 0.17877429623494856",
            "extra": "mean: 12.690380889399966 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "fef45a8f041ee45188f487310fdd8c42045b70b2",
          "message": "ci: update dependencies",
          "timestamp": "2021-10-25T17:52:58Z",
          "tree_id": "96fde6320fee74d1b32a92917876f7d073c132da",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/fef45a8f041ee45188f487310fdd8c42045b70b2"
        },
        "date": 1635185341795,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09950698608688766,
            "unit": "iter/sec",
            "range": "stddev: 0.1308525414860649",
            "extra": "mean: 10.049545658299996 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09119737108023242,
            "unit": "iter/sec",
            "range": "stddev: 1.2472036221579632",
            "extra": "mean: 10.965228362999994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4499226249187673,
            "unit": "iter/sec",
            "range": "stddev: 0.08201230751822201",
            "extra": "mean: 2.2226043871 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06858779450527334,
            "unit": "iter/sec",
            "range": "stddev: 0.32455997027123573",
            "extra": "mean: 14.579853561600022 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "29f2a3865deeed1d17a346fd92a55c72a3247a11",
          "message": "ci: dependency update",
          "timestamp": "2021-11-01T17:52:36Z",
          "tree_id": "decbbe90a5abc20707235618d2b7a61c32137f69",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/29f2a3865deeed1d17a346fd92a55c72a3247a11"
        },
        "date": 1635790291523,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08238026589616974,
            "unit": "iter/sec",
            "range": "stddev: 0.43890068852541453",
            "extra": "mean: 12.13882947720001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08496443912991294,
            "unit": "iter/sec",
            "range": "stddev: 0.18123730009516995",
            "extra": "mean: 11.769629862099986 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3555326143032283,
            "unit": "iter/sec",
            "range": "stddev: 0.10563278347639124",
            "extra": "mean: 2.8126814806000198 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0572572124522586,
            "unit": "iter/sec",
            "range": "stddev: 0.4389869315247954",
            "extra": "mean: 17.46504863179998 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "4ed8a8932a8901b166557384b95664650adbcf48",
          "message": "ci: pre-commit updates",
          "timestamp": "2021-11-03T17:54:06Z",
          "tree_id": "7f5a906939b1353a9fc190cfd65889e14681f04c",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/4ed8a8932a8901b166557384b95664650adbcf48"
        },
        "date": 1635962896137,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11232662555800783,
            "unit": "iter/sec",
            "range": "stddev: 0.36850821837506964",
            "extra": "mean: 8.902608753999994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10354306128086116,
            "unit": "iter/sec",
            "range": "stddev: 1.1199654815174933",
            "extra": "mean: 9.657817603900025 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.5131980415383096,
            "unit": "iter/sec",
            "range": "stddev: 0.08436463010424815",
            "extra": "mean: 1.9485655030999396 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07715816383934038,
            "unit": "iter/sec",
            "range": "stddev: 0.16957718153885115",
            "extra": "mean: 12.960391360300013 sec\nrounds: 10"
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
          "id": "939969061459a7df5e0ed425cd471827924c4eed",
          "message": "Merge pull request #874 from pandas-profiling/develop\n\nmerge master",
          "timestamp": "2021-11-03T22:43:41+01:00",
          "tree_id": "62a77a9b4abe1c49997ce6675394c14d8f8d93c2",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/939969061459a7df5e0ed425cd471827924c4eed"
        },
        "date": 1635976853538,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.09091407169932236,
            "unit": "iter/sec",
            "range": "stddev: 0.29358690074245347",
            "extra": "mean: 10.999397357399994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08919937246293354,
            "unit": "iter/sec",
            "range": "stddev: 0.7747325429310754",
            "extra": "mean: 11.210841202000006 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3881250605292654,
            "unit": "iter/sec",
            "range": "stddev: 0.09697447165494467",
            "extra": "mean: 2.5764891312000144 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.06171449478568568,
            "unit": "iter/sec",
            "range": "stddev: 0.5452776000736929",
            "extra": "mean: 16.203648810100027 sec\nrounds: 10"
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
          "id": "181e6cdda72e526d8b1b22a42afe35ac6efe8948",
          "message": "docs: move binary to external hosting",
          "timestamp": "2021-11-03T22:42:06+01:00",
          "tree_id": "62a77a9b4abe1c49997ce6675394c14d8f8d93c2",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/181e6cdda72e526d8b1b22a42afe35ac6efe8948"
        },
        "date": 1635976928855,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07751719369004201,
            "unit": "iter/sec",
            "range": "stddev: 0.155041730061006",
            "extra": "mean: 12.90036380830001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07686736235195411,
            "unit": "iter/sec",
            "range": "stddev: 0.14759435016054223",
            "extra": "mean: 13.009422587200016 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.34347325953751484,
            "unit": "iter/sec",
            "range": "stddev: 0.0912477114340997",
            "extra": "mean: 2.911434797999982 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.05468346844244901,
            "unit": "iter/sec",
            "range": "stddev: 0.2058172597998457",
            "extra": "mean: 18.28706240629997 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "f174d62ee14078ebe1daebc0bc8ce799c0735e38",
          "message": "ci: dependency update",
          "timestamp": "2021-11-09T17:52:44Z",
          "tree_id": "d7a80c82c8f5f7b6d3ade70c5df7989e32cbe50d",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/f174d62ee14078ebe1daebc0bc8ce799c0735e38"
        },
        "date": 1636481229922,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.11072141509218353,
            "unit": "iter/sec",
            "range": "stddev: 0.09130697853431734",
            "extra": "mean: 9.031676475299998 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.09756099310601153,
            "unit": "iter/sec",
            "range": "stddev: 1.488849193328588",
            "extra": "mean: 10.249998161799994 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.5007229832250384,
            "unit": "iter/sec",
            "range": "stddev: 0.08292882135601691",
            "extra": "mean: 1.9971122427000183 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.0776372184125042,
            "unit": "iter/sec",
            "range": "stddev: 0.10461595242620578",
            "extra": "mean: 12.880420247500012 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "a79b87116747454a911652b50e6a38152e1a105e",
          "message": "ci: dependency update",
          "timestamp": "2021-11-16T17:52:47Z",
          "tree_id": "0b347498ba4075a5e2e86ff5cd9f28f9b9702430",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/a79b87116747454a911652b50e6a38152e1a105e"
        },
        "date": 1637086080896,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.10335791559889872,
            "unit": "iter/sec",
            "range": "stddev: 0.11386129828035148",
            "extra": "mean: 9.675117713100002 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.10677987938285206,
            "unit": "iter/sec",
            "range": "stddev: 0.17354531285308258",
            "extra": "mean: 9.36506021340001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.4884547833642781,
            "unit": "iter/sec",
            "range": "stddev: 0.06489861904926894",
            "extra": "mean: 2.0472724068999923 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.07296315920684335,
            "unit": "iter/sec",
            "range": "stddev: 0.26821524435158023",
            "extra": "mean: 13.70554689339998 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "862dccb8ca99fc8fdfd34da54cfe49d4b3a5a3ba",
          "message": "ci: update dependencies",
          "timestamp": "2021-11-17T17:52:45Z",
          "tree_id": "f021ec5c5c50587a1a58402ea6945cbf23d7370a",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/862dccb8ca99fc8fdfd34da54cfe49d4b3a5a3ba"
        },
        "date": 1637172696742,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08492293579264437,
            "unit": "iter/sec",
            "range": "stddev: 0.1306854526702035",
            "extra": "mean: 11.77538188790001 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08544921533109244,
            "unit": "iter/sec",
            "range": "stddev: 0.1761216338613636",
            "extra": "mean: 11.702857611100024 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.36382101419196783,
            "unit": "iter/sec",
            "range": "stddev: 0.05318656744031227",
            "extra": "mean: 2.748604288900026 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.057125317703905415,
            "unit": "iter/sec",
            "range": "stddev: 0.16660385399514818",
            "extra": "mean: 17.505373102399993 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "20b933d5ad731349b80a4ce3d34dc505879149e4",
          "message": "ci: update dependencies",
          "timestamp": "2021-11-18T17:52:45Z",
          "tree_id": "4bc4c31d9a5e37f7403acabf83f5646293f84ae1",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/20b933d5ad731349b80a4ce3d34dc505879149e4"
        },
        "date": 1637259126499,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.08184549823506457,
            "unit": "iter/sec",
            "range": "stddev: 0.13531883044839788",
            "extra": "mean: 12.218142983599995 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.08130731077044905,
            "unit": "iter/sec",
            "range": "stddev: 0.0905915119936567",
            "extra": "mean: 12.299017032099993 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.35194971208716674,
            "unit": "iter/sec",
            "range": "stddev: 0.10548189870208968",
            "extra": "mean: 2.8413150107999856 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.055568053330310854,
            "unit": "iter/sec",
            "range": "stddev: 0.2168968549282555",
            "extra": "mean: 17.995951631699995 sec\nrounds: 10"
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
            "email": "sbrugman@users.noreply.github.com",
            "name": "Simon Brugman",
            "username": "sbrugman"
          },
          "distinct": true,
          "id": "2dd039093999e80efaeaa440ee0e79b833d2ffb3",
          "message": "ci: dependency update",
          "timestamp": "2021-11-19T17:52:22Z",
          "tree_id": "8c72baeef55d4f5e2dd99d1cf28f287638945ea8",
          "url": "https://github.com/pandas-profiling/pandas-profiling/commit/2dd039093999e80efaeaa440ee0e79b833d2ffb3"
        },
        "date": 1637345566239,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/bench.py::test_titanic_explorative",
            "value": 0.07690112184918267,
            "unit": "iter/sec",
            "range": "stddev: 0.1617434787294163",
            "extra": "mean: 13.00371146679999 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_default",
            "value": 0.07667788734281912,
            "unit": "iter/sec",
            "range": "stddev: 0.18023328849393283",
            "extra": "mean: 13.041569540499996 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_titanic_minimal",
            "value": 0.3276823392384216,
            "unit": "iter/sec",
            "range": "stddev: 0.07781030936051682",
            "extra": "mean: 3.051736026800029 sec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/bench.py::test_rdw_minimal",
            "value": 0.052523322995862584,
            "unit": "iter/sec",
            "range": "stddev: 0.17347342421539708",
            "extra": "mean: 19.039160947200024 sec\nrounds: 10"
          }
        ]
      }
    ]
  }
}