# [Changelog](https://github.com/feenes/mytb/releases)
## [v0.1.2](https://github.com/feenes/mytb/compare/v0.1.1...v0.1.2)
* removed dependency from minibelt (now included as mytb.minibelt)
* isort on more source files
* logcfg in curdir
## [v0.1.1](https://github.com/feenes/mytb/compare/v0.1.0...v0.1.1)
* stop python 3.5 compativility (so far only mytb.modules needs >=3.6)
* add github workflow for flake ind pytest
* add mod file.find with file_find_tuple and file_find
* add mod file.suffix_file.SuffixFile (not fully implemented)
* add mod importlib with import_obj, import_if_mod_exists
* add mod modules with get_modules and mk_modname
* add mod objects with AnyObj and VersionObject
* add mod parse with parse_paramstr
* add mod pickle with robust_unpickler and unpickle_robust (not fully implemented)
* enhance mod string with strip_accents
* cleanup/fix requirements and setup dependencies
* minor enhancements to README.md
## [v0.1.0](https://github.com/feenes/mytb/compare/v0.0.15...v0.1.0)
* support only python versions > 3.5
* remove code that ensured py2 backwards compatibility
* fixed suffix extraction of log config
* new function mytb.logging.config.setupLogging
## [v0.0.15](https://github.com/feenes/mytb/compare/v0.0.14...v0.0.15)
* minor update for argparse + logging config
* fix for robust_makedirs()
* first shot at code owners
## [v0.0.14](https://github.com/feenes/mytb/compare/v0.0.13...v0.0.14)
* robust makedirs() without race conditions
## [v0.0.13](https://github.com/feenes/mytb/compare/v0.0.12...v0.0.13)
* new mytb.aio.compat for bw compatibility layer for asyncio
## [v0.0.12](https://github.com/feenes/mytb/compare/v0.0.11...v0.0.12)
* limit version of minibelt for py2.
## [v0.0.11](https://github.com/feenes/mytb/compare/v0.0.10...v0.0.11)
* fix limit pytest version for py2
* add mytb.ipython to instantiate an interactive shell from an executable
* add a basic console log config (w timestamp name and pids)
* setup has now extra requirement for more granular installs
## [v0.0.10](https://github.com/feenes/mytb/compare/0.0.9...v0.0.10)
* add helper for creating pdb hooks
* attempt to improve urls, that show up on https://pypi.org
## [0.0.9](https://github.com/feenes/mytb/compare/0.0.8...0.0.9)
* add changelog
* enhance cli
## [0.0.8](https://github.com/feenes/mytb/compare/0.0.7...0.0.8)
* re-add accidentally deleted html table_reader
* module memory (for memory consumption analysis)
## [0.0.7](https://github.com/feenes/mytb/compare/v0.0.6...0.0.7)
* gitlabci: add stages
* add module lru_cache + tests
## [v0.0.6](https://github.com/feenes/mytb/compare/v0.0.5...v0.0.6)
* restructure requirements
* flake8 for py2 and py3 for gitlabci
* new module table_reader
## [v0.0.5](https://github.com/feenes/mytb/compare/v0.0.4...v0.0.5)
* also create gitlabci cfg
* add flake to travis
* new module datetime + tests
* some flake cleanup
## [v0.0.4](https://github.com/feenes/mytb/compare/v0.0.1...v0.0.4)
* some cleanup of repository (license file, isort cfg, travis cfg, readme)
* add pypy (py2 + py3) to tox
* add mytb command
* new command check_ci_cfg
* new module cli
* new module csv
* new module ipc.mutex
* new module os
* new module tempfile

## [v0.0.1](https://github.com/mhcomm/mytb/compare/05c8cfd1f8c053fbdf87e57f66508d7994afa52a...v0.0.1)
